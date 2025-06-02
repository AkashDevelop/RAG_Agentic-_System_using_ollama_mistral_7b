from openai import AsyncOpenAI
from config.settings import settings
from . import TOOL_REGISTRY
import json
import logging

client= AsyncOpenAI(
     base_url=settings.LLM_BASE_URL,
    api_key="ollama"
)

system_prompt= """
You are a federal register assistant.use these tools to answer quetions about us regulations.
when using tools:
1. use sql_search for specific keywords and date range
2. use vector_search for conceptual or broad queries
ALways summarize results in your response.

"""

async def execute_agent(user_query: str):

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query}
    ]

    response = await client.chat.completions.create(
        model=settings.LLM_MODEL,
        messages=messages,
        tools=[tool["schema"] for tool in TOOL_REGISTRY.values()],
        tool_choice="auto"
    )

    tool_calls = response.choices[0].message.tool_calls

    if tool_calls:
        for call in tool_calls:
            func_name = call.function.name
            try:
                kwargs = json.loads(call.function.arguments)  # ✅ FIXED
                if func_name in TOOL_REGISTRY:
                    result = await TOOL_REGISTRY[func_name]["function"](**kwargs)
                    messages.append({
                        "role": "tool",
                        "tool_call_id": call.id,
                        "name": func_name,
                        "content": json.dumps(result, default=str)  # ✅ json.dumps not json.dump
                    })
            except Exception as e:
                logging.error(f"Tool execution failed: {str(e)}")
                messages.append({
                    "role": "tool",
                    "tool_call_id": call.id,
                    "name": func_name,
                    "content": f"error: {str(e)}"
                })

    # Now i ask LLM to summarize final results
    final_response = await client.chat.completions.create(
        model=settings.LLM_MODEL,
        messages=messages
    )

    return final_response.choices[0].message.content
