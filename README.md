<div align="center">
<h1>💻 Code Agent:<br/>A Minimal, Terminal-First Coding Agent</h1>
</div>


**Code Agent** is a minimal, terminal-first coding agent that brings agentic code editing, file system access, and command execution into a lightweight CLI experience.

Inspired by tools like Claude Code, Code Agent enables large language models to iteratively reason, inspect codebases, modify files, and run commands through a transparent tool-use loop — without heavy frameworks or complex dependencies.


## ✨ Features

* **Agentic Coding Loop**
  Supports multi-step reasoning with iterative tool use (read, write, edit, search, run commands).

* **File-Aware Code Editing**
  Safely read, modify, and patch files with line numbers and uniqueness checks to prevent accidental changes.

* **Built-in Developer Tools**
  Native support for filesystem access, regex search, globbing, and shell execution.

* **Minimal & Hackable**
  Implemented with Python standard libraries only — easy to read, extend, and customize.

* **Model-Driven Workflow**
  Designed around modern LLM tool-use APIs, enabling tight feedback loops between reasoning and execution.


## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/Yuan-ManX/code-agent.git
cd code-agent

# Optional: create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Set your Anthropics API key
export ANTHROPIC_API_KEY="your_api_key_here"
```


## 💻 CLI Usage

Start the Code Agent:
```bash
python3 code_agent.py
```

Example CLI session:
```text
Code Agent | claude-opus-4-5 | /your/project/path
────────────────────────────────────────────────────────
❯ help
⏺ You can use the following tools: read, write, edit, glob, grep, bash
```


## 📂 Basic Operations

### 1️⃣ List project files
```text
❯ glob {"pat":"*.py"}
⏺ Glob(/path/to/file.py)
```

### 2️⃣ Read file contents
```text
❯ read {"path":"example.py","offset":0,"limit":10}
⏺ 1| import os
⏺ 2| import sys
...
```

### 3️⃣ Edit a file
```text
❯ edit {"path":"example.py","old":"print('Hello')","new":"print('Hello World')"}
⏺ ok
```

### 4️⃣ Run shell commands
```text
❯ bash {"cmd":"ls -la"}
⏺ total 56
⏺ -rw-r--r-- 1 user group 1234 Jan 12 12:00 example.py
...
```


## 📂 Commands

- `/c` - Clear conversation
- `/q` or `exit` - Quit


## 🎯 Philosophy

Code Agent is built around a simple idea:

> **Coding agents should be transparent, controllable, and easy to understand.**

Instead of hiding logic behind complex abstractions, Code Agent exposes the core agent loop directly — making it suitable for learning, experimentation, and building your own agentic developer tools.


## 🚀 Use Cases

* Exploring and editing unfamiliar codebases
* Prototyping agentic coding workflows
* Building custom AI developer tools
* Learning how modern code agents work under the hood

---

*Minimal by design. Powerful by composition.*
