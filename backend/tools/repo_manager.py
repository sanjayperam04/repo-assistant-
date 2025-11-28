"""Repository cloning and management"""
import os
import subprocess
import hashlib
from pathlib import Path

REPOS_DIR = Path("/tmp/legacycode_repos")
REPOS_DIR.mkdir(exist_ok=True)

def get_repo_path(repo_input: str) -> dict:
    """Convert GitHub URL or local path to local path, cloning if necessary"""
    # If it's a GitHub URL, clone it
    if repo_input.startswith(("https://github.com/", "http://github.com/", "git@github.com:")):
        return clone_repo(repo_input)
    
    # Otherwise treat as local path
    path = Path(repo_input)
    if not path.exists():
        return {"error": f"Path does not exist: {repo_input}"}
    
    return {"path": str(path), "status": "local"}

def clone_repo(github_url: str) -> dict:
    """Clone a GitHub repository and return local path"""
    try:
        # Validate GitHub URL
        if not github_url.startswith(("https://github.com/", "http://github.com/", "git@github.com:")):
            return {"error": "Invalid GitHub URL. Please provide a valid GitHub repository URL"}
        
        # Create unique directory name from URL
        repo_hash = hashlib.md5(github_url.encode()).hexdigest()[:8]
        repo_name = github_url.rstrip('/').split('/')[-1].replace('.git', '')
        local_path = REPOS_DIR / f"{repo_name}_{repo_hash}"
        
        # Check if already cloned
        if local_path.exists():
            return {
                "status": "already_cloned",
                "path": str(local_path),
                "message": f"Repository already cloned at {local_path}"
            }
        
        # Clone the repository
        result = subprocess.run(
            ["git", "clone", "--depth", "1", github_url, str(local_path)],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode != 0:
            return {"error": f"Failed to clone repository: {result.stderr}"}
        
        return {
            "status": "success",
            "path": str(local_path),
            "message": f"Successfully cloned {repo_name}"
        }
        
    except subprocess.TimeoutExpired:
        return {"error": "Clone timeout (120s limit). Repository might be too large."}
    except Exception as e:
        return {"error": f"Clone failed: {str(e)}"}

def get_repo_info(repo_path: str) -> dict:
    """Get basic info about a cloned repository"""
    path = Path(repo_path)
    if not path.exists():
        return {"error": "Repository path does not exist"}
    
    # Count files by extension
    file_counts = {}
    total_files = 0
    
    for file in path.rglob("*"):
        if file.is_file() and ".git" not in str(file):
            ext = file.suffix or "no_extension"
            file_counts[ext] = file_counts.get(ext, 0) + 1
            total_files += 1
    
    return {
        "path": str(path),
        "total_files": total_files,
        "file_types": file_counts,
        "size_mb": sum(f.stat().st_size for f in path.rglob("*") if f.is_file()) / (1024 * 1024)
    }
