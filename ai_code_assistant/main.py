import openai
import os
import json
import re
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
import logging
import subprocess
import tempfile
import ast

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AICodeAssistant:
    def __init__(self, api_key: str = None):
        """Initialize the AI Code Assistant with OpenAI API key."""
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass it to constructor.")
        
        openai.api_key = self.api_key
        self.code_history = []
        self.supported_languages = [
            "python", "javascript", "java", "cpp", "csharp", "php", 
            "ruby", "go", "rust", "swift", "kotlin", "typescript"
        ]
        
    def generate_code(self, description: str, language: str = "python", style: str = "clean") -> Optional[str]:
        """
        Generate code based on description.
        
        Args:
            description: Description of what the code should do
            language: Programming language to generate
            style: Code style (clean, commented, production, simple)
            
        Returns:
            Generated code or None if failed
        """
        try:
            logger.info(f"Generating {language} code for: {description}")
            
            # Create appropriate prompt based on style
            if style == "clean":
                prompt = f"Write clean, well-structured {language} code for the following task:\n\n{description}\n\nProvide only the code without explanations."
            elif style == "commented":
                prompt = f"Write well-commented {language} code for the following task:\n\n{description}\n\nInclude helpful comments explaining the logic."
            elif style == "production":
                prompt = f"Write production-ready {language} code for the following task:\n\n{description}\n\nInclude error handling, logging, and best practices."
            elif style == "simple":
                prompt = f"Write simple, easy-to-understand {language} code for the following task:\n\n{description}\n\nKeep it straightforward and minimal."
            else:
                prompt = f"Write {language} code for the following task:\n\n{description}"
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"You are an expert {language} programmer. Write clean, efficient, and correct code."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.3
            )
            
            code = response.choices[0].message.content.strip()
            
            # Save to history
            code_info = {
                "type": "generation",
                "description": description,
                "language": language,
                "style": style,
                "code": code,
                "timestamp": datetime.now().isoformat()
            }
            self.code_history.append(code_info)
            
            logger.info(f"Code generated successfully ({len(code)} characters)")
            return code
            
        except Exception as e:
            logger.error(f"Error generating code: {e}")
            return None
    
    def debug_code(self, code: str, error_message: str = None, language: str = "python") -> Optional[str]:
        """
        Debug and fix code issues.
        
        Args:
            code: Code to debug
            error_message: Error message if available
            language: Programming language
            
        Returns:
            Fixed code or None if failed
        """
        try:
            logger.info(f"Debugging {language} code")
            
            prompt = f"""Debug and fix the following {language} code:

Code:
{code}

{f"Error: {error_message}" if error_message else "Please identify and fix any issues."}

Provide the corrected code with explanations of what was fixed."""
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"You are an expert {language} debugger. Identify and fix code issues."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.2
            )
            
            result = response.choices[0].message.content.strip()
            
            # Save to history
            debug_info = {
                "type": "debug",
                "original_code": code,
                "error_message": error_message,
                "language": language,
                "fixed_code": result,
                "timestamp": datetime.now().isoformat()
            }
            self.code_history.append(debug_info)
            
            logger.info("Code debugging completed")
            return result
            
        except Exception as e:
            logger.error(f"Error debugging code: {e}")
            return None
    
    def explain_code(self, code: str, language: str = "python") -> Optional[str]:
        """
        Explain what code does.
        
        Args:
            code: Code to explain
            language: Programming language
            
        Returns:
            Code explanation or None if failed
        """
        try:
            logger.info(f"Explaining {language} code")
            
            prompt = f"""Explain what the following {language} code does:

{code}

Provide a clear, detailed explanation of:
1. What the code does
2. How it works
3. Key functions/methods
4. Important variables
5. Any notable patterns or techniques"""
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"You are an expert {language} programmer. Explain code clearly and accurately."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.3
            )
            
            explanation = response.choices[0].message.content.strip()
            
            # Save to history
            explain_info = {
                "type": "explanation",
                "code": code,
                "language": language,
                "explanation": explanation,
                "timestamp": datetime.now().isoformat()
            }
            self.code_history.append(explain_info)
            
            logger.info("Code explanation completed")
            return explanation
            
        except Exception as e:
            logger.error(f"Error explaining code: {e}")
            return None
    
    def optimize_code(self, code: str, language: str = "python", focus: str = "performance") -> Optional[str]:
        """
        Optimize code for various aspects.
        
        Args:
            code: Code to optimize
            language: Programming language
            focus: Optimization focus (performance, readability, memory, security)
            
        Returns:
            Optimized code or None if failed
        """
        try:
            logger.info(f"Optimizing {language} code for {focus}")
            
            focus_prompts = {
                "performance": "Optimize for speed and efficiency",
                "readability": "Optimize for code clarity and maintainability",
                "memory": "Optimize for memory usage and efficiency",
                "security": "Optimize for security and best practices"
            }
            
            prompt = f"""Optimize the following {language} code for {focus_prompts.get(focus, focus)}:

{code}

Provide the optimized code with explanations of the improvements made."""
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"You are an expert {language} optimizer. Provide efficient, well-optimized code."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.3
            )
            
            result = response.choices[0].message.content.strip()
            
            # Save to history
            optimize_info = {
                "type": "optimization",
                "original_code": code,
                "language": language,
                "focus": focus,
                "optimized_code": result,
                "timestamp": datetime.now().isoformat()
            }
            self.code_history.append(optimize_info)
            
            logger.info("Code optimization completed")
            return result
            
        except Exception as e:
            logger.error(f"Error optimizing code: {e}")
            return None
    
    def test_code(self, code: str, language: str = "python") -> Optional[str]:
        """
        Generate tests for code.
        
        Args:
            code: Code to test
            language: Programming language
            
        Returns:
            Test code or None if failed
        """
        try:
            logger.info(f"Generating tests for {language} code")
            
            prompt = f"""Generate comprehensive tests for the following {language} code:

{code}

Provide unit tests that cover:
1. Normal cases
2. Edge cases
3. Error cases
4. Different scenarios"""
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"You are an expert {language} tester. Write comprehensive, effective tests."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.3
            )
            
            tests = response.choices[0].message.content.strip()
            
            # Save to history
            test_info = {
                "type": "testing",
                "code": code,
                "language": language,
                "tests": tests,
                "timestamp": datetime.now().isoformat()
            }
            self.code_history.append(test_info)
            
            logger.info("Test generation completed")
            return tests
            
        except Exception as e:
            logger.error(f"Error generating tests: {e}")
            return None
    
    def convert_code(self, code: str, from_language: str, to_language: str) -> Optional[str]:
        """
        Convert code from one language to another.
        
        Args:
            code: Code to convert
            from_language: Source language
            to_language: Target language
            
        Returns:
            Converted code or None if failed
        """
        try:
            logger.info(f"Converting code from {from_language} to {to_language}")
            
            prompt = f"""Convert the following {from_language} code to {to_language}:

{code}

Maintain the same functionality and logic while using {to_language} conventions and best practices."""
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"You are an expert programmer who can convert code between {from_language} and {to_language}."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.3
            )
            
            converted_code = response.choices[0].message.content.strip()
            
            # Save to history
            convert_info = {
                "type": "conversion",
                "original_code": code,
                "from_language": from_language,
                "to_language": to_language,
                "converted_code": converted_code,
                "timestamp": datetime.now().isoformat()
            }
            self.code_history.append(convert_info)
            
            logger.info("Code conversion completed")
            return converted_code
            
        except Exception as e:
            logger.error(f"Error converting code: {e}")
            return None
    
    def analyze_code_complexity(self, code: str, language: str = "python") -> Optional[Dict[str, Any]]:
        """
        Analyze code complexity and provide metrics.
        
        Args:
            code: Code to analyze
            language: Programming language
            
        Returns:
            Complexity analysis or None if failed
        """
        try:
            logger.info(f"Analyzing {language} code complexity")
            
            # Basic complexity analysis
            lines = code.split('\n')
            non_empty_lines = [line for line in lines if line.strip()]
            
            # Count functions, classes, imports
            function_count = len(re.findall(r'def\s+\w+', code))
            class_count = len(re.findall(r'class\s+\w+', code))
            import_count = len(re.findall(r'^import\s+|^from\s+', code, re.MULTILINE))
            
            # Try to analyze with AI for more detailed metrics
            prompt = f"""Analyze the complexity of this {language} code:

{code}

Provide a JSON response with:
- complexity_level (low/medium/high)
- maintainability_score (1-10)
- readability_score (1-10)
- potential_issues (list)
- suggestions (list)"""
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a code analysis expert. Provide detailed complexity analysis in JSON format."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.3
            )
            
            result_text = response.choices[0].message.content.strip()
            
            try:
                ai_analysis = json.loads(result_text)
            except json.JSONDecodeError:
                ai_analysis = {}
            
            # Combine basic and AI analysis
            analysis = {
                "basic_metrics": {
                    "total_lines": len(lines),
                    "non_empty_lines": len(non_empty_lines),
                    "function_count": function_count,
                    "class_count": class_count,
                    "import_count": import_count
                },
                "ai_analysis": ai_analysis,
                "timestamp": datetime.now().isoformat()
            }
            
            # Save to history
            self.code_history.append({
                "type": "complexity_analysis",
                "code": code,
                "language": language,
                "analysis": analysis,
                "timestamp": datetime.now().isoformat()
            })
            
            logger.info("Code complexity analysis completed")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing code complexity: {e}")
            return None
    
    def get_code_history(self) -> List[Dict[str, Any]]:
        """Get history of all code operations."""
        return self.code_history.copy()
    
    def clear_history(self):
        """Clear the code history."""
        self.code_history = []
    
    def save_history(self, filename: str = None):
        """Save code history to JSON file."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"code_assistant_history_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.code_history, f, indent=2)
        
        logger.info(f"Code history saved to {filename}")

def main():
    """Main function to demonstrate the AI Code Assistant."""
    print("💻 AI Code Assistant")
    print("=" * 50)
    
    # Initialize the assistant
    try:
        assistant = AICodeAssistant()
        print("✅ Code assistant initialized successfully!")
    except ValueError as e:
        print(f"❌ Error: {e}")
        print("Please set your OpenAI API key as an environment variable: OPENAI_API_KEY")
        return
    
    print("\n🎯 Available commands:")
    print("- 'generate <description>' - Generate code")
    print("- 'debug <code>' - Debug code")
    print("- 'explain <code>' - Explain code")
    print("- 'optimize <code>' - Optimize code")
    print("- 'test <code>' - Generate tests")
    print("- 'convert <from> <to> <code>' - Convert code")
    print("- 'analyze <code>' - Analyze complexity")
    print("- 'history' - Show code history")
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
            history = assistant.get_code_history()
            if history:
                print(f"\n📋 Code History ({len(history)} entries):")
                for i, entry in enumerate(history, 1):
                    entry_type = entry.get('type', 'unknown')
                    print(f"{i}. {entry_type} - {entry.get('language', 'unknown')}")
            else:
                print("📋 No code operations yet.")
            continue
        elif user_input.lower() == 'clear':
            assistant.clear_history()
            print("🗑️ History cleared!")
            continue
        elif user_input.lower() == 'save':
            assistant.save_history()
            continue
        elif user_input.startswith('generate '):
            description = user_input[9:].strip()
            if description:
                print(f"\n💻 Generating code...")
                code = assistant.generate_code(description)
                if code:
                    print(f"✅ Generated code:\n{code}")
                else:
                    print("❌ Failed to generate code")
            else:
                print("❌ Please provide a description")
            continue
        elif user_input.startswith('debug '):
            code = user_input[6:].strip()
            if code:
                print(f"\n🐛 Debugging code...")
                result = assistant.debug_code(code)
                if result:
                    print(f"✅ Debugged code:\n{result}")
                else:
                    print("❌ Failed to debug code")
            else:
                print("❌ Please provide code to debug")
            continue
        elif user_input.startswith('explain '):
            code = user_input[8:].strip()
            if code:
                print(f"\n📖 Explaining code...")
                explanation = assistant.explain_code(code)
                if explanation:
                    print(f"✅ Explanation:\n{explanation}")
                else:
                    print("❌ Failed to explain code")
            else:
                print("❌ Please provide code to explain")
            continue
        elif user_input.startswith('optimize '):
            code = user_input[9:].strip()
            if code:
                print(f"\n⚡ Optimizing code...")
                result = assistant.optimize_code(code)
                if result:
                    print(f"✅ Optimized code:\n{result}")
                else:
                    print("❌ Failed to optimize code")
            else:
                print("❌ Please provide code to optimize")
            continue
        elif user_input.startswith('test '):
            code = user_input[5:].strip()
            if code:
                print(f"\n🧪 Generating tests...")
                tests = assistant.test_code(code)
                if tests:
                    print(f"✅ Generated tests:\n{tests}")
                else:
                    print("❌ Failed to generate tests")
            else:
                print("❌ Please provide code to test")
            continue
        elif user_input.startswith('convert '):
            parts = user_input[8:].split(' ', 2)
            if len(parts) == 3:
                from_lang, to_lang, code = parts
                print(f"\n🔄 Converting from {from_lang} to {to_lang}...")
                result = assistant.convert_code(code, from_lang, to_lang)
                if result:
                    print(f"✅ Converted code:\n{result}")
                else:
                    print("❌ Failed to convert code")
            else:
                print("❌ Please provide: convert <from_lang> <to_lang> <code>")
            continue
        elif user_input.startswith('analyze '):
            code = user_input[8:].strip()
            if code:
                print(f"\n📊 Analyzing code complexity...")
                analysis = assistant.analyze_code_complexity(code)
                if analysis:
                    print("✅ Analysis Results:")
                    basic = analysis.get('basic_metrics', {})
                    print(f"Lines: {basic.get('total_lines', 0)}")
                    print(f"Functions: {basic.get('function_count', 0)}")
                    print(f"Classes: {basic.get('class_count', 0)}")
                    
                    ai_analysis = analysis.get('ai_analysis', {})
                    if ai_analysis:
                        print(f"Complexity: {ai_analysis.get('complexity_level', 'unknown')}")
                        print(f"Maintainability: {ai_analysis.get('maintainability_score', 'N/A')}/10")
                else:
                    print("❌ Failed to analyze code")
            else:
                print("❌ Please provide code to analyze")
            continue
        elif not user_input:
            continue
        else:
            print("❌ Unknown command. Type 'help' for available commands.")

if __name__ == "__main__":
    main() 