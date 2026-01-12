# Code Agent

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
