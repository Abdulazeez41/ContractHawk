# 🦅 ContractHawk – Watchful Eyes on Every Line of Code

> A smart contract vulnerability analyzer combining **Slither**, **Mythril**, and **Solhint** with **AI-powered explanations** — to help developers catch real issues before deployment.

---

## 📌 What is ContractHawk?

**ContractHawk** is an automated Solidity contract analysis tool designed to detect vulnerabilities, code quality issues, and documentation gaps. It uses industry-standard tools:

- **Slither** – for static analysis and reentrancy detection
- **Mythril** – for symbolic execution-based bug detection
- **Solhint** – for linting and NatSpec enforcement

Plus, it adds a unique layer of **AI-powered explanation**, making complex findings easy to understand for developers at all skill levels.

---

## 🔍 Features

✅ Detects common security issues:

- Reentrancy
- Low-level calls
- Unchecked send values
- Integer overflow/underflow
- Timestamp dependence
- And more...

✅ Enforces clean code standards:

- Missing NatSpec tags (`@title`, `@author`, `@notice`)
- Use of strict inequalities
- Explicit type declarations

🧠 **AI-Powered Explainer**

- Converts technical findings into developer-friendly language
- Highlights the impact and how to fix each issue

📦 Modular architecture:

- Docker-first design
- Tool registry system
- Easy to extend with new analyzers or linters

---

## 🧰 Supported Tools

| Tool        | Purpose            | Description                                              |
| ----------- | ------------------ | -------------------------------------------------------- |
| **Slither** | Security Analyzer  | Detects high-sev issues like reentrancy, unchecked calls |
| **Mythril** | Symbolic Execution | Finds runtime bugs and edge cases                        |
| **Solhint** | Linter             | Enforces best practices and style guides                 |

---

## 🛠️ Installation & Usage

### 1. Clone the Repo

```bash
git clone https://github.com/yourname/contracthawk.git
cd contracthawk
```

### 2. Build and Run with Docker

```bash
docker compose up --build
```

This will:

- Analyze your `.sol` files in `contracts/`
- Output results to terminal and logs
- Explain findings using AI (via API)

---

## 📁 Folder Structure

```
.
├── contracts/              # Place your Solidity contracts here
├── logs/                   # Analysis reports are saved here
├── tools/                  # Tool integrations (Slither, Mythril, Solhint)
├── agents/                 # Core agent logic (BugHunterAgent, ExplainerAgent)
├── core/                   # Utilities and parsers
├── docker-compose.yml      # Docker setup for multi-tool execution
├── Dockerfile              # Base image for ContractHawk
├── requirements.txt        # Python dependencies
└── README.md               # You're reading it!
```

---

## 🧪 Example Vulnerable Contract

```solidity
pragma solidity ^0.8.24;

contract ReentrancyVictim {
    mapping(address => uint) public balances;

    function deposit() external payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw(uint amount) external {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        (bool sent, ) = msg.sender.call{value: amount}("");
        require(sent, "Failed to send Ether");
        balances[msg.sender] -= amount;
    }
}
```

This contract has a **reentrancy vulnerability**, which ContractHawk will clearly identify.

---

## 📊 Sample Output

```
🔴 REAL SECURITY VULNERABILITIES:
- High/Critical issues: 1
- Medium issues: 0
- Low issues: 1

🟠 STYLE/DOCUMENTATION WARNINGS:
- Linting warnings/info: 14

🟢 ALL ISSUES FOUND:
- Total: 16 issue(s) found across 1 contract.
```

And you'll get an AI-generated explanation like:

```
📘 Explanation:
Found 1 high-severity vulnerability — this is likely a reentrancy bug.
Review the function 'withdraw' where external calls happen before state updates.
```

---

## 📋 Roadmap

Future plans include:

- [ ] Add support for Foundry and Hardhat projects
- [ ] Export findings as SARIF or JSON format
- [ ] Integrate with CI/CD pipelines
- [ ] Add rule filtering (`--only-critical`)
- [ ] Create web UI for visual reporting

---

## 💬 Want to Contribute?

We welcome contributions from the community!

### Ways to Help:

- Add support for more detectors
- Improve parsing of tool outputs
- Create AI prompt templates for better explanations
- Build a frontend dashboard
- Write documentation and tutorials

---

## 📦 Folder Structure

```
.
├── contracts/              # Place your Solidity contracts here
├── logs/                   # Analysis reports are saved here
├── tools/                  # Tool integrations (Slither, Mythril, Solhint)
├── agents/                 # Core agent logic (BugHunterAgent, ExplainerAgent)
├── core/                   # Utilities and parsers
├── docker-compose.yml      # Docker setup for multi-tool execution
├── Dockerfile              # Base image for ContractHawk
├── requirements.txt        # Python dependencies
└── README.md               # You're reading it!
```

---

## 📝 License

MIT License – see `LICENSE` for details.

---

## 📢 Contact

Have questions or feedback?  
📧 Reach out via GitHub Issues or Discussions.

---

## 🏷️ Keywords

Smart Contract, Security Analyzer, Slither, Mythril, Solhint, Vulnerability Detection, Reentrancy, Gas Optimization, Solidity, Blockchain Security, Developer Tool, AI Explainer
