import openai
import os
import requests
from datetime import datetime
from typing import List, Optional
import logging
from PIL import Image
import io

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIImageGenerator:
    def __init__(self, api_key: str = None):
        """Initialize the AI Image Generator with OpenAI API key."""
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass it to constructor.")
        
        openai.api_key = self.api_key
        self.generated_images = []
        
    def generate_image(self, prompt: str, size: str = "1024x1024", quality: str = "standard", style: str = "vivid") -> Optional[str]:
        """
        Generate an image using OpenAI's DALL-E model.
        
        Args:
            prompt: Text description of the image to generate
            size: Image size (256x256, 512x512, 1024x1024, 1792x1024, 1024x1792)
            quality: Image quality (standard, hd)
            style: Image style (vivid, natural)
            
        Returns:
            URL of the generated image or None if failed
        """
        try:
            logger.info(f"Generating image with prompt: {prompt}")
            
            response = openai.Image.create(
                prompt=prompt,
                n=1,
                size=size,
                quality=quality,
                style=style
            )
            
            image_url = response['data'][0]['url']
            
            # Save image info
            image_info = {
                "prompt": prompt,
                "url": image_url,
                "size": size,
                "quality": quality,
                "style": style,
                "timestamp": datetime.now().isoformat()
            }
            self.generated_images.append(image_info)
            
            logger.info(f"Image generated successfully: {image_url}")
            return image_url
            
        except Exception as e:
            logger.error(f"Error generating image: {e}")
            return None
    
    def generate_variations(self, image_path: str, n: int = 1, size: str = "1024x1024") -> List[str]:
        """
        Generate variations of an existing image.
        
        Args:
            image_path: Path to the input image
            n: Number of variations to generate
            size: Size of generated images
            
        Returns:
            List of image URLs
        """
        try:
            logger.info(f"Generating {n} variations of image: {image_path}")
            
            response = openai.Image.create_variation(
                image=open(image_path, "rb"),
                n=n,
                size=size
            )
            
            urls = [data['url'] for data in response['data']]
            
            # Save variation info
            for url in urls:
                variation_info = {
                    "type": "variation",
                    "original_image": image_path,
                    "url": url,
                    "size": size,
                    "timestamp": datetime.now().isoformat()
                }
                self.generated_images.append(variation_info)
            
            logger.info(f"Generated {len(urls)} variations successfully")
            return urls
            
        except Exception as e:
            logger.error(f"Error generating variations: {e}")
            return []
    
    def download_image(self, url: str, filename: str = None) -> Optional[str]:
        """
        Download an image from URL and save it locally.
        
        Args:
            url: Image URL to download
            filename: Optional filename (auto-generated if not provided)
            
        Returns:
            Path to saved image file or None if failed
        """
        try:
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"generated_image_{timestamp}.png"
            
            response = requests.get(url)
            response.raise_for_status()
            
            with open(filename, 'wb') as f:
                f.write(response.content)
            
            logger.info(f"Image downloaded and saved as: {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Error downloading image: {e}")
            return None
    
    def get_generation_history(self) -> List[dict]:
        """Get history of all generated images."""
        return self.generated_images.copy()
    
    def clear_history(self):
        """Clear the generation history."""
        self.generated_images = []
    
    def save_history(self, filename: str = None):
        """Save generation history to JSON file."""
        import json
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"image_generation_history_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.generated_images, f, indent=2)
        
        logger.info(f"Generation history saved to {filename}")

def main():
    """Main function to demonstrate the AI Image Generator."""
    print("🎨 AI Image Generator")
    print("=" * 50)
    
    # Initialize the generator
    try:
        generator = AIImageGenerator()
        print("✅ Image generator initialized successfully!")
    except ValueError as e:
        print(f"❌ Error: {e}")
        print("Please set your OpenAI API key as an environment variable: OPENAI_API_KEY")
        return
    
    print("\n🎯 Available commands:")
    print("- 'generate <prompt>' - Generate an image")
    print("- 'variation <image_path>' - Generate variations")
    print("- 'download <url>' - Download an image")
    print("- 'history' - Show generation history")
    print("- 'clear' - Clear history")
    print("- 'save' - Save history to file")
    print("- 'quit' - Exit")
    print("-" * 50)
    
    while True:
        user_input = input("\nEnter command: ").strip()
        
        if user_input.lower() == 'quit':
            print("👋 Goodbye!")
            break
        elif user_input.lower() == 'history':
            history = generator.get_generation_history()
            if history:
                print(f"\n📋 Generation History ({len(history)} images):")
                for i, img in enumerate(history, 1):
                    print(f"{i}. {img.get('prompt', 'Variation')} - {img['url']}")
            else:
                print("📋 No images generated yet.")
            continue
        elif user_input.lower() == 'clear':
            generator.clear_history()
            print("🗑️ History cleared!")
            continue
        elif user_input.lower() == 'save':
            generator.save_history()
            continue
        elif user_input.startswith('generate '):
            prompt = user_input[9:].strip()
            if prompt:
                print(f"\n🎨 Generating image: '{prompt}'")
                url = generator.generate_image(prompt)
                if url:
                    print(f"✅ Image generated: {url}")
                    download = input("Download this image? (y/n): ").lower()
                    if download == 'y':
                        filename = generator.download_image(url)
                        if filename:
                            print(f"📥 Downloaded as: {filename}")
                else:
                    print("❌ Failed to generate image")
            else:
                print("❌ Please provide a prompt")
            continue
        elif user_input.startswith('variation '):
            image_path = user_input[10:].strip()
            if os.path.exists(image_path):
                print(f"\n🔄 Generating variations of: {image_path}")
                urls = generator.generate_variations(image_path)
                if urls:
                    print(f"✅ Generated {len(urls)} variations:")
                    for i, url in enumerate(urls, 1):
                        print(f"{i}. {url}")
                else:
                    print("❌ Failed to generate variations")
            else:
                print(f"❌ Image file not found: {image_path}")
            continue
        elif user_input.startswith('download '):
            url = user_input[9:].strip()
            if url:
                print(f"\n📥 Downloading: {url}")
                filename = generator.download_image(url)
                if filename:
                    print(f"✅ Downloaded as: {filename}")
                else:
                    print("❌ Failed to download image")
            else:
                print("❌ Please provide a URL")
            continue
        elif not user_input:
            continue
        else:
            print("❌ Unknown command. Type 'help' for available commands.")

if __name__ == "__main__":
    main() 