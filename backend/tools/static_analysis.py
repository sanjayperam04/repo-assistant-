"""Static code analysis using Ruff"""
import subprocess
from pathlib import Path

def analyze(repo_path: str, file_pattern: str = "**/*.py") -> dict:
    """Run static analysis and return violations"""
    repo = Path(repo_path)
    if not repo.exists():
        return {"error": f"Repository path {repo_path} does not exist"}
    
    try:
        # Run ruff
        result = subprocess.run(
            ["ruff", "check", str(repo), "--output-format=json"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        violations = []
        if result.stdout:
            import json
            violations = json.loads(result.stdout)
        
        return {
            "status": "completed",
            "total_violations": len(violations),
            "violations": violations[:50],  # Top 50
            "summary": summarize_violations(violations)
        }
    except FileNotFoundError:
        return {"error": "ruff not found - install with: pip install ruff"}
    except Exception as e:
        return {"error": f"Analysis failed: {str(e)}"}

def summarize_violations(violations: list) -> dict:
    """Summarize violations by severity"""
    summary = {"error": 0, "warning": 0, "info": 0}
    for v in violations:
        level = v.get("level", "warning")
        summary[level] = summary.get(level, 0) + 1
    return summary
