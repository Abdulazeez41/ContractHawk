import os
import json
import subprocess
from typing import Dict, Any
from agentopera.core.tools import FunctionTool
from core.slither_parser import extract_findings_from_slither_json

def run_slither_analysis(file_path: str):
    abs_file_path = os.path.abspath(file_path)
    json_output_path = "/tmp/slither_output.json"
    cmd = ["slither", abs_file_path, "--json", json_output_path]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        stderr = result.stderr.strip()

        with open(json_output_path, "r") as f:
            slither_json = json.load(f)

        categorized = extract_findings_from_slither_json(slither_json)

        return {
            "success": True,
            "output": result.stdout.strip(),
            "error": stderr,
            "parsed_findings": categorized,
            "raw_json": slither_json,
            "issue_count": sum(len(v) for v in categorized.values())
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "output": "",
            "error": "⏳ Slither timed out.",
            "parsed_findings": {},
            "raw_json": {},
            "issue_count": 0
        }
    except Exception as e:
        return {
            "success": False,
            "output": "",
            "error": f"🚫 Slither failed: {str(e)}",
            "parsed_findings": {},
            "raw_json": {},
            "issue_count": 0
        }

slither_tool = FunctionTool(
    func=run_slither_analysis,
    name="slither_analyzer",
    description="Run Slither static analysis on a Solidity file and return categorized vulnerabilities"
)
