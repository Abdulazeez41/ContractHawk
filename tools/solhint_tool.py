from agentopera.core.tools import FunctionTool
import subprocess
import json
import os

def run_solhint(file_path: str):
    abs_file_path = os.path.abspath(file_path)
    cmd = f"npx solhint {abs_file_path} --formatter json"

    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        output = result.stdout.strip()

        try:
            parsed_json = json.loads(output)
        except json.JSONDecodeError:
            parsed_json = []

        parsed = {
            "Solhint": []
        }
        for item in parsed_json:
            parsed["Solhint"].append({
                "message": item.get("message"),
                "line": item.get("line"),
                "ruleId": item.get("ruleId"),
                "severity": item.get("severity"),
            })

        return {
            "success": result.returncode == 0 or bool(parsed["Solhint"]),
            "output": output,
            "error": result.stderr.strip(),
            "parsed_findings": parsed,
            "raw_json": parsed_json
        }
    except Exception as e:
        return {
            "success": False,
            "output": "",
            "error": str(e),
            "parsed_findings": {},
            "raw_json": []
        }

solhint_tool = FunctionTool(
    func=run_solhint,
    name="solhint",
    description="Run Solhint linter and parse linting issues"
)
