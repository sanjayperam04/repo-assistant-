'use client'

import { useState } from 'react'
import CodeChat from '@/components/CodeChat'
import RepoSelector from '@/components/RepoSelector'

export default function Home() {
  const [repoPath, setRepoPath] = useState('')

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800">
      <div className="container mx-auto px-4 py-8">
        <header className="text-center mb-12">
          <h1 className="text-5xl font-bold text-white mb-4">
            LegacyCode MCP
          </h1>
          <p className="text-xl text-slate-300">
            Paste a GitHub repo URL and ask anything about the codebase 👇
          </p>
        </header>

        <div className="max-w-4xl mx-auto">
          <RepoSelector onRepoSelect={setRepoPath} currentRepo={repoPath} />
          
          {repoPath && (
            <div className="mt-8">
              <CodeChat repoPath={repoPath} />
            </div>
          )}
        </div>
      </div>
    </main>
  )
}
