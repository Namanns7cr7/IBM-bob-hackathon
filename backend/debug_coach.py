"""
Debug Coach - Provides debugging guidance based on error patterns
Uses template-based matching for common errors
"""
from typing import Dict, List, Any
import re


class DebugCoach:
    def __init__(self):
        self.error_patterns = self._initialize_error_patterns()
    
    def analyze_error(self, error_log: str, skill_level: str, detected_stack: Dict) -> Dict[str, Any]:
        """Analyze error log and provide debugging guidance"""
        error_log_lower = error_log.lower()
        
        # Match error pattern
        matched_pattern = self._match_error_pattern(error_log_lower)
        
        if matched_pattern:
            guidance = self._generate_guidance(matched_pattern, skill_level, detected_stack)
        else:
            guidance = self._generate_generic_guidance(error_log, skill_level)
        
        return guidance
    
    def _initialize_error_patterns(self) -> List[Dict[str, Any]]:
        """Initialize common error patterns"""
        return [
            {
                'name': 'NullPointerException',
                'patterns': [
                    r'nullpointerexception',
                    r'cannot read property.*of null',
                    r'cannot read property.*of undefined',
                    r'null is not an object',
                    r'typeerror.*null',
                    r'typeerror.*undefined'
                ],
                'bug_type': 'Null/Undefined Access',
                'meaning': 'You are trying to access a property or method on a null or undefined value.',
                'likely_causes': [
                    'Variable was not initialized',
                    'API returned null/undefined',
                    'Object property does not exist',
                    'Async data not loaded yet',
                    'Database query returned empty'
                ],
                'debugging_steps': [
                    'Read the stack trace to find the exact line',
                    'Check if the variable is null/undefined before using it',
                    'Add console.log or print statements to inspect values',
                    'Verify API responses and database queries',
                    'Use optional chaining (?.) or null checks'
                ],
                'possible_fix': 'Add null/undefined checks before accessing properties',
                'prevention': 'Always validate data before use, use Optional types, add default values',
                'concepts_to_learn': ['Null Safety', 'Optional Types', 'Defensive Programming']
            },
            {
                'name': '404 Not Found',
                'patterns': [
                    r'404',
                    r'not found',
                    r'cannot get',
                    r'no route found',
                    r'endpoint not found'
                ],
                'bug_type': 'Route/Endpoint Not Found',
                'meaning': 'The requested URL or API endpoint does not exist.',
                'likely_causes': [
                    'Incorrect URL or path',
                    'Route not registered in backend',
                    'HTTP method mismatch (GET vs POST)',
                    'Missing route parameters',
                    'Server not running'
                ],
                'debugging_steps': [
                    'Verify the URL is correct',
                    'Check if the route is defined in your backend',
                    'Confirm HTTP method matches (GET, POST, PUT, DELETE)',
                    'Check for typos in route path',
                    'Ensure server is running on correct port'
                ],
                'possible_fix': 'Register the route in your backend or fix the URL',
                'prevention': 'Use constants for API endpoints, test routes after creation',
                'concepts_to_learn': ['REST API', 'HTTP Methods', 'Routing']
            },
            {
                'name': '500 Internal Server Error',
                'patterns': [
                    r'500',
                    r'internal server error',
                    r'server error',
                    r'unhandled exception'
                ],
                'bug_type': 'Backend Exception',
                'meaning': 'An unhandled error occurred in the backend code.',
                'likely_causes': [
                    'Unhandled exception in backend code',
                    'Database connection failed',
                    'Invalid data processing',
                    'Missing environment variables',
                    'Syntax error in backend'
                ],
                'debugging_steps': [
                    'Check backend logs for detailed error',
                    'Look for stack trace in server console',
                    'Verify database connection',
                    'Check environment variables',
                    'Test the endpoint with valid data'
                ],
                'possible_fix': 'Add try-catch blocks and proper error handling',
                'prevention': 'Add comprehensive error handling, validate inputs, test edge cases',
                'concepts_to_learn': ['Exception Handling', 'Error Logging', 'Input Validation']
            },
            {
                'name': 'CORS Error',
                'patterns': [
                    r'cors',
                    r'cross-origin',
                    r'access-control-allow-origin',
                    r'blocked by cors policy'
                ],
                'bug_type': 'Cross-Origin Resource Sharing',
                'meaning': 'Browser blocked the request due to CORS policy.',
                'likely_causes': [
                    'Backend not configured for CORS',
                    'Frontend and backend on different domains',
                    'Missing CORS headers',
                    'Incorrect CORS configuration'
                ],
                'debugging_steps': [
                    'Check browser console for CORS error details',
                    'Verify backend CORS configuration',
                    'Ensure frontend URL is allowed in backend',
                    'Check if credentials are needed',
                    'Test with CORS browser extension temporarily'
                ],
                'possible_fix': 'Configure CORS in backend to allow frontend origin',
                'prevention': 'Set up CORS properly from the start, use environment variables for origins',
                'concepts_to_learn': ['CORS', 'HTTP Headers', 'Web Security']
            },
            {
                'name': 'Connection Refused',
                'patterns': [
                    r'connection refused',
                    r'econnrefused',
                    r'failed to connect',
                    r'network error',
                    r'unable to connect'
                ],
                'bug_type': 'Connection Error',
                'meaning': 'Cannot connect to the server or database.',
                'likely_causes': [
                    'Server is not running',
                    'Wrong port number',
                    'Firewall blocking connection',
                    'Database not started',
                    'Incorrect host/URL'
                ],
                'debugging_steps': [
                    'Check if server is running',
                    'Verify port number is correct',
                    'Test connection with curl or Postman',
                    'Check firewall settings',
                    'Verify database is running'
                ],
                'possible_fix': 'Start the server/database or fix connection settings',
                'prevention': 'Use health check endpoints, document setup steps clearly',
                'concepts_to_learn': ['Networking', 'Client-Server Architecture', 'Ports']
            },
            {
                'name': 'Module Not Found',
                'patterns': [
                    r'module not found',
                    r'cannot find module',
                    r'no module named',
                    r'importerror',
                    r'modulenotfounderror'
                ],
                'bug_type': 'Import/Dependency Error',
                'meaning': 'Required module or package is not installed or cannot be found.',
                'likely_causes': [
                    'Package not installed',
                    'Wrong import path',
                    'Virtual environment not activated',
                    'Package name typo',
                    'Missing dependency in package.json or requirements.txt'
                ],
                'debugging_steps': [
                    'Check if package is in dependencies file',
                    'Run npm install or pip install',
                    'Verify import path is correct',
                    'Check for typos in package name',
                    'Ensure virtual environment is activated'
                ],
                'possible_fix': 'Install the missing package or fix import path',
                'prevention': 'Keep dependencies updated, use lock files, document installation steps',
                'concepts_to_learn': ['Package Management', 'Dependencies', 'Virtual Environments']
            },
            {
                'name': 'Permission Denied',
                'patterns': [
                    r'permission denied',
                    r'access denied',
                    r'forbidden',
                    r'403',
                    r'unauthorized',
                    r'401'
                ],
                'bug_type': 'Authorization/Permission Error',
                'meaning': 'User does not have permission to perform this action.',
                'likely_causes': [
                    'Missing authentication token',
                    'Invalid credentials',
                    'Insufficient permissions',
                    'File system permissions',
                    'Database access rules'
                ],
                'debugging_steps': [
                    'Check if user is authenticated',
                    'Verify authentication token is valid',
                    'Check user roles and permissions',
                    'Review file/database access rules',
                    'Test with admin credentials'
                ],
                'possible_fix': 'Add proper authentication or adjust permissions',
                'prevention': 'Implement proper auth flow, test with different user roles',
                'concepts_to_learn': ['Authentication', 'Authorization', 'Security']
            },
            {
                'name': 'Database Connection Error',
                'patterns': [
                    r'database.*error',
                    r'connection.*database',
                    r'sql.*error',
                    r'query.*failed',
                    r'database.*timeout'
                ],
                'bug_type': 'Database Error',
                'meaning': 'Cannot connect to or query the database.',
                'likely_causes': [
                    'Database not running',
                    'Wrong connection string',
                    'Invalid credentials',
                    'Network issue',
                    'Database locked or busy'
                ],
                'debugging_steps': [
                    'Check if database is running',
                    'Verify connection string',
                    'Test credentials',
                    'Check database logs',
                    'Verify network connectivity'
                ],
                'possible_fix': 'Fix database connection settings or start database',
                'prevention': 'Use connection pooling, add retry logic, monitor database health',
                'concepts_to_learn': ['Database Connections', 'Connection Pooling', 'SQL']
            },
            {
                'name': 'Build Failed',
                'patterns': [
                    r'build failed',
                    r'compilation error',
                    r'syntax error',
                    r'parse error',
                    r'unexpected token'
                ],
                'bug_type': 'Build/Compilation Error',
                'meaning': 'Code has syntax errors or build configuration issues.',
                'likely_causes': [
                    'Syntax error in code',
                    'Missing dependency',
                    'Wrong configuration',
                    'Incompatible versions',
                    'Missing files'
                ],
                'debugging_steps': [
                    'Read the error message carefully',
                    'Check the line number mentioned',
                    'Look for syntax errors',
                    'Verify all dependencies are installed',
                    'Check build configuration files'
                ],
                'possible_fix': 'Fix syntax errors or update build configuration',
                'prevention': 'Use linters, enable auto-formatting, test builds frequently',
                'concepts_to_learn': ['Build Tools', 'Compilation', 'Syntax']
            }
        ]
    
    def _match_error_pattern(self, error_log_lower: str) -> Dict[str, Any] | None:
        """Match error log against known patterns"""
        for pattern_info in self.error_patterns:
            for pattern in pattern_info['patterns']:
                if re.search(pattern, error_log_lower):
                    return pattern_info
        return None
    
    def _generate_guidance(self, pattern: Dict[str, Any], skill_level: str, detected_stack: Dict) -> Dict[str, Any]:
        """Generate debugging guidance based on matched pattern"""
        guidance = {
            'bug_type': pattern['bug_type'],
            'meaning': pattern['meaning'],
            'likely_causes': pattern['likely_causes'],
            'debugging_steps': pattern['debugging_steps'],
            'possible_fix': pattern['possible_fix'],
            'prevention': pattern['prevention'],
            'concepts_to_learn': pattern['concepts_to_learn'],
            'mini_quiz': self._generate_quiz(pattern, skill_level)
        }
        
        # Adjust guidance based on skill level
        if skill_level == 'beginner':
            guidance['additional_help'] = 'Take it step by step. Start with the first debugging step.'
        elif skill_level == 'intermediate':
            guidance['additional_help'] = 'Review the concepts to learn for deeper understanding.'
        else:
            guidance['additional_help'] = 'Consider edge cases and add comprehensive error handling.'
        
        return guidance
    
    def _generate_generic_guidance(self, error_log: str, skill_level: str) -> Dict[str, Any]:
        """Generate generic debugging guidance for unknown errors"""
        return {
            'bug_type': 'Unknown Error',
            'meaning': 'The error pattern is not recognized. Follow general debugging steps.',
            'likely_causes': [
                'Check the error message for clues',
                'Look for stack trace information',
                'Review recent code changes'
            ],
            'debugging_steps': [
                'Read the full error message carefully',
                'Identify the file and line number',
                'Check recent changes in that area',
                'Add logging to understand the flow',
                'Search the error message online',
                'Check documentation for the library/framework'
            ],
            'possible_fix': 'Debug systematically using the steps above',
            'prevention': 'Add comprehensive error handling and logging',
            'concepts_to_learn': ['Debugging', 'Error Handling', 'Logging'],
            'mini_quiz': [
                {
                    'question': 'What is the first step in debugging any error?',
                    'answer': 'Read the error message carefully and identify the file and line number.'
                }
            ],
            'additional_help': 'Copy the error message and search online for similar issues.'
        }
    
    def _generate_quiz(self, pattern: Dict[str, Any], skill_level: str) -> List[Dict[str, str]]:
        """Generate quiz questions based on error pattern"""
        quiz_templates = {
            'NullPointerException': [
                {
                    'question': 'Why do null pointer errors occur?',
                    'answer': 'They occur when you try to access a property or method on a null or undefined value.'
                },
                {
                    'question': 'How can you prevent null pointer errors?',
                    'answer': 'Add null checks, use optional types, validate data before use, and provide default values.'
                }
            ],
            '404 Not Found': [
                {
                    'question': 'What does a 404 error mean?',
                    'answer': 'The requested URL or API endpoint does not exist on the server.'
                },
                {
                    'question': 'What should you check when you get a 404 error?',
                    'answer': 'Check the URL spelling, verify the route is registered, and confirm the HTTP method matches.'
                }
            ],
            '500 Internal Server Error': [
                {
                    'question': 'What does a 500 error indicate?',
                    'answer': 'An unhandled exception occurred in the backend code.'
                },
                {
                    'question': 'Where should you look to debug a 500 error?',
                    'answer': 'Check the backend logs and server console for the detailed error and stack trace.'
                }
            ]
        }
        
        return quiz_templates.get(pattern['name'], [
            {
                'question': f'What is the main cause of {pattern["bug_type"]}?',
                'answer': pattern['meaning']
            }
        ])

# Made with Bob
