import { useState } from 'react'
import LandingPage from './components/LandingPage'
import ReadmePreview from './components/ReadmePreview'
import VisualFileTree from './components/VisualFileTree'
import CodeSearch from './components/CodeSearch'
import DependencyGraph from './components/DependencyGraph'
import StackSummary from './components/StackSummary'
import CodeUnderstanding from './components/CodeUnderstanding'
import DebugCoach from './components/DebugCoach'
import LearningPath from './components/LearningPath'
import DebtMeter from './components/DebtMeter'
import QuizPanel from './components/QuizPanel'
import OfficialDocsTutor from './components/OfficialDocsTutor'
import DownloadPack from './components/DownloadPack'

function App() {
  const [activeTab, setActiveTab] = useState('overview')
  const [analysisData, setAnalysisData] = useState(null)
  const [repoId, setRepoId] = useState(null)
  const [sessionId, setSessionId] = useState(null)

  const handleAnalysisComplete = (data, id) => {
    setAnalysisData(data)
    setRepoId(id)
    setSessionId(data.session_id)
  }

  const handleReset = () => {
    setAnalysisData(null)
    setRepoId(null)
    setSessionId(null)
    setActiveTab('overview')
  }

  // Show landing page if no analysis
  if (!analysisData) {
    return <LandingPage onAnalysisComplete={handleAnalysisComplete} />
  }

  const tabs = [
    { id: 'overview', label: 'Overview', icon: '📊' },
    { id: 'readme', label: 'README', icon: '📄' },
    { id: 'structure', label: 'Structure', icon: '📁' },
    { id: 'search', label: 'Code Search', icon: '🔍' },
    { id: 'dependencies', label: 'Dependencies', icon: '📦' },
    { id: 'concepts', label: 'Concepts', icon: '💡' },
    { id: 'official-docs', label: 'Official Docs', icon: '📚' },
    { id: 'learn', label: 'Learning Path', icon: '🎓' },
    { id: 'debug', label: 'Debug', icon: '🐛' },
    { id: 'quiz', label: 'Quiz', icon: '❓' },
  ]

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <header className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 shadow-sm sticky top-0 z-50">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <button
                onClick={handleReset}
                className="text-2xl hover:scale-110 transition-transform"
                title="Analyze new repository"
              >
                🥋
              </button>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-primary-600 to-secondary-600 bg-clip-text text-transparent">
                  DebugSensei
                </h1>
                {analysisData.github_info && (
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    {analysisData.github_info.full_name}
                  </p>
                )}
              </div>
            </div>
            
            {/* Quick Stats */}
            <div className="hidden md:flex items-center gap-6 text-sm">
              <div className="flex items-center gap-2">
                <span className="text-gray-500 dark:text-gray-400">Language:</span>
                <span className="font-semibold text-gray-800 dark:text-white">
                  {analysisData.detected_stack?.primary_language || 'Unknown'}
                </span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-gray-500 dark:text-gray-400">Files:</span>
                <span className="font-semibold text-gray-800 dark:text-white">
                  {analysisData.stats?.total_files || 0}
                </span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-gray-500 dark:text-gray-400">Lines:</span>
                <span className="font-semibold text-gray-800 dark:text-white">
                  {analysisData.stats?.total_lines?.toLocaleString() || 0}
                </span>
              </div>
            </div>

            <button
              onClick={handleReset}
              className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors text-sm font-medium"
            >
              New Analysis
            </button>
          </div>
        </div>
      </header>

      {/* Tabs */}
      <div className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
        <div className="container mx-auto px-6">
          <div className="flex gap-1 overflow-x-auto">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-4 py-3 text-sm font-medium whitespace-nowrap transition-colors border-b-2 ${
                  activeTab === tab.id
                    ? 'border-primary-600 text-primary-600 dark:text-primary-400'
                    : 'border-transparent text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200'
                }`}
              >
                <span className="mr-2">{tab.icon}</span>
                {tab.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Main Content */}
      <main className="container mx-auto px-6 py-8">
        <div className="max-w-7xl mx-auto">
          {/* Overview Tab */}
          {activeTab === 'overview' && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div className="lg:col-span-2">
                  <StackSummary stackInfo={analysisData.detected_stack} />
                </div>
                <div>
                  <DebtMeter debtScore={analysisData.understanding_debt_score} />
                </div>
              </div>
              <CodeUnderstanding 
                summary={analysisData.project_summary}
                architecture={analysisData.architecture_flow}
              />
            </div>
          )}

          {/* README Tab */}
          {activeTab === 'readme' && (
            <ReadmePreview 
              repoId={repoId} 
              githubInfo={analysisData.github_info}
            />
          )}

          {/* Structure Tab */}
          {activeTab === 'structure' && (
            <VisualFileTree fileTree={analysisData.file_tree} />
          )}

          {/* Code Search Tab */}
          {activeTab === 'search' && (
            <CodeSearch repoId={repoId} />
          )}

          {/* Dependencies Tab */}
          {activeTab === 'dependencies' && (
            <DependencyGraph repoId={repoId} />
          )}

          {/* Concepts Tab */}
          {activeTab === 'concepts' && (
            <div className="card">
              <h2 className="text-xl font-bold mb-4 text-gray-800 dark:text-white">
                💡 Detected Concepts
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {analysisData.concepts_detected?.map((concept, index) => (
                  <div 
                    key={index}
                    className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700"
                  >
                    <h3 className="font-semibold text-gray-800 dark:text-white mb-2">
                      {concept.name}
                    </h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                      {concept.description}
                    </p>
                    <div className="flex items-center gap-2">
                      <span className="text-xs px-2 py-1 bg-primary-100 dark:bg-primary-900 text-primary-700 dark:text-primary-300 rounded">
                        {concept.category}
                      </span>
                      <span className="text-xs text-gray-500 dark:text-gray-400">
                        {concept.file_count} files
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Official Docs Tab */}
          {activeTab === 'official-docs' && (
            <OfficialDocsTutor 
              enrichedConcepts={analysisData.enriched_concepts}
              sessionId={sessionId}
            />
          )}

          {/* Learning Path Tab */}
          {activeTab === 'learn' && (
            <LearningPath 
              learningPath={analysisData.learning_path}
              debtScore={analysisData.understanding_debt_score}
            />
          )}

          {/* Debug Tab */}
          {activeTab === 'debug' && (
            <DebugCoach 
              repoId={repoId}
              stackInfo={analysisData.detected_stack}
              checklist={analysisData.debugging_checklist}
            />
          )}

          {/* Quiz Tab */}
          {activeTab === 'quiz' && (
            <QuizPanel 
              questions={analysisData.quiz_questions}
              sessionId={sessionId}
            />
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 mt-12">
        <div className="container mx-auto px-6 py-6">
          <div className="flex items-center justify-between">
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Made with ❤️ by DebugSensei
            </p>
            <DownloadPack sessionId={sessionId} />
          </div>
        </div>
      </footer>
    </div>
  )
}

export default App

// Made with Bob
