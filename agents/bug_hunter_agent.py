import os
import json
from datetime import datetime
from agentopera.core import CancellationToken
from agentopera.chatflow.messages import TextMessage
from agents.static_analyzer import StaticAnalyzerAgent
from agents.explainer_agent import ExplainerAgent
from tools.tool_registry import TOOL_REGISTRY

class BugHunterAgent:
    def __init__(self, log_dir="logs", selected_tools=["slither_analyzer", "mythril", "solhint"]):
        self.tools = [TOOL_REGISTRY[name] for name in selected_tools if name in TOOL_REGISTRY]
        self.analyzer_agent = StaticAnalyzerAgent(custom_tools=self.tools)
        self.explainer_agent = ExplainerAgent()
        os.makedirs(log_dir, exist_ok=True)
        self.log_dir = log_dir

    async def on_message(self, solidity_code: str, file_path: str):
        with open(file_path, "w") as f:
            f.write(solidity_code)

        all_results = []
        for tool in self.tools:
            print(f"\n🛠️ Running {tool.name}...")
            result = await tool.run_json({"file_path": file_path}, CancellationToken())
            all_results.append((tool.name, result))

        timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
        log_path = os.path.join(self.log_dir, f"report-{timestamp}.txt")

        total_issues = 0
        severity_totals = {
            "High": 0,
            "Critical": 0,
            "Medium": 0,
            "Low": 0,
            "Info": 0,
            "Warnings": 0,
            "Errors": 0
        }

        all_findings = []

        with open(log_path, "w") as log_file:
            for tool_name, response in all_results:
                log_file.write(f"\n=== {tool_name.upper()} REPORT ===\n")
                print(f"\n=== {tool_name.upper()} REPORT ===\n")

                if response.get("success"):
                    parsed = response.get("parsed_findings", {})
                    if response.get("success") or parsed:
                        print(f"📦 Raw result for {tool_name}:")
                        print(json.dumps(parsed, indent=2))

                        tool_issues = 0
                        tool_parsed = parsed.get(tool_name, parsed)

                        if isinstance(tool_parsed, dict):
                            for category, issues in tool_parsed.items():
                                if not isinstance(issues, list):
                                    continue
                                tool_issues += len(issues)

                                category_normalized = category.capitalize()
                                if category_normalized not in severity_totals:
                                    category_normalized = "Info"

                                severity_totals[category_normalized] += len(issues)
                                for issue in issues:
                                    all_findings.append({
                                        "tool": tool_name,
                                        "severity": category_normalized,
                                        **issue
                                    })
                                    log_file.write(f"[{category.upper()}] {json.dumps(issue, indent=2)}\n")
                                    print(f"[{category.upper()}] {json.dumps(issue, indent=2)}\n")
                        else:
                            log_file.write(f"[INFO] {tool_parsed}\n")
                            print(f"[INFO] {tool_parsed}\n")

                        total_issues += tool_issues
                        log_file.write("\n")
                    else:
                        error = response.get("error", "Unknown error")
                        print(f"❌ {tool_name} failed:\n{error}")
                        log_file.write(f"ERROR: {error}\n")

        real_vulnerabilities = (
            severity_totals.get("High", 0) +
            severity_totals.get("Medium", 0) +
            severity_totals.get("Critical", 0)
        )
        lint_warnings = (
            severity_totals.get("Warnings", 0) +
            severity_totals.get("Errors", 0) +
            severity_totals.get("Info", 0)
        )

        print("\n🔴 HIGH-SEVERITY ISSUES:")
        print(f"- High: {severity_totals['High']}")
        print(f"- Medium: {severity_totals['Medium']}")
        print(f"- Critical: {severity_totals['Critical']}")

        print("\n🟠 STYLE/DOCUMENTATION WARNINGS:")
        print(f"- Info: {severity_totals['Info']}")
        print(f"- Warnings: {severity_totals['Warnings']}")
        print(f"- Errors: {severity_totals['Errors']}")

        print("\n🟢 TOTAL ISSUES FOUND:")
        print(f"- Total: {total_issues} issue(s) found across 1 contract.")

        print(f"\n📝 Report saved to: {log_path}")

        if total_issues > 0:
            explanation_prompt = f"""
You are a smart contract security expert.

The following are vulnerability and lint findings from multiple tools. Please do the following for each issue:

1. Explain what the issue means in simple terms for a developer.
2. Recommend specific fixes or solutions for the issue.
3. Mention best practices if applicable.

Use clear formatting. Here's the list of issues:

{json.dumps(all_findings, indent=2)}

Total Issues: {total_issues}
High: {severity_totals['High']}
Medium: {severity_totals['Medium']}
Low: {severity_totals['Low']}
Critical: {severity_totals['Critical']}
Lint Warnings/Info: {lint_warnings}
"""
            explanation = await self.explainer_agent.on_messages([
                TextMessage(content=explanation_prompt, source="user")
            ])
            print(f"\n📘 Explanation:\n{explanation}")

            with open(log_path, "a") as log_file:
                log_file.write("\n=== EXPLANATION & SOLUTIONS ===\n")
                log_file.write(explanation + "\n")
