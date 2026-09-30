import time
import anthropic

client = anthropic.Anthropic()

PRICE_IN, PRICE_OUT = 4 / 1_000_000, 20 / 1_000_000  # Opus 5.5 standard pricing, USD/token
PROMPT = (
    "A Salesforce org has 40M Case records. Design an archival strategy that "
    "keeps reporting working. Give a numbered plan, max 200 words."
)

print(f"{'effort':<8}{'secs':>7}{'in_tok':>9}{'out_tok':>9}{'cost_usd':>11}")

for effort in ["low", "medium", "high", "xhigh", "max"]:
    start = time.perf_counter()
    with client.messages.stream(
        model="claude-opus-5-5",
        max_tokens=64000,                  # generous: xhigh/max think a lot
        output_config={"effort": effort},
        messages=[{"role": "user", "content": PROMPT}],
    ) as stream:
        r = stream.get_final_message()

    secs = time.perf_counter() - start
    cost = r.usage.input_tokens * PRICE_IN + r.usage.output_tokens * PRICE_OUT

    print(f"{effort:<8}{secs:>7.1f}{r.usage.input_tokens:>9}"
          f"{r.usage.output_tokens:>9}{cost:>11.4f}")
