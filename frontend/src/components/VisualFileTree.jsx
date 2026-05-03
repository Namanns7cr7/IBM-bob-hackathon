import { useState } from 'react'

function VisualFileTree({ fileTree }) {
  const [expandedFolders, setExpandedFolders] = useState(new Set())
  const [searchTerm, setSearchTerm] = useState('')

  const toggleFolder = (path) => {
    const newExpanded = new Set(expandedFolders)
    if (newExpanded.has(path)) {
      newExpanded.delete(path)
    } else {
      newExpanded.add(path)
    }
    setExpandedFolders(newExpanded)
  }

  const getFileIcon = (name) => {
    const ext = name.split('.').pop()?.toLowerCase()
    const iconMap = {
      'js': '📜',
      'jsx': '⚛️',
      'ts': '📘',
      'tsx': '⚛️',
      'py': '🐍',
      'java': '☕',
      'cpp': '⚙️',
      'c': '⚙️',
      'go': '🔷',
      'rs': '🦀',
      'html': '🌐',
      'css': '🎨',
      'scss': '🎨',
      'json': '📋',
      'md': '📄',
      'yml': '⚙️',
      'yaml': '⚙️',
      'xml': '📋',
      'sql': '🗄️',
      'sh': '🔧',
      'dockerfile': '🐳',
      'gitignore': '🚫',
    }
    return iconMap[ext] || '📄'
  }

  const renderTree = (items, level = 0) => {
    if (!items || items.length === 0) return null

    const filteredItems = searchTerm
      ? items.filter(item => 
          item.name.toLowerCase().includes(searchTerm.toLowerCase())
        )
      : items

    return filteredItems.map((item, index) => {
      const isFolder = item.type === 'directory'
      const isExpanded = expandedFolders.has(item.path)
      const indent = level * 20

      return (
        <div key={`${item.path}-${index}`}>
          <div
            className={`flex items-center gap-2 py-1.5 px-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded cursor-pointer transition-colors ${
              isFolder ? 'font-medium' : ''
            }`}
            style={{ paddingLeft: `${indent + 8}px` }}
            onClick={() => isFolder && toggleFolder(item.path)}
          >
            {isFolder && (
              <span className="text-gray-500 dark:text-gray-400 text-xs">
                {isExpanded ? '▼' : '▶'}
              </span>
            )}
            <span className="text-lg">
              {isFolder ? (isExpanded ? '📂' : '📁') : getFileIcon(item.name)}
            </span>
            <span className="text-sm text-gray-700 dark:text-gray-300 truncate">
              {item.name}
            </span>
            {item.size && (
              <span className="text-xs text-gray-400 dark:text-gray-500 ml-auto">
                {formatFileSize(item.size)}
              </span>
            )}
          </div>
          {isFolder && isExpanded && item.children && (
            <div>
              {renderTree(item.children, level + 1)}
            </div>
          )}
        </div>
      )
    })
  }

  const formatFileSize = (bytes) => {
    if (bytes < 1024) return `${bytes}B`
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)}KB`
    return `${(bytes / (1024 * 1024)).toFixed(1)}MB`
  }

  const expandAll = () => {
    const allPaths = new Set()
    const collectPaths = (items) => {
      items?.forEach(item => {
        if (item.type === 'directory') {
          allPaths.add(item.path)
          if (item.children) {
            collectPaths(item.children)
          }
        }
      })
    }
    collectPaths(fileTree)
    setExpandedFolders(allPaths)
  }

  const collapseAll = () => {
    setExpandedFolders(new Set())
  }

  if (!fileTree || fileTree.length === 0) {
    return (
      <div className="card">
        <p className="text-gray-500 dark:text-gray-400 text-center">
          No file tree available
        </p>
      </div>
    )
  }

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-bold text-gray-800 dark:text-white">
          📁 File Structure
        </h2>
        <div className="flex gap-2">
          <button
            onClick={expandAll}
            className="text-xs px-3 py-1 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
          >
            Expand All
          </button>
          <button
            onClick={collapseAll}
            className="text-xs px-3 py-1 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
          >
            Collapse All
          </button>
        </div>
      </div>

      {/* Search */}
      <div className="mb-4">
        <input
          type="text"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          placeholder="Search files..."
          className="w-full px-4 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg focus:border-primary-500 focus:ring-2 focus:ring-primary-200 dark:bg-gray-800 dark:text-white"
        />
      </div>

      {/* Tree */}
      <div className="max-h-96 overflow-y-auto border border-gray-200 dark:border-gray-700 rounded-lg p-2">
        {renderTree(fileTree)}
      </div>

      {/* Stats */}
      <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
        <div className="grid grid-cols-3 gap-4 text-center">
          <div>
            <p className="text-2xl font-bold text-primary-600 dark:text-primary-400">
              {countFiles(fileTree)}
            </p>
            <p className="text-xs text-gray-500 dark:text-gray-400">Files</p>
          </div>
          <div>
            <p className="text-2xl font-bold text-secondary-600 dark:text-secondary-400">
              {countFolders(fileTree)}
            </p>
            <p className="text-xs text-gray-500 dark:text-gray-400">Folders</p>
          </div>
          <div>
            <p className="text-2xl font-bold text-green-600 dark:text-green-400">
              {formatFileSize(getTotalSize(fileTree))}
            </p>
            <p className="text-xs text-gray-500 dark:text-gray-400">Total Size</p>
          </div>
        </div>
      </div>
    </div>
  )
}

function countFiles(items) {
  if (!items) return 0
  return items.reduce((count, item) => {
    if (item.type === 'file') return count + 1
    if (item.children) return count + countFiles(item.children)
    return count
  }, 0)
}

function countFolders(items) {
  if (!items) return 0
  return items.reduce((count, item) => {
    if (item.type === 'directory') {
      return count + 1 + (item.children ? countFolders(item.children) : 0)
    }
    return count
  }, 0)
}

function getTotalSize(items) {
  if (!items) return 0
  return items.reduce((total, item) => {
    if (item.size) return total + item.size
    if (item.children) return total + getTotalSize(item.children)
    return total
  }, 0)
}

export default VisualFileTree

// Made with Bob
