#!/usr/bin/env python3
"""
Code Agent — a minimal, terminal-first agentic coding assistant.
"""

import glob as globlib
import json
import os
import re
import subprocess
import urllib.request

# ======================
# Configuration
# ======================

API_URL = "https://api.anthropic.com/v1/messages"
MODEL = "claude-opus-4-5"
MAX_TOKENS = 8192
CWD = os.getcwd()

# ======================
# ANSI UI
# ======================

RESET, BOLD, DIM = "\033[0m", "\033[1m", "\033[2m"
BLUE, CYAN, GREEN, YELLOW, RED = (
    "\033[34m",
    "\033[36m",
    "\033[32m",
    "\033[33m",
    "\033[31m",
)


def separator():
    width = min(os.get_terminal_size().columns, 80)
    return f"{DIM}{'─' * width}{RESET}"


def bold(text: str) -> str:
    return f"{BOLD}{text}{RESET}"


def render_markdown(text: str) -> str:
    return re.sub(r"\*\*(.+?)\*\*", f"{BOLD}\\1{RESET}", text)


# ======================
# Tool Implementations
# ======================

def tool_read(args):
    path = args["path"]
    lines = open(path).readlines()
    offset = args.get("offset", 0)
    limit = args.get("limit", len(lines))
    selected = lines[offset : offset + limit]
    return "".join(
        f"{offset + i + 1:4}| {line}" for i, line in enumerate(selected)
    )


def tool_write(args):
    with open(args["path"], "w") as f:
        f.write(args["content"])
    return "ok"


def tool_edit(args):
    text = open(args["path"]).read()
    old, new = args["old"], args["new"]

    if old not in text:
        return "error: old_string not found"

    count = text.count(old)
    if not args.get("all") and count > 1:
        return (
            f"error: old_string appears {count} times; "
            "must be unique (set all=true to replace all)"
        )

    updated = text.replace(old, new, count if args.get("all") else 1)
    with open(args["path"], "w") as f:
        f.write(updated)
    return "ok"


def tool_glob(args):
    base = args.get("path", ".")
    pattern = f"{base}/{args['pat']}".replace("//", "/")
    files = globlib.glob(pattern, recursive=True)
    files = sorted(
        files,
        key=lambda f: os.path.getmtime(f) if os.path.isfile(f) else 0,
        reverse=True,
    )
    return "\n".join(files) or "none"


def tool_grep(args):
    regex = re.compile(args["pat"])
    hits = []
    for filepath in globlib.glob(args.get("path", ".") + "/**", recursive=True):
        try:
            for lineno, line in enumerate(open(filepath), 1):
                if regex.search(line):
                    hits.append(f"{filepath}:{lineno}:{line.rstrip()}")
        except Exception:
            continue
    return "\n".join(hits[:50]) or "none"


def tool_bash(args):
    result = subprocess.run(
        args["cmd"],
        shell=True,
        capture_output=True,
        text=True,
        timeout=30,
        cwd=CWD,
    )
    return (result.stdout + result.stderr).strip() or "(empty)"


# ======================
# Tool Registry
# ======================

TOOLS = {
    "read": (
        "Read a file with line numbers",
        {"path": "string", "offset": "number?", "limit": "number?"},
        tool_read,
    ),
    "write": (
        "Write content to a file (overwrite)",
        {"path": "string", "content": "string"},
        tool_write,
    ),
    "edit": (
        "Replace text in a file (requires unique match unless all=true)",
        {"path": "string", "old": "string", "new": "string", "all": "boolean?"},
        tool_edit,
    ),
    "glob": (
        "Find files by glob pattern",
        {"pat": "string", "path": "string?"},
        tool_glob,
    ),
    "grep": (
        "Search files using a regex pattern",
        {"pat": "string", "path": "string?"},
        tool_grep,
    ),
    "bash": (
        "Execute a shell command",
        {"cmd": "string"},
        tool_bash,
    ),
}


def run_tool(name, args):
    try:
        return TOOLS[name][2](args)
    except Exception as e:
        return f"error: {e}"


def tool_schema():
    schema = []
    for name, (desc, params, _) in TOOLS.items():
        props, required = {}, []
        for k, v in params.items():
            optional = v.endswith("?")
            base = v.rstrip("?")
            props[k] = {
                "type": "integer" if base == "number" else base
            }
            if not optional:
                required.append(k)
        schema.append(
            {
                "name": name,
                "description": desc,
                "input_schema": {
                    "type": "object",
                    "properties": props,
                    "required": required,
                },
            }
        )
    return schema


# ======================
# LLM API
# ======================

def call_llm(messages, system_prompt):
    payload = {
        "model": MODEL,
        "max_tokens": MAX_TOKENS,
        "system": system_prompt,
        "messages": messages,
        "tools": tool_schema(),
    }
    request = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode(),
        headers={
            "Content-Type": "application/json",
            "x-api-key": os.environ.get("ANTHROPIC_API_KEY", ""),
            "anthropic-version": "2023-06-01",
        },
    )
    return json.loads(urllib.request.urlopen(request).read())


# ======================
# Agent Loop
# ======================

SYSTEM_PROMPT = f"""
You are Code Agent, a terminal-based coding assistant.

Rules:
- Use tools to inspect files instead of guessing.
- Use edit only when the target string is known and stable.
- Prefer small, incremental changes.
- Do not fabricate file contents.
- Current working directory: {CWD}
""".strip()


def agent_loop(messages):
    while True:
        response = call_llm(messages, SYSTEM_PROMPT)
        blocks = response.get("content", [])
        tool_results = []

        for block in blocks:
            if block["type"] == "text":
                print(f"\n{CYAN}⏺{RESET} {render_markdown(block['text'])}")

            elif block["type"] == "tool_use":
                name = block["name"]
                args = block["input"]
                print(f"\n{GREEN}⏺ {name}{RESET}({DIM}{list(args.values())[0]}{RESET})")

                result = run_tool(name, args)
                preview = result.splitlines()[0][:80]
                print(f"  {DIM}⎿ {preview}{RESET}")

                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": block["id"],
                        "content": result,
                    }
                )

        messages.append({"role": "assistant", "content": blocks})

        if not tool_results:
            break

        messages.append({"role": "user", "content": tool_results})


# ======================
# CLI
# ======================

def main():
    print(f"{bold('Code Agent')} | {DIM}{MODEL} | {CWD}{RESET}\n")
    messages = []

    while True:
        try:
            print(separator())
            user_input = input(f"{BOLD}{BLUE}❯{RESET} ").strip()
            print(separator())

            if not user_input:
                continue
            if user_input in ("/q", "exit"):
                break
            if user_input == "/c":
                messages.clear()
                print(f"{GREEN}⏺ Conversation cleared{RESET}")
                continue

            messages.append({"role": "user", "content": user_input})
            agent_loop(messages)
            print()

        except (KeyboardInterrupt, EOFError):
            break
        except Exception as e:
            print(f"{RED}⏺ Error: {e}{RESET}")


if __name__ == "__main__":
    main()
