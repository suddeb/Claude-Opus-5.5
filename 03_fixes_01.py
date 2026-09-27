# BEFORE — Opus 5 (400 on Opus 5.5)

client.messages.create(
    model="claude-opus-5",
    max_tokens=1024,
    thinking={"type": "disabled"},          # ❌ not supported on 5.5
    messages=[{"role": "user", "content": "Classify: 'My invoice is wrong'"}],
)

# AFTER — Opus 5.5

client.messages.create(
    model="claude-opus-5-5",
    max_tokens=2048,                        # leave headroom: thinking still counts
    output_config={"effort": "low"},        # ✅ minimal thinking
    messages=[{"role": "user", "content": "Classify: 'My invoice is wrong'"}],
)
