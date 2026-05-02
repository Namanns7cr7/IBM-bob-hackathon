"""
Documentation Matcher
Maps detected concepts to official documentation and creates senior-style explanations
"""
from typing import Dict, List, Any
from official_docs_registry import OfficialDocsRegistry
from official_docs_fetcher import OfficialDocsFetcher


class DocsMatcher:
    def __init__(self):
        self.registry = OfficialDocsRegistry()
        self.fetcher = OfficialDocsFetcher()
    
    def match_concepts_to_docs(
        self,
        detected_concepts: List[Dict[str, Any]],
        skill_level: str = "intermediate"
    ) -> List[Dict[str, Any]]:
        """
        Match detected concepts to official documentation
        Returns enriched concept data with official docs and senior explanations
        """
        matched_docs = []
        
        for concept in detected_concepts[:15]:  # Limit to top 15 concepts
            concept_name = concept['name']
            
            # Get doc entry from registry
            doc_entry = self.registry.get_doc_entry(concept_name)
            
            if doc_entry:
                # Fetch official docs (cached or from web)
                official_docs = self.fetcher.fetch_docs(doc_entry)
                
                # Create enriched concept with official docs
                matched_doc = {
                    'concept': concept_name,
                    'where_used': concept.get('files', [])[:5],  # Top 5 files
                    'usage_count': concept.get('count', 0),
                    'category': concept.get('category', 'General'),
                    'weight': concept.get('weight', 5),
                    'official_source_name': official_docs['source_name'],
                    'official_source_url': official_docs['source_url'],
                    'official_docs_summary': official_docs['content'][:500] + '...' if len(official_docs['content']) > 500 else official_docs['content'],
                    'key_points': official_docs['key_points'],
                    'senior_explanation': self._generate_senior_explanation(
                        concept_name,
                        concept,
                        skill_level
                    ),
                    'why_it_matters_in_this_codebase': self._explain_why_it_matters(
                        concept_name,
                        concept
                    ),
                    'common_junior_mistake': self._get_common_mistake(concept_name),
                    'debugging_tip': self._get_debugging_tip(concept_name),
                    'production_concern': self._get_production_concern(concept_name),
                    'mini_quiz': self._generate_mini_quiz(concept_name, skill_level),
                    'cached': official_docs.get('cached', False),
                    'fallback': official_docs.get('fallback', False)
                }
                
                matched_docs.append(matched_doc)
        
        return matched_docs
    
    def _generate_senior_explanation(
        self,
        concept_name: str,
        concept: Dict[str, Any],
        skill_level: str
    ) -> str:
        """Generate senior engineer style explanation"""
        
        explanations = {
            "REST Controller": {
                "beginner": "Think of @RestController as the front door of your API. When someone makes an HTTP request (like clicking a button in the app), this controller receives it, processes it, and sends back a response. It's like a receptionist who handles all incoming requests.",
                "intermediate": "The @RestController is your HTTP request handler. It combines @Controller and @ResponseBody, meaning it automatically serializes your return values to JSON. Keep controllers thin - they should just validate input, call services, and return responses. Business logic belongs in the service layer.",
                "advanced": "REST Controllers are the entry point for your API layer. They handle HTTP concerns (status codes, headers, content negotiation) while delegating business logic to services. Use DTOs for request/response to decouple your API contract from domain models. Consider using @ControllerAdvice for global exception handling."
            },
            "Dependency Injection": {
                "beginner": "Instead of creating objects yourself with 'new', Spring creates them for you and 'injects' them where needed. It's like having a helper who automatically gives you the tools you need. This makes your code easier to test and change.",
                "intermediate": "DI inverts control - Spring manages object lifecycle and wiring. Use constructor injection (preferred) over field injection for better testability. The @Autowired annotation tells Spring to inject dependencies. This promotes loose coupling and makes unit testing easier with mocks.",
                "advanced": "DI is the core of Spring's IoC container. Constructor injection ensures immutability and makes dependencies explicit. Avoid circular dependencies. Use @Qualifier for multiple beans of same type. Consider using @Lazy for expensive beans. Profile-specific beans help manage different environments."
            },
            "State Management": {
                "beginner": "State is like the memory of your component. When you click a button and something changes on screen, that's state updating. Use useState to add state to your component. When state changes, React automatically updates what you see.",
                "intermediate": "State is component-local data that triggers re-renders when updated. Always use the setter function, never mutate state directly. For complex state, consider useReducer. Lift state up to share between components. Use Context API for deeply nested prop drilling.",
                "advanced": "State management is about data flow and re-render optimization. Consider state colocation - keep state as close to where it's used as possible. Use composition over prop drilling. For global state, evaluate if you need Redux/Zustand or if Context + useReducer suffices. Memoize expensive computations with useMemo."
            },
            "Async Function": {
                "beginner": "Async functions let your code wait for things without freezing. Like waiting for a pizza delivery - you can do other things while waiting. Use 'await' to wait for the result, and the code looks normal even though it's waiting.",
                "intermediate": "Async/await is syntactic sugar over Promises. It makes asynchronous code look synchronous, improving readability. Always use try-catch for error handling. Remember that await only works inside async functions. Use Promise.all() for parallel operations.",
                "advanced": "Async/await simplifies promise chains but doesn't change the underlying async nature. Be mindful of sequential vs parallel execution - unnecessary awaits can hurt performance. Use Promise.allSettled() when you need all results regardless of failures. Consider async generators for streaming data."
            },
            "Database Transaction": {
                "beginner": "A transaction is like a safety net for database changes. If anything goes wrong, all changes are undone (rolled back). It's all-or-nothing - either everything succeeds or nothing changes. This keeps your data consistent.",
                "intermediate": "@Transactional ensures ACID properties. Spring automatically rolls back on runtime exceptions. Be careful with transaction boundaries - keep them as short as possible. Avoid calling external services inside transactions. Use @Transactional(readOnly=true) for read operations.",
                "advanced": "Transaction management is critical for data integrity. Understand isolation levels and their trade-offs. Be aware of transaction propagation (REQUIRED, REQUIRES_NEW, etc.). Long transactions can cause deadlocks and performance issues. Consider optimistic locking for concurrent updates. Monitor transaction duration in production."
            }
        }
        
        # Get explanation for skill level, fallback to intermediate
        concept_explanations = explanations.get(concept_name, {})
        explanation = concept_explanations.get(
            skill_level,
            concept_explanations.get("intermediate", 
                f"This concept appears {concept.get('count', 0)} times in your codebase. It's an important pattern to understand for working with this project."
            )
        )
        
        return explanation
    
    def _explain_why_it_matters(self, concept_name: str, concept: Dict[str, Any]) -> str:
        """Explain why this concept matters in this specific codebase"""
        count = concept.get('count', 0)
        files = concept.get('files', [])
        
        if count > 10:
            return f"This is a core pattern in your codebase - used {count} times across {len(files)} files. Understanding this is essential for working on this project."
        elif count > 5:
            return f"This pattern appears {count} times in your code. It's important for understanding how the application works."
        else:
            return f"While used less frequently ({count} times), this concept is still important for specific features in your codebase."
    
    def _get_common_mistake(self, concept_name: str) -> str:
        """Get common junior developer mistakes for this concept"""
        mistakes = {
            "REST Controller": "Juniors often put business logic directly in controllers. Keep controllers thin - they should only handle HTTP concerns and delegate to services.",
            "Dependency Injection": "Common mistake: using field injection (@Autowired on fields) instead of constructor injection. Constructor injection is preferred because it makes dependencies explicit and enables immutability.",
            "State Management": "Juniors often mutate state directly (state.value = x) instead of using the setter. This breaks React's reactivity. Always use setState or the setter from useState.",
            "Async Function": "Forgetting to use 'await' or not handling errors with try-catch. Also, unnecessarily awaiting operations that could run in parallel.",
            "Database Transaction": "Making transactions too large or calling external APIs inside transactions. Keep transactions short and focused on database operations only.",
            "Repository Pattern": "Writing complex queries in controllers instead of in repositories. Repositories should encapsulate all data access logic.",
            "React useEffect": "Not providing a dependency array, causing infinite re-render loops. Or forgetting to return cleanup functions for subscriptions.",
            "Pydantic Model": "Not understanding that Pydantic validates and coerces types automatically. Juniors sometimes add manual validation that's already handled.",
            "Firebase Auth": "Not handling auth state changes properly or storing sensitive data in client-side state. Always use auth state listeners.",
            "ORM Entity": "Forgetting to use @Transactional when modifying entities, or creating N+1 query problems with lazy loading."
        }
        
        return mistakes.get(concept_name, "Take time to understand this concept thoroughly before using it in production code.")
    
    def _get_debugging_tip(self, concept_name: str) -> str:
        """Get debugging tip for this concept"""
        tips = {
            "REST Controller": "When debugging API issues, check: 1) Request mapping path, 2) HTTP method, 3) Request body format, 4) Response status code. Use @RestControllerAdvice for global exception handling.",
            "Dependency Injection": "If you get 'No qualifying bean' errors, check: 1) Is the class annotated with @Component/@Service/@Repository? 2) Is it in a package scanned by Spring? 3) Are there multiple beans of the same type?",
            "State Management": "Add console.log before setState to see what's triggering updates. Use React DevTools to inspect state changes. Check if you're mutating state directly.",
            "Async Function": "Add try-catch blocks and log errors. Use browser DevTools Network tab to see actual API calls. Check if you're awaiting promises properly.",
            "Database Transaction": "If you see 'Transaction rolled back' errors, check: 1) What exception was thrown? 2) Is @Transactional on the right method? 3) Are you calling the method from outside the class?",
            "Repository Pattern": "Enable SQL logging (spring.jpa.show-sql=true) to see actual queries. Check for N+1 problems. Verify your query methods are named correctly.",
            "React useEffect": "If effect runs too often, check dependency array. If it doesn't run, check if dependencies are changing. Use console.log to trace execution.",
            "Pydantic Model": "Validation errors show exactly which field failed. Read the error message carefully - it tells you what type was expected vs received.",
            "Firebase Auth": "Check browser console for auth errors. Verify Firebase config is correct. Use auth state listeners, don't rely on synchronous checks.",
            "ORM Entity": "Enable SQL logging to see what queries are generated. Check for lazy loading issues. Verify relationships are mapped correctly."
        }
        
        return tips.get(concept_name, "Add logging at key points to trace execution flow. Check official documentation for common pitfalls.")
    
    def _get_production_concern(self, concept_name: str) -> str:
        """Get production-level concerns for this concept"""
        concerns = {
            "REST Controller": "Production: Add rate limiting, input validation, proper error responses, API versioning, and monitoring. Never expose stack traces to clients.",
            "Dependency Injection": "Production: Be careful with singleton beans holding state. Ensure thread safety. Monitor bean creation time for performance.",
            "State Management": "Production: Avoid storing sensitive data in state. Consider state persistence for better UX. Monitor state size for performance.",
            "Async Function": "Production: Add timeout handling, retry logic for failed requests, proper error boundaries, and loading states for better UX.",
            "Database Transaction": "Production: Monitor transaction duration. Long transactions can cause deadlocks. Use connection pooling. Consider read replicas for scaling.",
            "Repository Pattern": "Production: Add query performance monitoring. Use pagination for large datasets. Consider caching for frequently accessed data.",
            "React useEffect": "Production: Clean up subscriptions to prevent memory leaks. Handle component unmounting gracefully. Consider debouncing expensive operations.",
            "Pydantic Model": "Production: Add custom validators for business rules. Consider using Field() for better validation messages. Monitor validation performance.",
            "Firebase Auth": "Production: Implement proper session management. Add security rules. Monitor auth failures. Consider rate limiting for auth endpoints.",
            "ORM Entity": "Production: Use database indexes for frequently queried fields. Monitor query performance. Consider using DTOs to avoid exposing entities directly."
        }
        
        return concerns.get(concept_name, "Production: Add proper error handling, logging, monitoring, and testing. Consider performance and security implications.")
    
    def _generate_mini_quiz(self, concept_name: str, skill_level: str) -> Dict[str, str]:
        """Generate a mini quiz question for this concept"""
        quizzes = {
            "REST Controller": {
                "question": "Why should you keep business logic out of REST controllers?",
                "answer": "Controllers should only handle HTTP concerns (request/response). Business logic belongs in the service layer for better separation of concerns, testability, and reusability."
            },
            "Dependency Injection": {
                "question": "Why is constructor injection preferred over field injection?",
                "answer": "Constructor injection makes dependencies explicit, enables immutability (final fields), and makes testing easier since you can create objects without Spring container."
            },
            "State Management": {
                "question": "Why can't you mutate state directly in React?",
                "answer": "React uses reference equality to detect changes. If you mutate state directly, the reference doesn't change, so React won't re-render. Always use the setter function."
            },
            "Async Function": {
                "question": "What's the difference between Promise.all() and awaiting promises sequentially?",
                "answer": "Promise.all() runs promises in parallel (faster), while sequential awaits run one after another. Use Promise.all() when operations are independent."
            },
            "Database Transaction": {
                "question": "When does Spring automatically rollback a transaction?",
                "answer": "Spring automatically rolls back transactions on unchecked exceptions (RuntimeException and its subclasses). Checked exceptions don't trigger rollback by default."
            }
        }
        
        return quizzes.get(concept_name, {
            "question": f"What is the main purpose of {concept_name} in this codebase?",
            "answer": "Review the official documentation and code examples to understand its role and best practices."
        })


# Made with Bob