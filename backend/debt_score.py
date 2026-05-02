"""
Understanding Debt Score Calculator
Calculates how much a developer needs to learn to understand the codebase
"""
from typing import Dict, List, Any


class DebtScoreCalculator:
    def __init__(self):
        # Concept weights (higher = more important to understand)
        self.concept_weights = {
            'JWT/Auth': 15,
            'Firebase Auth': 15,
            'Database Transaction': 12,
            'Firestore': 12,
            'Async Function': 10,
            'Async UI': 10,
            'Dependency Injection': 10,
            'Side Effects': 10,
            'ORM Entity': 8,
            'Repository Pattern': 8,
            'State Management': 8,
            'Exception Handling': 8,
            'Data Validation': 8,
            'REST Controller': 8,
            'Service Layer': 8,
            'API Call': 6,
            'REST Endpoint': 6,
            'API Route': 6,
            'Type Hints': 6,
            'Optional/Null Safety': 6,
            'Testing': 5,
            'React Component': 4,
            'Props': 4,
            'Basic OOP': 4,
            'Functions': 4
        }
        
        # Skill level adjustments
        self.skill_adjustments = {
            'beginner': 0,      # No reduction
            'intermediate': -20, # Reduce by 20
            'advanced': -40     # Reduce by 40
        }
    
    def calculate(
        self,
        detected_concepts: List[Dict[str, Any]],
        skill_level: str,
        total_files: int
    ) -> Dict[str, Any]:
        """Calculate understanding debt score"""
        
        # Calculate base score from concepts
        base_score = 0
        high_risk_concepts = []
        concept_breakdown = []
        
        for concept in detected_concepts:
            concept_name = concept['name']
            concept_count = concept.get('count', 0)
            concept_weight = concept.get('weight', 5)
            
            # Get weight from our mapping or use concept's weight
            weight = self.concept_weights.get(concept_name, concept_weight) or 5
            
            # Calculate contribution (capped at weight value)
            contribution = min(weight, concept_count * 0.5)
            base_score += contribution
            
            concept_breakdown.append({
                'name': concept_name,
                'weight': weight,
                'count': concept_count,
                'contribution': round(contribution, 1)
            })
            
            # Track high-risk concepts (weight >= 10)
            if weight >= 10:
                high_risk_concepts.append({
                    'name': concept_name,
                    'weight': weight,
                    'description': concept.get('description', ''),
                    'files': concept.get('files', [])[:3]  # Top 3 files
                })
        
        # Apply skill level adjustment
        adjustment = self.skill_adjustments.get(skill_level, 0)
        adjusted_score = base_score + adjustment
        
        # Cap between 0 and 100
        final_score = max(0, min(100, adjusted_score))
        
        # Determine risk level
        if final_score <= 30:
            risk_level = 'Low'
            risk_color = 'green'
            message = 'You have a good understanding of this codebase!'
        elif final_score <= 60:
            risk_level = 'Medium'
            risk_color = 'yellow'
            message = 'Some concepts need attention. Review the learning path.'
        else:
            risk_level = 'High'
            risk_color = 'red'
            message = 'Significant learning needed. Start with high-priority concepts.'
        
        return {
            'score': round(final_score, 1),
            'base_score': round(base_score, 1),
            'skill_adjustment': adjustment,
            'risk_level': risk_level,
            'risk_color': risk_color,
            'message': message,
            'high_risk_concepts': sorted(high_risk_concepts, key=lambda x: x['weight'], reverse=True),
            'concept_breakdown': sorted(concept_breakdown, key=lambda x: x['contribution'], reverse=True)[:10],
            'total_concepts': len(detected_concepts),
            'recommendation': self._get_recommendation(final_score, skill_level)
        }
    
    def _get_recommendation(self, score: float, skill_level: str) -> str:
        """Get personalized recommendation based on score"""
        if score <= 30:
            return "Great! Focus on code quality and best practices."
        elif score <= 60:
            if skill_level == 'beginner':
                return "Take your time learning each concept. Use the docs and quiz features."
            else:
                return "Review the high-priority concepts and practice with examples."
        else:
            if skill_level == 'beginner':
                return "Start with basics. Don't rush. Learn one concept at a time."
            elif skill_level == 'intermediate':
                return "Focus on high-weight concepts first. Build small projects to practice."
            else:
                return "Deep dive into architecture patterns. Consider pair programming or mentorship."
    
    def get_learning_priority(self, detected_concepts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Get prioritized list of concepts to learn"""
        priority_list = []
        
        for concept in detected_concepts:
            concept_name = concept['name']
            weight = self.concept_weights.get(concept_name, concept.get('weight', 5)) or 5
            
            priority_list.append({
                'name': concept_name,
                'weight': weight,
                'priority': 'High' if weight >= 10 else 'Medium' if weight >= 6 else 'Low',
                'description': concept.get('description', ''),
                'category': concept.get('category', 'General')
            })
        
        return sorted(priority_list, key=lambda x: x['weight'], reverse=True)

# Made with Bob
