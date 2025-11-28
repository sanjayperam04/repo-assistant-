'use client'

import { useState } from 'react'
import { FolderOpen } from 'lucide-react'

interface RepoSelectorProps {
  onRepoSelect: (path: string) => void
  currentRepo: string
}

export default function RepoSelector({ onRepoSelect, currentRepo }: RepoSelectorProps) {
  const [path, setPath] = useState(currentRepo)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (path.trim()) {
      onRepoSelect(path.trim())
    }
  }

  return (
    <form onSubmit={handleSubmit} className="bg-slate-800 rounded-lg p-6 shadow-xl">
      <label className="block text-slate-300 mb-2 font-medium">
        GitHub Repository URL
      </label>
      <div className="flex gap-2">
        <div className="flex-1 relative">
          <FolderOpen className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={20} />
          <input
            type="text"
            value={path}
            onChange={(e) => setPath(e.target.value)}
            placeholder="https://github.com/username/repository"
            className="w-full bg-slate-700 text-white rounded-lg pl-12 pr-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <button
          type="submit"
          className="bg-blue-600 hover:bg-blue-700 text-white rounded-lg px-6 py-3 font-medium transition-colors"
        >
          Clone & Load
        </button>
      </div>
      {currentRepo && (
        <p className="mt-2 text-sm text-slate-400">
          Loaded: {currentRepo}
        </p>
      )}
      <p className="mt-2 text-xs text-slate-500">
        Paste any public GitHub repository URL
      </p>
    </form>
  )
}
