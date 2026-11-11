
import json
import os

from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama


def get_llm():
    return ChatOllama(
        model=os.getenv("OLLAMA_MODEL", "qwen2.5-coder:7b"),
        base_url=os.getenv(
            "OLLAMA_BASE_URL",
            "http://localhost:11434"
        ),
        temperature=0.1,
        format="json",
    )


def ask_json(system_prompt: str, user_prompt: str) -> dict:
    safe_system_prompt = (
        system_prompt.replace("{", "{{").replace("}", "}}")
    )

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            safe_system_prompt
            + "\nReturn valid JSON only. Do not use markdown fences."
        ),
        ("human", "{input}"),
    ])

    response = (prompt | get_llm()).invoke({
        "input": user_prompt
    })

    content = response.content

    if isinstance(content, list):
        content = "".join(
            str(item.get("text", ""))
            if isinstance(item, dict)
            else str(item)
            for item in content
        )

    text = str(content).strip()

    if text.startswith("```"):
        text = text.split("\n", 1)[-1].rsplit("```", 1)[0].strip()

    try:
        result = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Ollama returned invalid JSON: {text[:800]}"
        ) from exc

    if not isinstance(result, dict):
        raise ValueError("Expected a JSON object from Ollama.")

    return result
