import { useState } from 'react'
import UploadPanel from './components/UploadPanel'
import StackSummary from './components/StackSummary'
import FileTree from './components/FileTree'
import CodeUnderstanding from './components/CodeUnderstanding'
import DebugCoach from './components/DebugCoach'
import LearningPath from './components/LearningPath'
import DebtMeter from './components/DebtMeter'
import QuizPanel from './components/QuizPanel'
import DocsPanel from './components/DocsPanel'
import OfficialDocsTutor from './components/OfficialDocsTutor'
import DownloadPack from './components/DownloadPack'

function App() {
  const [activeTab, setActiveTab] = useState('understand')
  const [analysisData, setAnalysisData] = useState(null)
  const [repoId, setRepoId] = useState(null)
  const [sessionId, setSessionId] = useState(null)
  const [loading, setLoading] = useState(false)

  const tabs = [
    { id: 'understand', label: 'Understand', icon: '📖' },
    { id: 'concepts', label: 'Concepts', icon: '💡' },
    { id: 'official-docs', label: 'Official Docs', icon: '📚' },
    { id: 'debug', label: 'Debug', icon: '🐛' },
    { id: 'learn', label: 'Learn', icon: '🎓' },
    { id: 'quiz', label: 'Quiz', icon: '❓' },
    { id: 'download', label: 'Download', icon: '📦' },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white">
      {/* Header */}
      <header className="bg-gray-800 border-b border-gray-700 shadow-lg">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="text-4xl">🥋</div>
              <div>
                <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
                  DebugSensei
                </h1>
                <p className="text-sm text-gray-400">Understand any codebase. Debug smarter. Learn while you build.</p>
              </div>
            </div>
            {analysisData && (
              <div className="text-sm text-gray-400">
                {analysisData.detected_stack?.primary_language} • {analysisData.stats?.total_files} files
              </div>
            )}
          </div>
        </div>
      </header>

      <div className="container mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Left Sidebar - Upload & Settings */}
          <div className="lg:col-span-1">
            <UploadPanel
              onAnalysisComplete={(data, id) => {
                setAnalysisData(data)
                setRepoId(id)
                setSessionId(data.session_id)
              }}
              loading={loading}
              setLoading={setLoading}
            />
            
            {analysisData && (
              <div className="mt-6">
                <StackSummary data={analysisData.detected_stack} stats={analysisData.stats} />
              </div>
            )}
          </div>

          {/* Main Content Area */}
          <div className="lg:col-span-2">
            {!analysisData && !loading && (
              <div className="card text-center py-16">
                <div className="text-7xl mb-6">🥋</div>
                <h2 className="text-3xl font-bold mb-3 bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
                  Build with AI. Understand with DebugSensei.
                </h2>
                <p className="text-xl text-gray-400 mb-8 max-w-2xl mx-auto">
                  Stop vibe-coding. Start understanding. Learn while you build.
                </p>
                
                <div className="max-w-3xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                  <div className="bg-gray-800 rounded-lg p-6 border border-gray-700 hover:border-blue-500 transition-colors">
                    <div className="text-4xl mb-3">📖</div>
                    <h3 className="font-bold text-lg mb-2 text-white">Understand Any Codebase</h3>
                    <p className="text-sm text-gray-400">
                      Upload any project. Get instant architecture explanation, stack detection, and concept mapping.
                    </p>
                    <p className="text-xs text-blue-400 mt-2 font-semibold">80% faster understanding</p>
                  </div>
                  
                  <div className="bg-gray-800 rounded-lg p-6 border border-gray-700 hover:border-purple-500 transition-colors">
                    <div className="text-4xl mb-3">🐛</div>
                    <h3 className="font-bold text-lg mb-2 text-white">Debug Smarter</h3>
                    <p className="text-sm text-gray-400">
                      Paste any error. Get step-by-step debugging guidance that teaches you why, not just how.
                    </p>
                    <p className="text-xs text-purple-400 mt-2 font-semibold">75% faster debugging</p>
                  </div>
                  
                  <div className="bg-gray-800 rounded-lg p-6 border border-gray-700 hover:border-green-500 transition-colors">
                    <div className="text-4xl mb-3">🎓</div>
                    <h3 className="font-bold text-lg mb-2 text-white">Learn While You Build</h3>
                    <p className="text-sm text-gray-400">
                      Track your understanding debt. Get personalized learning paths. Take quizzes to reinforce concepts.
                    </p>
                    <p className="text-xs text-green-400 mt-2 font-semibold">Close the knowledge gap</p>
                  </div>
                </div>

                <div className="bg-gradient-to-r from-blue-900/30 to-purple-900/30 rounded-lg p-6 max-w-2xl mx-auto border border-blue-500/30">
                  <p className="text-sm text-gray-300 mb-2">
                    <span className="font-bold text-blue-400">The Problem:</span> AI helps you code 3x faster, but understanding lags behind by 60-80%.
                  </p>
                  <p className="text-sm text-gray-300">
                    <span className="font-bold text-purple-400">The Solution:</span> DebugSensei helps you build with AI without losing your ability to understand, debug, and grow.
                  </p>
                </div>
              </div>
            )}

            {loading && (
              <div className="card text-center py-20">
                <div className="animate-spin text-6xl mb-4">⚙️</div>
                <h2 className="text-2xl font-bold mb-2 text-gray-800 dark:text-white">Analyzing your codebase...</h2>
                <p className="text-gray-600 dark:text-gray-400">This may take a few moments</p>
              </div>
            )}

            {analysisData && !loading && (
              <>
                {/* Tab Navigation */}
                <div className="bg-gray-800 rounded-lg p-2 mb-6 flex space-x-2 overflow-x-auto">
                  {tabs.map(tab => (
                    <button
                      key={tab.id}
                      onClick={() => setActiveTab(tab.id)}
                      className={`flex items-center space-x-2 px-4 py-2 rounded-lg font-medium transition-colors whitespace-nowrap ${
                        activeTab === tab.id
                          ? 'bg-primary-600 text-white'
                          : 'text-gray-400 hover:text-white hover:bg-gray-700'
                      }`}
                    >
                      <span>{tab.icon}</span>
                      <span>{tab.label}</span>
                    </button>
                  ))}
                </div>

                {/* Tab Content */}
                <div className="space-y-6">
                  {activeTab === 'understand' && (
                    <>
                      <CodeUnderstanding data={analysisData} />
                      <FileTree files={analysisData.file_tree} />
                    </>
                  )}
                  
                  {activeTab === 'concepts' && (
                    <div className="space-y-6">
                      <div className="card">
                        <h2 className="text-2xl font-bold mb-4 text-gray-800 dark:text-white">
                          💡 Concepts Detected
                        </h2>
                        <div className="space-y-3">
                          {analysisData.concepts_detected?.map((concept, idx) => (
                            <div key={idx} className="border border-gray-200 dark:border-gray-700 rounded-lg p-4">
                              <div className="flex items-start justify-between">
                                <div className="flex-1">
                                  <h3 className="font-semibold text-lg text-gray-800 dark:text-white">{concept.name}</h3>
                                  <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">{concept.description}</p>
                                  <div className="flex items-center space-x-4 mt-2 text-xs text-gray-500">
                                    <span className="bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 px-2 py-1 rounded">
                                      {concept.category}
                                    </span>
                                    <span>Used {concept.count} times</span>
                                    <span>Weight: {concept.weight}</span>
                                  </div>
                                </div>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                      <DocsPanel docs={analysisData.docs_matches} />
                    </div>
                  )}
                  
                  {activeTab === 'debug' && (
                    <DebugCoach repoId={repoId} />
                  )}
                  
                  {activeTab === 'learn' && (
                    <LearningPath path={analysisData.learning_path} />
                  )}
                  
                  {activeTab === 'official-docs' && (
                    <OfficialDocsTutor
                      enrichedConcepts={analysisData.enriched_concepts}
                      skillLevel={analysisData.skill_level || 'intermediate'}
                    />
                  )}
                  
                  {activeTab === 'quiz' && (
                    <QuizPanel questions={analysisData.quiz_questions} />
                  )}
                  
                  {activeTab === 'download' && (
                    <DownloadPack sessionId={sessionId} />
                  )}
                </div>
              </>
            )}
          </div>

          {/* Right Sidebar - Debt Meter & Progress */}
          <div className="lg:col-span-1">
            {analysisData && (
              <DebtMeter score={analysisData.understanding_debt_score} />
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default App

// Made with Bob
