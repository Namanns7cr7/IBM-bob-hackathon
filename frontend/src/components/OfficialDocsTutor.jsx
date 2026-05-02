import { useState } from 'react'

function OfficialDocsTutor({ enrichedConcepts, skillLevel }) {
  const [selectedConcept, setSelectedConcept] = useState(null)

  if (!enrichedConcepts || enrichedConcepts.length === 0) {
    return (
      <div className="card">
        <h2 className="text-2xl font-bold mb-4">📚 Official Docs Tutor</h2>
        <p className="text-gray-400">No concepts with official documentation available yet.</p>
      </div>
    )
  }

  const concept = selectedConcept || enrichedConcepts[0]

  return (
    <div className="space-y-6">
      {/* Concept Selector */}
      <div className="card">
        <h2 className="text-2xl font-bold mb-4">📚 Official Docs Tutor</h2>
        <p className="text-gray-400 mb-4">
          Learn from official documentation with senior engineer explanations
        </p>
        
        <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
          {enrichedConcepts.map((c, idx) => (
            <button
              key={idx}
              onClick={() => setSelectedConcept(c)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                concept.concept === c.concept
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
              }`}
            >
              {c.concept}
            </button>
          ))}
        </div>
      </div>

      {/* Concept Details */}
      <div className="card">
        <div className="flex items-start justify-between mb-4">
          <div>
            <h3 className="text-2xl font-bold text-blue-400">{concept.concept}</h3>
            <p className="text-sm text-gray-400 mt-1">
              Category: {concept.category} • Used {concept.usage_count} times
            </p>
          </div>
          <span className="px-3 py-1 bg-purple-600 rounded-full text-xs font-semibold">
            Weight: {concept.weight}
          </span>
        </div>

        {/* Official Source */}
        <div className="bg-gray-800 rounded-lg p-4 mb-4 border border-gray-700">
          <div className="flex items-center justify-between mb-2">
            <h4 className="font-bold text-green-400">📖 Official Source</h4>
            <a
              href={concept.official_source_url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-sm text-blue-400 hover:text-blue-300 underline"
            >
              {concept.official_source_name} →
            </a>
          </div>
          <p className="text-sm text-gray-300">{concept.official_docs_summary}</p>
        </div>

        {/* Senior Explanation */}
        <div className="bg-gradient-to-r from-purple-900/30 to-blue-900/30 rounded-lg p-4 mb-4 border border-purple-500/30">
          <h4 className="font-bold text-purple-400 mb-2">🎓 How a Senior Would Explain It</h4>
          <p className="text-gray-300 leading-relaxed">{concept.senior_explanation}</p>
        </div>

        {/* Why It Matters */}
        <div className="bg-gray-800 rounded-lg p-4 mb-4">
          <h4 className="font-bold text-yellow-400 mb-2">💡 Why It Matters in This Codebase</h4>
          <p className="text-gray-300">{concept.why_it_matters}</p>
        </div>

        {/* Where Used */}
        {concept.where_used && concept.where_used.length > 0 && (
          <div className="bg-gray-800 rounded-lg p-4 mb-4">
            <h4 className="font-bold text-blue-400 mb-2">📍 Where It's Used</h4>
            <ul className="space-y-1">
              {concept.where_used.slice(0, 5).map((file, idx) => (
                <li key={idx} className="text-sm text-gray-400 font-mono">
                  • {file}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Common Mistakes */}
        {concept.common_mistakes && concept.common_mistakes.length > 0 && (
          <div className="bg-red-900/20 rounded-lg p-4 mb-4 border border-red-500/30">
            <h4 className="font-bold text-red-400 mb-2">⚠️ Common Junior Mistakes</h4>
            <ul className="space-y-2">
              {concept.common_mistakes.map((mistake, idx) => (
                <li key={idx} className="text-sm text-gray-300">
                  <span className="text-red-400 font-bold">×</span> {mistake}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Debugging Tips */}
        {concept.debugging_tips && concept.debugging_tips.length > 0 && (
          <div className="bg-green-900/20 rounded-lg p-4 mb-4 border border-green-500/30">
            <h4 className="font-bold text-green-400 mb-2">🔧 Debugging Tips</h4>
            <ul className="space-y-2">
              {concept.debugging_tips.map((tip, idx) => (
                <li key={idx} className="text-sm text-gray-300">
                  <span className="text-green-400 font-bold">✓</span> {tip}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Production Concerns */}
        {concept.production_concerns && concept.production_concerns.length > 0 && (
          <div className="bg-orange-900/20 rounded-lg p-4 mb-4 border border-orange-500/30">
            <h4 className="font-bold text-orange-400 mb-2">🚀 Production Concerns</h4>
            <ul className="space-y-2">
              {concept.production_concerns.map((concern, idx) => (
                <li key={idx} className="text-sm text-gray-300">
                  • {concern}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Key Points */}
        {concept.key_points && concept.key_points.length > 0 && (
          <div className="bg-gray-800 rounded-lg p-4">
            <h4 className="font-bold text-blue-400 mb-2">🎯 Key Points to Remember</h4>
            <ul className="space-y-2">
              {concept.key_points.map((point, idx) => (
                <li key={idx} className="text-sm text-gray-300">
                  {idx + 1}. {point}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* Mini Quiz */}
      {concept.mini_quiz && concept.mini_quiz.length > 0 && (
        <div className="card">
          <h3 className="text-xl font-bold mb-4">❓ Test Your Understanding</h3>
          <div className="space-y-4">
            {concept.mini_quiz.map((quiz, idx) => (
              <div key={idx} className="bg-gray-800 rounded-lg p-4">
                <p className="font-semibold text-blue-400 mb-2">Q: {quiz.question}</p>
                <details className="mt-2">
                  <summary className="cursor-pointer text-sm text-gray-400 hover:text-gray-300">
                    Show Answer
                  </summary>
                  <p className="mt-2 text-sm text-green-400 bg-gray-900 rounded p-3">
                    {quiz.answer}
                  </p>
                </details>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default OfficialDocsTutor

// Made with Bob