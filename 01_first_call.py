# 01_first_call.py

import anthropic
client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-5-5",            # no date suffix
    max_tokens=8000,                    # covers thinking + visible text
    output_config={"effort": "medium"}, # the one dial; medium is the default
    messages=[{
        "role": "user",
        "content": "Explain the trade-offs of event-driven vs request/response "
                   "integration for a CRM in 5 bullet points.",
    }],
)

# Read by block type — the first block is usually 'thinking', not 'text'
for block in response.content:
    print(block.type)
    if block.type == "text":
        print(block.text)

print("\nUsage:", response.usage)
