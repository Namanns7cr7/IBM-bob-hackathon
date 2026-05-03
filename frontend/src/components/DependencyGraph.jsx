import { useState, useEffect } from 'react'

function DependencyGraph({ repoId }) {
  const [graphData, setGraphData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [filter, setFilter] = useState('all')
  const [searchTerm, setSearchTerm] = useState('')

  useEffect(() => {
    if (repoId) {
      fetchDependencyGraph()
    }
  }, [repoId])

  const fetchDependencyGraph = async () => {
    try {
      setLoading(true)
      const response = await fetch(`http://localhost:8000/dependency-graph/${repoId}`)
      
      if (!response.ok) {
        throw new Error('Failed to fetch dependency graph')
      }

      const data = await response.json()
      setGraphData(data)
    } catch (err) {
      setError('Failed to load dependency graph')
      console.error('Dependency graph error:', err)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="card">
        <div className="flex items-center gap-3">
          <div className="animate-spin h-5 w-5 border-2 border-primary-600 border-t-transparent rounded-full"></div>
          <p className="text-gray-600 dark:text-gray-400">Loading dependency graph...</p>
        </div>
      </div>
    )
  }

  if (error || !graphData) {
    return (
      <div className="card bg-gray-50 dark:bg-gray-800">
        <p className="text-gray-500 dark:text-gray-400 text-center">
          📦 No dependencies found or unable to parse dependency files
        </p>
      </div>
    )
  }

  const filteredNodes = graphData.nodes.filter(node => {
    if (filter !== 'all' && node.type !== filter) return false
    if (searchTerm && !node.label.toLowerCase().includes(searchTerm.toLowerCase())) return false
    return true
  })

  const packageTypes = [
    { value: 'all', label: 'All Packages', icon: '📦' },
    { value: 'npm', label: 'NPM', icon: '📜' },
    { value: 'pip', label: 'Python', icon: '🐍' },
    { value: 'maven', label: 'Maven', icon: '☕' },
    { value: 'go', label: 'Go', icon: '🔷' },
  ]

  return (
    <div className="card">
      <h2 className="text-xl font-bold mb-4 text-gray-800 dark:text-white">
        📊 Dependency Graph
      </h2>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div className="p-4 bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-900 dark:to-blue-800 rounded-lg">
          <p className="text-2xl font-bold text-blue-600 dark:text-blue-300">
            {graphData.stats.total_dependencies}
          </p>
          <p className="text-xs text-blue-700 dark:text-blue-400">Total Dependencies</p>
        </div>
        <div className="p-4 bg-gradient-to-br from-green-50 to-green-100 dark:from-green-900 dark:to-green-800 rounded-lg">
          <p className="text-2xl font-bold text-green-600 dark:text-green-300">
            {graphData.stats.npm_packages || 0}
          </p>
          <p className="text-xs text-green-700 dark:text-green-400">NPM Packages</p>
        </div>
        <div className="p-4 bg-gradient-to-br from-yellow-50 to-yellow-100 dark:from-yellow-900 dark:to-yellow-800 rounded-lg">
          <p className="text-2xl font-bold text-yellow-600 dark:text-yellow-300">
            {graphData.stats.pip_packages || 0}
          </p>
          <p className="text-xs text-yellow-700 dark:text-yellow-400">Python Packages</p>
        </div>
        <div className="p-4 bg-gradient-to-br from-purple-50 to-purple-100 dark:from-purple-900 dark:to-purple-800 rounded-lg">
          <p className="text-2xl font-bold text-purple-600 dark:text-purple-300">
            {graphData.edges.length}
          </p>
          <p className="text-xs text-purple-700 dark:text-purple-400">Connections</p>
        </div>
      </div>

      {/* Filters */}
      <div className="flex flex-col md:flex-row gap-3 mb-6">
        <input
          type="text"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          placeholder="Search dependencies..."
          className="flex-1 px-4 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg focus:border-primary-500 focus:ring-2 focus:ring-primary-200 dark:bg-gray-800 dark:text-white"
        />
        <div className="flex gap-2 overflow-x-auto">
          {packageTypes.map((type) => (
            <button
              key={type.value}
              onClick={() => setFilter(type.value)}
              className={`px-4 py-2 rounded-lg text-sm font-medium whitespace-nowrap transition-colors ${
                filter === type.value
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
              }`}
            >
              <span className="mr-1">{type.icon}</span>
              {type.label}
            </button>
          ))}
        </div>
      </div>

      {/* Visual Graph */}
      <div className="mb-6 p-6 bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-800 dark:to-gray-900 rounded-lg border-2 border-dashed border-gray-300 dark:border-gray-600">
        <div className="flex items-center justify-center">
          <div className="text-center">
            <div className="text-6xl mb-4">🕸️</div>
            <p className="text-gray-600 dark:text-gray-400 mb-2">
              Interactive graph visualization
            </p>
            <p className="text-sm text-gray-500 dark:text-gray-500">
              {filteredNodes.length} nodes • {graphData.edges.length} edges
            </p>
          </div>
        </div>
      </div>

      {/* Dependency List */}
      <div className="space-y-2 max-h-96 overflow-y-auto">
        {filteredNodes.filter(node => node.category !== 'root').map((node, index) => (
          <div
            key={index}
            className="p-4 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 hover:border-primary-500 dark:hover:border-primary-500 transition-colors"
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <span className="text-2xl">
                  {node.type === 'npm' ? '📜' : node.type === 'pip' ? '🐍' : '📦'}
                </span>
                <div>
                  <p className="font-semibold text-gray-800 dark:text-white">
                    {node.label}
                  </p>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    Version: {node.version}
                  </p>
                </div>
              </div>
              <span className="px-3 py-1 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-full text-xs font-medium">
                {node.type}
              </span>
            </div>
          </div>
        ))}
      </div>

      {filteredNodes.filter(node => node.category !== 'root').length === 0 && (
        <div className="text-center py-8 text-gray-500 dark:text-gray-400">
          No dependencies match your filter
        </div>
      )}

      {/* Info */}
      <div className="mt-6 p-4 bg-blue-50 dark:bg-blue-900 rounded-lg">
        <p className="text-sm text-blue-800 dark:text-blue-200">
          💡 <strong>Tip:</strong> Dependencies are automatically detected from package.json, requirements.txt, pom.xml, and other package manager files.
        </p>
      </div>
    </div>
  )
}

export default DependencyGraph

// Made with Bob
