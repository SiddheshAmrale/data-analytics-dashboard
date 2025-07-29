#!/usr/bin/env python3
"""
AI Projects Repository Quality Evaluator

This script evaluates the quality of the AI projects repository
and provides recommendations for improvement.
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

class RepositoryEvaluator:
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
        self.scores = {}
        self.recommendations = []
        
    def evaluate_documentation(self) -> int:
        """Evaluate documentation quality (25 points max)"""
        score = 0
        
        # README.md evaluation (10 points)
        readme_path = self.repo_path / "README.md"
        if readme_path.exists():
            score += 2
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if "installation" in content.lower():
                    score += 2
                if "usage" in content.lower():
                    score += 2
                if "example" in content.lower():
                    score += 2
                if len(content) > 500:  # Comprehensive README
                    score += 2
        
        # Individual project READMEs (10 points)
        project_dirs = ["ai_chat_assistant", "ai_image_generator", "ai_text_summarizer", 
                       "ai_sentiment_analyzer", "ai_code_assistant"]
        
        for project_dir in project_dirs:
            project_readme = self.repo_path / project_dir / "README.md"
            if project_readme.exists():
                score += 2
        
        # Technical documentation (5 points)
        if (self.repo_path / "repository_quality_checklist.md").exists():
            score += 2
        if (self.repo_path / "evaluate_ai_projects.py").exists():
            score += 2
        if score > 25:
            score = 25
            
        return score
    
    def evaluate_project_structure(self) -> int:
        """Evaluate project structure (20 points max)"""
        score = 0
        
        # Organization (10 points)
        project_dirs = ["ai_chat_assistant", "ai_image_generator", "ai_text_summarizer", 
                       "ai_sentiment_analyzer", "ai_code_assistant"]
        
        for project_dir in project_dirs:
            project_path = self.repo_path / project_dir
            if project_path.exists():
                score += 1
                if (project_path / "main.py").exists():
                    score += 1
                if (project_path / "requirements.txt").exists():
                    score += 1
                if (project_path / "README.md").exists():
                    score += 1
        
        # Configuration (10 points)
        if (self.repo_path / "README.md").exists():
            score += 2
        if (self.repo_path / "repository_quality_checklist.md").exists():
            score += 2
        if (self.repo_path / "evaluate_ai_projects.py").exists():
            score += 2
        
        # Check for .gitignore
        if (self.repo_path / ".gitignore").exists():
            score += 2
        else:
            self.recommendations.append("Add a .gitignore file")
        
        # Check for license
        license_files = list(self.repo_path.glob("LICENSE*"))
        if license_files:
            score += 2
        else:
            self.recommendations.append("Add a LICENSE file")
        
        if score > 20:
            score = 20
            
        return score
    
    def evaluate_code_quality(self) -> int:
        """Evaluate code quality (25 points max)"""
        score = 0
        
        # Check main.py files for code quality indicators
        project_dirs = ["ai_chat_assistant", "ai_image_generator", "ai_text_summarizer", 
                       "ai_sentiment_analyzer", "ai_code_assistant"]
        
        for project_dir in project_dirs:
            main_file = self.repo_path / project_dir / "main.py"
            if main_file.exists():
                score += 2  # Basic structure
                
                with open(main_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # Code standards (10 points)
                    if "import" in content:
                        score += 1
                    if "def " in content:
                        score += 1
                    if "class " in content:
                        score += 1
                    if "try:" in content and "except" in content:
                        score += 1
                    if "logging" in content:
                        score += 1
                    
                    # Code documentation (10 points)
                    if '"""' in content or "'''" in content:
                        score += 2
                    if "#" in content:
                        score += 1
                    if "def " in content and ":" in content:
                        score += 1
                    if "class " in content and ":" in content:
                        score += 1
                    if "main()" in content:
                        score += 1
        
        if score > 25:
            score = 25
            
        return score
    
    def evaluate_testing(self) -> int:
        """Evaluate testing and quality assurance (20 points max)"""
        score = 0
        
        # Check for test files
        test_files = list(self.repo_path.rglob("*test*.py"))
        if test_files:
            score += 5
        else:
            self.recommendations.append("Add unit tests for the projects")
        
        # Check for requirements.txt files (dependency management)
        req_files = list(self.repo_path.rglob("requirements.txt"))
        if req_files:
            score += 5
        else:
            self.recommendations.append("Add requirements.txt files")
        
        # Check for configuration files
        config_files = list(self.repo_path.rglob("*.yml")) + list(self.repo_path.rglob("*.yaml"))
        if config_files:
            score += 5
        else:
            self.recommendations.append("Add configuration files for CI/CD")
        
        # Check for documentation
        doc_files = list(self.repo_path.rglob("*.md"))
        if len(doc_files) > 5:
            score += 5
        
        if score > 20:
            score = 20
            
        return score
    
    def evaluate_git_practices(self) -> int:
        """Evaluate Git practices (10 points max)"""
        score = 0
        
        # Check for .gitignore
        if (self.repo_path / ".gitignore").exists():
            score += 3
        else:
            self.recommendations.append("Create a .gitignore file")
        
        # Check for README
        if (self.repo_path / "README.md").exists():
            score += 3
        
        # Check for license
        license_files = list(self.repo_path.glob("LICENSE*"))
        if license_files:
            score += 2
        else:
            self.recommendations.append("Add a LICENSE file")
        
        # Check for contributing guidelines
        contributing_files = list(self.repo_path.glob("CONTRIBUTING*"))
        if contributing_files:
            score += 2
        else:
            self.recommendations.append("Add CONTRIBUTING.md guidelines")
        
        if score > 10:
            score = 10
            
        return score
    
    def evaluate_deployment(self) -> int:
        """Evaluate deployment and operations (10 points max)"""
        score = 0
        
        # Check for deployment files
        deployment_files = list(self.repo_path.rglob("Dockerfile*")) + list(self.repo_path.rglob("docker-compose*"))
        if deployment_files:
            score += 3
        
        # Check for environment files
        env_files = list(self.repo_path.rglob(".env*"))
        if env_files:
            score += 2
        
        # Check for setup files
        setup_files = list(self.repo_path.rglob("setup.py")) + list(self.repo_path.rglob("pyproject.toml"))
        if setup_files:
            score += 3
        
        # Check for documentation about deployment
        readme_path = self.repo_path / "README.md"
        if readme_path.exists():
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if "deploy" in content.lower() or "install" in content.lower():
                    score += 2
        
        if score > 10:
            score = 10
            
        return score
    
    def evaluate_repository(self) -> Dict:
        """Evaluate the entire repository"""
        print("🔍 Evaluating AI Projects Repository...")
        print("=" * 50)
        
        # Evaluate each category
        doc_score = self.evaluate_documentation()
        structure_score = self.evaluate_project_structure()
        code_score = self.evaluate_code_quality()
        testing_score = self.evaluate_testing()
        git_score = self.evaluate_git_practices()
        deployment_score = self.evaluate_deployment()
        
        total_score = doc_score + structure_score + code_score + testing_score + git_score + deployment_score
        
        # Determine grade
        if total_score >= 90:
            grade = "A"
        elif total_score >= 80:
            grade = "B"
        elif total_score >= 70:
            grade = "C"
        elif total_score >= 60:
            grade = "D"
        else:
            grade = "F"
        
        # Generate report
        report = {
            "evaluation_date": datetime.now().isoformat(),
            "repository_path": str(self.repo_path),
            "scores": {
                "documentation": doc_score,
                "project_structure": structure_score,
                "code_quality": code_score,
                "testing_qa": testing_score,
                "git_practices": git_score,
                "deployment_operations": deployment_score
            },
            "total_score": total_score,
            "grade": grade,
            "recommendations": self.recommendations
        }
        
        return report
    
    def print_report(self, report: Dict):
        """Print the evaluation report"""
        print(f"\n📊 Repository Quality Report")
        print(f"Date: {report['evaluation_date']}")
        print(f"Repository: {report['repository_path']}")
        print("=" * 50)
        
        print(f"\n📈 Scores:")
        print(f"  Documentation: {report['scores']['documentation']}/25")
        print(f"  Project Structure: {report['scores']['project_structure']}/20")
        print(f"  Code Quality: {report['scores']['code_quality']}/25")
        print(f"  Testing & QA: {report['scores']['testing_qa']}/20")
        print(f"  Git Practices: {report['scores']['git_practices']}/10")
        print(f"  Deployment & Operations: {report['scores']['deployment_operations']}/10")
        
        print(f"\n🎯 Total Score: {report['total_score']}/100")
        print(f"📊 Grade: {report['grade']}")
        
        # Grade description
        grade_descriptions = {
            "A": "Excellent - Production-ready quality with comprehensive documentation",
            "B": "Good - Solid foundation with minor improvements needed",
            "C": "Fair - Basic functionality with significant improvements needed",
            "D": "Poor - Functional but needs major improvements",
            "F": "Unacceptable - Complete overhaul required"
        }
        
        print(f"\n📝 Grade Description: {grade_descriptions.get(report['grade'], 'Unknown')}")
        
        if report['recommendations']:
            print(f"\n🔧 Recommendations:")
            for i, rec in enumerate(report['recommendations'], 1):
                print(f"  {i}. {rec}")
        
        # Priority actions
        print(f"\n🚀 Priority Actions:")
        if report['total_score'] < 80:
            print("  1. Add comprehensive documentation")
            print("  2. Implement testing framework")
            print("  3. Set up CI/CD pipeline")
        else:
            print("  1. Add advanced features")
            print("  2. Optimize performance")
            print("  3. Add monitoring and logging")
        
        return report

def main():
    """Main evaluation function"""
    evaluator = RepositoryEvaluator()
    report = evaluator.evaluate_repository()
    evaluator.print_report(report)
    
    # Save report to file
    report_file = "repository_evaluation_report.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n💾 Detailed report saved to: {report_file}")
    
    return report

if __name__ == "__main__":
    main() 