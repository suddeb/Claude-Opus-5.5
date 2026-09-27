case_tool = {
    "name": "create_case",
    "description": "Create a support case in the CRM.",
    "strict": True,  # ✅ inputs are guaranteed to match input_schema
    "input_schema": {
        "type": "object",
        "properties": {
            "subject":  {"type": "string"},
            "priority": {"type": "string", "enum": ["Low", "Medium", "High"]},

        },
        "required": ["subject", "priority"],
        "additionalProperties": False,
    },
}

response = client.messages.create(
    model="claude-opus-5-5",
    max_tokens=4096,
    tools=[case_tool],
    tool_choice={"type": "auto"},  # ✅ only "auto" or "none" on 5.5
    messages=[{
        "role": "user",
        "content": "Customer says checkout is down for all users. "
                   "Use the create_case tool.",  # direct it in the prompt instead
    }],
)
