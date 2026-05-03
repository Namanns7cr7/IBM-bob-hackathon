"""
DebugSensei - FastAPI Backend
Main application file with all API endpoints
"""
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Any
import zipfile
import shutil
import uuid
from pathlib import Path

from repo_analyzer import RepoAnalyzer
from stack_detector import StackDetector
from concept_detector import ConceptDetector
from debug_coach import DebugCoach
from debt_score import DebtScoreCalculator
from docs_retriever import DocsRetriever
from cache_manager import CacheManager
from ai_reasoner import AIReasoner
from official_docs_registry import OfficialDocsRegistry
from official_docs_fetcher import OfficialDocsFetcher
from docs_matcher import DocsMatcher
from local_memory import LocalMemory
from report_generator import ReportGenerator
from git_cloner import GitCloner

# Initialize FastAPI app
app = FastAPI(
    title="DebugSensei API",
    description="Universal learning and debugging mentor for AI-assisted developers",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
cache_manager = CacheManager()
docs_retriever = DocsRetriever()
ai_reasoner = AIReasoner(use_ai=False)  # Set to True with API key for AI features
debug_coach = DebugCoach()
debt_calculator = DebtScoreCalculator()
docs_matcher = DocsMatcher()
local_memory = LocalMemory()
report_generator = ReportGenerator()
git_cloner = GitCloner()

# Create necessary directories
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


# Pydantic models for request/response
class AnalyzeRequest(BaseModel):
    repo_id: str
    skill_level: str  # beginner, intermediate, advanced
    goal: str  # learn, debug, interview_ready, production_ready


class DebugRequest(BaseModel):
    repo_id: str
    error_log: str
    skill_level: str


class FeatureWalkthroughRequest(BaseModel):
    repo_id: str
    feature_name: str
    skill_level: str


class MemoryRequest(BaseModel):
    session_id: str


class GitHubURLRequest(BaseModel):
    github_url: str
    skill_level: str = "intermediate"
    goal: str = "learn"


class UploadResponse(BaseModel):
    repo_id: str
    message: str


class HealthResponse(BaseModel):
    status: str
    version: str


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "version": "1.0.0"
    }


