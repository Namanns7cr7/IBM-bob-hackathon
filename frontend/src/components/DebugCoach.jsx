import { useState } from 'react'
import { debugError } from '../api'

function DebugCoach({ repoId }) {
  const [errorLog, setErrorLog] = useState('')
  const [skillLevel, setSkillLevel] = useState('intermediate')
  const [guidance, setGuidance] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleDebug = async () => {
    if (!errorLog.trim()) {
      setError('Please paste an error log')
      return
    }

    setLoading(true)
    setError(null)

    try {
      const result = await debugError(repoId, errorLog, skillLevel)
      setGuidance(result)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to analyze error')
      console.error('Debug error:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div className="card">
        <h2 className="text-2xl font-bold mb-4 text-gray-800 dark:text-white">
          🐛 Debugging Coach
        </h2>
        
        <p className="text-gray-600 dark:text-gray-400 mb-4">
          Paste your error log below and get step-by-step debugging guidance.
        </p>

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

        {/* Error Log Input */}
        <div className="mb-4">
          <label className="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">
            Error Log
          </label>
          <textarea
            value={errorLog}
            onChange={(e) => setErrorLog(e.target.value)}
            placeholder="Paste your error message or stack trace here..."
            className="input-field font-mono text-sm"
            rows="8"
            disabled={loading}
          />
        </div>

        {/* Error Message */}
        {error && (
          <div className="mb-4 p-3 bg-red-100 dark:bg-red-900 border border-red-400 dark:border-red-700 text-red-700 dark:text-red-200 rounded-lg text-sm">
            {error}
          </div>
        )}

        {/* Debug Button */}
        <button
          onClick={handleDebug}
          disabled={!errorLog.trim() || loading}
          className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? 'Analyzing...' : '🔍 Debug This Error'}
        </button>
      </div>

      {/* Guidance Results */}
      {guidance && (
        <div className="space-y-4">
          {/* Bug Type */}
          <div className="card">
            <div className="flex items-start space-x-3">
              <span className="text-3xl">🎯</span>
              <div className="flex-1">
                <h3 className="text-xl font-bold text-gray-800 dark:text-white mb-2">
                  {guidance.bug_type}
                </h3>
                <p className="text-gray-700 dark:text-gray-300">
                  {guidance.meaning}
                </p>
              </div>
            </div>
          </div>

          {/* Likely Causes */}
          <div className="card">
            <h3 className="text-lg font-bold mb-3 text-gray-800 dark:text-white">
              🔍 Likely Causes
            </h3>
            <ul className="space-y-2">
              {guidance.likely_causes?.map((cause, idx) => (
                <li key={idx} className="flex items-start space-x-2">
                  <span className="text-primary-600 dark:text-primary-400">•</span>
                  <span className="text-gray-700 dark:text-gray-300">{cause}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Debugging Steps */}
          <div className="card">
            <h3 className="text-lg font-bold mb-3 text-gray-800 dark:text-white">
              📋 Debugging Steps
            </h3>
            <div className="space-y-3">
              {guidance.debugging_steps?.map((step, idx) => (
                <div key={idx} className="flex items-start space-x-3">
                  <span className="flex-shrink-0 w-6 h-6 bg-primary-600 text-white rounded-full flex items-center justify-center text-sm font-bold">
                    {idx + 1}
                  </span>
                  <p className="text-gray-700 dark:text-gray-300 flex-1">{step}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Possible Fix */}
          <div className="card bg-green-50 dark:bg-green-900 border-2 border-green-200 dark:border-green-700">
            <h3 className="text-lg font-bold mb-2 text-green-800 dark:text-green-200">
              ✅ Possible Fix
            </h3>
            <p className="text-green-700 dark:text-green-300">
              {guidance.possible_fix}
            </p>
          </div>

          {/* Prevention */}
          <div className="card">
            <h3 className="text-lg font-bold mb-2 text-gray-800 dark:text-white">
              🛡️ Prevention
            </h3>
            <p className="text-gray-700 dark:text-gray-300">
              {guidance.prevention}
            </p>
          </div>

          {/* Concepts to Learn */}
          {guidance.concepts_to_learn && guidance.concepts_to_learn.length > 0 && (
            <div className="card">
              <h3 className="text-lg font-bold mb-3 text-gray-800 dark:text-white">
                📚 Concepts to Learn
              </h3>
              <div className="flex flex-wrap gap-2">
                {guidance.concepts_to_learn.map((concept, idx) => (
                  <span
                    key={idx}
                    className="bg-purple-100 dark:bg-purple-900 text-purple-800 dark:text-purple-200 px-3 py-1 rounded-lg text-sm font-medium"
                  >
                    {concept}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Mini Quiz */}
          {guidance.mini_quiz && guidance.mini_quiz.length > 0 && (
            <div className="card">
              <h3 className="text-lg font-bold mb-3 text-gray-800 dark:text-white">
                ❓ Quick Quiz
              </h3>
              <div className="space-y-4">
                {guidance.mini_quiz.map((q, idx) => (
                  <div key={idx} className="border border-gray-200 dark:border-gray-700 rounded-lg p-4">
                    <p className="font-semibold text-gray-800 dark:text-white mb-2">
                      Q: {q.question}
                    </p>
                    <details className="text-sm">
                      <summary className="cursor-pointer text-primary-600 dark:text-primary-400 hover:underline">
                        Show Answer
                      </summary>
                      <p className="mt-2 text-gray-700 dark:text-gray-300 pl-4 border-l-2 border-primary-600">
                        {q.answer}
                      </p>
                    </details>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Additional Help */}
          {guidance.additional_help && (
            <div className="card bg-blue-50 dark:bg-blue-900 border border-blue-200 dark:border-blue-700">
              <p className="text-sm text-blue-800 dark:text-blue-200">
                💡 <strong>Tip:</strong> {guidance.additional_help}
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default DebugCoach

// Made with Bob
