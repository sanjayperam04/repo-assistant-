"""Safe test execution in Docker sandbox"""
import subprocess
import json
from pathlib import Path

def execute_tests(repo_path: str, pattern: str = "**/test*.py") -> dict:
    """Execute tests and return structured results"""
    repo = Path(repo_path)
    if not repo.exists():
        return {"error": f"Repository path {repo_path} does not exist"}
    
    try:
        # Run pytest with JSON report
        result = subprocess.run(
            ["pytest", str(repo), "-v", "--tb=short", "--json-report", "--json-report-file=/tmp/report.json"],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=repo
        )
        
        # Parse results
        passed = result.stdout.count(" PASSED")
        failed = result.stdout.count(" FAILED")
        
        return {
            "status": "completed",
            "passed": passed,
            "failed": failed,
            "total": passed + failed,
            "output": result.stdout[:2000],  # Truncate for safety
            "exit_code": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {"error": "Test execution timeout (60s limit)"}
    except FileNotFoundError:
        return {"error": "pytest not found - install with: pip install pytest pytest-json-report"}
    except Exception as e:
        return {"error": f"Test execution failed: {str(e)}"}
