# LegacyCode MCP

> AI-powered codebase analysis and navigation platform for legacy software systems

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Next.js 15](https://img.shields.io/badge/Next.js-15-black)](https://nextjs.org/)

LegacyCode MCP is a full-stack application that enables developers to understand, analyze, and refactor large legacy codebases through natural language conversations. By combining static analysis, semantic code search, and AI-powered insights, it transforms weeks of manual code exploration into minutes of interactive dialogue.

## Overview

Traditional code exploration requires extensive manual navigation, grep searches, and documentation reading. LegacyCode MCP streamlines this process by:

- **Automatically cloning and indexing** GitHub repositories
- **Extracting semantic code structure** using Tree-sitter AST parsing
- **Providing conversational access** to codebase insights via Groq's Llama 3.3 70B
- **Running static analysis** and test suites in isolated environments
- **Generating refactoring suggestions** based on AST transformations

## Key Features

### 🔗 GitHub Integration
Seamlessly clone and analyze any public GitHub repository by simply pasting its URL. Repositories are automatically cached for instant subsequent access.

### 🔍 Intelligent Code Indexing
Tree-sitter-based parsing extracts functions, classes, and variables from Python codebases, building a comprehensive symbol table for rapid navigation.

### 🔎 Semantic Search
Find symbols, patterns, and code structures using natural language queries. Search across entire codebases in milliseconds.

### 🧪 Safe Test Execution
Execute test suites (pytest) in sandboxed environments with structured result reporting and failure analysis.

### 📊 Static Analysis
Integrated Ruff linting provides real-time code quality metrics, violation detection, and automated fix suggestions.

### 🤖 AI-Powered Insights
Leverage Groq's Llama 3.3 70B model for intelligent code explanations, architecture analysis, and development guidance.

### 💾 Smart Caching
Cloned repositories persist locally, eliminating redundant network operations and enabling offline analysis.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (Next.js 15)                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Chat UI      │  │ Code Explorer│  │ Dashboard    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└────────────────────────────┬────────────────────────────────┘
                             │ REST API
┌────────────────────────────┴────────────────────────────────┐
│                  Backend (FastAPI + FastMCP)                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              MCP Server (5 Core Tools)               │   │
│  │  • index_repo    • find_symbols   • run_tests       │   │
│  │  • analyze_code  • refactor_code                     │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Tree-sitter  │  │ Ruff/mypy    │  │ Groq AI      │      │
│  │ Parser       │  │ Analysis     │  │ Integration  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

## Technology Stack

### Backend
- **FastAPI** - High-performance REST API framework
- **FastMCP** - Model Context Protocol server implementation
- **Tree-sitter** - Incremental parsing for code analysis
- **Ruff** - Fast Python linter and formatter
- **Groq** - LLM inference platform (Llama 3.3 70B)
- **Docker** - Containerized test execution
- **SQLAlchemy** - Database ORM
- **FAISS** - Vector similarity search

### Frontend
- **Next.js 15** - React framework with App Router
- **React 19** - UI component library
- **Tailwind CSS** - Utility-first styling
- **TanStack Query** - Async state management
- **Lucide React** - Icon system

## Installation

### Prerequisites
- Python 3.10 or higher
- Node.js 18 or higher
- Git
- Groq API key ([Get one here](https://console.groq.com))

### Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your GROQ_API_KEY

# Start server
uvicorn api.main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The application will be available at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Usage

### Basic Workflow

1. **Navigate** to http://localhost:3000
2. **Enter** a GitHub repository URL (e.g., `https://github.com/pallets/flask`)
3. **Click** "Clone & Load" to initialize the repository
4. **Interact** with your codebase through natural language

### Example Queries

#### Code Analysis
```
"Index this repo"
"Analyze code quality"
"Run tests"
```

#### Symbol Search
```
"Find all authentication functions"
"Search for database models"
"Show me the main entry point"
```

#### AI-Powered Insights
```
"What does this codebase do?"
"Explain the authentication flow"
"How is dependency injection implemented?"
"What are the main architectural patterns?"
```

## API Reference

### REST Endpoints

#### POST `/api/v1/chat`
Execute conversational queries against a repository.

**Request:**
```json
{
  "message": "Index this repo",
  "repo_url": "https://github.com/username/repository",
  "context": ["optional", "context", "paths"]
}
```

**Response:**
```json
{
  "response": "Indexed repository: {...}",
  "tool_used": "index_repo"
}
```

#### POST `/api/v1/tool`
Direct tool execution endpoint.

**Request:**
```json
{
  "tool": "find_symbols",
  "repo_path": "/path/to/repo",
  "params": {"query": "authenticate"}
}
```

#### GET `/health`
Health check endpoint.

## MCP Tools

### `index_repo`
Scans repository and builds comprehensive symbol table using Tree-sitter.

### `find_symbols`
Semantic search across codebase for functions, classes, and variables.

### `run_tests`
Executes pytest in sandboxed environment with structured result reporting.

### `analyze_code`
Runs Ruff static analysis and returns violations ranked by severity.

### `refactor_code`
Generates AST-based refactoring suggestions (rename, extract, inline).

## Configuration

### Environment Variables

```bash
# Backend (.env)
GROQ_API_KEY=your_groq_api_key_here

# Optional
DATABASE_URL=sqlite:///./legacycode.db
REDIS_URL=redis://localhost:6379
```

### Repository Storage

Cloned repositories are stored in `/tmp/legacycode_repos/` by default. Configure via:

```python
# backend/tools/repo_manager.py
REPOS_DIR = Path("/custom/path/to/repos")
```

## Development

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Code Quality

```bash
# Backend linting
ruff check .
mypy .

# Frontend linting
npm run lint
```

## Roadmap

- [ ] Multi-language support (JavaScript, TypeScript, Java, Go)
- [ ] Private repository authentication (GitHub OAuth)
- [ ] Real-time collaboration features
- [ ] Advanced refactoring operations
- [ ] Code complexity visualization
- [ ] Integration with CI/CD pipelines
- [ ] Custom MCP tool plugins
- [ ] Vector embeddings for semantic code search

## Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting pull requests.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [FastMCP](https://github.com/jlowin/fastmcp) - MCP server framework
- [Tree-sitter](https://tree-sitter.github.io/) - Incremental parsing library
- [Groq](https://groq.com/) - LLM inference platform
- [Ruff](https://github.com/astral-sh/ruff) - Fast Python linter

## Support

- **Documentation**: [docs.legacycode-mcp.dev](https://docs.legacycode-mcp.dev)
- **Issues**: [GitHub Issues](https://github.com/yourusername/legacycode-mcp/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/legacycode-mcp/discussions)

---

**Built with ❤️ for developers navigating legacy codebases**
