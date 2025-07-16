import argparse
import os
import asyncio
import hashlib
import json
from datetime import datetime
from agents.bug_hunter_agent import BugHunterAgent
from utils.hash_tracker import compute_file_hash, load_hash_cache, save_hash_cache
from utils.contract_scanner import get_all_solidity_files

async def analyze_file(file_path, agent, skip_hashes, only_critical, save_dir):
    file_hash_now = compute_file_hash(file_path)
    if skip_hashes.get(file_path) == file_hash_now:
        print(f"⏩ Skipping unchanged file: {file_path}")
        return

    print(f"🔍 Analyzing: {file_path}")
    with open(file_path) as f:
        solidity_code = f.read()

    await agent.on_message(
        solidity_code,
        file_path=file_path,
        only_critical=only_critical,
        save_per_contract=save_dir is not None,
        output_dir=save_dir
    )
    skip_hashes[file_path] = file_hash_now


def main():
    parser = argparse.ArgumentParser(description="Bug Hunter CLI Runner")
    parser.add_argument("--dir", default="contracts", help="Directory of Solidity files")
    parser.add_argument("--only-critical", action="store_true", help="Only show critical/high issues")
    parser.add_argument("--save-per-contract", action="store_true", help="Save separate report per contract")
    parser.add_argument("--json", action="store_true", help="Export raw JSON from Slither")
    parser.add_argument("--skip-unchanged", action="store_true", help="Skip files that haven't changed")

    args = parser.parse_args()
    solidity_files = get_all_solidity_files(args.dir)
    if not solidity_files:
        print("❌ No Solidity files found.")
        return

    print(f"📦 Found {len(solidity_files)} contract(s)")
    hashes_path = ".cache_hashes.json"
    old_hashes = load_hash_cache(hashes_path) if args.skip_unchanged else {}

    agent = BugHunterAgent(selected_tools=["slither"], json_mode=args.json)

    async def run_all():
        for path in solidity_files:
            await analyze_file(
                path,
                agent,
                old_hashes,
                only_critical=args.only_critical,
                save_dir="per_contract_reports" if args.save_per_contract else None
            )

    asyncio.run(run_all())

    if args.skip_unchanged:
        save_hash_cache(hashes_path, old_hashes)


if __name__ == "__main__":
    main()