@app.post("/upload-repo", response_model=UploadResponse)
async def upload_repo(file: UploadFile = File(...)):
    """
    Upload a zipped repository for analysis
    """
    # Validate file type
    if not file.filename or not file.filename.endswith('.zip'):
        raise HTTPException(status_code=400, detail="Only ZIP files are supported")
    
    # Generate unique repo ID
    repo_id = str(uuid.uuid4())
    repo_path = UPLOAD_DIR / repo_id
    repo_path.mkdir(exist_ok=True)
    
    # Save uploaded file
    zip_path = repo_path / "repo.zip"
    try:
        with open(zip_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Extract zip file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(repo_path)
        
        # Remove zip file after extraction
        zip_path.unlink()
        
        return {
            "repo_id": repo_id,
            "message": "Repository uploaded and extracted successfully"
        }
    
    except zipfile.BadZipFile:
        # Clean up on error
        shutil.rmtree(repo_path, ignore_errors=True)
        raise HTTPException(status_code=400, detail="Invalid ZIP file")
    except Exception as e:
        # Clean up on error
        shutil.rmtree(repo_path, ignore_errors=True)
        raise HTTPException(status_code=500, detail=f"Error processing upload: {str(e)}")

@app.post("/analyze-github-url")
async def analyze_github_url(request: GitHubURLRequest):
    """
    Clone and analyze a GitHub repository from URL (like CodeWiki)
    """
    try:
        # Clone the repository
        clone_result = git_cloner.clone_repository(request.github_url)
        
        if not clone_result['success']:
            raise HTTPException(status_code=400, detail="Failed to clone repository")
        
        repo_id = clone_result['session_id']
        repo_path = Path(clone_result['repo_path'])
        
        # Check cache first
        cache_key = cache_manager.generate_cache_key(
            repo_id,
            request.skill_level,
            request.goal
        )
        
        cached_result = cache_manager.get_cached_analysis(cache_key)
        if cached_result:
            cached_data = cached_result.get('data', {})
            if cached_data:
                cached_data['github_info'] = clone_result['repo_info']
                cached_data['repo_stats'] = clone_result['stats']
                return cached_data
        
        # Analyze the cloned repository (same as upload analysis)
        analyzer = RepoAnalyzer(str(repo_path))
        analysis_result = analyzer.analyze()
        
        detector = StackDetector(
            str(repo_path),
            analysis_result['file_tree'],
            analysis_result['config_files']
        )
        stack_info = detector.detect()
        
        concept_detector = ConceptDetector(
            analysis_result['source_files'],
            stack_info['primary_language']
        )
        detected_concepts = concept_detector.detect()
        
        enriched_concepts = docs_matcher.match_concepts_to_docs(
            detected_concepts,
            request.skill_level
        )
        
        debt_score = debt_calculator.calculate(
            detected_concepts,
            request.skill_level,
            analysis_result['stats']['total_files']
        )
        
        docs_matches = docs_retriever.get_docs_for_concepts(detected_concepts, limit=5)
        
        repo_summary = {
            'detected_stack': stack_info,
            'concepts_detected': detected_concepts,
            'stats': analysis_result['stats']
        }
        
        ai_insights = ai_reasoner.generate_learning_summary(
            repo_summary,
            request.skill_level,
            request.goal
        )
        
        quiz_questions = ai_reasoner.generate_quiz_questions(
            detected_concepts,
            request.skill_level
        )
        
        learning_path = debt_calculator.get_learning_priority(detected_concepts)
        
        session_id = local_memory.create_session(
            repo_id=repo_id,
            repo_name=clone_result['repo_info']['full_name'],
            skill_level=request.skill_level,
            goal=request.goal
        )
        
        result = {
            "repo_id": repo_id,
            "session_id": session_id,
            "github_info": clone_result['repo_info'],
            "repo_stats": clone_result['stats'],
            "detected_stack": stack_info,
            "file_tree": analysis_result['file_tree'][:100],
            "stats": analysis_result['stats'],
            "project_summary": ai_insights['project_summary'],
            "architecture_flow": ai_insights['architecture_flow'],
            "concepts_detected": detected_concepts[:15],
            "enriched_concepts": enriched_concepts[:10],
            "docs_matches": docs_matches,
            "debugging_checklist": ai_insights['debugging_checklist'],
            "learning_path": learning_path[:10],
            "quiz_questions": quiz_questions,
            "understanding_debt_score": debt_score
        }
        
        cache_manager.save_analysis(cache_key, result)
        
        return result
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"GitHub analysis error: {str(e)}")

