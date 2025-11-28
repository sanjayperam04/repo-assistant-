# LegacyCode MCP - Usage Guide

## 🚀 Quick Start

### 1. Access the App
Open your browser and go to: **http://localhost:3000**

### 2. Load a Repository
Paste any public GitHub repository URL in the input field:
```
https://github.com/username/repository
```

Examples to try:
- `https://github.com/pallets/flask` - Flask web framework
- `https://github.com/psf/requests` - Requests HTTP library
- `https://github.com/django/django` - Django web framework

Click **"Clone & Load"** - the app will automatically clone the repository.

### 3. Start Chatting

Once loaded, you can ask questions about the codebase:

#### 📊 Code Analysis Commands
- **"Index this repo"** - Scans all Python files and builds a symbol table
- **"Analyze code quality"** - Runs Ruff linter and shows violations
- **"Run tests"** - Executes pytest in the repository

#### 🔍 Search Commands
- **"Find processOrder function"** - Searches for specific symbols
- **"Find all classes"** - Lists all class definitions
- **"Search for authentication"** - Finds symbols matching a query

#### 🤖 AI-Powered Questions
- **"What does this codebase do?"** - AI explains the project
- **"Explain the authentication flow"** - AI describes specific functionality
- **"How do I add a new feature?"** - AI provides guidance
- **"What are the main components?"** - AI breaks down architecture

#### 💡 General Programming
- **"What is dependency injection?"** - Ask any programming question
- **"Explain Python decorators"** - Get explanations
- **"Best practices for API design"** - Get recommendations

## 🎯 Example Workflow

1. **Load a repo**: `https://github.com/pallets/flask`
2. **Index it**: "Index this repo"
3. **Explore**: "Find all route handlers"
4. **Analyze**: "Analyze code quality"
5. **Ask AI**: "Explain how Flask routing works"

## 📁 Repository Caching

Cloned repositories are cached in `/tmp/legacycode_repos/`. If you load the same repo again, it will use the cached version instantly.

## 🔧 Supported Languages

Currently optimized for **Python** repositories:
- Tree-sitter parsing for Python
- Ruff linting
- pytest execution

## 💡 Tips

- Start with "Index this repo" to build the symbol table
- Use specific function/class names for better search results
- The AI has access to Groq Llama 3.3 70B for intelligent responses
- Larger repos may take longer to clone and index

## 🐛 Troubleshooting

**"Repository error"**: Make sure the GitHub URL is public and valid  
**"0 symbols found"**: The repo might not have Python files  
**"Test execution failed"**: The repo might not have pytest installed  

## 🎨 Features

✅ Automatic GitHub cloning  
✅ Code indexing with Tree-sitter  
✅ Symbol search  
✅ Static analysis with Ruff  
✅ Test execution with pytest  
✅ AI-powered chat with Groq  
✅ Repository caching  
✅ Real-time streaming responses  

Enjoy exploring legacy codebases! 🚀
