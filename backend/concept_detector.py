"""
Concept Detector - Detects programming concepts and patterns in code
Uses keyword and pattern matching for local detection
"""
import re
from typing import Dict, List, Any


class ConceptDetector:
    def __init__(self, source_files: List[Dict], primary_language: str):
        self.source_files = source_files
        self.primary_language = primary_language
        self.detected_concepts = []
    
    def detect(self) -> List[Dict[str, Any]]:
        """Main detection method"""
        if self.primary_language == 'Java':
            self._detect_java_concepts()
        elif self.primary_language == 'Python':
            self._detect_python_concepts()
        elif self.primary_language in ['JavaScript', 'TypeScript']:
            self._detect_javascript_concepts()
        elif self.primary_language == 'Dart':
            self._detect_dart_concepts()
        else:
            self._detect_generic_concepts()
        
        return self.detected_concepts
    
    def _detect_java_concepts(self):
        """Detect Java/Spring Boot concepts"""
        concept_patterns = {
            'REST Controller': {
                'patterns': [r'@RestController', r'@Controller'],
                'weight': 12,
                'category': 'Architecture',
                'description': 'Handles HTTP requests and returns responses'
            },
            'Service Layer': {
                'patterns': [r'@Service'],
                'weight': 10,
                'category': 'Architecture',
                'description': 'Contains business logic separated from controllers'
            },
            'Repository Pattern': {
                'patterns': [r'@Repository', r'JpaRepository', r'CrudRepository'],
                'weight': 10,
                'category': 'Data Access',
                'description': 'Abstracts database operations'
            },
            'Dependency Injection': {
                'patterns': [r'@Autowired', r'@Inject'],
                'weight': 10,
                'category': 'Design Pattern',
                'description': 'Automatically provides dependencies to classes'
            },
            'ORM Entity': {
                'patterns': [r'@Entity', r'@Table'],
                'weight': 8,
                'category': 'Data Access',
                'description': 'Maps Java objects to database tables'
            },
            'Database Transaction': {
                'patterns': [r'@Transactional'],
                'weight': 12,
                'category': 'Data Access',
                'description': 'Ensures database operations are atomic'
            },
            'REST Endpoint': {
                'patterns': [r'@GetMapping', r'@PostMapping', r'@PutMapping', r'@DeleteMapping', r'@RequestMapping'],
                'weight': 6,
                'category': 'API',
                'description': 'Defines HTTP endpoints for API'
            },
            'Exception Handling': {
                'patterns': [r'\btry\b', r'\bcatch\b', r'@ExceptionHandler'],
                'weight': 8,
                'category': 'Error Handling',
                'description': 'Handles errors and exceptions gracefully'
            },
            'Optional/Null Safety': {
                'patterns': [r'Optional<', r'Optional\.'],
                'weight': 6,
                'category': 'Best Practice',
                'description': 'Prevents null pointer exceptions'
            },
            'Data Validation': {
                'patterns': [r'@Valid', r'@NotNull', r'@NotEmpty', r'@Size'],
                'weight': 6,
                'category': 'Validation',
                'description': 'Validates input data'
            }
        }
        
        self._scan_for_concepts(concept_patterns)
    
    def _detect_python_concepts(self):
        """Detect Python/FastAPI concepts"""
        concept_patterns = {
            'FastAPI App': {
                'patterns': [r'FastAPI\(\)', r'from fastapi import'],
                'weight': 10,
                'category': 'Framework',
                'description': 'Modern Python web framework'
            },
            'API Route': {
                'patterns': [r'@app\.get', r'@app\.post', r'@app\.put', r'@app\.delete', r'@router\.'],
                'weight': 6,
                'category': 'API',
                'description': 'Defines API endpoints'
            },
            'Async Function': {
                'patterns': [r'\basync def\b', r'\bawait\b'],
                'weight': 10,
                'category': 'Concurrency',
                'description': 'Asynchronous programming for better performance'
            },
            'Data Validation': {
                'patterns': [r'BaseModel', r'from pydantic import'],
                'weight': 8,
                'category': 'Validation',
                'description': 'Validates and serializes data'
            },
            'Type Hints': {
                'patterns': [r':\s*str', r':\s*int', r':\s*List\[', r':\s*Dict\[', r'->\s*\w+'],
                'weight': 6,
                'category': 'Best Practice',
                'description': 'Adds type information to Python code'
            },
            'Exception Handling': {
                'patterns': [r'\btry:', r'\bexcept\b', r'\braise\b'],
                'weight': 8,
                'category': 'Error Handling',
                'description': 'Handles errors and exceptions'
            },
            'Dependency Injection': {
                'patterns': [r'Depends\(', r'from fastapi import.*Depends'],
                'weight': 10,
                'category': 'Design Pattern',
                'description': 'Manages dependencies in FastAPI'
            },
            'Database ORM': {
                'patterns': [r'from sqlalchemy', r'Session', r'query\('],
                'weight': 8,
                'category': 'Data Access',
                'description': 'Object-Relational Mapping for databases'
            }
        }
        
        self._scan_for_concepts(concept_patterns)
    
    def _detect_javascript_concepts(self):
        """Detect JavaScript/React concepts"""
        concept_patterns = {
            'React Component': {
                'patterns': [r'function\s+[A-Z]\w+', r'const\s+[A-Z]\w+\s*=', r'export default function'],
                'weight': 8,
                'category': 'UI',
                'description': 'Reusable UI building blocks'
            },
            'State Management': {
                'patterns': [r'useState', r'useReducer', r'this\.setState'],
                'weight': 8,
                'category': 'State',
                'description': 'Manages component data and UI state'
            },
            'Side Effects': {
                'patterns': [r'useEffect', r'componentDidMount', r'componentDidUpdate'],
                'weight': 10,
                'category': 'Lifecycle',
                'description': 'Handles side effects like API calls'
            },
            'Props': {
                'patterns': [r'\bprops\b', r'\bprops\.', r'function\s+\w+\(\{[^}]+\}\)'],
                'weight': 6,
                'category': 'Data Flow',
                'description': 'Passes data between components'
            },
            'API Call': {
                'patterns': [r'\bfetch\(', r'axios\.', r'\.then\(', r'\.catch\('],
                'weight': 6,
                'category': 'Network',
                'description': 'Communicates with backend APIs'
            },
            'Async/Await': {
                'patterns': [r'\basync\s+function', r'\basync\s+\(', r'\bawait\b'],
                'weight': 10,
                'category': 'Concurrency',
                'description': 'Handles asynchronous operations'
            },
            'Event Handling': {
                'patterns': [r'onClick', r'onChange', r'onSubmit', r'addEventListener'],
                'weight': 4,
                'category': 'Interaction',
                'description': 'Responds to user interactions'
            },
            'List Rendering': {
                'patterns': [r'\.map\(', r'\.filter\(', r'\.forEach\('],
                'weight': 4,
                'category': 'Rendering',
                'description': 'Renders lists of data'
            },
            'Context API': {
                'patterns': [r'createContext', r'useContext', r'Context\.Provider'],
                'weight': 8,
                'category': 'State',
                'description': 'Shares state across components'
            }
        }
        
        self._scan_for_concepts(concept_patterns)
    
    def _detect_dart_concepts(self):
        """Detect Dart/Flutter concepts"""
        concept_patterns = {
            'Stateful Widget': {
                'patterns': [r'extends StatefulWidget', r'createState\(\)'],
                'weight': 8,
                'category': 'UI',
                'description': 'Widget with mutable state'
            },
            'Stateless Widget': {
                'patterns': [r'extends StatelessWidget'],
                'weight': 6,
                'category': 'UI',
                'description': 'Widget without mutable state'
            },
            'Async UI': {
                'patterns': [r'FutureBuilder', r'Future<'],
                'weight': 10,
                'category': 'Async',
                'description': 'Builds UI based on async data'
            },
            'Stream': {
                'patterns': [r'StreamBuilder', r'Stream<'],
                'weight': 10,
                'category': 'Async',
                'description': 'Handles real-time data streams'
            },
            'Firebase Auth': {
                'patterns': [r'FirebaseAuth', r'signInWithEmailAndPassword'],
                'weight': 15,
                'category': 'Backend',
                'description': 'User authentication with Firebase'
            },
            'Firestore': {
                'patterns': [r'FirebaseFirestore', r'collection\(', r'doc\('],
                'weight': 12,
                'category': 'Database',
                'description': 'Cloud database operations'
            },
            'Navigation': {
                'patterns': [r'Navigator\.push', r'Navigator\.pop', r'MaterialPageRoute'],
                'weight': 6,
                'category': 'Navigation',
                'description': 'Screen navigation'
            },
            'State Management': {
                'patterns': [r'setState\(', r'Provider', r'ChangeNotifier'],
                'weight': 8,
                'category': 'State',
                'description': 'Manages app state'
            }
        }
        
        self._scan_for_concepts(concept_patterns)
    
    def _detect_generic_concepts(self):
        """Detect generic programming concepts"""
        concept_patterns = {
            'Functions': {
                'patterns': [r'\bdef\s+\w+', r'\bfunction\s+\w+', r'\bfunc\s+\w+'],
                'weight': 4,
                'category': 'Basic',
                'description': 'Reusable blocks of code'
            },
            'Classes': {
                'patterns': [r'\bclass\s+\w+'],
                'weight': 6,
                'category': 'OOP',
                'description': 'Object-oriented programming structures'
            },
            'Error Handling': {
                'patterns': [r'\btry\b', r'\bcatch\b', r'\bexcept\b'],
                'weight': 8,
                'category': 'Error Handling',
                'description': 'Handles errors gracefully'
            }
        }
        
        self._scan_for_concepts(concept_patterns)
    
    def _scan_for_concepts(self, concept_patterns: Dict[str, Dict]):
        """Scan source files for concept patterns"""
        concept_matches = {}
        
        for file_info in self.source_files[:30]:  # Limit to first 30 files
            file_path = file_info.get('path', '')
            
            # Read file content if available
            content = self._get_file_content(file_info)
            if not content:
                continue
            
            for concept_name, concept_info in concept_patterns.items():
                for pattern in concept_info['patterns']:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    if matches:
                        if concept_name not in concept_matches:
                            concept_matches[concept_name] = {
                                'name': concept_name,
                                'count': 0,
                                'files': [],
                                'weight': concept_info['weight'],
                                'category': concept_info['category'],
                                'description': concept_info['description']
                            }
                        concept_matches[concept_name]['count'] += len(matches)
                        if file_path not in concept_matches[concept_name]['files']:
                            concept_matches[concept_name]['files'].append(file_path)
        
        # Convert to list and sort by count
        self.detected_concepts = sorted(
            concept_matches.values(),
            key=lambda x: x['count'],
            reverse=True
        )
    
    def _get_file_content(self, file_info: Dict) -> str:
        """Get file content from structure if available"""
        # Return content if it was extracted during analysis
        return file_info.get('content', '')
    
    def get_high_priority_concepts(self) -> List[Dict[str, Any]]:
        """Get concepts with high weight (important to understand)"""
        return [c for c in self.detected_concepts if c['weight'] >= 8]

# Made with Bob
