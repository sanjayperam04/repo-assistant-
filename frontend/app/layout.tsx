import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'LegacyCode MCP - AI Codebase Navigator',
  description: 'Understand and refactor legacy codebases with AI',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  )
}
