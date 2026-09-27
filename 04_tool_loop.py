messages = [{"role": "user", "content": "Customer says checkout is down. Log it."}]

while True:
    response = client.messages.create(
        model="claude-opus-5-5",
        max_tokens=8000,
        output_config={"effort": "medium"},
        tools=[case_tool],
        messages=messages,
    )

    # ✅ Append ALL blocks, thinking included — don't rebuild or filter
    messages.append({"role": "assistant", "content": response.content})
    tool_results = []
    for block in response.content:
        if block.type == "tool_use":
            result = f"Case created: {block.input['subject']} ({block.input['priority']})"
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": result,
            })

    if not tool_results:
        break

    messages.append({"role": "user", "content": tool_results})

print(next(b.text for b in response.content if b.type == "text"))
