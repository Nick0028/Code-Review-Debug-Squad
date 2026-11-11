# Code Review & Debug Squad — Local LLM Edition

A Streamlit multi-agent code review MVP using **Ollama locally** (no Gemini/OpenAI API key).
It includes four LangChain agents: Bug Finder, Style/Lint, Fixer and Test Writer.
ChromaDB retrieves local coding guidance; Python AST and Ruff provide static checks.
Generated pytest tests run in a disposable Docker container with networking disabled.

## Requirements
- Windows 10/11
- Python 3.10–3.12 recommended
- Ollama for Windows
- 8 GB RAM minimum recommended for a quantized 7B model; 16 GB+ is preferable
- Docker Desktop for isolated test execution

## 1. Install Ollama and download a model

Install Ollama from https://ollama.com/download

In PowerShell:

```powershell
ollama pull qwen2.5-coder:7b
ollama run qwen2.5-coder:7b
```

Try a coding question, then type `/bye`. If your computer has limited RAM, use
`qwen2.5-coder:3b` and update `OLLAMA_MODEL` in `.env`.

## 2. Set up the Python project

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

No API key is required. The `.env` file is already configured for local Ollama.

## 3. Build the test sandbox image

Install and start Docker Desktop, then run this in the project root:

```powershell
docker build -f Dockerfile.sandbox -t code-review-sandbox:latest .
```

## 4. Start the app

Make sure Ollama is running:

```powershell
streamlit run app.py
```

## Architecture
Streamlit -> Orchestrator -> ChromaDB retrieval -> four LangChain agents using local Ollama ->
Docker test runner -> Markdown report.

## Notes
- All four LLM agents use local Ollama; no Gemini or OpenAI API is called.
- ChromaDB embeddings use a local Sentence Transformers model. First use downloads model weights.
- Python-only MVP.
- LLM suggestions can be wrong; inspect fixes.
- The quality score is heuristic, not an industry-standard metric.
- Docker is required for isolated test execution.
