"""
Local Learning Memory
Stores user's learning progress locally on their machine
"""
import json
import uuid
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime


class LocalMemory:
    def __init__(self, memory_dir: str = "local_memory"):
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(exist_ok=True)
    
    def create_session(
        self,
        repo_id: str,
        repo_name: str,
        skill_level: str,
        goal: str
    ) -> str:
        """Create a new learning session"""
        session_id = str(uuid.uuid4())
        
        session_data = {
            'session_id': session_id,
            'repo_id': repo_id,
            'repo_name': repo_name,
            'skill_level': skill_level,
            'goal': goal,
            'concepts_learned': [],
            'debug_sessions': [],
            'feature_walkthroughs': [],
            'quiz_scores': [],
            'notes': [],
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'total_time_spent': 0,  # minutes
            'understanding_debt_history': []
        }
        
        self._save_session(session_id, session_data)
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session data"""
        session_file = self.memory_dir / f"{session_id}.json"
        
        if session_file.exists():
            try:
                with open(session_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        
        return None
    
    def update_session(self, session_id: str, updates: Dict[str, Any]):
        """Update session data"""
        session_data = self.get_session(session_id)
        
        if session_data:
            session_data.update(updates)
            session_data['updated_at'] = datetime.now().isoformat()
            self._save_session(session_id, session_data)
    
    def add_concept_learned(
        self,
        session_id: str,
        concept: str,
        confidence: str = "learning"
    ):
        """Record that a concept was learned"""
        session_data = self.get_session(session_id)
        
        if session_data:
            concept_entry = {
                'concept': concept,
                'confidence': confidence,  # learning, understood, mastered
                'learned_at': datetime.now().isoformat(),
                'review_count': 0
            }
            
            # Check if concept already exists
            existing = next(
                (c for c in session_data['concepts_learned'] if c['concept'] == concept),
                None
            )
            
            if existing:
                existing['review_count'] += 1
                existing['confidence'] = confidence
                existing['last_reviewed'] = datetime.now().isoformat()
            else:
                session_data['concepts_learned'].append(concept_entry)
            
            self._save_session(session_id, session_data)
    
    def add_debug_session(
        self,
        session_id: str,
        error_type: str,
        resolution: str,
        time_spent: int = 0
    ):
        """Record a debugging session"""
        session_data = self.get_session(session_id)
        
        if session_data:
            debug_entry = {
                'error_type': error_type,
                'resolution': resolution,
                'time_spent_minutes': time_spent,
                'debugged_at': datetime.now().isoformat(),
                'success': True
            }
            
            session_data['debug_sessions'].append(debug_entry)
            session_data['total_time_spent'] += time_spent
            self._save_session(session_id, session_data)
    
    def add_feature_walkthrough(
        self,
        session_id: str,
        feature_name: str,
        files_explored: List[str],
        concepts_learned: List[str]
    ):
        """Record a feature walkthrough"""
        session_data = self.get_session(session_id)
        
        if session_data:
            walkthrough_entry = {
                'feature_name': feature_name,
                'files_explored': files_explored,
                'concepts_learned': concepts_learned,
                'completed_at': datetime.now().isoformat()
            }
            
            session_data['feature_walkthroughs'].append(walkthrough_entry)
            
            # Also add concepts to concepts_learned
            for concept in concepts_learned:
                self.add_concept_learned(session_id, concept, "learning")
            
            self._save_session(session_id, session_data)
    
    def add_quiz_score(
        self,
        session_id: str,
        concept: str,
        score: int,
        total: int
    ):
        """Record a quiz score"""
        session_data = self.get_session(session_id)
        
        if session_data:
            quiz_entry = {
                'concept': concept,
                'score': score,
                'total': total,
                'percentage': round((score / total) * 100, 1) if total > 0 else 0,
                'taken_at': datetime.now().isoformat()
            }
            
            session_data['quiz_scores'].append(quiz_entry)
            
            # Update concept confidence based on score
            if quiz_entry['percentage'] >= 80:
                self.add_concept_learned(session_id, concept, "mastered")
            elif quiz_entry['percentage'] >= 60:
                self.add_concept_learned(session_id, concept, "understood")
            
            self._save_session(session_id, session_data)
    
    def add_note(
        self,
        session_id: str,
        note: str,
        category: str = "general"
    ):
        """Add a learning note"""
        session_data = self.get_session(session_id)
        
        if session_data:
            note_entry = {
                'note': note,
                'category': category,
                'created_at': datetime.now().isoformat()
            }
            
            session_data['notes'].append(note_entry)
            self._save_session(session_id, session_data)
    
    def update_understanding_debt(
        self,
        session_id: str,
        debt_score: float,
        level: str
    ):
        """Track understanding debt over time"""
        session_data = self.get_session(session_id)
        
        if session_data:
            debt_entry = {
                'score': debt_score,
                'level': level,
                'recorded_at': datetime.now().isoformat()
            }
            
            session_data['understanding_debt_history'].append(debt_entry)
            self._save_session(session_id, session_data)
    
    def get_learning_stats(self, session_id: str) -> Dict[str, Any]:
        """Get learning statistics for a session"""
        session_data = self.get_session(session_id)
        
        if not session_data:
            return {}
        
        concepts_learned = session_data.get('concepts_learned', [])
        debug_sessions = session_data.get('debug_sessions', [])
        quiz_scores = session_data.get('quiz_scores', [])
        
        # Calculate stats
        mastered_concepts = [c for c in concepts_learned if c.get('confidence') == 'mastered']
        understood_concepts = [c for c in concepts_learned if c.get('confidence') == 'understood']
        learning_concepts = [c for c in concepts_learned if c.get('confidence') == 'learning']
        
        avg_quiz_score = 0
        if quiz_scores:
            avg_quiz_score = sum(q['percentage'] for q in quiz_scores) / len(quiz_scores)
        
        successful_debugs = len([d for d in debug_sessions if d.get('success', False)])
        
        return {
            'total_concepts': len(concepts_learned),
            'mastered_concepts': len(mastered_concepts),
            'understood_concepts': len(understood_concepts),
            'learning_concepts': len(learning_concepts),
            'total_debug_sessions': len(debug_sessions),
            'successful_debugs': successful_debugs,
            'total_quizzes': len(quiz_scores),
            'average_quiz_score': round(avg_quiz_score, 1),
            'total_time_spent': session_data.get('total_time_spent', 0),
            'feature_walkthroughs': len(session_data.get('feature_walkthroughs', [])),
            'notes_count': len(session_data.get('notes', []))
        }
    
    def get_all_sessions(self) -> List[Dict[str, Any]]:
        """Get all learning sessions"""
        sessions = []
        
        for session_file in self.memory_dir.glob("*.json"):
            try:
                with open(session_file, 'r', encoding='utf-8') as f:
                    session_data = json.load(f)
                    
                    # Add summary info
                    sessions.append({
                        'session_id': session_data['session_id'],
                        'repo_name': session_data['repo_name'],
                        'skill_level': session_data['skill_level'],
                        'goal': session_data['goal'],
                        'created_at': session_data['created_at'],
                        'updated_at': session_data['updated_at'],
                        'concepts_learned': len(session_data.get('concepts_learned', [])),
                        'debug_sessions': len(session_data.get('debug_sessions', [])),
                        'total_time_spent': session_data.get('total_time_spent', 0)
                    })
            except Exception:
                continue
        
        # Sort by updated_at descending
        sessions.sort(key=lambda x: x['updated_at'], reverse=True)
        return sessions
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a session"""
        session_file = self.memory_dir / f"{session_id}.json"
        
        if session_file.exists():
            try:
                session_file.unlink()
                return True
            except Exception:
                pass
        
        return False
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get overall memory statistics"""
        sessions = self.get_all_sessions()
        
        total_concepts = sum(s['concepts_learned'] for s in sessions)
        total_debugs = sum(s['debug_sessions'] for s in sessions)
        total_time = sum(s['total_time_spent'] for s in sessions)
        
        return {
            'total_sessions': len(sessions),
            'total_concepts_learned': total_concepts,
            'total_debug_sessions': total_debugs,
            'total_time_spent_minutes': total_time,
            'total_time_spent_hours': round(total_time / 60, 1),
            'memory_dir': str(self.memory_dir),
            'privacy_note': 'All learning data is stored locally on your machine'
        }
    
    def _save_session(self, session_id: str, session_data: Dict[str, Any]):
        """Save session data to file"""
        session_file = self.memory_dir / f"{session_id}.json"
        
        try:
            with open(session_file, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Failed to save session {session_id}: {str(e)}")


# Made with Bob