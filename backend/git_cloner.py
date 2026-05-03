"""
Git Repository Cloner
Clones GitHub repositories for analysis
"""
import os
import shutil
import subprocess
import tempfile
import uuid
from pathlib import Path
from typing import Dict, Optional, Any
import re

class GitCloner:
    def __init__(self, base_upload_dir: str = "uploads"):
        self.base_upload_dir = Path(base_upload_dir)
        self.base_upload_dir.mkdir(exist_ok=True)
    
    def parse_github_url(self, url: str) -> Optional[Dict[str, str]]:
        """
        Parse GitHub URL to extract owner and repo name
        Supports formats:
        - https://github.com/owner/repo
        - https://github.com/owner/repo.git
        - git@github.com:owner/repo.git
        """
        patterns = [
            r'github\.com[:/]([^/]+)/([^/\.]+)',  # HTTPS or SSH
            r'github\.com/([^/]+)/([^/]+)\.git',  # HTTPS with .git
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                owner, repo = match.groups()
                # Remove .git suffix if present
                repo = repo.replace('.git', '')
                return {
                    'owner': owner,
                    'repo': repo,
                    'full_name': f"{owner}/{repo}"
                }
        return None
    
    def clone_repository(self, github_url: str, branch: str = "main") -> Dict[str, Any]:
        """
        Clone a GitHub repository and return analysis metadata
        
        Args:
            github_url: GitHub repository URL
            branch: Branch to clone (default: main)
        
        Returns:
            Dict with session_id, repo_path, and metadata
        """
        # Parse GitHub URL
        repo_info = self.parse_github_url(github_url)
        if not repo_info:
            raise ValueError(f"Invalid GitHub URL: {github_url}")
        
        # Generate session ID
        session_id = str(uuid.uuid4())
        session_dir = self.base_upload_dir / session_id
        session_dir.mkdir(parents=True, exist_ok=True)
        
        # Clone repository
        repo_path = session_dir / repo_info['repo']
        
        try:
            # Try main branch first
            result = subprocess.run(
                ['git', 'clone', '--depth', '1', '--branch', branch, github_url, str(repo_path)],
                capture_output=True,
                text=True,
                timeout=120  # 2 minute timeout
            )
            
            # If main branch fails, try master
            if result.returncode != 0 and branch == "main":
                result = subprocess.run(
                    ['git', 'clone', '--depth', '1', '--branch', 'master', github_url, str(repo_path)],
                    capture_output=True,
                    text=True,
                    timeout=120
                )
            
            # If still fails, clone without specifying branch
            if result.returncode != 0:
                result = subprocess.run(
                    ['git', 'clone', '--depth', '1', github_url, str(repo_path)],
                    capture_output=True,
                    text=True,
                    timeout=120
                )
            
            if result.returncode != 0:
                raise Exception(f"Git clone failed: {result.stderr}")
            
            # Get repository statistics
            stats = self._get_repo_stats(repo_path)
            
            return {
                'session_id': session_id,
                'repo_path': str(repo_path),
                'repo_info': repo_info,
                'stats': stats,
                'github_url': github_url,
                'success': True
            }
        
        except subprocess.TimeoutExpired:
            # Cleanup on timeout
            if session_dir.exists():
                shutil.rmtree(session_dir)
            raise Exception("Repository clone timed out (>2 minutes). Repository may be too large.")
        
        except Exception as e:
            # Cleanup on error
            if session_dir.exists():
                shutil.rmtree(session_dir)
            raise Exception(f"Failed to clone repository: {str(e)}")
    
    def _get_repo_stats(self, repo_path: Path) -> Dict[str, Any]:
        """Get basic statistics about the cloned repository"""
        stats = {
            'total_files': 0,
            'total_lines': 0,
            'file_types': {},
            'size_mb': 0
        }
        
        try:
            # Count files and lines
            for file_path in repo_path.rglob('*'):
                if file_path.is_file() and not self._is_ignored(file_path):
                    stats['total_files'] += 1
                    
                    # Count file type
                    ext = file_path.suffix or 'no_extension'
                    stats['file_types'][ext] = stats['file_types'].get(ext, 0) + 1
                    
                    # Count lines for text files
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            stats['total_lines'] += sum(1 for _ in f)
                    except:
                        pass
            
            # Calculate directory size
            total_size = sum(f.stat().st_size for f in repo_path.rglob('*') if f.is_file())
            stats['size_mb'] = round(total_size / (1024 * 1024), 2)
        
        except Exception as e:
            print(f"Error calculating stats: {e}")
        
        return stats
    
    def _is_ignored(self, file_path: Path) -> bool:
        """Check if file should be ignored (e.g., .git, node_modules)"""
        ignored_dirs = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', 'dist', 'build'}
        return any(part in ignored_dirs for part in file_path.parts)
    
    def cleanup_session(self, session_id: str) -> bool:
        """Remove cloned repository and session directory"""
        session_dir = self.base_upload_dir / session_id
        if session_dir.exists():
            try:
                shutil.rmtree(session_dir)
                return True
            except Exception as e:
                print(f"Error cleaning up session {session_id}: {e}")
                return False
        return False

# Made with Bob
