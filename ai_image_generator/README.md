# AI Image Generator

A powerful AI image generation tool using OpenAI's DALL-E model to create stunning images from text descriptions.

## Features

- 🎨 **Text-to-Image Generation**: Create images from text prompts using DALL-E
- 🔄 **Image Variations**: Generate variations of existing images
- 📥 **Image Download**: Download generated images locally
- 📋 **Generation History**: Track all generated images
- ⚙️ **Customizable**: Multiple sizes, qualities, and styles
- 💾 **History Management**: Save and load generation history

## Installation

1. Clone or download this project
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your OpenAI API key:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```
   Or create a `.env` file:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```

## Usage

### Basic Usage

Run the main script:
```bash
python main.py
```

### Programmatic Usage

```python
from main import AIImageGenerator

# Initialize the generator
generator = AIImageGenerator(api_key="your-api-key")

# Generate an image
url = generator.generate_image("A beautiful sunset over mountains")
print(f"Generated image: {url}")

# Download the image
filename = generator.download_image(url)
print(f"Downloaded as: {filename}")
```

### Advanced Features

#### Custom Image Parameters
```python
# Generate with custom parameters
url = generator.generate_image(
    prompt="A futuristic city skyline",
    size="1792x1024",  # Wide format
    quality="hd",       # High quality
    style="vivid"       # Vivid style
)
```

#### Generate Image Variations
```python
# Generate variations of an existing image
variations = generator.generate_variations(
    image_path="my_image.png",
    n=3,  # Generate 3 variations
    size="1024x1024"
)
```

#### Batch Processing
```python
# Generate multiple images
prompts = [
    "A cat sitting on a windowsill",
    "A robot in a garden",
    "A spaceship flying through space"
]

for prompt in prompts:
    url = generator.generate_image(prompt)
    if url:
        generator.download_image(url)
```

## API Reference

### AIImageGenerator Class

#### Constructor
```python
AIImageGenerator(api_key: str = None)
```
- `api_key`: OpenAI API key (optional if set as environment variable)

#### Methods

- `generate_image(prompt: str, size: str = "1024x1024", quality: str = "standard", style: str = "vivid") -> Optional[str]`
  - Generate image from text prompt
  - `prompt`: Text description of desired image
  - `size`: Image size (256x256, 512x512, 1024x1024, 1792x1024, 1024x1792)
  - `quality`: Image quality (standard, hd)
  - `style`: Image style (vivid, natural)

- `generate_variations(image_path: str, n: int = 1, size: str = "1024x1024") -> List[str]`
  - Generate variations of existing image
  - `image_path`: Path to input image file
  - `n`: Number of variations to generate
  - `size`: Size of generated variations

- `download_image(url: str, filename: str = None) -> Optional[str]`
  - Download image from URL
  - `url`: Image URL to download
  - `filename`: Optional filename (auto-generated if not provided)

- `get_generation_history() -> List[dict]`
  - Get history of all generated images

- `clear_history()`
  - Clear generation history

- `save_history(filename: str = None)`
  - Save generation history to JSON file

## Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key

### Image Generation Parameters

#### Sizes
- `256x256`: Small square
- `512x512`: Medium square
- `1024x1024`: Large square (default)
- `1792x1024`: Wide format
- `1024x1792`: Tall format

#### Qualities
- `standard`: Standard quality (faster, cheaper)
- `hd`: High definition quality (slower, more expensive)

#### Styles
- `vivid`: More dramatic, saturated colors
- `natural`: More realistic, natural colors

## Examples

### Example 1: Basic Image Generation
```
Enter command: generate A majestic dragon flying over a medieval castle
🎨 Generating image: 'A majestic dragon flying over a medieval castle'
✅ Image generated: https://oaidalleapiprodscus.blob.core.windows.net/...
Download this image? (y/n): y
📥 Downloaded as: generated_image_20231201_143022.png
```

### Example 2: Image Variations
```
Enter command: variation my_photo.png
🔄 Generating variations of: my_photo.png
✅ Generated 1 variations:
1. https://oaidalleapiprodscus.blob.core.windows.net/...
```

### Example 3: Custom Parameters
```python
# Generate a wide, high-quality image
url = generator.generate_image(
    prompt="A panoramic view of the Grand Canyon at sunset",
    size="1792x1024",
    quality="hd",
    style="natural"
)
```

## Best Practices

### Writing Effective Prompts

1. **Be Specific**: "A red sports car on a winding mountain road" vs "A car"
2. **Include Details**: Mention style, lighting, perspective
3. **Use Descriptive Language**: "Majestic", "Serene", "Dramatic"
4. **Specify Art Style**: "Oil painting of", "Digital art of", "Photograph of"

### Example Prompts

- "A serene Japanese garden with cherry blossoms in spring, soft lighting, watercolor style"
- "A futuristic cityscape at night with neon lights and flying cars, cinematic lighting"
- "A cozy coffee shop interior with warm lighting, people reading books, photorealistic"

## Troubleshooting

### Common Issues

1. **API Key Error**
   - Ensure your OpenAI API key is set correctly
   - Check that the key has sufficient credits

2. **Content Policy Violations**
   - Avoid prompts that violate OpenAI's content policy
   - Refrain from generating harmful, violent, or inappropriate content

3. **Image Download Failures**
   - Check internet connection
   - Ensure write permissions in the directory

4. **Large File Sizes**
   - Generated images can be large (several MB)
   - Ensure sufficient disk space

## Cost Considerations

- **Standard Quality**: ~$0.02 per image
- **HD Quality**: ~$0.08 per image
- **Variations**: ~$0.02 per variation
- Monitor your usage in OpenAI dashboard

## Contributing

Feel free to contribute to this project by:
- Adding new features (e.g., batch processing, image editing)
- Improving error handling
- Enhancing documentation
- Reporting bugs

## License

This project is open source and available under the MIT License. 