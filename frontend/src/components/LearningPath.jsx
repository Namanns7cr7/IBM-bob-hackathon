function LearningPath({ path }) {
  if (!path || path.length === 0) return null

  return (
    <div className="card">
      <h2 className="text-2xl font-bold mb-4 text-gray-800 dark:text-white">
        🎓 Your Learning Path
      </h2>
      
      <p className="text-gray-600 dark:text-gray-400 mb-6">
        Follow this personalized path to master the concepts in this codebase.
      </p>

      <div className="space-y-4">
        {path.map((item, idx) => (
          <div
            key={idx}
            className="border-l-4 border-primary-600 bg-gray-50 dark:bg-gray-800 rounded-r-lg p-4 hover:shadow-md transition-shadow"
          >
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center space-x-3 mb-2">
                  <span className="flex-shrink-0 w-8 h-8 bg-primary-600 text-white rounded-full flex items-center justify-center font-bold">
                    {item.step || idx + 1}
                  </span>
                  <h3 className="text-lg font-bold text-gray-800 dark:text-white">
                    {item.name || item.topic}
                  </h3>
                </div>
                <p className="text-gray-700 dark:text-gray-300 ml-11">
                  {item.description}
                </p>
                <div className="flex items-center space-x-3 mt-3 ml-11">
                  {item.category && (
                    <span className="text-xs bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 px-2 py-1 rounded">
                      {item.category}
                    </span>
                  )}
                  {item.priority && (
                    <span className={`text-xs px-2 py-1 rounded font-medium ${
                      item.priority === 'High'
                        ? 'bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200'
                        : item.priority === 'Medium'
                        ? 'bg-yellow-100 dark:bg-yellow-900 text-yellow-800 dark:text-yellow-200'
                        : 'bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200'
                    }`}>
                      {item.priority} Priority
                    </span>
                  )}
                  {item.weight && (
                    <span className="text-xs text-gray-500 dark:text-gray-400">
                      Weight: {item.weight}
                    </span>
                  )}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-6 p-4 bg-blue-50 dark:bg-blue-900 border border-blue-200 dark:border-blue-700 rounded-lg">
        <p className="text-sm text-blue-800 dark:text-blue-200">
          💡 <strong>Pro Tip:</strong> Focus on high-priority concepts first. Build small projects to practice each concept before moving to the next.
        </p>
      </div>
    </div>
  )
}

export default LearningPath

// Made with Bob
