import time, anthropic

client = anthropic.Anthropic()

for label, kwargs in [
    ("standard", {"output_config": {"effort": "medium"}}),
    ("fast",     {"output_config": {"effort": "medium"}, "speed": "fast",
                  "betas": ["fast-mode-2026-02-01"]}),
]:
    t = time.perf_counter()
    r = client.beta.messages.create(
        model="claude-opus-5-5",
        max_tokens=4000,
        messages=[{"role": "user", "content": "Write a 300-word release note for an API upgrade."}],
        **kwargs,
    )

    print(f"{label:<9} {time.perf_counter() - t:5.1f}s  out_tokens={r.usage.output_tokens}  speed={r.usage.speed}")
