"""File upload endpoint for repository uploads"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import zipfile
import shutil
import uuid

router = APIRouter()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/api/v1/upload")
async def upload_repo(file: UploadFile = File(...)):
    """Upload a repository as a zip file"""
    if not file.filename.endswith('.zip'):
        raise HTTPException(400, "Only .zip files are supported")
    
    # Create unique directory for this upload
    repo_id = str(uuid.uuid4())[:8]
    repo_path = UPLOAD_DIR / repo_id
    repo_path.mkdir(exist_ok=True)
    
    # Save uploaded file
    zip_path = repo_path / file.filename
    with zip_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Extract zip
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(repo_path)
        
        # Remove zip file after extraction
        zip_path.unlink()
        
        return {
            "repo_id": repo_id,
            "repo_path": str(repo_path),
            "message": "Repository uploaded and extracted successfully"
        }
    except Exception as e:
        # Cleanup on error
        shutil.rmtree(repo_path, ignore_errors=True)
        raise HTTPException(500, f"Failed to extract zip: {str(e)}")

@router.get("/api/v1/repos")
async def list_repos():
    """List all uploaded repositories"""
    repos = []
    for repo_dir in UPLOAD_DIR.iterdir():
        if repo_dir.is_dir():
            repos.append({
                "repo_id": repo_dir.name,
                "repo_path": str(repo_dir)
            })
    return {"repos": repos}

@router.delete("/api/v1/repos/{repo_id}")
async def delete_repo(repo_id: str):
    """Delete an uploaded repository"""
    repo_path = UPLOAD_DIR / repo_id
    if not repo_path.exists():
        raise HTTPException(404, "Repository not found")
    
    shutil.rmtree(repo_path)
    return {"message": f"Repository {repo_id} deleted successfully"}
