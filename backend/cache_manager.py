"""
Cache Manager - Manages caching of analysis results
Uses JSON files for simple file-based caching
"""
import json
import hashlib
from pathlib import Path
from typing import Dict, Any
from datetime import datetime


class CacheManager:
    def __init__(self, cache_dir: str = "cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
    
    def generate_cache_key(self, repo_id: str, skill_level: str, goal: str) -> str:
        """Generate a unique cache key"""
        key_string = f"{repo_id}_{skill_level}_{goal}"
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def get_cached_analysis(self, cache_key: str) -> Dict[str, Any] | None:
        """Retrieve cached analysis if it exists"""
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        if cache_file.exists():
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cached_data = json.load(f)
                    
                    # Check if cache is still valid (optional: add expiration logic)
                    return cached_data
            except Exception:
                pass
        
        return None
    
    def save_analysis(self, cache_key: str, analysis_data: Dict[str, Any]) -> bool:
        """Save analysis results to cache"""
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        try:
            # Add metadata
            cache_data = {
                'cached_at': datetime.now().isoformat(),
                'data': analysis_data
            }
            
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2)
            
            return True
        except Exception:
            return False
    
    def clear_cache(self, cache_key: str | None = None) -> bool:
        """Clear specific cache or all cache"""
        try:
            if cache_key:
                cache_file = self.cache_dir / f"{cache_key}.json"
                if cache_file.exists():
                    cache_file.unlink()
            else:
                # Clear all cache files
                for cache_file in self.cache_dir.glob("*.json"):
                    cache_file.unlink()
            
            return True
        except Exception:
            return False
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        cache_files = list(self.cache_dir.glob("*.json"))
        
        total_size = sum(f.stat().st_size for f in cache_files)
        
        return {
            'total_cached': len(cache_files),
            'total_size_bytes': total_size,
            'total_size_mb': round(total_size / (1024 * 1024), 2)
        }

# Made with Bob
