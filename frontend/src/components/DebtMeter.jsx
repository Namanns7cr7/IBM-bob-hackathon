function DebtMeter({ score }) {
  if (!score) return null

  const { score: debtScore, risk_level, risk_color, message, high_risk_concepts } = score

  // Calculate circle progress
  const radius = 70
  const circumference = 2 * Math.PI * radius
  const progress = ((100 - debtScore) / 100) * circumference

  const getColorClasses = () => {
    switch (risk_color) {
      case 'green':
        return {
          bg: 'bg-green-100 dark:bg-green-900',
          border: 'border-green-500',
          text: 'text-green-700 dark:text-green-300',
          stroke: 'stroke-green-500'
        }
      case 'yellow':
        return {
          bg: 'bg-yellow-100 dark:bg-yellow-900',
          border: 'border-yellow-500',
          text: 'text-yellow-700 dark:text-yellow-300',
          stroke: 'stroke-yellow-500'
        }
      case 'red':
        return {
          bg: 'bg-red-100 dark:bg-red-900',
          border: 'border-red-500',
          text: 'text-red-700 dark:text-red-300',
          stroke: 'stroke-red-500'
        }
      default:
        return {
          bg: 'bg-gray-100 dark:bg-gray-900',
          border: 'border-gray-500',
          text: 'text-gray-700 dark:text-gray-300',
          stroke: 'stroke-gray-500'
        }
    }
  }

  const colors = getColorClasses()

  return (
    <div className="space-y-6">
      {/* Debt Score Card */}
      <div className="card">
        <h3 className="text-lg font-bold mb-4 text-gray-800 dark:text-white">
          📊 Understanding Debt
        </h3>

        {/* Circular Progress */}
        <div className="flex flex-col items-center mb-4">
          <div className="relative">
            <svg width="160" height="160" className="transform -rotate-90">
              {/* Background circle */}
              <circle
                cx="80"
                cy="80"
                r={radius}
                className="stroke-gray-200 dark:stroke-gray-700"
                strokeWidth="12"
                fill="none"
              />
              {/* Progress circle */}
              <circle
                cx="80"
                cy="80"
                r={radius}
                className={colors.stroke}
                strokeWidth="12"
                fill="none"
                strokeDasharray={circumference}
                strokeDashoffset={progress}
                strokeLinecap="round"
              />
            </svg>
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <span className="text-4xl font-bold text-gray-800 dark:text-white">
                {Math.round(debtScore)}
              </span>
              <span className="text-xs text-gray-500 dark:text-gray-400">/ 100</span>
            </div>
          </div>

          {/* Risk Level Badge */}
          <div className={`mt-4 px-4 py-2 rounded-full ${colors.bg} border-2 ${colors.border}`}>
            <span className={`font-bold ${colors.text}`}>
              {risk_level} Understanding Debt
            </span>
          </div>
        </div>

        {/* Message */}
        <p className="text-sm text-center text-gray-700 dark:text-gray-300 mb-4">
          {message}
        </p>

        {/* Recommendation */}
        {score.recommendation && (
          <div className="p-3 bg-blue-50 dark:bg-blue-900 border border-blue-200 dark:border-blue-700 rounded-lg">
            <p className="text-xs text-blue-800 dark:text-blue-200">
              💡 {score.recommendation}
            </p>
          </div>
        )}
      </div>

      {/* High Risk Concepts */}
      {high_risk_concepts && high_risk_concepts.length > 0 && (
        <div className="card">
          <h3 className="text-lg font-bold mb-3 text-gray-800 dark:text-white">
            ⚠️ High-Priority Concepts
          </h3>
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
            Focus on these concepts to reduce your understanding debt:
          </p>
          <div className="space-y-3">
            {high_risk_concepts.slice(0, 5).map((concept, idx) => (
              <div
                key={idx}
                className="border border-gray-200 dark:border-gray-700 rounded-lg p-3"
              >
                <div className="flex items-start justify-between mb-2">
                  <h4 className="font-semibold text-gray-800 dark:text-white">
                    {concept.name}
                  </h4>
                  <span className="text-xs bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200 px-2 py-1 rounded font-medium">
                    Weight: {concept.weight}
                  </span>
                </div>
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                  {concept.description}
                </p>
                {concept.files && concept.files.length > 0 && (
                  <div className="text-xs text-gray-500 dark:text-gray-400">
                    Found in: {concept.files.join(', ')}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Stats */}
      {score.concept_breakdown && score.concept_breakdown.length > 0 && (
        <div className="card">
          <h3 className="text-lg font-bold mb-3 text-gray-800 dark:text-white">
            📈 Concept Breakdown
          </h3>
          <div className="space-y-2">
            {score.concept_breakdown.slice(0, 5).map((concept, idx) => (
              <div key={idx} className="flex items-center justify-between text-sm">
                <span className="text-gray-700 dark:text-gray-300">{concept.name}</span>
                <div className="flex items-center space-x-2">
                  <span className="text-gray-500 dark:text-gray-400">
                    {concept.count}x
                  </span>
                  <span className="text-primary-600 dark:text-primary-400 font-medium">
                    +{concept.contribution}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default DebtMeter

// Made with Bob
