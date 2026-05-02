"""
Report Generator
Generates downloadable Markdown learning pack from session data
"""
from typing import Dict, Any
from datetime import datetime
from local_memory import LocalMemory


class ReportGenerator:
    def __init__(self):
        self.memory = LocalMemory()
    
    def generate_learning_pack(
        self,
        session_id: str,
        analysis_data: Dict[str, Any]
    ) -> str:
        """Generate comprehensive Markdown learning pack"""
        
        session_data = self.memory.get_session(session_id)
        if not session_data:
            return "# Error: Session not found"
        
        stats = self.memory.get_learning_stats(session_id)
        
        # Build the report
        report = self._build_header(session_data)
        report += self._build_summary(session_data, analysis_data, stats)
        report += self._build_stack_section(analysis_data)
        report += self._build_senior_walkthrough(analysis_data)
        report += self._build_reading_order(analysis_data)
        report += self._build_concepts_section(analysis_data)
        report += self._build_official_docs_section(analysis_data)
        report += self._build_debugging_section(session_data, analysis_data)
        report += self._build_learning_progress(session_data, stats)
        report += self._build_quiz_section(session_data, analysis_data)
        report += self._build_next_steps(session_data, analysis_data, stats)
        report += self._build_footer()
        
        return report
    
    def _build_header(self, session_data: Dict[str, Any]) -> str:
        """Build report header"""
        repo_name = session_data.get('repo_name', 'Unknown')
        created_at = session_data.get('created_at', '')
        
        return f"""# DebugSensei Learning Pack
## {repo_name}

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Session Started:** {created_at}  
**Skill Level:** {session_data.get('skill_level', 'intermediate')}  
**Learning Goal:** {session_data.get('goal', 'learn')}

---

"""
    
    def _build_summary(
        self,
        session_data: Dict[str, Any],
        analysis_data: Dict[str, Any],
        stats: Dict[str, Any]
    ) -> str:
        """Build executive summary"""
        return f"""## 📊 Learning Summary

### Your Progress
- **Concepts Learned:** {stats.get('total_concepts', 0)} ({stats.get('mastered_concepts', 0)} mastered, {stats.get('understood_concepts', 0)} understood)
- **Debug Sessions:** {stats.get('total_debug_sessions', 0)} ({stats.get('successful_debugs', 0)} successful)
- **Quizzes Taken:** {stats.get('total_quizzes', 0)} (Average: {stats.get('average_quiz_score', 0)}%)
- **Feature Walkthroughs:** {stats.get('feature_walkthroughs', 0)}
- **Time Spent:** {stats.get('total_time_spent', 0)} minutes

### Understanding Debt
- **Current Score:** {analysis_data.get('understanding_debt', {}).get('score', 'N/A')}/100
- **Risk Level:** {analysis_data.get('understanding_debt', {}).get('level', 'N/A')}

---

"""
    
    def _build_stack_section(self, analysis_data: Dict[str, Any]) -> str:
        """Build detected stack section"""
        stack = analysis_data.get('detected_stack', {})
        
        section = """## 🛠️ Detected Technology Stack

"""
        
        section += f"**Primary Language:** {stack.get('primary_language', 'Unknown')}  \n"
        section += f"**Primary Framework:** {stack.get('primary_framework', 'Unknown')}  \n\n"
        
        if stack.get('languages'):
            section += "### Languages\n"
            for lang, info in stack.get('languages', {}).items():
                section += f"- **{lang}:** {info.get('percentage', 0)}% ({info.get('count', 0)} files)\n"
            section += "\n"
        
        if stack.get('frameworks'):
            section += "### Frameworks & Tools\n"
            for fw in stack.get('frameworks', []):
                section += f"- **{fw.get('name')}** ({fw.get('type')}) - {fw.get('language')}\n"
            section += "\n"
        
        section += "---\n\n"
        return section
    
    def _build_senior_walkthrough(self, analysis_data: Dict[str, Any]) -> str:
        """Build senior walkthrough section"""
        walkthrough = analysis_data.get('senior_walkthrough', {})
        
        return f"""## 🥋 Senior Engineer's Walkthrough

### Project Purpose
{walkthrough.get('project_summary', 'A well-structured application following industry best practices.')}

### Architecture Overview
{walkthrough.get('architecture_flow', 'Standard layered architecture with clear separation of concerns.')}

### How to Approach This Codebase
{walkthrough.get('debugging_checklist', 'Start with the entry points, understand the data flow, then dive into specific features.')}

---

"""
    
    def _build_reading_order(self, analysis_data: Dict[str, Any]) -> str:
        """Build recommended reading order"""
        reading_order = analysis_data.get('reading_order', [])
        
        section = """## 📖 Recommended Reading Order

A senior engineer would explore this codebase in this order:

"""
        
        for i, step in enumerate(reading_order, 1):
            section += f"### {i}. {step.get('step', 'Step')}\n"
            section += f"{step.get('description', '')}\n\n"
            
            if step.get('files'):
                section += "**Files to read:**\n"
                for file in step.get('files', [])[:5]:
                    section += f"- `{file}`\n"
                section += "\n"
        
        section += "---\n\n"
        return section
    
    def _build_concepts_section(self, analysis_data: Dict[str, Any]) -> str:
        """Build concepts detected section"""
        concepts = analysis_data.get('concepts_detected', [])
        
        section = """## 💡 Programming Concepts Detected

These are the key concepts used in your codebase:

"""
        
        for concept in concepts[:10]:
            section += f"### {concept.get('name')}\n"
            section += f"**Category:** {concept.get('category')}  \n"
            section += f"**Used:** {concept.get('count')} times  \n"
            section += f"**Priority:** {'High' if concept.get('weight', 0) >= 10 else 'Medium' if concept.get('weight', 0) >= 6 else 'Low'}  \n\n"
            section += f"{concept.get('description', '')}\n\n"
            
            if concept.get('files'):
                section += "**Found in:**\n"
                for file in concept.get('files', [])[:3]:
                    section += f"- `{file}`\n"
                section += "\n"
        
        section += "---\n\n"
        return section
    
    def _build_official_docs_section(self, analysis_data: Dict[str, Any]) -> str:
        """Build official documentation section"""
        docs = analysis_data.get('official_docs_tutor', [])
        
        section = """## 📚 Official Documentation References

Learn from the official sources:

"""
        
        for doc in docs[:10]:
            section += f"### {doc.get('concept')}\n"
            section += f"**Source:** [{doc.get('official_source_name')}]({doc.get('official_source_url')})  \n\n"
            
            section += "**Key Points:**\n"
            for point in doc.get('key_points', []):
                section += f"- {point}\n"
            section += "\n"
            
            section += f"**Senior's Explanation:**  \n{doc.get('senior_explanation', '')}\n\n"
            
            section += f"**Why It Matters Here:**  \n{doc.get('why_it_matters_in_this_codebase', '')}\n\n"
            
            section += f"**Common Mistake:**  \n{doc.get('common_junior_mistake', '')}\n\n"
            
            section += f"**Debugging Tip:**  \n{doc.get('debugging_tip', '')}\n\n"
            
            section += "---\n\n"
        
        return section
    
    def _build_debugging_section(
        self,
        session_data: Dict[str, Any],
        analysis_data: Dict[str, Any]
    ) -> str:
        """Build debugging lessons section"""
        debug_sessions = session_data.get('debug_sessions', [])
        
        section = """## 🐛 Debugging Lessons Learned

"""
        
        if debug_sessions:
            section += "### Your Debug Sessions\n\n"
            for i, debug in enumerate(debug_sessions, 1):
                section += f"#### Session {i}: {debug.get('error_type')}\n"
                section += f"**Resolution:** {debug.get('resolution')}  \n"
                section += f"**Time Spent:** {debug.get('time_spent_minutes', 0)} minutes  \n"
                section += f"**Date:** {debug.get('debugged_at', '')}  \n\n"
        
        checklist = analysis_data.get('debugging_checklist', [])
        if checklist:
            section += "### General Debugging Checklist\n\n"
            for item in checklist:
                section += f"- {item}\n"
            section += "\n"
        
        section += "---\n\n"
        return section
    
    def _build_learning_progress(
        self,
        session_data: Dict[str, Any],
        stats: Dict[str, Any]
    ) -> str:
        """Build learning progress section"""
        concepts = session_data.get('concepts_learned', [])
        
        section = """## 🎓 Your Learning Progress

"""
        
        if concepts:
            section += "### Concepts Mastered\n"
            mastered = [c for c in concepts if c.get('confidence') == 'mastered']
            for concept in mastered:
                section += f"- ✅ **{concept.get('concept')}** (Reviewed {concept.get('review_count', 0)} times)\n"
            section += "\n"
            
            section += "### Concepts Understood\n"
            understood = [c for c in concepts if c.get('confidence') == 'understood']
            for concept in understood:
                section += f"- 📖 **{concept.get('concept')}** (Reviewed {concept.get('review_count', 0)} times)\n"
            section += "\n"
            
            section += "### Currently Learning\n"
            learning = [c for c in concepts if c.get('confidence') == 'learning']
            for concept in learning:
                section += f"- 📝 **{concept.get('concept')}**\n"
            section += "\n"
        
        section += "---\n\n"
        return section
    
    def _build_quiz_section(
        self,
        session_data: Dict[str, Any],
        analysis_data: Dict[str, Any]
    ) -> str:
        """Build quiz section"""
        quiz_scores = session_data.get('quiz_scores', [])
        quiz_questions = analysis_data.get('quiz_questions', [])
        
        section = """## ❓ Quiz Questions & Answers

"""
        
        if quiz_scores:
            section += "### Your Quiz Performance\n\n"
            for quiz in quiz_scores:
                section += f"**{quiz.get('concept')}:** {quiz.get('score')}/{quiz.get('total')} ({quiz.get('percentage')}%)  \n"
            section += "\n"
        
        if quiz_questions:
            section += "### Practice Questions\n\n"
            for i, q in enumerate(quiz_questions, 1):
                section += f"#### Question {i}\n"
                section += f"**Q:** {q.get('question')}  \n"
                section += f"**A:** {q.get('answer')}  \n\n"
        
        section += "---\n\n"
        return section
    
    def _build_next_steps(
        self,
        session_data: Dict[str, Any],
        analysis_data: Dict[str, Any],
        stats: Dict[str, Any]
    ) -> str:
        """Build next steps section"""
        learning_path = analysis_data.get('learning_path', [])
        
        section = """## 🚀 Next Steps

### Recommended Learning Path

"""
        
        for i, step in enumerate(learning_path[:5], 1):
            section += f"{i}. **{step.get('name')}** ({step.get('priority')} Priority)  \n"
            section += f"   {step.get('description')}  \n\n"
        
        section += """### Safe First Contribution Tasks

Here are some safe tasks you can tackle now:

1. **Add comments** to complex functions you now understand
2. **Write unit tests** for simple utility functions
3. **Improve error messages** to be more descriptive
4. **Add input validation** where it's missing
5. **Refactor small functions** to be more readable

### Keep Learning

- Review the official documentation links regularly
- Practice with the quiz questions
- Debug real errors as they come up
- Build small features to apply what you learned

---

"""
        return section
    
    def _build_footer(self) -> str:
        """Build report footer"""
        return """## 🥋 Remember

**You learned from YOUR codebase, not generic tutorials.**

**You have official documentation references, not just opinions.**

**You debugged like a senior, not just copied fixes.**

**Keep this learning pack. Review it. Build on it.**

---

*Generated by DebugSensei - Your Senior Engineer Mentor*  
*All learning data stored locally on your machine*

**Made with 🥋 by developers, for developers**
"""


# Made with Bob