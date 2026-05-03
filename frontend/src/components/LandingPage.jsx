import { useState } from 'react'
import { uploadRepo, analyzeRepo, analyzeGitHubUrl } from '../api'

function LandingPage({ onAnalysisComplete }) {
  const [uploadMode, setUploadMode] = useState('github') // 'github' or 'zip'
  const [githubUrl, setGithubUrl] = useState('')
  const [file, setFile] = useState(null)
  const [skillLevel, setSkillLevel] = useState('intermediate')
  const [goal, setGoal] = useState('learn')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [progress, setProgress] = useState('')

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0]
    if (selectedFile && selectedFile.name.endsWith('.zip')) {
      setFile(selectedFile)
      setError(null)
    } else {
      setError('Please select a ZIP file')
      setFile(null)
    }
  }

  const handleAnalyze = async () => {
    if (uploadMode === 'github' && !githubUrl.trim()) {
      setError('Please enter a GitHub URL')
      return
    }

    if (uploadMode === 'zip' && !file) {
      setError('Please select a ZIP file')
      return
    }

    // Validate GitHub URL
    if (uploadMode === 'github' && !githubUrl.includes('github.com')) {
      setError('Please enter a valid GitHub repository URL')
      return
    }

    setLoading(true)
    setError(null)
    setProgress(uploadMode === 'github' ? 'Cloning repository...' : 'Uploading ZIP file...')

    try {
      if (uploadMode === 'github') {
        setTimeout(() => setProgress('Analyzing codebase structure...'), 1000)
        setTimeout(() => setProgress('Detecting technologies and frameworks...'), 2000)
        setTimeout(() => setProgress('Extracting README and documentation...'), 3000)
        setTimeout(() => setProgress('Building dependency graph...'), 4000)
        
        const analysisData = await analyzeGitHubUrl(githubUrl, skillLevel, goal)
        
        setProgress('Analysis complete!')
        onAnalysisComplete(analysisData, analysisData.repo_id)
      } else {
        // ZIP upload flow
        setProgress('Uploading file...')
        const uploadResponse = await uploadRepo(file)
        const repoId = uploadResponse.repo_id

        setProgress('Analyzing codebase...')
        const analysisData = await analyzeRepo(repoId, skillLevel, goal)
        
        setProgress('Analysis complete!')
        onAnalysisComplete(analysisData, repoId)
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Analysis failed. Please try again.')
      console.error('Analysis error:', err)
      setProgress('')
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !loading) {
      handleAnalyze()
    }
  }

  const exampleRepos = [
    { name: 'React', url: 'https://github.com/facebook/react' },
    { name: 'Vue.js', url: 'https://github.com/vuejs/vue' },
    { name: 'FastAPI', url: 'https://github.com/tiangolo/fastapi' },
    { name: 'Flask', url: 'https://github.com/pallets/flask' },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-secondary-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 flex items-center justify-center p-4">
      <div className="max-w-4xl w-full">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <h1 className="text-5xl md:text-6xl font-bold mb-4 bg-gradient-to-r from-primary-600 to-secondary-600 bg-clip-text text-transparent">
            DebugSensei
          </h1>
          <p className="text-xl md:text-2xl text-gray-600 dark:text-gray-300 mb-2">
            Understand Any Codebase in Seconds
          </p>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            Paste a GitHub URL or upload a ZIP file for instant insights
          </p>
        </div>

        {/* Main Input Card */}
        <div className="card shadow-2xl mb-8">
          {/* Upload Mode Toggle */}
          <div className="flex gap-2 mb-6">
            <button
              onClick={() => setUploadMode('github')}
              className={`flex-1 py-3 px-4 rounded-lg font-medium transition-all ${
                uploadMode === 'github'
                  ? 'bg-gradient-to-r from-primary-600 to-secondary-600 text-white shadow-lg'
                  : 'bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300'
              }`}
              disabled={loading}
            >
              🔗 GitHub URL
            </button>
            <button
              onClick={() => setUploadMode('zip')}
              className={`flex-1 py-3 px-4 rounded-lg font-medium transition-all ${
                uploadMode === 'zip'
                  ? 'bg-gradient-to-r from-primary-600 to-secondary-600 text-white shadow-lg'
                  : 'bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300'
              }`}
              disabled={loading}
            >
              📁 Upload ZIP
            </button>
          </div>

          {/* GitHub URL Input */}
          {uploadMode === 'github' && (
            <div className="mb-4">
              <input
                type="text"
                value={githubUrl}
                onChange={(e) => setGithubUrl(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="https://github.com/username/repository"
                className="w-full px-6 py-4 text-lg border-2 border-gray-300 dark:border-gray-600 rounded-lg focus:border-primary-500 focus:ring-2 focus:ring-primary-200 dark:bg-gray-800 dark:text-white transition-all"
                disabled={loading}
              />
            </div>
          )}

          {/* ZIP File Upload */}
          {uploadMode === 'zip' && (
            <div className="mb-4">
              <input
                type="file"
                accept=".zip"
                onChange={handleFileChange}
                className="w-full text-sm text-gray-500 file:mr-4 file:py-3 file:px-6 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-primary-50 file:text-primary-700 hover:file:bg-primary-100 dark:file:bg-primary-900 dark:file:text-primary-300"
                disabled={loading}
              />
              {file && (
                <p className="text-xs text-green-600 dark:text-green-400 mt-2">
                  ✓ {file.name}
                </p>
              )}
            </div>
          )}

          {/* Skill Level & Goal */}
          <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
              <label className="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">
                Skill Level
              </label>
              <select
                value={skillLevel}
                onChange={(e) => setSkillLevel(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-800 dark:text-white"
                disabled={loading}
              >
                <option value="beginner">Beginner</option>
                <option value="intermediate">Intermediate</option>
                <option value="advanced">Advanced</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">
                Goal
              </label>
              <select
                value={goal}
                onChange={(e) => setGoal(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-800 dark:text-white"
                disabled={loading}
              >
                <option value="learn">Learn Codebase</option>
                <option value="debug">Debug Error</option>
                <option value="interview_ready">Interview Ready</option>
                <option value="production_ready">Production Ready</option>
              </select>
            </div>
          </div>

          {/* Analyze Button */}
          <button
            onClick={handleAnalyze}
            disabled={loading || (uploadMode === 'github' && !githubUrl.trim()) || (uploadMode === 'zip' && !file)}
            className="w-full px-8 py-4 bg-gradient-to-r from-primary-600 to-secondary-600 text-white font-semibold rounded-lg hover:from-primary-700 hover:to-secondary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all transform hover:scale-105 active:scale-95 shadow-lg"
          >
            {loading ? (
              <span className="flex items-center justify-center gap-2">
                <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                Analyzing...
              </span>
            ) : (
              '🔍 Analyze Codebase'
            )}
          </button>

          {/* Progress Indicator */}
          {loading && progress && (
            <div className="mt-4 p-4 bg-primary-50 dark:bg-primary-900 rounded-lg">
              <div className="flex items-center gap-3">
                <div className="animate-pulse h-2 w-2 bg-primary-600 rounded-full"></div>
                <p className="text-sm text-primary-700 dark:text-primary-300 font-medium">
                  {progress}
                </p>
              </div>
              <div className="mt-2 w-full bg-gray-200 dark:bg-gray-700 rounded-full h-1.5">
                <div className="bg-gradient-to-r from-primary-600 to-secondary-600 h-1.5 rounded-full animate-progress"></div>
              </div>
            </div>
          )}

          {/* Error Message */}
          {error && (
            <div className="mt-4 p-4 bg-red-50 dark:bg-red-900 border border-red-200 dark:border-red-700 rounded-lg">
              <p className="text-sm text-red-700 dark:text-red-200">
                ⚠️ {error}
              </p>
            </div>
          )}
        </div>

        {/* Example Repositories (only for GitHub mode) */}
        {uploadMode === 'github' && (
          <div className="text-center">
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
              Try these popular repositories:
            </p>
            <div className="flex flex-wrap justify-center gap-2">
              {exampleRepos.map((repo) => (
                <button
                  key={repo.url}
                  onClick={() => setGithubUrl(repo.url)}
                  disabled={loading}
                  className="px-4 py-2 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg text-sm text-gray-700 dark:text-gray-300 hover:border-primary-500 hover:text-primary-600 dark:hover:text-primary-400 transition-all disabled:opacity-50"
                >
                  {repo.name}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12">
          <div className="text-center p-6 bg-white dark:bg-gray-800 rounded-lg shadow-md">
            <div className="text-4xl mb-3">🎯</div>
            <h3 className="font-semibold text-gray-800 dark:text-white mb-2">Instant Analysis</h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Get comprehensive codebase insights in seconds
            </p>
          </div>
          <div className="text-center p-6 bg-white dark:bg-gray-800 rounded-lg shadow-md">
            <div className="text-4xl mb-3">📚</div>
            <h3 className="font-semibold text-gray-800 dark:text-white mb-2">Official Docs</h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Learn from official documentation sources
            </p>
          </div>
          <div className="text-center p-6 bg-white dark:bg-gray-800 rounded-lg shadow-md">
            <div className="text-4xl mb-3">🗺️</div>
            <h3 className="font-semibold text-gray-800 dark:text-white mb-2">Visual Maps</h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Explore file trees and dependency graphs
            </p>
          </div>
        </div>
      </div>

      <style jsx>{`
        @keyframes progress {
          0% { width: 0%; }
          100% { width: 100%; }
        }
        .animate-progress {
          animation: progress 5s ease-in-out infinite;
        }
      `}</style>
    </div>
  )
}

export default LandingPage

// Made with Bob
