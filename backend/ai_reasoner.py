"""
AI Reasoner - Interface for AI-powered reasoning
Uses fallback template-based responses for MVP
Includes placeholders for IBM watsonx integration
"""
from typing import Dict, List, Any


class AIReasoner:
    def __init__(self, use_ai: bool = False, api_key: str | None = None):
        self.use_ai = use_ai
        self.api_key = api_key
        
        # TODO: Initialize IBM watsonx client when API key is provided
        # if self.use_ai and self.api_key:
        #     from ibm_watson_machine_learning.foundation_models import Model
        #     self.model = Model(
        #         model_id="ibm/granite-13b-chat-v2",
        #         credentials={
        #             "apikey": self.api_key,
        #             "url": "https://us-south.ml.cloud.ibm.com"
        #         },
        #         project_id="YOUR_PROJECT_ID"
        #     )
    
    def generate_learning_summary(
        self,
        repo_summary: Dict[str, Any],
        skill_level: str,
        goal: str
    ) -> Dict[str, Any]:
        """Generate learning-focused summary of the codebase"""
        
        if self.use_ai and self.api_key:
            # TODO: Call IBM watsonx API
            # prompt = self._build_summary_prompt(repo_summary, skill_level, goal)
            # response = self.model.generate_text(prompt=prompt, params={...})
            # return self._parse_ai_response(response)
            pass
        
        # Fallback: Template-based response
        return self._generate_fallback_summary(repo_summary, skill_level, goal)
    
    def debug_with_context(
        self,
        repo_summary: Dict[str, Any],
        error_log: str,
        skill_level: str
    ) -> Dict[str, Any]:
        """Provide debugging guidance with codebase context"""
        
        if self.use_ai and self.api_key:
            # TODO: Call IBM watsonx API
            # prompt = self._build_debug_prompt(repo_summary, error_log, skill_level)
            # response = self.model.generate_text(prompt=prompt, params={...})
            # return self._parse_ai_response(response)
            pass
        
        # Fallback: Use debug_coach.py template-based logic
        from debug_coach import DebugCoach
        coach = DebugCoach()
        return coach.analyze_error(error_log, skill_level, repo_summary.get('detected_stack', {}))
    
    def generate_quiz_questions(
        self,
        concepts: List[Dict[str, Any]],
        skill_level: str
    ) -> List[Dict[str, str]]:
        """Generate quiz questions for detected concepts"""
        
        if self.use_ai and self.api_key:
            # TODO: Call IBM watsonx API for quiz generation
            pass
        
        # Fallback: Template-based quiz
        return self._generate_fallback_quiz(concepts, skill_level)
    
    def _generate_fallback_summary(
        self,
        repo_summary: Dict[str, Any],
        skill_level: str,
        goal: str
    ) -> Dict[str, Any]:
        """Generate template-based summary"""
        
        stack = repo_summary.get('detected_stack', {})
        primary_language = stack.get('primary_language', 'Unknown')
        primary_framework = stack.get('primary_framework', 'Unknown')
        concepts = repo_summary.get('concepts_detected', [])
        
        # Generate project summary based on stack
        if primary_framework == 'Spring Boot':
            project_summary = (
                f"This is a {primary_language} {primary_framework} backend application. "
                "The code follows a layered architecture where controllers receive HTTP requests, "
                "services handle business logic, repositories communicate with the database, "
                "and entities represent stored data. This separation of concerns makes the code "
                "maintainable and testable."
            )
            architecture_flow = [
                "Client Request",
                "REST Controller",
                "Service Layer",
                "Repository",
                "Database",
                "Response"
            ]
        elif primary_framework == 'FastAPI':
            project_summary = (
                f"This is a {primary_language} {primary_framework} backend API. "
                "FastAPI is a modern, fast web framework that uses Python type hints for "
                "automatic validation and documentation. The code uses async/await for "
                "better performance and Pydantic models for data validation."
            )
            architecture_flow = [
                "Client Request",
                "API Route",
                "Business Logic",
                "Database/External API",
                "Response"
            ]
        elif primary_framework == 'React':
            project_summary = (
                f"This is a {primary_language} {primary_framework} frontend application. "
                "React uses components to build user interfaces. Components manage their own "
                "state and can be composed to create complex UIs. The app uses hooks like "
                "useState and useEffect to manage state and side effects."
            )
            architecture_flow = [
                "User Interaction",
                "Component",
                "State Update",
                "Re-render",
                "Updated UI"
            ]
        elif primary_framework == 'Flutter':
            project_summary = (
                f"This is a {primary_language} {primary_framework} mobile application. "
                "Flutter uses widgets to build cross-platform mobile apps. Widgets are "
                "immutable descriptions of the UI. The app uses StatefulWidgets for "
                "interactive components and Firebase for backend services."
            )
            architecture_flow = [
                "User Interaction",
                "Widget",
                "State Change",
                "Rebuild",
                "Updated UI"
            ]
        else:
            project_summary = (
                f"This is a {primary_language} application using {primary_framework}. "
                "The codebase is organized into modules and follows standard patterns "
                "for the technology stack."
            )
            architecture_flow = [
                "Input",
                "Processing",
                "Output"
            ]
        
        # Generate learning path based on concepts
        learning_path = self._generate_learning_path(concepts, skill_level, primary_language)
        
        # Generate debugging checklist
        debugging_checklist = [
            "Read the error message and stack trace carefully",
            "Identify the file and line number where the error occurred",
            "Check the values of variables at that point",
            "Trace back to where those values came from",
            "Add logging or debugging statements",
            "Test with different inputs",
            "Fix the issue and add a test to prevent regression"
        ]
        
        return {
            'project_summary': project_summary,
            'architecture_flow': architecture_flow,
            'learning_path': learning_path,
            'debugging_checklist': debugging_checklist
        }
    
    def _generate_learning_path(
        self,
        concepts: List[Dict[str, Any]],
        skill_level: str,
        language: str
    ) -> List[Dict[str, str]]:
        """Generate ordered learning path"""
        
        # Base learning path by language
        base_paths = {
            'Java': [
                {'step': 1, 'topic': 'Java Basics', 'description': 'Classes, objects, methods'},
                {'step': 2, 'topic': 'OOP Principles', 'description': 'Inheritance, polymorphism, encapsulation'},
                {'step': 3, 'topic': 'Collections', 'description': 'Lists, maps, sets'},
                {'step': 4, 'topic': 'Exception Handling', 'description': 'Try-catch, custom exceptions'},
                {'step': 5, 'topic': 'Spring Boot Basics', 'description': 'Controllers, services, repositories'},
                {'step': 6, 'topic': 'Dependency Injection', 'description': 'IoC container, @Autowired'},
                {'step': 7, 'topic': 'REST APIs', 'description': 'HTTP methods, endpoints, JSON'},
                {'step': 8, 'topic': 'Database Access', 'description': 'JPA, repositories, entities'},
                {'step': 9, 'topic': 'Testing', 'description': 'Unit tests, integration tests'}
            ],
            'Python': [
                {'step': 1, 'topic': 'Python Basics', 'description': 'Functions, data types, control flow'},
                {'step': 2, 'topic': 'Type Hints', 'description': 'Adding types to Python code'},
                {'step': 3, 'topic': 'Exception Handling', 'description': 'Try-except, raising exceptions'},
                {'step': 4, 'topic': 'Async Programming', 'description': 'Async/await, coroutines'},
                {'step': 5, 'topic': 'FastAPI Basics', 'description': 'Routes, request/response models'},
                {'step': 6, 'topic': 'Data Validation', 'description': 'Pydantic models'},
                {'step': 7, 'topic': 'Database Integration', 'description': 'SQLAlchemy, async databases'},
                {'step': 8, 'topic': 'Testing', 'description': 'Pytest, test fixtures'}
            ],
            'JavaScript': [
                {'step': 1, 'topic': 'JavaScript Basics', 'description': 'Variables, functions, objects'},
                {'step': 2, 'topic': 'React Fundamentals', 'description': 'Components, JSX, props'},
                {'step': 3, 'topic': 'State Management', 'description': 'useState, state updates'},
                {'step': 4, 'topic': 'Side Effects', 'description': 'useEffect, lifecycle'},
                {'step': 5, 'topic': 'API Integration', 'description': 'Fetch, axios, async/await'},
                {'step': 6, 'topic': 'Event Handling', 'description': 'User interactions, forms'},
                {'step': 7, 'topic': 'Advanced Hooks', 'description': 'useContext, useReducer, custom hooks'},
                {'step': 8, 'topic': 'Testing', 'description': 'Jest, React Testing Library'}
            ],
            'Dart': [
                {'step': 1, 'topic': 'Dart Basics', 'description': 'Variables, functions, classes'},
                {'step': 2, 'topic': 'Flutter Widgets', 'description': 'Stateless and stateful widgets'},
                {'step': 3, 'topic': 'State Management', 'description': 'setState, state patterns'},
                {'step': 4, 'topic': 'Async Programming', 'description': 'Future, async/await, streams'},
                {'step': 5, 'topic': 'Firebase Integration', 'description': 'Auth, Firestore, storage'},
                {'step': 6, 'topic': 'Navigation', 'description': 'Routes, navigation patterns'},
                {'step': 7, 'topic': 'UI Design', 'description': 'Material Design, layouts'},
                {'step': 8, 'topic': 'Testing', 'description': 'Widget tests, integration tests'}
            ]
        }
        
        path = base_paths.get(language, base_paths['JavaScript'])
        
        # Adjust based on skill level
        if skill_level == 'advanced':
            path = path[4:]  # Skip basics
        elif skill_level == 'intermediate':
            path = path[2:]  # Skip very basics
        
        return path[:6]  # Return top 6 steps
    
    def _generate_fallback_quiz(
        self,
        concepts: List[Dict[str, Any]],
        skill_level: str
    ) -> List[Dict[str, str]]:
        """Generate template-based quiz questions"""
        
        quiz_questions = []
        
        for concept in concepts[:5]:  # Top 5 concepts
            concept_name = concept['name']
            
            if concept_name == 'REST Controller':
                quiz_questions.append({
                    'question': 'Why should controllers not contain business logic?',
                    'answer': 'Controllers should only handle HTTP requests and responses. Business logic belongs in the service layer for better separation of concerns and testability.'
                })
            elif concept_name == 'Dependency Injection':
                quiz_questions.append({
                    'question': 'What problem does dependency injection solve?',
                    'answer': 'It removes hard-coded dependencies, making code more modular, testable, and maintainable. The framework manages object creation and wiring.'
                })
            elif concept_name == 'State Management':
                quiz_questions.append({
                    'question': 'When should you use state in a component?',
                    'answer': 'Use state for data that changes over time and affects what the component renders. State triggers re-renders when updated.'
                })
            elif concept_name == 'Async Function':
                quiz_questions.append({
                    'question': 'Why use async/await instead of callbacks?',
                    'answer': 'Async/await makes asynchronous code look synchronous, improving readability and making error handling easier with try-catch.'
                })
            elif concept_name == 'Exception Handling':
                quiz_questions.append({
                    'question': 'What is the purpose of exception handling?',
                    'answer': 'To gracefully handle errors, prevent crashes, provide meaningful error messages, and maintain application stability.'
                })
        
        # Add generic questions if not enough concept-specific ones
        if len(quiz_questions) < 3:
            quiz_questions.extend([
                {
                    'question': 'What is the first step when debugging an error?',
                    'answer': 'Read the error message carefully and identify the file and line number where the error occurred.'
                },
                {
                    'question': 'Why is code organization important?',
                    'answer': 'Good organization makes code easier to understand, maintain, test, and scale. It follows the principle of separation of concerns.'
                }
            ])
        
        return quiz_questions[:5]
    
    def _build_summary_prompt(self, repo_summary: Dict, skill_level: str, goal: str) -> str:
        """Build prompt for AI summary generation"""
        # TODO: Implement when integrating with IBM watsonx
        return ""
    
    def _build_debug_prompt(self, repo_summary: Dict, error_log: str, skill_level: str) -> str:
        """Build prompt for AI debugging assistance"""
        # TODO: Implement when integrating with IBM watsonx
        return ""

# Made with Bob
