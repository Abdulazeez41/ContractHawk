from agentopera.core.tools import FunctionTool
import subprocess
import json
import os

def run_mythril(file_path: str):
    abs_file_path = os.path.abspath(file_path)
    cmd = f"myth analyze {abs_file_path} --execution-timeout 60 --max-depth 30 --solv 0.8.24 --outform json"

    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=90)
        output = result.stdout.strip()

        try:
            json_data = json.loads(output)
        except json.JSONDecodeError:
            return {
                "success": False,
                "output": output,
                "error": "Failed to parse Mythril JSON output",
                "parsed_findings": {},
                "raw_json": {}
            }

        parsed = {
            "High": [],
            "Medium": [],
            "Low": [],
            "Unknown": []
        }

        for issue in json_data.get("issues", []):
            severity = issue.get("severity", "Unknown")
            category = severity.capitalize() if severity.capitalize() in parsed else "Unknown"
            parsed[category].append({
                "title": issue.get("title"),
                "description": issue.get("description"),
                "contract": issue.get("contract"),
                "function": issue.get("function"),
                "line": issue.get("lineno"),
                "swc-id": issue.get("swc-id"),
                "severity": severity,
            })

        return {
            "success": bool(json_data.get("issues")) or result.returncode == 0,
            "output": output,
            "error": result.stderr.strip(),
            "parsed_findings": {"Mythril": parsed},
            "raw_json": json_data
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "output": "",
            "error": f"Command '{cmd}' timed out after 90 seconds",
            "parsed_findings": {},
            "raw_json": {}
        }
    except Exception as e:
        return {
            "success": False,
            "output": "",
            "error": str(e),
            "parsed_findings": {},
            "raw_json": {}
        }


mythril_tool = FunctionTool(
    func=run_mythril,
    name="mythril",
    description="Run Mythril symbolic analyzer and parse vulnerabilities"
)