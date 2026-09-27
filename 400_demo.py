#!/usr/bin/env python3
"""
Technical Potpourri — Opus 5.5 video, SECTION 1 (Hook) screen recording.

Screen direction:
  Terminal — run a Python script using model="claude-opus-5-5" with
  thinking={"type": "disabled"}. Show the red 400 error. Zoom in on:
  "thinking.type.disabled" is not supported for this model.

Usage:
  python hook_400_demo.py            # the "broken" Opus 5 style call -> real 400 from the API
  python hook_400_demo.py --fixed    # the Opus 5.5 way (effort instead of thinking) -> works
  python hook_400_demo.py --offline  # no API call; prints the documented error (backup take only)

Requirements:
  pip install --upgrade anthropic
  export ANTHROPIC_API_KEY="sk-ant-..."
"""

import argparse
import json
import sys
import time

# ANSI colours for a readable terminal on camera
RED, AMBER, GREEN, DIM, BOLD, RESET = "\033[91m", "\033[93m", "\033[92m", "\033[2m", "\033[1m", "\033[0m"

MODEL = "claude-opus-5-5"
PROMPT = "Classify this support message: 'My invoice is wrong'"

# Error text as documented in the Opus 5.5 migration guide (used only with --offline)
DOCUMENTED_ERROR = (
    '"thinking.type.disabled" is not supported for this model. '
    'Use "thinking.type.adaptive" and "output_config.effort" to control thinking behavior.'
)


def banner(title: str, colour: str) -> None:
    print(f"\n{colour}{BOLD}{'─' * 64}\n  {title}\n{'─' * 64}{RESET}")


def show_request(kwargs: dict) -> None:
    """Print the request so the viewer sees exactly what was sent."""
    print(f"{DIM}client.messages.create({RESET}")
    for k, v in kwargs.items():
        print(f"    {AMBER}{k}{RESET}={json.dumps(v)},")
    print(f"{DIM}){RESET}\n")


def show_error(status: int, err_type: str, message: str) -> None:
    banner(f"✖  {status} — {err_type}", RED)
    print(f"{RED}{BOLD}{message}{RESET}\n")


def run_broken(client) -> None:
    """The Opus 5 habit: switch thinking off for a cheap, fast call."""
    import anthropic

    kwargs = {
        "model": MODEL,
        "max_tokens": 1024,
        "thinking": {"type": "disabled"},  # ❌ worked on Opus 5, rejected on Opus 5.5
        "messages": [{"role": "user", "content": PROMPT}],
    }
    banner("Opus 5 habit → Opus 5.5 model", AMBER)
    show_request(kwargs)
    try:
        client.messages.create(**kwargs)
        print(f"{GREEN}Unexpected: the request succeeded. Check the current docs — behaviour may have changed.{RESET}")
    except anthropic.BadRequestError as e:
        body = e.body if isinstance(e.body, dict) else {}
        err = body.get("error", {}) if isinstance(body.get("error"), dict) else {}
        show_error(e.status_code, err.get("type", "invalid_request_error"), err.get("message", str(e)))
        sys.exit(1)


def run_fixed(client) -> None:
    """The Opus 5.5 way: thinking is always on; effort is the dial."""
    kwargs = {
        "model": MODEL,
        "max_tokens": 2048,                 # thinking tokens count toward max_tokens
        "output_config": {"effort": "low"},  # ✅ replaces thinking: disabled
        "messages": [{"role": "user", "content": PROMPT}],
    }
    banner("Opus 5.5 way — effort instead of thinking", GREEN)
    show_request(kwargs)
    start = time.perf_counter()
    r = client.messages.create(**kwargs)
    secs = time.perf_counter() - start

    # Read by block type: the first block is usually 'thinking', not 'text'
    text = "".join(b.text for b in r.content if b.type == "text")
    print(f"{GREEN}{BOLD}✔ 200 OK{RESET}  {DIM}({secs:.1f}s, output_tokens={r.usage.output_tokens}){RESET}\n")
    print(text)


def run_offline() -> None:
    """Backup take only: no network. Prints the documented error text."""
    banner("Opus 5 habit → Opus 5.5 model  (offline replay)", AMBER)
    show_request({
        "model": MODEL,
        "max_tokens": 1024,
        "thinking": {"type": "disabled"},
        "messages": [{"role": "user", "content": PROMPT}],
    })
    time.sleep(1.2)  # a beat, as if waiting on the network
    show_error(400, "invalid_request_error", DOCUMENTED_ERROR)
    sys.exit(1)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = p.add_mutually_exclusive_group()
    g.add_argument("--fixed", action="store_true", help="run the working Opus 5.5 request")
    g.add_argument("--offline", action="store_true", help="print the documented error without calling the API")
    args = p.parse_args()

    if args.offline:
        run_offline()
        return

    import anthropic
    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY
    run_fixed(client) if args.fixed else run_broken(client)


if __name__ == "__main__":
    main()
