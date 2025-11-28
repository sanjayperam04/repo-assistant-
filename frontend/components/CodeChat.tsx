'use client'

import { useState } from 'react'
import { Send } from 'lucide-react'

interface Message {
  role: 'user' | 'assistant'
  content: string
  tool?: string
}

export default function CodeChat({ repoPath }: { repoPath: string }) {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)

  const sendMessage = async () => {
    if (!input.trim()) return

    const userMessage: Message = { role: 'user', content: input }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      const response = await fetch('http://localhost:8000/api/v1/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: input,
          repo_url: repoPath
        })
      })

      const data = await response.json()
      const assistantMessage: Message = {
        role: 'assistant',
        content: typeof data.response === 'string' ? data.response : JSON.stringify(data.response, null, 2),
        tool: data.tool_used
      }
      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: `Error: ${error instanceof Error ? error.message : 'Failed to connect to backend'}`,
      }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-slate-800 rounded-lg shadow-2xl overflow-hidden">
      <div className="h-[500px] overflow-y-auto p-6 space-y-4">
        {messages.length === 0 && (
          <div className="text-center text-slate-400 mt-20">
            <p className="text-lg mb-4">🚀 Repository loaded! Start exploring...</p>
            <div className="text-sm space-y-2">
              <p>💡 Try asking:</p>
              <p className="text-slate-500">"Index this repo"</p>
              <p className="text-slate-500">"Find all functions"</p>
              <p className="text-slate-500">"Run tests"</p>
              <p className="text-slate-500">"Analyze code quality"</p>
              <p className="text-slate-500">"What does this codebase do?"</p>
            </div>
          </div>
        )}
        
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[80%] rounded-lg p-4 ${
                msg.role === 'user'
                  ? 'bg-blue-600 text-white'
                  : 'bg-slate-700 text-slate-100'
              }`}
            >
              {msg.tool && (
                <div className="text-xs text-slate-400 mb-2">
                  🔧 {msg.tool}
                </div>
              )}
              <pre className="whitespace-pre-wrap font-sans">{msg.content}</pre>
            </div>
          </div>
        ))}
        
        {loading && (
          <div className="flex justify-start">
            <div className="bg-slate-700 rounded-lg p-4 text-slate-300">
              Thinking...
            </div>
          </div>
        )}
      </div>

      <div className="border-t border-slate-700 p-4">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
            placeholder="Ask about your codebase..."
            className="flex-1 bg-slate-700 text-white rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={loading}
          />
          <button
            onClick={sendMessage}
            disabled={loading || !input.trim()}
            className="bg-blue-600 hover:bg-blue-700 disabled:bg-slate-600 text-white rounded-lg px-6 py-3 flex items-center gap-2 transition-colors"
          >
            <Send size={20} />
          </button>
        </div>
      </div>
    </div>
  )
}
