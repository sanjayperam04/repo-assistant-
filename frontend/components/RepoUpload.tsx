'use client'

import { useState } from 'react'
import { Upload, Folder } from 'lucide-react'

interface RepoUploadProps {
  onRepoUploaded: (repoPath: string) => void
}

export default function RepoUpload({ onRepoUploaded }: RepoUploadProps) {
  const [uploading, setUploading] = useState(false)
  const [dragActive, setDragActive] = useState(false)

  const handleUpload = async (file: File) => {
    if (!file.name.endsWith('.zip')) {
      alert('Please upload a .zip file')
      return
    }

    setUploading(true)
    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch('http://localhost:8000/api/v1/upload', {
        method: 'POST',
        body: formData
      })

      const data = await response.json()
      if (response.ok) {
        onRepoUploaded(data.repo_path)
      } else {
        alert(`Upload failed: ${data.detail || 'Unknown error'}`)
      }
    } catch (error) {
      alert(`Upload failed: ${error instanceof Error ? error.message : 'Network error'}`)
    } finally {
      setUploading(false)
    }
  }

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true)
    } else if (e.type === "dragleave") {
      setDragActive(false)
    }
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleUpload(e.dataTransfer.files[0])
    }
  }

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      handleUpload(e.target.files[0])
    }
  }

  return (
    <div
      className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
        dragActive ? 'border-blue-500 bg-blue-500/10' : 'border-slate-600 bg-slate-800/50'
      }`}
      onDragEnter={handleDrag}
      onDragLeave={handleDrag}
      onDragOver={handleDrag}
      onDrop={handleDrop}
    >
      <input
        type="file"
        id="file-upload"
        accept=".zip"
        onChange={handleFileInput}
        className="hidden"
        disabled={uploading}
      />
      
      <label
        htmlFor="file-upload"
        className="cursor-pointer flex flex-col items-center gap-3"
      >
        {uploading ? (
          <>
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
            <p className="text-slate-300">Uploading and extracting...</p>
          </>
        ) : (
          <>
            <Upload className="text-slate-400" size={48} />
            <div>
              <p className="text-slate-300 font-medium mb-1">
                Drop your repository .zip here or click to browse
              </p>
              <p className="text-sm text-slate-500">
                Upload a zipped codebase to analyze
              </p>
            </div>
          </>
        )}
      </label>
    </div>
  )
}
