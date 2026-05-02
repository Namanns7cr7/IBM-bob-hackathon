import { useState } from 'react'

function QuizPanel({ questions }) {
  const [showAnswers, setShowAnswers] = useState({})

  if (!questions || questions.length === 0) {
    return (
      <div className="card text-center py-10">
        <div className="text-6xl mb-4">❓</div>
        <p className="text-gray-600 dark:text-gray-400">
          No quiz questions available yet. Analyze a codebase first!
        </p>
      </div>
    )
  }

  const toggleAnswer = (idx) => {
    setShowAnswers(prev => ({
      ...prev,
      [idx]: !prev[idx]
    }))
  }

  return (
    <div className="card">
      <h2 className="text-2xl font-bold mb-4 text-gray-800 dark:text-white">
        ❓ Test Your Understanding
      </h2>
      
      <p className="text-gray-600 dark:text-gray-400 mb-6">
        Answer these questions to reinforce your learning.
      </p>

      <div className="space-y-4">
        {questions.map((q, idx) => (
          <div
            key={idx}
            className="border border-gray-200 dark:border-gray-700 rounded-lg p-4 hover:shadow-md transition-shadow"
          >
            <div className="flex items-start space-x-3 mb-3">
              <span className="flex-shrink-0 w-8 h-8 bg-purple-600 text-white rounded-full flex items-center justify-center font-bold text-sm">
                {idx + 1}
              </span>
              <p className="font-semibold text-gray-800 dark:text-white flex-1">
                {q.question}
              </p>
            </div>

            <button
              onClick={() => toggleAnswer(idx)}
              className="ml-11 text-sm text-primary-600 dark:text-primary-400 hover:underline font-medium"
            >
              {showAnswers[idx] ? '▲ Hide Answer' : '▼ Show Answer'}
            </button>

            {showAnswers[idx] && (
              <div className="ml-11 mt-3 p-3 bg-green-50 dark:bg-green-900 border-l-4 border-green-500 rounded">
                <p className="text-sm text-green-800 dark:text-green-200">
                  <strong>Answer:</strong> {q.answer}
                </p>
              </div>
            )}
          </div>
        ))}
      </div>

      <div className="mt-6 p-4 bg-purple-50 dark:bg-purple-900 border border-purple-200 dark:border-purple-700 rounded-lg">
        <p className="text-sm text-purple-800 dark:text-purple-200">
          💡 <strong>Learning Tip:</strong> Try to answer each question before revealing the answer. This helps reinforce your understanding.
        </p>
      </div>
    </div>
  )
}

export default QuizPanel

// Made with Bob
