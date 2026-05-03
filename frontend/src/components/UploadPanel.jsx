import { useState } from 'react'
import { uploadRepo, analyzeRepo, analyzeGitHubUrl } from '../api'

function UploadPanel({ onAnalysisComplete, loading, setLoading }) {
  const [file, setFile] = useState(null)
  const [githubUrl, setGithubUrl] = useState('')
  const [uploadMode, setUploadMode] = useState('file') // 'file' or 'github'
  const [skillLevel, setSkillLevel] = useState('intermediate')
  const [goal, setGoal] = useState('learn')
  const [error, setError] = useState(null)

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
    if (uploadMode === 'file' && !file) {
      setError('Please select a file first')
      return
    }
    
    if (uploadMode === 'github' && !githubUrl) {
      setError('Please enter a GitHub URL')
      return
    }

    setLoading(true)
    setError(null)

    try {
      if (uploadMode === 'github') {
        // Analyze GitHub URL directly
        const analysisData = await analyzeGitHubUrl(githubUrl, skillLevel, goal)
        onAnalysisComplete(analysisData, analysisData.repo_id)
      } else {
        // Step 1: Upload repo
        const uploadResponse = await uploadRepo(file)
        const repoId = uploadResponse.repo_id

        // Step 2: Analyze repo
        const analysisData = await analyzeRepo(repoId, skillLevel, goal)
        
        onAnalysisComplete(analysisData, repoId)
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Analysis failed. Please try again.')
      console.error('Analysis error:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="card">
      <h2 className="text-xl font-bold mb-4 text-gray-800 dark:text-white">
        📤 Upload Codebase
      </h2>

      {/* Upload Mode Toggle */}
      <div className="mb-4 flex gap-2">
        <button
          onClick={() => setUploadMode('file')}
          className={`flex-1 py-2 px-4 rounded-lg text-sm font-medium transition-colors ${
            uploadMode === 'file'
              ? 'bg-primary-600 text-white'
              : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
          }`}
          disabled={loading}
        >
          📁 Upload ZIP
        </button>
        <button
          onClick={() => setUploadMode('github')}
          className={`flex-1 py-2 px-4 rounded-lg text-sm font-medium transition-colors ${
            uploadMode === 'github'
              ? 'bg-primary-600 text-white'
              : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
          }`}
          disabled={loading}
        >
          🔗 GitHub URL
        </button>
      </div>

      {/* File Upload */}
      {uploadMode === 'file' && (
        <div className="mb-4">
          <label className="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">
            ZIP File
          </label>
          <input
            type="file"
            accept=".zip"
            onChange={handleFileChange}
            className="w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-primary-50 file:text-primary-700 hover:file:bg-primary-100 dark:file:bg-primary-900 dark:file:text-primary-300"
            disabled={loading}
          />
          {file && (
            <p className="text-xs text-green-600 dark:text-green-400 mt-1">
              ✓ {file.name}
            </p>
          )}
        </div>
      )}

      {/* GitHub URL Input */}
      {uploadMode === 'github' && (
        <div className="mb-4">
          <label className="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">
            GitHub Repository URL
          </label>
          <input
            type="text"
            value={githubUrl}
            onChange={(e) => setGithubUrl(e.target.value)}
            placeholder="https://github.com/username/repo"
            className="input-field"
            disabled={loading}
          />
          <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
            Example: https://github.com/facebook/react
          </p>
        </div>
      )}

      {/* Skill Level */}
      <div className="mb-4">
        <label className="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">
          Your Skill Level
        </label>
        <select
          value={skillLevel}
          onChange={(e) => setSkillLevel(e.target.value)}
          className="input-field"
          disabled={loading}
        >
          <option value="beginner">Beginner</option>
          <option value="intermediate">Intermediate</option>
          <option value="advanced">Advanced</option>
        </select>
      </div>

      {/* Goal */}
      <div className="mb-4">
        <label className="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">
          Your Goal
        </label>
        <select
          value={goal}
          onChange={(e) => setGoal(e.target.value)}
          className="input-field"
          disabled={loading}
        >
          <option value="learn">Learn Codebase</option>
          <option value="debug">Debug Error</option>
          <option value="interview_ready">Interview Ready</option>
          <option value="production_ready">Production Ready</option>
        </select>
      </div>

      {/* Error Message */}
      {error && (
        <div className="mb-4 p-3 bg-red-100 dark:bg-red-900 border border-red-400 dark:border-red-700 text-red-700 dark:text-red-200 rounded-lg text-sm">
          {error}
        </div>
      )}

      {/* Analyze Button */}
      <button
        onClick={handleAnalyze}
        disabled={(uploadMode === 'file' && !file) || (uploadMode === 'github' && !githubUrl) || loading}
        className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {loading ? (
          <span className="flex items-center justify-center">
            <svg className="animate-spin h-5 w-5 mr-2" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
            </svg>
            Analyzing...
          </span>
        ) : (
          '🔍 Analyze Codebase'
        )}
      </button>

      {/* Info */}
      <div className="mt-4 p-3 bg-blue-50 dark:bg-blue-900 border border-blue-200 dark:border-blue-700 rounded-lg">
        <p className="text-xs text-blue-800 dark:text-blue-200">
          💡 <strong>Tip:</strong> {uploadMode === 'file'
            ? 'Upload a ZIP file of your project.'
            : 'Paste any public GitHub repository URL.'} We'll analyze the structure, detect concepts, and create a personalized learning path.
        </p>
      </div>
    </div>
  )
}

export default UploadPanel

// Made with Bob
