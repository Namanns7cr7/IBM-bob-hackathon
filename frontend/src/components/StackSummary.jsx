function StackSummary({ data, stats }) {
  if (!data) return null

  return (
    <div className="card">
      <h3 className="text-lg font-bold mb-3 text-gray-800 dark:text-white">
        🔧 Stack Summary
      </h3>
      
      <div className="space-y-3">
        {/* Primary Stack */}
        <div>
          <p className="text-xs text-gray-500 dark:text-gray-400 mb-1">Primary Language</p>
          <p className="font-semibold text-gray-800 dark:text-white">{data.primary_language || 'Unknown'}</p>
        </div>

        {data.primary_framework && (
          <div>
            <p className="text-xs text-gray-500 dark:text-gray-400 mb-1">Primary Framework</p>
            <p className="font-semibold text-gray-800 dark:text-white">{data.primary_framework}</p>
          </div>
        )}

        {/* Languages */}
        {data.languages && Object.keys(data.languages).length > 0 && (
          <div>
            <p className="text-xs text-gray-500 dark:text-gray-400 mb-2">Languages</p>
            <div className="space-y-1">
              {Object.entries(data.languages).slice(0, 3).map(([lang, info]) => (
                <div key={lang} className="flex items-center justify-between text-sm">
                  <span className="text-gray-700 dark:text-gray-300">{lang}</span>
                  <span className="text-gray-500 dark:text-gray-400">{info.percentage}%</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Frameworks */}
        {data.frameworks && data.frameworks.length > 0 && (
          <div>
            <p className="text-xs text-gray-500 dark:text-gray-400 mb-2">Tools & Frameworks</p>
            <div className="flex flex-wrap gap-2">
              {data.frameworks.slice(0, 4).map((fw, idx) => (
                <span
                  key={idx}
                  className="text-xs bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 px-2 py-1 rounded"
                >
                  {fw.name}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Stats */}
        {stats && (
          <div className="pt-3 border-t border-gray-200 dark:border-gray-700">
            <div className="grid grid-cols-2 gap-2 text-sm">
              <div>
                <p className="text-xs text-gray-500 dark:text-gray-400">Files</p>
                <p className="font-semibold text-gray-800 dark:text-white">{stats.total_files}</p>
              </div>
              <div>
                <p className="text-xs text-gray-500 dark:text-gray-400">Source Files</p>
                <p className="font-semibold text-gray-800 dark:text-white">{stats.source_files}</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default StackSummary

// Made with Bob
