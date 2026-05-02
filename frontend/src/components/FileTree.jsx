import { useState } from 'react'

function FileTree({ files }) {
  const [expanded, setExpanded] = useState(false)

  if (!files || files.length === 0) return null

  const displayFiles = expanded ? files : files.slice(0, 20)

  return (
    <div className="card">
      <h2 className="text-xl font-bold mb-4 text-gray-800 dark:text-white">
        📁 File Structure
      </h2>
      
      <div className="bg-gray-50 dark:bg-gray-900 rounded-lg p-4 max-h-96 overflow-y-auto">
        <div className="font-mono text-sm space-y-1">
          {displayFiles.map((file, idx) => (
            <div
              key={idx}
              className="flex items-center text-gray-700 dark:text-gray-300"
              style={{ paddingLeft: `${file.level * 20}px` }}
            >
              <span className="mr-2">
                {file.type === 'directory' ? '📁' : '📄'}
              </span>
              <span className={file.type === 'directory' ? 'font-semibold' : ''}>
                {file.name}
              </span>
            </div>
          ))}
        </div>
      </div>

      {files.length > 20 && (
        <button
          onClick={() => setExpanded(!expanded)}
          className="mt-3 text-sm text-primary-600 dark:text-primary-400 hover:underline"
        >
          {expanded ? '▲ Show Less' : `▼ Show All (${files.length} files)`}
        </button>
      )}
    </div>
  )
}

export default FileTree

// Made with Bob
