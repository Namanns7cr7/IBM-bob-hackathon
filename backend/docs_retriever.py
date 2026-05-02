"""
Docs Retriever - Retrieves relevant documentation from local knowledge base
"""
from pathlib import Path
from typing import List, Dict, Any
import re


class DocsRetriever:
    def __init__(self, docs_base_path: str = "docs_knowledge"):
        self.docs_base_path = Path(docs_base_path)
        self.concept_to_doc_map = self._build_concept_map()
    
    def _build_concept_map(self) -> Dict[str, str]:
        """Map concepts to documentation files"""
        return {
            # Java concepts
            'REST Controller': 'java/rest_api.md',
            'Service Layer': 'java/spring_boot.md',
            'Repository Pattern': 'java/repository_pattern.md',
            'Dependency Injection': 'java/dependency_injection.md',
            'ORM Entity': 'java/spring_boot.md',
            'Database Transaction': 'java/spring_boot.md',
            'REST Endpoint': 'java/rest_api.md',
            'Exception Handling': 'java/exceptions.md',
            'Optional/Null Safety': 'java/oop.md',
            'Data Validation': 'java/spring_boot.md',
            'Basic OOP': 'java/oop.md',
            'Collections': 'java/collections.md',
            
            # Python concepts
            'FastAPI App': 'python/fastapi.md',
            'API Route': 'python/fastapi.md',
            'Async Function': 'python/async.md',
            'Type Hints': 'python/type_hints.md',
            'Functions': 'python/functions.md',
            
            # JavaScript/React concepts
            'React Component': 'javascript/react.md',
            'State Management': 'javascript/state_management.md',
            'Side Effects': 'javascript/hooks.md',
            'Props': 'javascript/components.md',
            'API Call': 'javascript/async.md',
            'Async/Await': 'javascript/async.md',
            'Event Handling': 'javascript/components.md',
            'List Rendering': 'javascript/components.md',
            'Context API': 'javascript/state_management.md',
            
            # Flutter/Dart concepts
            'Stateful Widget': 'flutter/stateful_widget.md',
            'Stateless Widget': 'flutter/widgets.md',
            'Async UI': 'flutter/async.md',
            'Stream': 'flutter/async.md',
            'Firebase Auth': 'flutter/firebase.md',
            'Firestore': 'flutter/firebase.md',
            'Navigation': 'flutter/widgets.md'
        }
    
    def get_docs_for_concepts(self, concepts: List[Dict[str, Any]], limit: int = 5) -> List[Dict[str, Any]]:
        """Retrieve documentation for detected concepts"""
        docs = []
        seen_files = set()
        
        for concept in concepts[:limit]:
            concept_name = concept['name']
            doc_path = self.concept_to_doc_map.get(concept_name)
            
            if doc_path and doc_path not in seen_files:
                full_path = self.docs_base_path / doc_path
                content = self._read_doc_file(full_path)
                
                if content:
                    docs.append({
                        'concept': concept_name,
                        'file': doc_path,
                        'content': content,
                        'category': concept.get('category', 'General')
                    })
                    seen_files.add(doc_path)
        
        return docs
    
    def get_doc_by_concept(self, concept_name: str) -> Dict[str, Any] | None:
        """Get documentation for a specific concept"""
        doc_path = self.concept_to_doc_map.get(concept_name)
        
        if doc_path:
            full_path = self.docs_base_path / doc_path
            content = self._read_doc_file(full_path)
            
            if content:
                return {
                    'concept': concept_name,
                    'file': doc_path,
                    'content': content
                }
        
        return None
    
    def search_docs(self, query: str, language: str | None = None) -> List[Dict[str, Any]]:
        """Search documentation by query"""
        results = []
        
        # Determine which language folder to search
        if language:
            search_paths = [self.docs_base_path / language.lower()]
        else:
            search_paths = [
                self.docs_base_path / 'java',
                self.docs_base_path / 'python',
                self.docs_base_path / 'javascript',
                self.docs_base_path / 'flutter'
            ]
        
        query_lower = query.lower()
        
        for search_path in search_paths:
            if not search_path.exists():
                continue
            
            for doc_file in search_path.glob('*.md'):
                content = self._read_doc_file(doc_file)
                if content and query_lower in content.lower():
                    results.append({
                        'file': str(doc_file.relative_to(self.docs_base_path)),
                        'title': doc_file.stem.replace('_', ' ').title(),
                        'content': self._extract_relevant_section(content, query_lower),
                        'language': search_path.name
                    })
        
        return results[:5]  # Return top 5 results
    
    def _read_doc_file(self, file_path: Path) -> str:
        """Read documentation file"""
        try:
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
        except Exception:
            pass
        return ""
    
    def _extract_relevant_section(self, content: str, query: str, context_lines: int = 5) -> str:
        """Extract relevant section from documentation"""
        lines = content.split('\n')
        relevant_lines = []
        
        for i, line in enumerate(lines):
            if query in line.lower():
                # Get context around the match
                start = max(0, i - context_lines)
                end = min(len(lines), i + context_lines + 1)
                relevant_lines.extend(lines[start:end])
                break
        
        if relevant_lines:
            return '\n'.join(relevant_lines)
        
        # If no match, return first few lines
        return '\n'.join(lines[:10])
    
    def get_all_available_docs(self) -> List[Dict[str, str]]:
        """Get list of all available documentation"""
        docs_list = []
        
        for language_dir in ['java', 'python', 'javascript', 'flutter']:
            lang_path = self.docs_base_path / language_dir
            if lang_path.exists():
                for doc_file in lang_path.glob('*.md'):
                    docs_list.append({
                        'language': language_dir,
                        'title': doc_file.stem.replace('_', ' ').title(),
                        'file': str(doc_file.relative_to(self.docs_base_path))
                    })
        
        return docs_list

# Made with Bob
