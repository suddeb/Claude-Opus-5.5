# Claude Opus 5.5 WILL Break Your Code (Fix These 3 Things)

Code samples for the **Technical Potpourri** video *"Claude Opus 5.5 WILL Break Your Code (Fix These 3 Things)"* (host: Sudipta Deb).

YouTube Video Link: 

Opus 5.5 was released on 22 Sep 2026. These scripts show the new `effort` control, the three breaking changes you hit when you swap the model ID, and fast mode.

## What's new in Opus 5.5

| | Opus 5 | Opus 5.5 |
|---|---|---|
| Model ID | `claude-opus-5` | `claude-opus-5-5` (no date suffix) |
| Price (per 1M tokens, in / out) | $5 / $25 | $4 / $20 |
| Thinking | Configurable | **Always on** (adaptive), no `budget_tokens` |
| Default effort | `high` | `medium` |
| Terminal-Bench 4.0 | 52.3% | 66.4% |
| CursorBench 4.0 | 46.6 | 57.8 |
| FrontierCode | 48.0 | 54.4 |
| GDPval (Elo) | 1708 | 1846 |

- 1M token context window by default; up to 128K output tokens synchronously, 300K via the Batches API (beta).
- **Effort** is the single dial, set in `output_config`: `low`, `medium`, `high`, `xhigh`, `max`. At the same effort level, 5.5 tends to think more per turn than Opus 5, so don't carry over old settings.
- Thinking tokens count against `max_tokens`. Thinking text comes back empty by default (you get the block and a signature).
- **Fast mode** (research preview, Claude API only): up to 2.5x faster output at $8 / $40 per 1M tokens.
- Cache reads drop to $0.20 / 1M tokens, the minimum cacheable prompt drops to 512 tokens, and batch is still 50% off.

## Breaking changes

1. **You can't disable thinking.** `thinking={"type": "disabled"}` returns a 400. Delete the field and use `effort: "low"`.
2. **Forced tool use is gone.** `tool_choice` of type `any` or `tool` returns a 400; only `auto` and `none` are allowed. Use `strict: true` tools and name the tool in the prompt, or use structured outputs if you want guaranteed JSON.
3. **Keep thinking blocks in tool loops.** Append `response.content` back unmodified. Don't rebuild the assistant message from text and tool calls only. Also stop using `response.content[0].text`, because the first block is usually a thinking block.

Before flipping the model ID, grep your codebase for `thinking`, `tool_choice` and `content[0]`.

## Scripts

| File | Video step | What it shows |
|---|---|---|
| [400_demo.py](400_demo.py) | Section 1 — Hook | Reproduces the 400 from `thinking: disabled` (`--fixed` for the working call, `--offline` for a backup take) |
| [01_first_call.py](01_first_call.py) | Demo 2 | Minimal Opus 5.5 request with `effort`; reads the response by block type and prints usage |
| [02_effort_sweep.py](02_effort_sweep.py) | Demo 3 | Runs one prompt at all five effort levels and prints latency, tokens and cost at $4 / $20 |
| [03_fixes_01.py](03_fixes_01.py) | Demo 4 | Breaking change #1: replace `thinking: disabled` with `effort: "low"` |
| [03_fixes_02.py](03_fixes_02.py) | Demo 5 | Breaking change #2: strict tool use with `tool_choice: auto` |
| [04_tool_loop.py](04_tool_loop.py) | Demo 6 | Breaking change #3: tool loop that appends thinking blocks untouched |
| [05_fast_mode.py](05_fast_mode.py) | Demo 7 | Standard vs fast mode timing |

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install --upgrade anthropic      # older SDKs don't know output_config effort
export ANTHROPIC_API_KEY="sk-ant-..."
python -c "import anthropic; print(anthropic.__version__)"
python 01_first_call.py
```

## Notes

- **Effort sweep:** read all five answers and find where quality stops improving for your task. Measure cost per task, not cost per token, because more thinking per turn changes your real bill. Point the sweep at your hardest real prompt.
- **Fast mode** is not available on Bedrock, Vertex or Foundry yet, and you pay double per token, so use it where a human waits on latency. If it isn't enabled for your org, the call fails with an error about an organization rate limit of 0 fast mode input tokens per minute. See the [fast mode docs](https://platform.claude.com/docs/en/build-with-claude/fast-mode).

## Sources

- [Introducing Claude Opus 5.5 — Anthropic](https://www.anthropic.com/claude-opus-5-5)
- [What's new in Claude Opus 5.5](https://platform.claude.com/docs/en/models/opus-5-5/whats-new-opus-5-5)
- [Migrating to Claude Opus 5.5](https://platform.claude.com/docs/en/models/opus-5-5/migration-guide)
- VentureBeat — Opus 5.5 beats Fable 5.1 at 60% cheaper API price
- MacRumors — Anthropic Launches Claude Opus 5.5

Written version with the full migration checklist: sudipta-deb.in
