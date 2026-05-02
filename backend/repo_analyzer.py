"""
Repository Analyzer - Analyzes repository structure and extracts metadata
"""
from pathlib import Path
from typing import Dict, List, Any
import os


class RepoAnalyzer:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.file_tree = []
        self.source_files = []
        self.config_files = []
        self.stats = {
            'total_files': 0,
            'total_dirs': 0,
            'total_size': 0,
            'file_types': {}
        }
        
        # Directories to ignore
        self.ignore_dirs = {
            'node_modules', '__pycache__', '.git', '.venv', 'venv',
            'build', 'dist', 'target', '.idea', '.vscode', 'coverage'
        }
        
        # Config file patterns
        self.config_patterns = {
            'package.json', 'requirements.txt', 'pom.xml', 'build.gradle',
            'build.gradle.kts', 'pubspec.yaml', 'Cargo.toml', 'go.mod',
            'composer.json', 'Gemfile', 'pyproject.toml', '.env'
        }
        
        # Source file extensions
        self.source_extensions = {
            '.py', '.java', '.js', '.jsx', '.ts', '.tsx', '.dart',
            '.go', '.rs', '.cpp', '.c', '.h', '.hpp', '.cs', '.php',
            '.rb', '.kt', '.swift', '.scala', '.r', '.m', '.vue'
        }
    
    def analyze(self) -> Dict[str, Any]:
        """Main analysis method"""
        if not self.repo_path.exists():
            raise ValueError(f"Repository path does not exist: {self.repo_path}")
        
        # Scan directory structure
        self._scan_directory(self.repo_path)
        
        return {
            'file_tree': self.file_tree,
            'source_files': self.source_files,
            'config_files': self.config_files,
            'stats': self.stats
        }
    
    def _scan_directory(self, directory: Path, relative_path: str = ""):
        """Recursively scan directory"""
        try:
            for item in directory.iterdir():
                # Skip hidden files and ignored directories
                if item.name.startswith('.') and item.name not in {'.env', '.gitignore'}:
                    continue
                
                if item.is_dir():
                    if item.name in self.ignore_dirs:
                        continue
                    
                    self.stats['total_dirs'] += 1
                    
                    # Add directory to tree
                    dir_info = {
                        'name': item.name,
                        'path': str(Path(relative_path) / item.name) if relative_path else item.name,
                        'type': 'directory'
                    }
                    self.file_tree.append(dir_info)
                    
                    # Recursively scan subdirectory
                    new_relative = str(Path(relative_path) / item.name) if relative_path else item.name
                    self._scan_directory(item, new_relative)
                
                elif item.is_file():
                    self._process_file(item, relative_path)
        
        except PermissionError:
            pass  # Skip directories we can't access
    
    def _process_file(self, file_path: Path, relative_path: str):
        """Process individual file"""
        try:
            file_size = file_path.stat().st_size
            extension = file_path.suffix.lower()
            
            # Update stats
            self.stats['total_files'] += 1
            self.stats['total_size'] += file_size
            self.stats['file_types'][extension] = self.stats['file_types'].get(extension, 0) + 1
            
            # Build file info
            file_info = {
                'name': file_path.name,
                'path': str(Path(relative_path) / file_path.name) if relative_path else file_path.name,
                'type': 'file',
                'extension': extension,
                'size': file_size
            }
            
            self.file_tree.append(file_info)
            
            # Categorize file
            if file_path.name in self.config_patterns:
                self.config_files.append(file_info)
            
            if extension in self.source_extensions:
                # Read file content for source files (with size limit)
                if file_size < 500000:  # 500KB limit
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            file_info['content'] = content
                            file_info['lines'] = len(content.split('\n'))
                    except:
                        pass
                
                self.source_files.append(file_info)
        
        except (PermissionError, OSError):
            pass  # Skip files we can't access
    
    def get_file_by_path(self, file_path: str) -> Dict[str, Any] | None:
        """Get file info by path"""
        for file_info in self.file_tree:
            if file_info['path'] == file_path:
                return file_info
        return None
    
    def get_files_by_extension(self, extension: str) -> List[Dict[str, Any]]:
        """Get all files with specific extension"""
        return [f for f in self.file_tree if f.get('extension') == extension]

# Made with Bob