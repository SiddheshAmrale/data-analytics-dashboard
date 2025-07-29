#!/usr/bin/env python3
"""
Security scanning system for AI Projects Collection.

Provides comprehensive security checks including:
- Dependency vulnerability scanning
- Code security analysis
- API key detection
- Configuration security validation
"""

import os
import re
import json
import subprocess
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging


class SecurityScanner:
    """Comprehensive security scanner for AI projects."""
    
    def __init__(self, project_root: str = "."):
        """Initialize security scanner.
        
        Args:
            project_root: Root directory of the project
        """
        self.project_root = Path(project_root)
        self.logger = logging.getLogger(__name__)
        self.scan_results = {}
        
    def scan_dependencies(self) -> Dict[str, Any]:
        """Scan for dependency vulnerabilities.
        
        Returns:
            Dictionary with vulnerability scan results
        """
        self.logger.info("Scanning dependencies for vulnerabilities...")
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "vulnerabilities": [],
            "warnings": [],
            "summary": {}
        }
        
        try:
            # Check if safety is available
            result = subprocess.run(
                ["safety", "check", "--json"],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            if result.returncode == 0:
                vulns = json.loads(result.stdout)
                results["vulnerabilities"] = vulns
                results["summary"]["total_vulnerabilities"] = len(vulns)
            else:
                results["warnings"].append("Safety check failed or no vulnerabilities found")
                
        except FileNotFoundError:
            results["warnings"].append("Safety tool not installed")
        except Exception as e:
            results["warnings"].append(f"Error running safety check: {e}")
        
        self.scan_results["dependencies"] = results
        return results
    
    def scan_code_security(self) -> Dict[str, Any]:
        """Scan code for security issues.
        
        Returns:
            Dictionary with code security scan results
        """
        self.logger.info("Scanning code for security issues...")
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "issues": [],
            "warnings": [],
            "summary": {}
        }
        
        # Patterns to check for
        security_patterns = {
            "hardcoded_api_key": r"sk-[a-zA-Z0-9]{48}",
            "hardcoded_password": r"password\s*=\s*['\"][^'\"]+['\"]",
            "sql_injection": r"execute\s*\(\s*[\"'].*\+.*[\"']",
            "command_injection": r"os\.system\s*\(|subprocess\.run\s*\(",
            "eval_usage": r"eval\s*\(",
            "exec_usage": r"exec\s*\(",
            "pickle_usage": r"pickle\.loads\s*\(",
            "yaml_load": r"yaml\.load\s*\(",
        }
        
        python_files = list(self.project_root.rglob("*.py"))
        total_issues = 0
        
        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')
                
                file_issues = []
                
                for pattern_name, pattern in security_patterns.items():
                    matches = re.finditer(pattern, content, re.IGNORECASE)
                    
                    for match in matches:
                        line_num = content[:match.start()].count('\n') + 1
                        line_content = lines[line_num - 1].strip()
                        
                        issue = {
                            "pattern": pattern_name,
                            "line": line_num,
                            "content": line_content,
                            "severity": "high" if pattern_name in ["hardcoded_api_key", "eval_usage", "exec_usage"] else "medium"
                        }
                        file_issues.append(issue)
                        total_issues += 1
                
                if file_issues:
                    results["issues"].append({
                        "file": str(file_path.relative_to(self.project_root)),
                        "issues": file_issues
                    })
                    
            except Exception as e:
                results["warnings"].append(f"Error scanning {file_path}: {e}")
        
        results["summary"]["total_files_scanned"] = len(python_files)
        results["summary"]["total_issues_found"] = total_issues
        
        self.scan_results["code_security"] = results
        return results
    
    def scan_configuration_security(self) -> Dict[str, Any]:
        """Scan configuration files for security issues.
        
        Returns:
            Dictionary with configuration security scan results
        """
        self.logger.info("Scanning configuration files for security issues...")
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "issues": [],
            "warnings": [],
            "summary": {}
        }
        
        config_files = [
            ".env",
            ".env.local",
            ".env.production",
            "config.py",
            "settings.py",
            "docker-compose.yml",
            "Dockerfile"
        ]
        
        total_issues = 0
        
        for config_file in config_files:
            file_path = self.project_root / config_file
            
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    file_issues = []
                    
                    # Check for hardcoded secrets
                    secret_patterns = [
                        r"OPENAI_API_KEY\s*=\s*['\"][^'\"]+['\"]",
                        r"SECRET_KEY\s*=\s*['\"][^'\"]+['\"]",
                        r"PASSWORD\s*=\s*['\"][^'\"]+['\"]",
                        r"TOKEN\s*=\s*['\"][^'\"]+['\"]",
                    ]
                    
                    for pattern in secret_patterns:
                        matches = re.finditer(pattern, content, re.IGNORECASE)
                        
                        for match in matches:
                            line_num = content[:match.start()].count('\n') + 1
                            line_content = content.split('\n')[line_num - 1].strip()
                            
                            issue = {
                                "type": "hardcoded_secret",
                                "line": line_num,
                                "content": line_content[:50] + "..." if len(line_content) > 50 else line_content,
                                "severity": "high"
                            }
                            file_issues.append(issue)
                            total_issues += 1
                    
                    # Check for insecure permissions in Docker
                    if config_file == "Dockerfile":
                        if "USER root" in content and "USER app" not in content:
                            file_issues.append({
                                "type": "insecure_docker_user",
                                "line": content.find("USER root") // 80 + 1,
                                "content": "Running as root user",
                                "severity": "high"
                            })
                            total_issues += 1
                    
                    if file_issues:
                        results["issues"].append({
                            "file": config_file,
                            "issues": file_issues
                        })
                        
                except Exception as e:
                    results["warnings"].append(f"Error scanning {config_file}: {e}")
        
        results["summary"]["total_config_files_scanned"] = len(config_files)
        results["summary"]["total_issues_found"] = total_issues
        
        self.scan_results["configuration_security"] = results
        return results
    
    def scan_file_permissions(self) -> Dict[str, Any]:
        """Scan file permissions for security issues.
        
        Returns:
            Dictionary with file permission scan results
        """
        self.logger.info("Scanning file permissions...")
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "issues": [],
            "warnings": [],
            "summary": {}
        }
        
        sensitive_files = [
            ".env",
            ".env.local",
            ".env.production",
            "*.key",
            "*.pem",
            "*.p12",
            "*.pfx"
        ]
        
        total_issues = 0
        
        for pattern in sensitive_files:
            for file_path in self.project_root.rglob(pattern):
                try:
                    stat = file_path.stat()
                    mode = stat.st_mode & 0o777
                    
                    # Check if file is world-readable
                    if mode & 0o004:
                        results["issues"].append({
                            "file": str(file_path.relative_to(self.project_root)),
                            "issue": "World-readable file",
                            "permissions": oct(mode),
                            "severity": "high"
                        })
                        total_issues += 1
                    
                    # Check if file is world-writable
                    if mode & 0o002:
                        results["issues"].append({
                            "file": str(file_path.relative_to(self.project_root)),
                            "issue": "World-writable file",
                            "permissions": oct(mode),
                            "severity": "critical"
                        })
                        total_issues += 1
                        
                except Exception as e:
                    results["warnings"].append(f"Error checking {file_path}: {e}")
        
        results["summary"]["total_issues_found"] = total_issues
        
        self.scan_results["file_permissions"] = results
        return results
    
    def scan_git_security(self) -> Dict[str, Any]:
        """Scan Git repository for security issues.
        
        Returns:
            Dictionary with Git security scan results
        """
        self.logger.info("Scanning Git repository for security issues...")
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "issues": [],
            "warnings": [],
            "summary": {}
        }
        
        # Check .gitignore
        gitignore_path = self.project_root / ".gitignore"
        if not gitignore_path.exists():
            results["issues"].append({
                "issue": "Missing .gitignore file",
                "severity": "medium",
                "recommendation": "Create a .gitignore file to exclude sensitive files"
            })
        
        # Check for sensitive files in Git
        sensitive_patterns = [
            r"\.env",
            r"\.key$",
            r"\.pem$",
            r"secrets/",
            r"config\.local",
            r"settings\.local"
        ]
        
        try:
            # Get list of tracked files
            result = subprocess.run(
                ["git", "ls-files"],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            if result.returncode == 0:
                tracked_files = result.stdout.strip().split('\n')
                
                for file_path in tracked_files:
                    for pattern in sensitive_patterns:
                        if re.search(pattern, file_path, re.IGNORECASE):
                            results["issues"].append({
                                "file": file_path,
                                "issue": "Sensitive file tracked in Git",
                                "severity": "high",
                                "recommendation": "Remove from Git and add to .gitignore"
                            })
                            break
                            
        except Exception as e:
            results["warnings"].append(f"Error checking Git repository: {e}")
        
        results["summary"]["total_issues_found"] = len(results["issues"])
        
        self.scan_results["git_security"] = results
        return results
    
    def run_full_scan(self) -> Dict[str, Any]:
        """Run a complete security scan.
        
        Returns:
            Dictionary with all scan results
        """
        self.logger.info("Starting comprehensive security scan...")
        
        full_results = {
            "scan_timestamp": datetime.now().isoformat(),
            "project_root": str(self.project_root),
            "scans": {}
        }
        
        # Run all scans
        full_results["scans"]["dependencies"] = self.scan_dependencies()
        full_results["scans"]["code_security"] = self.scan_code_security()
        full_results["scans"]["configuration_security"] = self.scan_configuration_security()
        full_results["scans"]["file_permissions"] = self.scan_file_permissions()
        full_results["scans"]["git_security"] = self.scan_git_security()
        
        # Generate summary
        total_issues = 0
        critical_issues = 0
        high_issues = 0
        medium_issues = 0
        
        for scan_name, scan_result in full_results["scans"].items():
            if "issues" in scan_result:
                for issue_group in scan_result["issues"]:
                    if isinstance(issue_group, dict) and "issues" in issue_group:
                        for issue in issue_group["issues"]:
                            total_issues += 1
                            severity = issue.get("severity", "medium")
                            if severity == "critical":
                                critical_issues += 1
                            elif severity == "high":
                                high_issues += 1
                            elif severity == "medium":
                                medium_issues += 1
        
        full_results["summary"] = {
            "total_issues": total_issues,
            "critical_issues": critical_issues,
            "high_issues": high_issues,
            "medium_issues": medium_issues,
            "overall_severity": "critical" if critical_issues > 0 else "high" if high_issues > 0 else "medium" if medium_issues > 0 else "low"
        }
        
        self.scan_results = full_results
        return full_results
    
    def generate_report(self, output_file: Optional[str] = None) -> str:
        """Generate a security scan report.
        
        Args:
            output_file: Optional file to save the report
            
        Returns:
            Report content as string
        """
        if not self.scan_results:
            self.run_full_scan()
        
        report_lines = [
            "=" * 60,
            "SECURITY SCAN REPORT",
            "=" * 60,
            f"Scan Date: {self.scan_results.get('scan_timestamp', 'Unknown')}",
            f"Project: {self.scan_results.get('project_root', 'Unknown')}",
            "",
            "SUMMARY:",
            f"  Total Issues: {self.scan_results['summary']['total_issues']}",
            f"  Critical: {self.scan_results['summary']['critical_issues']}",
            f"  High: {self.scan_results['summary']['high_issues']}",
            f"  Medium: {self.scan_results['summary']['medium_issues']}",
            f"  Overall Severity: {self.scan_results['summary']['overall_severity'].upper()}",
            "",
            "DETAILED RESULTS:",
            ""
        ]
        
        for scan_name, scan_result in self.scan_results["scans"].items():
            report_lines.extend([
                f"{scan_name.upper().replace('_', ' ')}:",
                "-" * 40
            ])
            
            if "issues" in scan_result and scan_result["issues"]:
                for issue_group in scan_result["issues"]:
                    if isinstance(issue_group, dict) and "issues" in issue_group:
                        report_lines.append(f"  File: {issue_group['file']}")
                        for issue in issue_group["issues"]:
                            report_lines.append(f"    [{issue['severity'].upper()}] {issue.get('content', 'Unknown issue')}")
                    else:
                        report_lines.append(f"  [{issue_group.get('severity', 'medium').upper()}] {issue_group.get('issue', 'Unknown issue')}")
            else:
                report_lines.append("  No issues found")
            
            if "warnings" in scan_result and scan_result["warnings"]:
                report_lines.append("  Warnings:")
                for warning in scan_result["warnings"]:
                    report_lines.append(f"    - {warning}")
            
            report_lines.append("")
        
        report_content = "\n".join(report_lines)
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(report_content)
        
        return report_content


def main():
    """Main function for security scanning."""
    scanner = SecurityScanner()
    
    print("🔒 Starting security scan...")
    results = scanner.run_full_scan()
    
    print("\n📊 Scan Results:")
    print(f"Total Issues: {results['summary']['total_issues']}")
    print(f"Critical: {results['summary']['critical_issues']}")
    print(f"High: {results['summary']['high_issues']}")
    print(f"Medium: {results['summary']['medium_issues']}")
    print(f"Overall Severity: {results['summary']['overall_severity'].upper()}")
    
    # Generate report
    report = scanner.generate_report("security_scan_report.txt")
    print(f"\n📄 Report saved to: security_scan_report.txt")
    
    return results


if __name__ == "__main__":
    main() 