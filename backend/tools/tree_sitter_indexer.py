"""Tree-sitter based code indexing and symbol search"""
import os
from pathlib import Path
from typing import List, Dict
import tree_sitter_python as tspython
from tree_sitter import Language, Parser

PY_LANGUAGE = Language(tspython.language())

def index_repository(repo_path: str) -> dict:
    """Index repository and extract symbols"""
    repo = Path(repo_path)
    if not repo.exists():
        return {"error": f"Repository path {repo_path} does not exist"}
    
    parser = Parser(PY_LANGUAGE)
    symbols = []
    file_count = 0
    
    for py_file in repo.rglob("*.py"):
        if "venv" in str(py_file) or ".venv" in str(py_file):
            continue
            
        try:
            code = py_file.read_bytes()
            tree = parser.parse(code)
            file_symbols = extract_symbols(tree.root_node, str(py_file), code)
            symbols.extend(file_symbols)
            file_count += 1
        except Exception as e:
            continue
    
    return {
        "status": "success",
        "files_indexed": file_count,
        "symbols_found": len(symbols),
        "symbols": symbols[:100]  # Return first 100 for preview
    }

def extract_symbols(node, file_path: str, code: bytes) -> List[Dict]:
    """Extract function and class definitions"""
    symbols = []
    
    if node.type == "function_definition":
        name_node = node.child_by_field_name("name")
        if name_node:
            symbols.append({
                "type": "function",
                "name": name_node.text.decode(),
                "file": file_path,
                "line": node.start_point[0] + 1
            })
    
    elif node.type == "class_definition":
        name_node = node.child_by_field_name("name")
        if name_node:
            symbols.append({
                "type": "class",
                "name": name_node.text.decode(),
                "file": file_path,
                "line": node.start_point[0] + 1
            })
    
    for child in node.children:
        symbols.extend(extract_symbols(child, file_path, code))
    
    return symbols

def search_symbols(query: str, repo_path: str, language: str = "python") -> list:
    """Search for symbols matching query"""
    result = index_repository(repo_path)
    if "error" in result:
        return []
    
    query_lower = query.lower()
    matches = [
        s for s in result.get("symbols", [])
        if query_lower in s["name"].lower()
    ]
    
    return matches[:20]  # Return top 20 matches
