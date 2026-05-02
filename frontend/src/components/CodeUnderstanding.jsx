function CodeUnderstanding({ data }) {
  if (!data) return null

  return (
    <div className="space-y-6">
      {/* Project Summary */}
      <div className="card">
        <h2 className="text-2xl font-bold mb-4 text-gray-800 dark:text-white">
          📖 Your Codebase Explained
        </h2>
        <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
          {data.project_summary}
        </p>
      </div>

      {/* Architecture Flow */}
      {data.architecture_flow && data.architecture_flow.length > 0 && (
        <div className="card">
          <h3 className="text-xl font-bold mb-4 text-gray-800 dark:text-white">
            🏗️ Architecture Flow
          </h3>
          <div className="flex items-center justify-center flex-wrap gap-3">
            {data.architecture_flow.map((step, idx) => (
              <div key={idx} className="flex items-center">
                <div className="bg-primary-100 dark:bg-primary-900 text-primary-800 dark:text-primary-200 px-4 py-2 rounded-lg font-medium">
                  {step}
                </div>
                {idx < data.architecture_flow.length - 1 && (
                  <span className="mx-2 text-2xl text-gray-400">→</span>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Debugging Checklist */}
      {data.debugging_checklist && data.debugging_checklist.length > 0 && (
        <div className="card">
          <h3 className="text-xl font-bold mb-4 text-gray-800 dark:text-white">
            🐛 Debugging Checklist
          </h3>
          <div className="space-y-2">
            {data.debugging_checklist.map((step, idx) => (
              <div key={idx} className="flex items-start space-x-3">
                <span className="flex-shrink-0 w-6 h-6 bg-primary-600 text-white rounded-full flex items-center justify-center text-sm font-bold">
                  {idx + 1}
                </span>
                <p className="text-gray-700 dark:text-gray-300 flex-1">{step}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default CodeUnderstanding

// Made with Bob
