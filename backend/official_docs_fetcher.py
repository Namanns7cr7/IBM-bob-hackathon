"""
Official Documentation Fetcher
Fetches and caches official documentation from web sources
"""
import json
import hashlib
from pathlib import Path
from typing import Dict, Any, Optional
import requests
from bs4 import BeautifulSoup
import time


class OfficialDocsFetcher:
    def __init__(self, cache_dir: str = "docs_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.timeout = 10  # seconds
        self.max_retries = 2
    
    def fetch_docs(self, doc_entry: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fetch documentation for a concept
        Returns cached version if available, otherwise fetches from web
        """
        concept = doc_entry['concept']
        source_url = doc_entry['source_url']
        
        # Check cache first
        cached_doc = self._get_from_cache(source_url)
        if cached_doc:
            return {
                'concept': concept,
                'source_name': doc_entry['source_name'],
                'source_url': source_url,
                'content': cached_doc['content'],
                'key_points': doc_entry['key_points'],
                'cached': True,
                'fetch_time': cached_doc.get('fetch_time', 'unknown')
            }
        
        # Try to fetch from web
        try:
            content = self._fetch_from_web(source_url)
            if content:
                # Save to cache
                self._save_to_cache(source_url, content)
                return {
                    'concept': concept,
                    'source_name': doc_entry['source_name'],
                    'source_url': source_url,
                    'content': content,
                    'key_points': doc_entry['key_points'],
                    'cached': False,
                    'fetch_time': time.strftime('%Y-%m-%d %H:%M:%S')
                }
        except Exception as e:
            print(f"Failed to fetch {source_url}: {str(e)}")
        
        # Fallback to registry summary
        return {
            'concept': concept,
            'source_name': doc_entry['source_name'],
            'source_url': source_url,
            'content': doc_entry['fallback_summary'],
            'key_points': doc_entry['key_points'],
            'cached': False,
            'fallback': True,
            'fetch_time': 'fallback'
        }
    
    def _fetch_from_web(self, url: str) -> Optional[str]:
        """Fetch and extract readable content from URL"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        for attempt in range(self.max_retries):
            try:
                response = requests.get(url, headers=headers, timeout=self.timeout)
                response.raise_for_status()
                
                # Parse HTML
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Remove unwanted elements
                for element in soup(['script', 'style', 'nav', 'header', 'footer', 
                                    'aside', 'iframe', 'noscript', 'meta', 'link']):
                    element.decompose()
                
                # Extract main content
                # Try common content containers
                main_content = None
                for selector in ['main', 'article', '.content', '#content', 
                               '.documentation', '.doc-content', '.markdown-body']:
                    main_content = soup.select_one(selector)
                    if main_content:
                        break
                
                if not main_content:
                    main_content = soup.body
                
                if main_content:
                    # Get text and clean it
                    text = main_content.get_text(separator='\n', strip=True)
                    
                    # Clean up excessive whitespace
                    lines = [line.strip() for line in text.split('\n') if line.strip()]
                    text = '\n'.join(lines)
                    
                    # Limit length (keep first 3000 characters)
                    if len(text) > 3000:
                        text = text[:3000] + '\n\n[Content truncated for brevity...]'
                    
                    return text
                
                return None
                
            except requests.RequestException as e:
                if attempt < self.max_retries - 1:
                    time.sleep(1)  # Wait before retry
                    continue
                raise e
        
        return None
    
    def _get_cache_key(self, url: str) -> str:
        """Generate cache key from URL"""
        return hashlib.md5(url.encode()).hexdigest()
    
    def _get_from_cache(self, url: str) -> Optional[Dict[str, Any]]:
        """Get cached documentation"""
        cache_key = self._get_cache_key(url)
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        if cache_file.exists():
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        
        return None
    
    def _save_to_cache(self, url: str, content: str):
        """Save documentation to cache"""
        cache_key = self._get_cache_key(url)
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        try:
            cache_data = {
                'url': url,
                'content': content,
                'fetch_time': time.strftime('%Y-%m-%d %H:%M:%S'),
                'cached_at': time.time()
            }
            
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Failed to cache {url}: {str(e)}")
    
    def clear_cache(self, url: Optional[str] = None):
        """Clear cache for specific URL or all cache"""
        if url:
            cache_key = self._get_cache_key(url)
            cache_file = self.cache_dir / f"{cache_key}.json"
            if cache_file.exists():
                cache_file.unlink()
        else:
            # Clear all cache
            for cache_file in self.cache_dir.glob("*.json"):
                cache_file.unlink()
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        cache_files = list(self.cache_dir.glob("*.json"))
        total_size = sum(f.stat().st_size for f in cache_files)
        
        return {
            'total_cached': len(cache_files),
            'total_size_bytes': total_size,
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'cache_dir': str(self.cache_dir)
        }


# Made with Bob