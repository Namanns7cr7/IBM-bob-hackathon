import { useState } from 'react'
import { downloadReport } from '../api'

function DownloadPack({ sessionId }) {
  const [downloading, setDownloading] = useState(false)
  const [error, setError] = useState(null)

  const handleDownload = async () => {
    if (!sessionId) {
      setError('No session ID available. Please analyze a repository first.')
      return
    }

    setDownloading(true)
    setError(null)

    try {
      const response = await downloadReport(sessionId)
      
      // Create blob and download
      const blob = new Blob([response.report], { type: 'text/markdown' })
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = response.filename || `debugsensei_learning_pack_${sessionId.slice(0, 8)}.md`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to download learning pack')
    } finally {
      setDownloading(false)
    }
  }

  return (
    <div className="card">
      <div className="flex items-start justify-between mb-4">
        <div>
          <h3 className="text-xl font-bold text-purple-400">📦 Download Learning Pack</h3>
          <p className="text-sm text-gray-400 mt-1">
            Get a comprehensive Markdown report with all your learning progress
          </p>
        </div>
      </div>

      <div className="bg-gradient-to-r from-purple-900/30 to-blue-900/30 rounded-lg p-6 mb-4 border border-purple-500/30">
        <h4 className="font-bold text-white mb-3">📄 What's Included:</h4>
        <ul className="space-y-2 text-sm text-gray-300">
          <li className="flex items-start">
            <span className="text-green-400 mr-2">✓</span>
            <span>Project summary and architecture overview</span>
          </li>
          <li className="flex items-start">
            <span className="text-green-400 mr-2">✓</span>
            <span>Stack detection and technology breakdown</span>
          </li>
          <li className="flex items-start">
            <span className="text-green-400 mr-2">✓</span>
            <span>Senior engineer walkthrough and explanations</span>
          </li>
          <li className="flex items-start">
            <span className="text-green-400 mr-2">✓</span>
            <span>Recommended reading order for files</span>
          </li>
          <li className="flex items-start">
            <span className="text-green-400 mr-2">✓</span>
            <span>All detected concepts with official docs references</span>
          </li>
          <li className="flex items-start">
            <span className="text-green-400 mr-2">✓</span>
            <span>Debugging lessons and common pitfalls</span>
          </li>
          <li className="flex items-start">
            <span className="text-green-400 mr-2">✓</span>
            <span>Your learning progress and quiz scores</span>
          </li>
          <li className="flex items-start">
            <span className="text-green-400 mr-2">✓</span>
            <span>Next steps and recommended learning path</span>
          </li>
        </ul>
      </div>

      <button
        onClick={handleDownload}
        disabled={downloading || !sessionId}
        className={`w-full py-3 px-6 rounded-lg font-semibold transition-all ${
          downloading || !sessionId
            ? 'bg-gray-700 text-gray-400 cursor-not-allowed'
            : 'bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white shadow-lg hover:shadow-xl'
        }`}
      >
        {downloading ? (
          <span className="flex items-center justify-center">
            <svg className="animate-spin h-5 w-5 mr-2" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
            </svg>
            Generating Report...
          </span>
        ) : (
          <span className="flex items-center justify-center">
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Download Learning Pack (.md)
          </span>
        )}
      </button>

      {error && (
        <div className="mt-4 p-3 bg-red-900/30 border border-red-500/50 rounded-lg">
          <p className="text-sm text-red-400">{error}</p>
        </div>
      )}

      {!sessionId && (
        <div className="mt-4 p-3 bg-yellow-900/30 border border-yellow-500/50 rounded-lg">
          <p className="text-sm text-yellow-400">
            ⚠️ Please analyze a repository first to generate a learning pack
          </p>
        </div>
      )}

      <div className="mt-4 p-4 bg-gray-800 rounded-lg border border-gray-700">
        <h4 className="font-semibold text-sm text-gray-300 mb-2">💡 Pro Tip:</h4>
        <p className="text-xs text-gray-400">
          The learning pack is a Markdown file that you can open in any text editor or Markdown viewer. 
          It's perfect for offline learning, sharing with teammates, or keeping as a reference guide.
        </p>
      </div>
    </div>
  )
}

export default DownloadPack

// Made with Bob