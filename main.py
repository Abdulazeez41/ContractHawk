import os
import sys
import glob
import asyncio
from dotenv import load_dotenv
from agents.bug_hunter_agent import BugHunterAgent

load_dotenv()

CONTRACT_DIR = "contracts"

def read_contract(file_path: str) -> str:
    if not os.path.isfile(file_path):
        print(f"❌ Contract not found: {file_path}")
        return None
    with open(file_path, "r") as f:
        return f.read()

def main():
    selected = ["slither", "mythril", "solhint"]
    agent = BugHunterAgent(selected_tools=selected)

    async def run_all():
        solidity_files = glob.glob(f"{CONTRACT_DIR}/*.sol")
        if not solidity_files:
            print(f"❌ No .sol files found in {CONTRACT_DIR}/")
            return

        for file_path in solidity_files:
            solidity_code = read_contract(file_path)
            if solidity_code:
                print(f"\n📄 Analyzing contract: {file_path}")
                print("🛠️ Running BugHunterAgent...\n")
                await agent.on_message(solidity_code, file_path=file_path)

    asyncio.run(run_all())

if __name__ == "__main__":
    main()
