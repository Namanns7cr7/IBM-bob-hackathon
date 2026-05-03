import { useState, useEffect } from 'react'
import ReactMarkdown from 'react-markdown'

function ReadmePreview({ repoId, githubInfo }) {
  const [readme, setReadme] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    if (repoId) {
      fetchReadme()
    }
  }, [repoId])

  const fetchReadme = async () => {
    try {
      setLoading(true)
      const response = await fetch(`http://localhost:8000/readme/${repoId}`)
      if (response.ok) {
        const data = await response.json()
        setReadme(data.content)
      } else {
        setError('README not found')
      }
    } catch (err) {
      setError('Failed to load README')
      console.error('README fetch error:', err)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="card">
        <div className="flex items-center gap-3">
          <div className="animate-spin h-5 w-5 border-2 border-primary-600 border-t-transparent rounded-full"></div>
          <p className="text-gray-600 dark:text-gray-400">Loading README...</p>
        </div>
      </div>
    )
  }

  if (error || !readme) {
    return (
      <div className="card bg-gray-50 dark:bg-gray-800">
        <p className="text-gray-500 dark:text-gray-400 text-center">
          📄 No README found in this repository
        </p>
      </div>
    )
  }

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-bold text-gray-800 dark:text-white flex items-center gap-2">
          📄 README
          {githubInfo && (
            <span className="text-sm font-normal text-gray-500 dark:text-gray-400">
              {githubInfo.full_name}
            </span>
          )}
        </h2>
        <a
          href={`https://github.com/${githubInfo?.full_name}`}
          target="_blank"
          rel="noopener noreferrer"
          className="text-sm text-primary-600 hover:text-primary-700 dark:text-primary-400 flex items-center gap-1"
        >
          View on GitHub
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
          </svg>
        </a>
      </div>
      
      <div className="prose prose-sm dark:prose-invert max-w-none">
        <ReactMarkdown
          components={{
            h1: ({node, ...props}) => <h1 className="text-2xl font-bold mt-6 mb-4 text-gray-900 dark:text-white" {...props} />,
            h2: ({node, ...props}) => <h2 className="text-xl font-bold mt-5 mb-3 text-gray-800 dark:text-gray-100" {...props} />,
            h3: ({node, ...props}) => <h3 className="text-lg font-semibold mt-4 mb-2 text-gray-800 dark:text-gray-100" {...props} />,
            p: ({node, ...props}) => <p className="mb-3 text-gray-700 dark:text-gray-300 leading-relaxed" {...props} />,
            code: ({node, inline, ...props}) => 
              inline ? (
                <code className="px-1.5 py-0.5 bg-gray-100 dark:bg-gray-800 text-primary-600 dark:text-primary-400 rounded text-sm font-mono" {...props} />
              ) : (
                <code className="block p-4 bg-gray-100 dark:bg-gray-800 rounded-lg overflow-x-auto text-sm font-mono" {...props} />
              ),
            pre: ({node, ...props}) => <pre className="mb-4 overflow-x-auto" {...props} />,
            a: ({node, ...props}) => <a className="text-primary-600 hover:text-primary-700 dark:text-primary-400 underline" target="_blank" rel="noopener noreferrer" {...props} />,
            ul: ({node, ...props}) => <ul className="list-disc list-inside mb-3 space-y-1 text-gray-700 dark:text-gray-300" {...props} />,
            ol: ({node, ...props}) => <ol className="list-decimal list-inside mb-3 space-y-1 text-gray-700 dark:text-gray-300" {...props} />,
            blockquote: ({node, ...props}) => <blockquote className="border-l-4 border-primary-500 pl-4 italic text-gray-600 dark:text-gray-400 my-4" {...props} />,
          }}
        >
          {readme}
        </ReactMarkdown>
      </div>
    </div>
  )
}

export default ReadmePreview

// Made with Bob
