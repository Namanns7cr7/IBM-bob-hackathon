import { useState } from 'react'

function CodeSearch({ repoId }) {
  const [query, setQuery] = useState('')
  const [filePattern, setFilePattern] = useState('*')
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [selectedResult, setSelectedResult] = useState(null)

  const handleSearch = async () => {
    if (!query.trim()) {
      setError('Please enter a search query')
      return
    }

    setLoading(true)
    setError(null)

    try {
      const response = await fetch(
        `http://localhost:8000/search-code/${repoId}?query=${encodeURIComponent(query)}&file_pattern=${filePattern}`
      )
      
      if (!response.ok) {
        throw new Error('Search failed')
      }

      const data = await response.json()
      setResults(data)
    } catch (err) {
      setError('Search failed. Please try again.')
      console.error('Search error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !loading) {
      handleSearch()
    }
  }

  const filePatterns = [
    { value: '*', label: 'All Files' },
    { value: '*.js', label: 'JavaScript' },
    { value: '*.jsx', label: 'React' },
    { value: '*.ts', label: 'TypeScript' },
    { value: '*.tsx', label: 'TypeScript React' },
    { value: '*.py', label: 'Python' },
    { value: '*.java', label: 'Java' },
    { value: '*.cpp', label: 'C++' },
    { value: '*.go', label: 'Go' },
  ]

  return (
    <div className="card">
      <h2 className="text-xl font-bold mb-4 text-gray-800 dark:text-white">
        🔍 Code Search
      </h2>

      {/* Search Input */}
      <div className="space-y-4 mb-6">
        <div className="flex gap-3">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Search for functions, variables, patterns..."
            className="flex-1 px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:border-primary-500 focus:ring-2 focus:ring-primary-200 dark:bg-gray-800 dark:text-white"
            disabled={loading}
          />
          <button
            onClick={handleSearch}
            disabled={loading || !query.trim()}
            className="px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-medium"
          >
            {loading ? 'Searching...' : 'Search'}
          </button>
        </div>

        <div className="flex items-center gap-3">
          <label className="text-sm text-gray-600 dark:text-gray-400">
            File Type:
          </label>
          <select
            value={filePattern}
            onChange={(e) => setFilePattern(e.target.value)}
            className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-sm dark:bg-gray-800 dark:text-white"
            disabled={loading}
          >
            {filePatterns.map((pattern) => (
              <option key={pattern.value} value={pattern.value}>
                {pattern.label}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Error */}
      {error && (
        <div className="mb-4 p-3 bg-red-50 dark:bg-red-900 border border-red-200 dark:border-red-700 rounded-lg text-sm text-red-700 dark:text-red-200">
          {error}
        </div>
      )}

      {/* Results */}
      {results && (
        <div>
          <div className="mb-4 p-3 bg-blue-50 dark:bg-blue-900 rounded-lg">
            <p className="text-sm text-blue-800 dark:text-blue-200">
              Found <strong>{results.total_matches}</strong> matches for "<strong>{results.query}</strong>"
            </p>
          </div>

          <div className="space-y-2 max-h-96 overflow-y-auto">
            {results.results.map((result, index) => (
              <div
                key={index}
                className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 hover:border-primary-500 dark:hover:border-primary-500 transition-colors cursor-pointer"
                onClick={() => setSelectedResult(selectedResult === index ? null : index)}
              >
                <div className="flex items-start justify-between mb-2">
                  <div className="flex-1">
                    <p className="text-sm font-mono text-primary-600 dark:text-primary-400">
                      {result.file}
                    </p>
                    <p className="text-xs text-gray-500 dark:text-gray-400">
                      Line {result.line} • {result.match_count} {result.match_count === 1 ? 'match' : 'matches'}
                    </p>
                  </div>
                  <button className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200">
                    {selectedResult === index ? '▼' : '▶'}
                  </button>
                </div>

                <div className="font-mono text-sm bg-white dark:bg-gray-900 p-2 rounded border border-gray-200 dark:border-gray-700">
                  <code className="text-gray-800 dark:text-gray-200">
                    {result.content}
                  </code>
                </div>

                {/* Context */}
                {selectedResult === index && (
                  <div className="mt-3 pt-3 border-t border-gray-200 dark:border-gray-700">
                    <p className="text-xs text-gray-500 dark:text-gray-400 mb-2">Context:</p>
                    <pre className="font-mono text-xs bg-white dark:bg-gray-900 p-3 rounded border border-gray-200 dark:border-gray-700 overflow-x-auto">
                      <code className="text-gray-700 dark:text-gray-300">{result.context}</code>
                    </pre>
                  </div>
                )}
              </div>
            ))}
          </div>

          {results.results.length === 0 && (
            <div className="text-center py-8 text-gray-500 dark:text-gray-400">
              No matches found. Try a different search term.
            </div>
          )}
        </div>
      )}

      {/* Tips */}
      {!results && !loading && (
        <div className="mt-6 p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
          <p className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
            💡 Search Tips:
          </p>
          <ul className="text-sm text-gray-600 dark:text-gray-400 space-y-1">
            <li>• Search for function names, class names, or variables</li>
            <li>• Use file type filters to narrow results</li>
            <li>• Click on results to see context</li>
            <li>• Search is case-insensitive</li>
          </ul>
        </div>
      )}
    </div>
  )
}

export default CodeSearch

// Made with Bob
