"""
Official Documentation Registry
Maps programming concepts to their official documentation sources
"""
from typing import Dict, List, Any, Optional


class OfficialDocsRegistry:
    def __init__(self):
        self.registry = self._build_registry()
    
    def _build_registry(self) -> Dict[str, Dict[str, Any]]:
        """Build comprehensive registry of official documentation sources"""
        return {
            # Java Core Concepts
            "Java Classes and Objects": {
                "concept": "Java Classes and Objects",
                "language": "Java",
                "framework": None,
                "source_name": "Oracle Java Documentation",
                "source_url": "https://docs.oracle.com/javase/tutorial/java/concepts/",
                "fallback_summary": "Classes are blueprints for objects. Objects are instances of classes with state (fields) and behavior (methods).",
                "key_points": [
                    "A class is a template that defines the form of an object",
                    "Objects are instances of classes",
                    "Fields store the state of an object",
                    "Methods define the behavior of an object"
                ]
            },
            "Java Exception Handling": {
                "concept": "Java Exception Handling",
                "language": "Java",
                "framework": None,
                "source_name": "Oracle Java Documentation",
                "source_url": "https://docs.oracle.com/javase/tutorial/essential/exceptions/",
                "fallback_summary": "Exceptions are events that disrupt normal program flow. Use try-catch blocks to handle exceptions gracefully.",
                "key_points": [
                    "try block contains code that might throw an exception",
                    "catch block handles the exception",
                    "finally block always executes",
                    "Checked exceptions must be caught or declared"
                ]
            },
            "Java Optional": {
                "concept": "Java Optional",
                "language": "Java",
                "framework": None,
                "source_name": "Oracle Java Documentation",
                "source_url": "https://docs.oracle.com/javase/8/docs/api/java/util/Optional.html",
                "fallback_summary": "Optional is a container that may or may not contain a non-null value. It helps avoid NullPointerException.",
                "key_points": [
                    "Use Optional.of() for non-null values",
                    "Use Optional.ofNullable() when value might be null",
                    "Use isPresent() to check if value exists",
                    "Use orElse() to provide default value"
                ]
            },
            "Java Collections": {
                "concept": "Java Collections",
                "language": "Java",
                "framework": None,
                "source_name": "Oracle Java Documentation",
                "source_url": "https://docs.oracle.com/javase/tutorial/collections/",
                "fallback_summary": "Collections Framework provides data structures like List, Set, Map to store and manipulate groups of objects.",
                "key_points": [
                    "List maintains insertion order (ArrayList, LinkedList)",
                    "Set contains unique elements (HashSet, TreeSet)",
                    "Map stores key-value pairs (HashMap, TreeMap)",
                    "Use generics for type safety"
                ]
            },
            
            # Spring Boot Concepts
            "REST Controller": {
                "concept": "REST Controller",
                "language": "Java",
                "framework": "Spring Boot",
                "source_name": "Spring Framework Documentation",
                "source_url": "https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-controller.html",
                "fallback_summary": "@RestController combines @Controller and @ResponseBody. It handles HTTP requests and returns data directly (usually JSON).",
                "key_points": [
                    "@RestController marks a class as a REST API controller",
                    "Methods return data directly, not view names",
                    "Automatically serializes return values to JSON",
                    "Use @GetMapping, @PostMapping, etc. for HTTP methods"
                ]
            },
            "Service Layer": {
                "concept": "Service Layer",
                "language": "Java",
                "framework": "Spring Boot",
                "source_name": "Spring Framework Documentation",
                "source_url": "https://docs.spring.io/spring-framework/reference/core/beans/classpath-scanning.html",
                "fallback_summary": "@Service marks a class as a service layer component. It contains business logic, separated from controllers and repositories.",
                "key_points": [
                    "@Service is a specialization of @Component",
                    "Contains business logic and orchestration",
                    "Sits between controllers and repositories",
                    "Should be stateless and reusable"
                ]
            },
            "Dependency Injection": {
                "concept": "Dependency Injection",
                "language": "Java",
                "framework": "Spring Boot",
                "source_name": "Spring Framework Documentation",
                "source_url": "https://docs.spring.io/spring-framework/reference/core/beans/dependencies/factory-collaborators.html",
                "fallback_summary": "Dependency Injection is a design pattern where Spring automatically provides (injects) dependencies to classes, removing hard-coded dependencies.",
                "key_points": [
                    "Spring IoC container manages object creation",
                    "@Autowired tells Spring to inject dependencies",
                    "Constructor injection is preferred over field injection",
                    "Promotes loose coupling and testability"
                ]
            },
            "Repository Pattern": {
                "concept": "Repository Pattern",
                "language": "Java",
                "framework": "Spring Boot",
                "source_name": "Spring Data JPA Documentation",
                "source_url": "https://docs.spring.io/spring-data/jpa/reference/repositories.html",
                "fallback_summary": "@Repository marks a class as a data access layer. Spring Data JPA provides automatic CRUD operations.",
                "key_points": [
                    "Abstracts database operations",
                    "Extends JpaRepository for automatic CRUD methods",
                    "Can define custom queries with @Query",
                    "Handles database exceptions"
                ]
            },
            "Database Transaction": {
                "concept": "Database Transaction",
                "language": "Java",
                "framework": "Spring Boot",
                "source_name": "Spring Framework Documentation",
                "source_url": "https://docs.spring.io/spring-framework/reference/data-access/transaction.html",
                "fallback_summary": "@Transactional ensures database operations are atomic. If any operation fails, all changes are rolled back.",
                "key_points": [
                    "ACID properties: Atomicity, Consistency, Isolation, Durability",
                    "@Transactional on methods or classes",
                    "Automatic rollback on runtime exceptions",
                    "Use for operations that modify multiple tables"
                ]
            },
            "ORM Entity": {
                "concept": "ORM Entity",
                "language": "Java",
                "framework": "Spring Boot",
                "source_name": "JPA Documentation",
                "source_url": "https://docs.oracle.com/javaee/7/tutorial/persistence-intro.htm",
                "fallback_summary": "@Entity marks a class as a JPA entity that maps to a database table. Each instance represents a row.",
                "key_points": [
                    "@Entity maps Java class to database table",
                    "@Id marks the primary key field",
                    "@Column customizes column mapping",
                    "Relationships: @OneToMany, @ManyToOne, @ManyToMany"
                ]
            },
            
            # Python Core Concepts
            "Python Exception Handling": {
                "concept": "Python Exception Handling",
                "language": "Python",
                "framework": None,
                "source_name": "Python Official Documentation",
                "source_url": "https://docs.python.org/3/tutorial/errors.html",
                "fallback_summary": "Use try-except blocks to handle errors. The except block catches specific exceptions and handles them gracefully.",
                "key_points": [
                    "try block contains code that might raise an exception",
                    "except block handles specific exception types",
                    "else block runs if no exception occurred",
                    "finally block always executes for cleanup"
                ]
            },
            "Python Type Hints": {
                "concept": "Python Type Hints",
                "language": "Python",
                "framework": None,
                "source_name": "Python Official Documentation",
                "source_url": "https://docs.python.org/3/library/typing.html",
                "fallback_summary": "Type hints add optional type information to Python code, improving code clarity and enabling better IDE support.",
                "key_points": [
                    "Use : type for variable annotations",
                    "Use -> type for return type annotations",
                    "List[str], Dict[str, int] for generic types",
                    "Optional[str] for values that can be None"
                ]
            },
            "Python Async": {
                "concept": "Python Async",
                "language": "Python",
                "framework": None,
                "source_name": "Python Official Documentation",
                "source_url": "https://docs.python.org/3/library/asyncio.html",
                "fallback_summary": "async/await enables asynchronous programming. Async functions can pause execution while waiting for I/O operations.",
                "key_points": [
                    "async def defines an asynchronous function",
                    "await pauses execution until result is ready",
                    "Improves performance for I/O-bound operations",
                    "Use asyncio.run() to run async functions"
                ]
            },
            
            # FastAPI Concepts
            "FastAPI App": {
                "concept": "FastAPI App",
                "language": "Python",
                "framework": "FastAPI",
                "source_name": "FastAPI Official Documentation",
                "source_url": "https://fastapi.tiangolo.com/tutorial/first-steps/",
                "fallback_summary": "FastAPI is a modern Python web framework for building APIs. It's fast, easy to use, and provides automatic API documentation.",
                "key_points": [
                    "FastAPI() creates the application instance",
                    "Automatic data validation using Pydantic",
                    "Automatic interactive API docs at /docs",
                    "Built on Starlette and Pydantic"
                ]
            },
            "API Route": {
                "concept": "API Route",
                "language": "Python",
                "framework": "FastAPI",
                "source_name": "FastAPI Official Documentation",
                "source_url": "https://fastapi.tiangolo.com/tutorial/path-params/",
                "fallback_summary": "Routes define API endpoints. Use @app.get, @app.post, etc. decorators to create endpoints that handle HTTP requests.",
                "key_points": [
                    "@app.get() for GET requests",
                    "@app.post() for POST requests",
                    "Path parameters in URL: /items/{item_id}",
                    "Query parameters: /items/?skip=0&limit=10"
                ]
            },
            "Pydantic Model": {
                "concept": "Pydantic Model",
                "language": "Python",
                "framework": "FastAPI",
                "source_name": "Pydantic Documentation",
                "source_url": "https://docs.pydantic.dev/latest/",
                "fallback_summary": "Pydantic models define data schemas with automatic validation. FastAPI uses them for request/response validation.",
                "key_points": [
                    "Inherit from BaseModel",
                    "Automatic data validation",
                    "Type conversion and coercion",
                    "Generates JSON schema automatically"
                ]
            },
            
            # JavaScript Core Concepts
            "JavaScript Promises": {
                "concept": "JavaScript Promises",
                "language": "JavaScript",
                "framework": None,
                "source_name": "MDN Web Docs",
                "source_url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise",
                "fallback_summary": "Promises represent eventual completion or failure of an asynchronous operation. They help avoid callback hell.",
                "key_points": [
                    "Promise has three states: pending, fulfilled, rejected",
                    ".then() handles successful completion",
                    ".catch() handles errors",
                    ".finally() runs regardless of outcome"
                ]
            },
            "JavaScript Async/Await": {
                "concept": "JavaScript Async/Await",
                "language": "JavaScript",
                "framework": None,
                "source_name": "MDN Web Docs",
                "source_url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function",
                "fallback_summary": "async/await makes asynchronous code look synchronous. It's syntactic sugar over Promises.",
                "key_points": [
                    "async function always returns a Promise",
                    "await pauses execution until Promise resolves",
                    "Use try-catch for error handling",
                    "Makes async code more readable"
                ]
            },
            
            # React Concepts
            "React Component": {
                "concept": "React Component",
                "language": "JavaScript",
                "framework": "React",
                "source_name": "React Official Documentation",
                "source_url": "https://react.dev/learn/your-first-component",
                "fallback_summary": "Components are reusable UI building blocks. They accept props and return JSX describing what should appear on screen.",
                "key_points": [
                    "Function components are JavaScript functions",
                    "Return JSX to describe UI",
                    "Can accept props as parameters",
                    "Component names must start with capital letter"
                ]
            },
            "React State": {
                "concept": "React State",
                "language": "JavaScript",
                "framework": "React",
                "source_name": "React Official Documentation",
                "source_url": "https://react.dev/learn/state-a-components-memory",
                "fallback_summary": "State is component memory. When state changes, React re-renders the component. Use useState hook to add state.",
                "key_points": [
                    "useState returns [value, setter]",
                    "State updates trigger re-renders",
                    "State is local to component instance",
                    "Never mutate state directly, use setter"
                ]
            },
            "React useEffect": {
                "concept": "React useEffect",
                "language": "JavaScript",
                "framework": "React",
                "source_name": "React Official Documentation",
                "source_url": "https://react.dev/reference/react/useEffect",
                "fallback_summary": "useEffect lets you perform side effects in components. It runs after render and can sync with external systems.",
                "key_points": [
                    "Runs after every render by default",
                    "Dependency array controls when it runs",
                    "Return cleanup function if needed",
                    "Use for data fetching, subscriptions, DOM updates"
                ]
            },
            "React Props": {
                "concept": "React Props",
                "language": "JavaScript",
                "framework": "React",
                "source_name": "React Official Documentation",
                "source_url": "https://react.dev/learn/passing-props-to-a-component",
                "fallback_summary": "Props are arguments passed to components. They flow from parent to child and are read-only.",
                "key_points": [
                    "Props are passed like HTML attributes",
                    "Props are read-only (immutable)",
                    "Destructure props for cleaner code",
                    "Use prop types for validation"
                ]
            },
            
            # Flutter/Dart Concepts
            "Stateful Widget": {
                "concept": "Stateful Widget",
                "language": "Dart",
                "framework": "Flutter",
                "source_name": "Flutter Official Documentation",
                "source_url": "https://docs.flutter.dev/ui/interactivity",
                "fallback_summary": "StatefulWidget has mutable state that can change over time. Use setState() to update UI when state changes.",
                "key_points": [
                    "Extends StatefulWidget class",
                    "createState() returns State object",
                    "setState() triggers rebuild",
                    "Use for interactive widgets"
                ]
            },
            "Stateless Widget": {
                "concept": "Stateless Widget",
                "language": "Dart",
                "framework": "Flutter",
                "source_name": "Flutter Official Documentation",
                "source_url": "https://docs.flutter.dev/ui/widgets-intro",
                "fallback_summary": "StatelessWidget is immutable. It doesn't change over time and is rebuilt only when parent changes.",
                "key_points": [
                    "Extends StatelessWidget class",
                    "build() method returns widget tree",
                    "Immutable and efficient",
                    "Use for static UI elements"
                ]
            },
            "FutureBuilder": {
                "concept": "FutureBuilder",
                "language": "Dart",
                "framework": "Flutter",
                "source_name": "Flutter Official Documentation",
                "source_url": "https://api.flutter.dev/flutter/widgets/FutureBuilder-class.html",
                "fallback_summary": "FutureBuilder builds UI based on Future result. It handles loading, success, and error states automatically.",
                "key_points": [
                    "Takes a Future and builder function",
                    "snapshot.connectionState shows loading state",
                    "snapshot.hasData checks if data is ready",
                    "snapshot.hasError checks for errors"
                ]
            },
            "Firebase Auth": {
                "concept": "Firebase Auth",
                "language": "Dart",
                "framework": "Flutter",
                "source_name": "Firebase Documentation",
                "source_url": "https://firebase.google.com/docs/auth",
                "fallback_summary": "Firebase Authentication provides backend services for user authentication. Supports email/password, Google, Facebook, etc.",
                "key_points": [
                    "FirebaseAuth.instance for auth operations",
                    "signInWithEmailAndPassword() for login",
                    "createUserWithEmailAndPassword() for signup",
                    "authStateChanges() stream for auth state"
                ]
            },
            "Firestore": {
                "concept": "Firestore",
                "language": "Dart",
                "framework": "Flutter",
                "source_name": "Firebase Documentation",
                "source_url": "https://firebase.google.com/docs/firestore",
                "fallback_summary": "Cloud Firestore is a NoSQL cloud database. Data is stored in documents organized into collections.",
                "key_points": [
                    "FirebaseFirestore.instance for database access",
                    "collection() to reference collections",
                    "doc() to reference documents",
                    "Real-time listeners with snapshots()"
                ]
            }
        }
    
    def get_doc_entry(self, concept: str) -> Optional[Dict[str, Any]]:
        """Get documentation entry for a concept"""
        return self.registry.get(concept)
    
    def get_docs_by_language(self, language: str) -> List[Dict[str, Any]]:
        """Get all documentation entries for a language"""
        return [
            doc for doc in self.registry.values()
            if doc['language'] == language
        ]
    
    def get_docs_by_framework(self, framework: str) -> List[Dict[str, Any]]:
        """Get all documentation entries for a framework"""
        return [
            doc for doc in self.registry.values()
            if doc['framework'] == framework
        ]
    
    def search_docs(self, query: str) -> List[Dict[str, Any]]:
        """Search documentation entries by concept name"""
        query_lower = query.lower()
        return [
            doc for doc in self.registry.values()
            if query_lower in doc['concept'].lower()
        ]
    
    def get_all_concepts(self) -> List[str]:
        """Get list of all concept names"""
        return list(self.registry.keys())
    
    def get_all_sources(self) -> List[Dict[str, str]]:
        """Get list of all unique documentation sources"""
        sources = {}
        for doc in self.registry.values():
            source_name = doc['source_name']
            if source_name not in sources:
                sources[source_name] = {
                    'name': source_name,
                    'url': doc['source_url'].split('/')[0] + '//' + doc['source_url'].split('/')[2]
                }
        return list(sources.values())


# Made with Bob