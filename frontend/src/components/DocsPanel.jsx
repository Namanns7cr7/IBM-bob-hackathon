import { useState } from 'react'

function DocsPanel({ docs }) {
  const [expandedDoc, setExpandedDoc] = useState(null)

  if (!docs || docs.length === 0) {
    return (
      <div className="card text-center py-10">
        <div className="text-6xl mb-4">📚</div>
        <p className="text-gray-600 dark:text-gray-400">
          No documentation available yet. Analyze a codebase first!
        </p>
      </div>
    )
  }

  const toggleDoc = (idx) => {
    setExpandedDoc(expandedDoc === idx ? null : idx)
  }

  return (
    <div className="card">
      <h2 className="text-2xl font-bold mb-4 text-gray-800 dark:text-white">
        📚 Relevant Documentation
      </h2>
      
      <p className="text-gray-600 dark:text-gray-400 mb-6">
        Learn more about the concepts used in this codebase.
      </p>

      <div className="space-y-3">
        {docs.map((doc, idx) => (
          <div
            key={idx}
            className="border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden"
          >
            <button
              onClick={() => toggleDoc(idx)}
              className="w-full p-4 text-left hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
            >
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  <h3 className="font-semibold text-gray-800 dark:text-white mb-1">
                    {doc.concept}
                  </h3>
                  <div className="flex items-center space-x-2 text-xs">
                    <span className="bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 px-2 py-1 rounded">
                      {doc.category || 'General'}
                    </span>
                    <span className="text-gray-500 dark:text-gray-400">
                      {doc.file}
                    </span>
                  </div>
                </div>
                <span className="text-gray-400 text-xl">
                  {expandedDoc === idx ? '▲' : '▼'}
                </span>
              </div>
            </button>

            {expandedDoc === idx && (
              <div className="p-4 bg-gray-50 dark:bg-gray-900 border-t border-gray-200 dark:border-gray-700">
                <div className="prose dark:prose-invert max-w-none">
                  <pre className="whitespace-pre-wrap text-sm text-gray-700 dark:text-gray-300 font-sans">
                    {doc.content}
                  </pre>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>

      <div className="mt-6 p-4 bg-blue-50 dark:bg-blue-900 border border-blue-200 dark:border-blue-700 rounded-lg">
        <p className="text-sm text-blue-800 dark:text-blue-200">
          💡 <strong>Tip:</strong> Click on any concept to expand and read the documentation. These docs are curated to match the concepts found in your codebase.
        </p>
      </div>
    </div>
  )
}

export default DocsPanel

// Made with Bob
