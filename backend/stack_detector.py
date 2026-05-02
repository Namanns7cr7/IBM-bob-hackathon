"""
Stack Detector - Detects programming languages and frameworks
Uses file extensions and config files for local detection
"""
from pathlib import Path
from typing import Dict, List, Any
import json


class StackDetector:
    def __init__(self, repo_path: str, file_tree: List[Dict], config_files: List[Dict]):
        self.repo_path = Path(repo_path)
        self.file_tree = file_tree
        self.config_files = config_files
        self.detected_languages = {}
        self.detected_frameworks = []
        self.primary_language = None
        self.primary_framework = None
    
    def detect(self) -> Dict[str, Any]:
        """Main detection method"""
        self._detect_languages()
        self._detect_frameworks()
        self._determine_primary_stack()
        
        return {
            'languages': self.detected_languages,
            'frameworks': self.detected_frameworks,
            'primary_language': self.primary_language,
            'primary_framework': self.primary_framework,
            'stack_summary': self._generate_summary()
        }
    
    def _detect_languages(self):
        """Detect programming languages from file extensions"""
        language_map = {
            '.py': 'Python',
            '.java': 'Java',
            '.js': 'JavaScript',
            '.jsx': 'JavaScript',
            '.ts': 'TypeScript',
            '.tsx': 'TypeScript',
            '.dart': 'Dart',
            '.go': 'Go',
            '.rs': 'Rust',
            '.cpp': 'C++',
            '.c': 'C',
            '.h': 'C/C++',
            '.hpp': 'C++',
            '.cs': 'C#',
            '.php': 'PHP',
            '.rb': 'Ruby',
            '.kt': 'Kotlin',
            '.swift': 'Swift',
            '.scala': 'Scala',
            '.r': 'R',
            '.m': 'Objective-C',
            '.vue': 'Vue.js',
            '.html': 'HTML',
            '.css': 'CSS',
            '.scss': 'SCSS',
            '.sql': 'SQL'
        }
        
        language_counts = {}
        
        for file_info in self.file_tree:
            if file_info['type'] == 'file':
                ext = file_info.get('extension', '')
                if ext in language_map:
                    lang = language_map[ext]
                    language_counts[lang] = language_counts.get(lang, 0) + 1
        
        # Convert to percentage
        total = sum(language_counts.values())
        if total > 0:
            self.detected_languages = {
                lang: {
                    'count': count,
                    'percentage': round((count / total) * 100, 1)
                }
                for lang, count in sorted(language_counts.items(), key=lambda x: x[1], reverse=True)
            }
    
    def _detect_frameworks(self):
        """Detect frameworks from config files and patterns"""
        framework_detectors = [
            self._detect_java_frameworks,
            self._detect_python_frameworks,
            self._detect_javascript_frameworks,
            self._detect_mobile_frameworks,
            self._detect_other_frameworks
        ]
        
        for detector in framework_detectors:
            frameworks = detector()
            self.detected_frameworks.extend(frameworks)
    
    def _detect_java_frameworks(self) -> List[Dict[str, str]]:
        """Detect Java frameworks"""
        frameworks = []
        
        # Check for Maven/Spring Boot
        if self._file_exists('pom.xml'):
            frameworks.append({
                'name': 'Maven',
                'type': 'Build Tool',
                'language': 'Java'
            })
            
            # Check pom.xml content for Spring Boot
            pom_content = self._read_file('pom.xml')
            if pom_content and 'spring-boot' in pom_content.lower():
                frameworks.append({
                    'name': 'Spring Boot',
                    'type': 'Framework',
                    'language': 'Java'
                })
        
        # Check for Gradle
        if self._file_exists('build.gradle') or self._file_exists('build.gradle.kts'):
            frameworks.append({
                'name': 'Gradle',
                'type': 'Build Tool',
                'language': 'Java/Kotlin'
            })
            
            gradle_content = self._read_file('build.gradle')
            if gradle_content and 'spring-boot' in gradle_content.lower():
                frameworks.append({
                    'name': 'Spring Boot',
                    'type': 'Framework',
                    'language': 'Java'
                })
        
        return frameworks
    
    def _detect_python_frameworks(self) -> List[Dict[str, str]]:
        """Detect Python frameworks"""
        frameworks = []
        
        # Check requirements.txt
        if self._file_exists('requirements.txt'):
            req_content = self._read_file('requirements.txt')
            if req_content:
                req_lower = req_content.lower()
                if 'fastapi' in req_lower:
                    frameworks.append({
                        'name': 'FastAPI',
                        'type': 'Framework',
                        'language': 'Python'
                    })
                if 'flask' in req_lower:
                    frameworks.append({
                        'name': 'Flask',
                        'type': 'Framework',
                        'language': 'Python'
                    })
                if 'django' in req_lower:
                    frameworks.append({
                        'name': 'Django',
                        'type': 'Framework',
                        'language': 'Python'
                    })
        
        # Check pyproject.toml
        if self._file_exists('pyproject.toml'):
            frameworks.append({
                'name': 'Poetry/Modern Python',
                'type': 'Package Manager',
                'language': 'Python'
            })
        
        return frameworks
    
    def _detect_javascript_frameworks(self) -> List[Dict[str, str]]:
        """Detect JavaScript/TypeScript frameworks"""
        frameworks = []
        
        if self._file_exists('package.json'):
            pkg_content = self._read_file('package.json')
            if pkg_content:
                try:
                    pkg_data = json.loads(pkg_content)
                    dependencies = {**pkg_data.get('dependencies', {}), **pkg_data.get('devDependencies', {})}
                    
                    if 'react' in dependencies:
                        frameworks.append({
                            'name': 'React',
                            'type': 'Framework',
                            'language': 'JavaScript'
                        })
                    if 'next' in dependencies:
                        frameworks.append({
                            'name': 'Next.js',
                            'type': 'Framework',
                            'language': 'JavaScript'
                        })
                    if 'vue' in dependencies:
                        frameworks.append({
                            'name': 'Vue.js',
                            'type': 'Framework',
                            'language': 'JavaScript'
                        })
                    if 'angular' in dependencies or '@angular/core' in dependencies:
                        frameworks.append({
                            'name': 'Angular',
                            'type': 'Framework',
                            'language': 'TypeScript'
                        })
                    if 'express' in dependencies:
                        frameworks.append({
                            'name': 'Express.js',
                            'type': 'Framework',
                            'language': 'JavaScript'
                        })
                    if 'vite' in dependencies:
                        frameworks.append({
                            'name': 'Vite',
                            'type': 'Build Tool',
                            'language': 'JavaScript'
                        })
                except:
                    pass
        
        return frameworks
    
    def _detect_mobile_frameworks(self) -> List[Dict[str, str]]:
        """Detect mobile frameworks"""
        frameworks = []
        
        # Flutter
        if self._file_exists('pubspec.yaml'):
            frameworks.append({
                'name': 'Flutter',
                'type': 'Framework',
                'language': 'Dart'
            })
            
            pubspec_content = self._read_file('pubspec.yaml')
            if pubspec_content:
                if 'firebase' in pubspec_content.lower():
                    frameworks.append({
                        'name': 'Firebase',
                        'type': 'Backend Service',
                        'language': 'Dart'
                    })
        
        # React Native
        if self._file_exists('package.json'):
            pkg_content = self._read_file('package.json')
            if pkg_content and 'react-native' in pkg_content.lower():
                frameworks.append({
                    'name': 'React Native',
                    'type': 'Framework',
                    'language': 'JavaScript'
                })
        
        return frameworks
    
    def _detect_other_frameworks(self) -> List[Dict[str, str]]:
        """Detect other frameworks"""
        frameworks = []
        
        # Go
        if self._file_exists('go.mod'):
            frameworks.append({
                'name': 'Go Modules',
                'type': 'Package Manager',
                'language': 'Go'
            })
        
        # Rust
        if self._file_exists('Cargo.toml'):
            frameworks.append({
                'name': 'Cargo',
                'type': 'Package Manager',
                'language': 'Rust'
            })
        
        # PHP
        if self._file_exists('composer.json'):
            frameworks.append({
                'name': 'Composer',
                'type': 'Package Manager',
                'language': 'PHP'
            })
            
            composer_content = self._read_file('composer.json')
            if composer_content and 'laravel' in composer_content.lower():
                frameworks.append({
                    'name': 'Laravel',
                    'type': 'Framework',
                    'language': 'PHP'
                })
        
        # Ruby
        if self._file_exists('Gemfile'):
            frameworks.append({
                'name': 'Bundler',
                'type': 'Package Manager',
                'language': 'Ruby'
            })
            
            gemfile_content = self._read_file('Gemfile')
            if gemfile_content and 'rails' in gemfile_content.lower():
                frameworks.append({
                    'name': 'Ruby on Rails',
                    'type': 'Framework',
                    'language': 'Ruby'
                })
        
        return frameworks
    
    def _determine_primary_stack(self):
        """Determine the primary language and framework"""
        if self.detected_languages:
            self.primary_language = max(
                self.detected_languages.items(),
                key=lambda x: x[1]['count']
            )[0]
        
        if self.detected_frameworks:
            # Prioritize frameworks over build tools
            framework_priority = ['Framework', 'Backend Service', 'Build Tool', 'Package Manager']
            for priority in framework_priority:
                for fw in self.detected_frameworks:
                    if fw['type'] == priority:
                        self.primary_framework = fw['name']
                        return
    
    def _generate_summary(self) -> str:
        """Generate a human-readable summary"""
        parts = []
        
        if self.primary_language:
            parts.append(f"Primary Language: {self.primary_language}")
        
        if self.primary_framework:
            parts.append(f"Primary Framework: {self.primary_framework}")
        
        if self.detected_frameworks:
            other_frameworks = [fw['name'] for fw in self.detected_frameworks if fw['name'] != self.primary_framework]
            if other_frameworks:
                parts.append(f"Other Tools: {', '.join(other_frameworks[:3])}")
        
        return ' | '.join(parts) if parts else "Stack detection in progress"
    
    def _file_exists(self, filename: str) -> bool:
        """Check if a file exists in the repository"""
        for file_info in self.file_tree:
            if file_info['type'] == 'file' and file_info['name'].lower() == filename.lower():
                return True
        return False
    
    def _read_file(self, filename: str, max_size: int = 100000) -> str:
        """Read file content safely"""
        try:
            for file_info in self.file_tree:
                if file_info['type'] == 'file' and file_info['name'].lower() == filename.lower():
                    file_path = self.repo_path / file_info['path']
                    if file_path.exists() and file_path.stat().st_size < max_size:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            return f.read()
        except:
            pass
        return ""

# Made with Bob
