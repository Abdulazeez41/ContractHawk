import argparse
import asyncio
import hashlib
import json
import os
from datetime import datetime
from agents.bug_hunter_agent import BugHunterAgent
from utils.contract_scanner import find_all_solidity_files
from utils.hash_tracker import load_hashes, save_hashes
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn

DEFAULT_DIR = "contracts"
LOG_DIR = "logs"
HASH_CACHE = "cache/hashes.json"


async def analyze_contract(agent: BugHunterAgent, file_path: str, args) -> dict:
    with open(file_path, "r") as f:
        content = f.read()

    contract_hash = hashlib.sha256(content.encode()).hexdigest()
    if args.skip_unchanged and file_path in known_hashes and known_hashes[file_path] == contract_hash:
        return {"skipped": True, "path": file_path, "hash": contract_hash}

    result = await agent.on_message(content, file_path=file_path, return_summary=True)
    summary = result.get("summary")
    findings = result.get("findings", [])

    if args.only_critical:
        findings = [f for f in findings if f.get("severity", "").lower() == "critical"]
        if not findings:
            return {"skipped": True, "path": file_path, "hash": contract_hash}

    if args.save_per_contract:
        timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
        filename = os.path.basename(file_path).replace(".sol", "")
        out_path = os.path.join(LOG_DIR, f"{filename}-{timestamp}.{'json' if args.json else 'txt'}")
        os.makedirs(LOG_DIR, exist_ok=True)
        with open(out_path, "w") as f:
            if args.json:
                json.dump({"path": file_path, "summary": summary, "findings": findings}, f, indent=2)
            else:
                f.write(summary)

    known_hashes[file_path] = contract_hash
    return {"skipped": False, "path": file_path, "hash": contract_hash, "summary": summary, "findings": findings}


async def batch_scan(args):
    files = find_all_solidity_files(args.dir)
    agent = BugHunterAgent(selected_tools=["slither"])
    results = []

    with Progress(
        SpinnerColumn(),
        TextColumn("{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%")
    ) as progress:
        task = progress.add_task("Analyzing contracts...", total=len(files))

        for file_path in files:
            result = await analyze_contract(agent, file_path, args)
            results.append(result)
            progress.advance(task)

    save_hashes(HASH_CACHE, known_hashes)

    if args.json:
        output_path = os.path.join(LOG_DIR, f"batch_report-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}.json")
        with open(output_path, "w") as f:
            json.dump(results, f, indent=2)
        print(f"\n✅ Full batch results saved to {output_path}")
    else:
        for r in results:
            if not r.get("skipped"):
                print(f"\n--- {r['path']} ---\n{r['summary']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch scan Solidity contracts with BugHunterAgent")
    parser.add_argument("--dir", type=str, default=DEFAULT_DIR, help="Directory to scan")
    parser.add_argument("--json", action="store_true", help="Save full output in JSON format")
    parser.add_argument("--only-critical", action="store_true", help="Include only critical severity issues")
    parser.add_argument("--save-per-contract", action="store_true", help="Save individual report files per contract")
    parser.add_argument("--skip-unchanged", action="store_true", help="Skip contracts that haven't changed since last scan")

    args = parser.parse_args()
    known_hashes = load_hashes(HASH_CACHE)
    asyncio.run(batch_scan(args))
