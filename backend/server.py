"""LegacyCode MCP Server - AI Codebase Navigator"""
import os
from pathlib import Path
from fastmcp import FastMCP

mcp = FastMCP("legacycode-mcp")

@mcp.tool()
def index_repo(repo_path: str) -> dict:
    """Index a codebase and build symbol table"""
    from tools.tree_sitter_indexer import index_repository
    return index_repository(repo_path)

@mcp.tool()
def find_symbols(query: str, repo_path: str, language: str = "python") -> list:
    """Search for symbols (functions, classes, variables) in codebase"""
    from tools.tree_sitter_indexer import search_symbols
    return search_symbols(query, repo_path, language)

@mcp.tool()
def run_tests(repo_path: str, pattern: str = "**/test*.py") -> dict:
    """Execute tests in a safe sandbox environment"""
    from tools.sandbox import execute_tests
    return execute_tests(repo_path, pattern)

@mcp.tool()
def analyze_code(repo_path: str, file_pattern: str = "**/*.py") -> dict:
    """Run static analysis (linting, type checking)"""
    from tools.static_analysis import analyze
    return analyze(repo_path, file_pattern)

@mcp.tool()
def refactor_code(repo_path: str, action: str, target: str, dry_run: bool = True) -> dict:
    """Generate refactoring suggestions (rename, extract, inline)"""
    from tools.refactoring import refactor
    return refactor(repo_path, action, target, dry_run)

if __name__ == "__main__":
    mcp.run()