@app.get("/readme/{repo_id}")
async def get_readme(repo_id: str):
    """
    Extract and return README content from repository
    """
    repo_path = UPLOAD_DIR / repo_id
    
    if not repo_path.exists():
        raise HTTPException(status_code=404, detail="Repository not found")
    
    # Look for README files (case-insensitive)
    readme_patterns = ['README.md', 'readme.md', 'Readme.md', 'README.MD', 
                       'README.txt', 'readme.txt', 'README', 'readme']
    
    for pattern in readme_patterns:
        for readme_file in repo_path.rglob(pattern):
            try:
                with open(readme_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    return {
                        "content": content,
                        "filename": readme_file.name,
                        "path": str(readme_file.relative_to(repo_path))
                    }
            except Exception as e:
                continue
    

@app.post("/search-code/{repo_id}")
async def search_code(repo_id: str, query: str, file_pattern: str = "*"):
    """
    Search for code patterns in repository
    """
    repo_path = UPLOAD_DIR / repo_id
    
    if not repo_path.exists():
        raise HTTPException(status_code=404, detail="Repository not found")
    
    try:
        results = []
        search_pattern = query.lower()
        
        # Search through files
        for file_path in repo_path.rglob(file_pattern):
            if file_path.is_file() and not any(part.startswith('.') for part in file_path.parts):
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                        for line_num, line in enumerate(lines, 1):
                            if search_pattern in line.lower():
                                # Get context (2 lines before and after)
                                start = max(0, line_num - 3)
                                end = min(len(lines), line_num + 2)
                                context = ''.join(lines[start:end])
                                
                                results.append({
                                    'file': str(file_path.relative_to(repo_path)),
                                    'line': line_num,
                                    'content': line.strip(),
                                    'context': context,
                                    'match_count': line.lower().count(search_pattern)
                                })
                except:
                    continue
        
        # Sort by relevance (match count)
        results.sort(key=lambda x: x['match_count'], reverse=True)
        
        return {
            'query': query,
            'total_matches': len(results),
            'results': results[:100]  # Limit to 100 results
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")


@app.get("/dependency-graph/{repo_id}")
async def get_dependency_graph(repo_id: str):
    """
    Generate dependency graph for repository
    """
    repo_path = UPLOAD_DIR / repo_id
    
    if not repo_path.exists():
        raise HTTPException(status_code=404, detail="Repository not found")
    
    try:
        dependencies = {
            'nodes': [],
            'edges': [],
            'stats': {}
        }
        
        # Detect package files
        package_files = {
            'package.json': 'npm',
            'requirements.txt': 'pip',
            'pom.xml': 'maven',
            'build.gradle': 'gradle',
            'Cargo.toml': 'cargo',
            'go.mod': 'go',
            'Gemfile': 'bundler',
            'composer.json': 'composer'
        }
        
        for pkg_file, pkg_manager in package_files.items():
            for file_path in repo_path.rglob(pkg_file):
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        
                        # Parse dependencies based on file type
                        if pkg_file == 'package.json':
                            import json
                            data = json.loads(content)
                            deps = {**data.get('dependencies', {}), **data.get('devDependencies', {})}
                            for dep, version in deps.items():
                                dependencies['nodes'].append({
                                    'id': dep,
                                    'label': dep,
                                    'version': version,
                                    'type': 'npm',
                                    'category': 'dependency'
                                })
                        
                        elif pkg_file == 'requirements.txt':
                            for line in content.split('\n'):
                                line = line.strip()
                                if line and not line.startswith('#'):
                                    parts = line.split('==')
                                    dep = parts[0].strip()
                                    version = parts[1].strip() if len(parts) > 1 else 'latest'
                                    dependencies['nodes'].append({
                                        'id': dep,
                                        'label': dep,
                                        'version': version,
                                        'type': 'pip',
                                        'category': 'dependency'
                                    })
                except:
                    continue
        
        # Add project as root node
        dependencies['nodes'].insert(0, {
            'id': 'project',
            'label': repo_id,
            'type': 'project',
            'category': 'root'
        })
        
        # Create edges from project to dependencies
        for node in dependencies['nodes'][1:]:
            dependencies['edges'].append({
                'from': 'project',
                'to': node['id'],
                'type': 'depends_on'
            })
        
        # Calculate stats
        dependencies['stats'] = {
            'total_dependencies': len(dependencies['nodes']) - 1,
            'npm_packages': len([n for n in dependencies['nodes'] if n.get('type') == 'npm']),
            'pip_packages': len([n for n in dependencies['nodes'] if n.get('type') == 'pip']),
        }
        
        return dependencies
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Dependency graph error: {str(e)}")

    raise HTTPException(status_code=404, detail="README not found in repository")




@app.post("/analyze")
async def analyze_repo(request: AnalyzeRequest):
    """
    Analyze uploaded repository and return comprehensive insights
    """
    repo_path = UPLOAD_DIR / request.repo_id
    
    if not repo_path.exists():
        raise HTTPException(status_code=404, detail="Repository not found")
    
    # Check cache first
    cache_key = cache_manager.generate_cache_key(
        request.repo_id,
        request.skill_level,
        request.goal
    )
    
    cached_result = cache_manager.get_cached_analysis(cache_key)
    if cached_result:
        return cached_result.get('data')
    
    try:
        # Step 1: Analyze repository structure
        analyzer = RepoAnalyzer(str(repo_path))
        analysis_result = analyzer.analyze()
        
        # Step 2: Detect stack (languages and frameworks)
        detector = StackDetector(
            str(repo_path),
            analysis_result['file_tree'],
            analysis_result['config_files']
        )
        stack_info = detector.detect()
        
        # Step 3: Detect concepts
        concept_detector = ConceptDetector(
            analysis_result['source_files'],
            stack_info['primary_language']
        )
        detected_concepts = concept_detector.detect()
        
        # Step 4: Match concepts to official docs with senior explanations
        enriched_concepts = docs_matcher.match_concepts_to_docs(
            detected_concepts,
            request.skill_level
        )
        
        # Step 5: Calculate understanding debt score
        debt_score = debt_calculator.calculate(
            detected_concepts,
            request.skill_level,
            analysis_result['stats']['total_files']
        )
        
        # Step 6: Get relevant documentation (legacy)
        docs_matches = docs_retriever.get_docs_for_concepts(detected_concepts, limit=5)
        
        # Step 7: Generate AI-powered insights (or fallback)
        repo_summary = {
            'detected_stack': stack_info,
            'concepts_detected': detected_concepts,
            'stats': analysis_result['stats']
        }
        
        ai_insights = ai_reasoner.generate_learning_summary(
            repo_summary,
            request.skill_level,
            request.goal
        )
        
        # Step 8: Generate quiz questions
        quiz_questions = ai_reasoner.generate_quiz_questions(
            detected_concepts,
            request.skill_level
        )
        
        # Step 9: Get learning priority
        learning_path = debt_calculator.get_learning_priority(detected_concepts)
        
        # Step 10: Create learning session in local memory
        session_id = local_memory.create_session(
            repo_id=request.repo_id,
            repo_name=str(repo_path.name),
            skill_level=request.skill_level,
            goal=request.goal
        )
        
        # Compile final response
        result = {
            "repo_id": request.repo_id,
            "session_id": session_id,
            "detected_stack": stack_info,
            "file_tree": analysis_result['file_tree'][:100],  # Limit for response size
            "stats": analysis_result['stats'],
            "project_summary": ai_insights['project_summary'],
            "architecture_flow": ai_insights['architecture_flow'],
            "concepts_detected": detected_concepts[:15],  # Top 15 concepts
            "enriched_concepts": enriched_concepts[:10],  # Top 10 with official docs
            "docs_matches": docs_matches,
            "debugging_checklist": ai_insights['debugging_checklist'],
            "learning_path": learning_path[:10],  # Top 10 learning items
            "quiz_questions": quiz_questions,
            "understanding_debt_score": debt_score
        }
        
        # Cache the result
        cache_manager.save_analysis(cache_key, result)
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")


@app.post("/debug")
async def debug_error(request: DebugRequest):
    """
    Provide debugging guidance for an error log
    """
    repo_path = UPLOAD_DIR / request.repo_id
    
    if not repo_path.exists():
        raise HTTPException(status_code=404, detail="Repository not found")
    
    try:
        # Get basic repo info for context
        analyzer = RepoAnalyzer(str(repo_path))
        analysis_result = analyzer.analyze()
        
        detector = StackDetector(
            str(repo_path),
            analysis_result['file_tree'],
            analysis_result['config_files']
        )
        stack_info = detector.detect()
        
        # Analyze error with context
        guidance = debug_coach.analyze_error(
            request.error_log,
            request.skill_level,
            stack_info
        )
        
        return guidance
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Debug analysis error: {str(e)}")


@app.get("/docs/{concept}")
async def get_docs(concept: str):
    """
    Get documentation for a specific concept
    """
    doc = docs_retriever.get_doc_by_concept(concept)
    
    if doc:
        return doc
    else:
        raise HTTPException(status_code=404, detail="Documentation not found for this concept")


@app.get("/docs")
async def list_docs():
    """
    List all available documentation
    """
    return {
        "available_docs": docs_retriever.get_all_available_docs()
    }


@app.get("/cache/stats")
async def get_cache_stats():
    """
    Get cache statistics
    """
    return cache_manager.get_cache_stats()


@app.delete("/cache/{cache_key}")
async def clear_cache(cache_key: str):
    """
    Clear specific cache entry
    """
    success = cache_manager.clear_cache(cache_key)
    if success:
        return {"message": "Cache cleared successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to clear cache")


@app.delete("/repo/{repo_id}")
async def delete_repo(repo_id: str):
    """
    Delete uploaded repository
    """
    repo_path = UPLOAD_DIR / repo_id
    
    if not repo_path.exists():
        raise HTTPException(status_code=404, detail="Repository not found")
    
    try:
        shutil.rmtree(repo_path)
        return {"message": "Repository deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete repository: {str(e)}")


@app.post("/feature-walkthrough")
async def feature_walkthrough(request: FeatureWalkthroughRequest):
    """
    Get end-to-end walkthrough of a feature like a senior engineer would explain
    """
    repo_path = UPLOAD_DIR / request.repo_id
    
    if not repo_path.exists():
        raise HTTPException(status_code=404, detail="Repository not found")
    
    try:
        # Analyze repository
        analyzer = RepoAnalyzer(str(repo_path))
        analysis_result = analyzer.analyze()
        
        detector = StackDetector(
            str(repo_path),
            analysis_result['file_tree'],
            analysis_result['config_files']
        )
        stack_info = detector.detect()
        
        concept_detector = ConceptDetector(
            analysis_result['source_files'],
            stack_info['primary_language']
        )
        detected_concepts = concept_detector.detect()
        
        # Match concepts to official docs with senior explanations
        enriched_concepts = docs_matcher.match_concepts_to_docs(
            detected_concepts,
            request.skill_level
        )
        
        # Generate senior walkthrough
        walkthrough = {
            "feature_name": request.feature_name,
            "skill_level": request.skill_level,
            "stack": stack_info,
            "senior_explanation": f"Let me walk you through how {request.feature_name} works in this {stack_info['primary_language']} {stack_info['primary_framework']} application.",
            "concepts_involved": enriched_concepts[:10],
            "reading_order": [
                {"step": 1, "file": "Entry point (main file)", "why": "Start where the application begins"},
                {"step": 2, "file": "Configuration files", "why": "Understand how the app is configured"},
                {"step": 3, "file": "Core business logic", "why": "See the main functionality"},
                {"step": 4, "file": "Data models/entities", "why": "Understand the data structure"},
                {"step": 5, "file": "API endpoints/routes", "why": "See how external requests are handled"}
            ],
            "common_pitfalls": [
                "Not understanding the data flow",
                "Skipping error handling",
                "Ignoring edge cases",
                "Not reading the documentation"
            ]
        }
        
        return walkthrough
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Feature walkthrough error: {str(e)}")


@app.get("/download-report/{session_id}")
async def download_report(session_id: str):
    """
    Generate and download comprehensive learning pack
    """
    try:
        # Get session data from local memory
        session_data = local_memory.get_session(session_id)
        
        if not session_data:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Generate learning pack
        report_content = report_generator.generate_learning_pack(
            session_id,
            session_data.get('repo_summary', {})
        )
        
        return {
            "session_id": session_id,
            "report": report_content,
            "format": "markdown",
            "filename": f"debugsensei_learning_pack_{session_id[:8]}.md"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Report generation error: {str(e)}")


@app.get("/memory/{session_id}")
async def get_memory(session_id: str):
    """
    Get learning memory for a session
    """
    try:
        session_data = local_memory.get_session(session_id)
        
        if not session_data:
            raise HTTPException(status_code=404, detail="Session not found")
        
        stats = local_memory.get_learning_stats(session_id)
        
        return {
            "session_id": session_id,
            "session_data": session_data,
            "stats": stats
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Memory retrieval error: {str(e)}")


@app.post("/memory/concept-learned")
async def mark_concept_learned(session_id: str, concept_name: str):
    """
    Mark a concept as learned in local memory
    """
    try:
        local_memory.add_concept_learned(session_id, concept_name)
        return {"message": "Concept marked as learned", "concept": concept_name}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update memory: {str(e)}")


@app.get("/official-docs/cache-stats")
async def get_docs_cache_stats():
    """
    Get official docs cache statistics
    """
    try:
        # Access fetcher through docs_matcher
        stats = docs_matcher.fetcher.get_cache_stats()
        return stats
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get cache stats: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Made with Bob
