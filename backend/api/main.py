"""FastAPI REST API for MCP server"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import os
from dotenv import load_dotenv
from groq import Groq
from api.upload import router as upload_router

# Load environment variables
load_dotenv()

app = FastAPI(title="LegacyCode MCP API")

# Include upload router
app.include_router(upload_router)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Groq client
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY", ""))

class ChatRequest(BaseModel):
    message: str
    repo_url: str  # GitHub URL or local path
    context: Optional[List[str]] = None

class ToolCall(BaseModel):
    tool: str
    repo_path: str
    params: dict = {}

@app.post("/api/v1/chat")
async def chat(request: ChatRequest):
    """Chat endpoint with MCP tool orchestration"""
    # Import MCP tools
    from tools.tree_sitter_indexer import search_symbols, index_repository
    from tools.sandbox import execute_tests
    from tools.static_analysis import analyze
    from tools.repo_manager import get_repo_path
    
    # Convert repo URL/path to local path
    repo_result = get_repo_path(request.repo_url)
    if "error" in repo_result:
        return {"response": f"Repository error: {repo_result['error']}", "tool_used": "none"}
    
    repo_path = repo_result["path"]
    
    # If just cloned, inform user
    if repo_result.get("status") == "success":
        return {"response": f"✅ Successfully cloned repository! Now you can ask: 'index this repo', 'find functions', 'run tests', or 'analyze code'", "tool_used": "clone"}
    
    # Simple orchestration - in production, use Groq tool calling
    message_lower = request.message.lower()
    
    if "index" in message_lower:
        result = index_repository(repo_path)
        return {"response": f"Indexed repository: {result}", "tool_used": "index_repo"}
    
    elif "test" in message_lower:
        result = execute_tests(repo_path)
        return {"response": f"Test results: {result}", "tool_used": "run_tests"}
    
    elif "analyze" in message_lower or "lint" in message_lower:
        result = analyze(repo_path)
        return {"response": f"Analysis: {result}", "tool_used": "analyze_code"}
    
    elif "find" in message_lower or "search" in message_lower:
        # Extract search term (simplified)
        words = request.message.split()
        query = words[-1] if words else ""
        result = search_symbols(query, repo_path)
        return {"response": f"Found symbols: {result}", "tool_used": "find_symbols"}
    
    else:
        # Use Groq for general questions
        if not groq_client.api_key:
            return {
                "response": "Please configure GROQ_API_KEY in backend/.env to use AI chat. For now, try: 'index this repo', 'find <symbol>', 'run tests', or 'analyze code'",
                "tool_used": "none"
            }
        
        try:
            completion = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": request.message}],
                temperature=0.7,
                max_tokens=1024
            )
            return {"response": completion.choices[0].message.content, "tool_used": "llm"}
        except Exception as e:
            return {"response": f"LLM error: {str(e)}", "tool_used": "llm"}

@app.post("/api/v1/tool")
async def execute_tool(call: ToolCall):
    """Direct tool execution endpoint"""
    from tools.tree_sitter_indexer import search_symbols, index_repository
    from tools.sandbox import execute_tests
    from tools.static_analysis import analyze
    
    tools = {
        "index_repo": lambda: index_repository(call.repo_path),
        "find_symbols": lambda: search_symbols(call.params.get("query", ""), call.repo_path),
        "run_tests": lambda: execute_tests(call.repo_path, call.params.get("pattern", "**/test*.py")),
        "analyze_code": lambda: analyze(call.repo_path, call.params.get("file_pattern", "**/*.py"))
    }
    
    if call.tool not in tools:
        raise HTTPException(400, f"Unknown tool: {call.tool}")
    
    result = tools[call.tool]()
    return {"tool": call.tool, "result": result}

@app.get("/health")
async def health():
    return {"status": "healthy"}
