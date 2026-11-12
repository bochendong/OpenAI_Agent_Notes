# OpenAI Agent Notes

Study notes and example code for the OpenAI Agents SDK.

## Project structure

```text
.
├── notebooks/
│   ├── basicCommuation.ipynb      # Basic agent interactions
│   ├── functionTool.ipynb         # Function tools
│   ├── handOff.ipynb              # Agent handoffs
│   ├── RunContextWrapper.ipynb    # Shared run context
│   └── sourceCommunication.ipynb # Image input and follow-up messages
├── Examples/NoteBookCreator/    # Agents that generate notebook sections
├── requirements.txt             # Python dependencies
├── check_env.py                 # Environment check script
└── README.md
```

## Quick start

### 1. Prerequisites

- Python 3.9+
- pip

### 2. Create a virtual environment

Create and activate a virtual environment if you do not already have one.

```bash
python3 -m venv venv

# macOS/Linux
source venv/bin/activate

# Windows
# venv\Scripts\activate
```

When the environment is active, your shell prompt displays `(venv)`.

### 3. Install dependencies

With the virtual environment active, run:

```bash
pip install -r requirements.txt
```

### 4. Configure your API key

Create a file named `.env` in the project root. Include the leading dot in the filename.

**From the command line**

```bash
# macOS/Linux
echo "OPENAI_API_KEY=your_api_key_here" > .env

# Windows (PowerShell)
echo "OPENAI_API_KEY=your_api_key_here" | Out-File -Encoding utf8 .env
```

**In a text editor**

Create `.env` and add the following line:

```dotenv
OPENAI_API_KEY=your_api_key_here
```

Sign in to the [OpenAI Platform](https://platform.openai.com/), open the API Keys page, and create a key. Replace `your_api_key_here` with that key. Keep the key private and out of version control.

### 5. Check your environment

With the virtual environment active, run:

```bash
python check_env.py
```

The script checks the Python version, virtual environment, installed dependencies, `.env` file, and API key configuration.

## Notebook examples

### `notebooks/basicCommuation.ipynb`

Basic agent runs, structured output with Pydantic models, and session management with `SQLiteSession`.

### `notebooks/functionTool.ipynb`

Custom tools defined with `@function_tool`, the built-in `WebSearchTool`, and chained tool calls.

### `notebooks/handOff.ipynb`

Multiple agents, handoffs between agents, and a routing agent.

### `notebooks/RunContextWrapper.ipynb`

Sharing context between tools and agents with `RunContextWrapper`.

### `notebooks/sourceCommunication.ipynb`

Image input and follow-up questions with a shared session.

## Main dependencies

- `openai` — OpenAI Python SDK
- `openai-agents` — OpenAI Agents SDK
- `pydantic` — Data validation
- `python-dotenv` — Environment variable management
- `jupyter` — Jupyter Notebook environment
- `httpx` — HTTP client
- `fastapi` — Optional web framework

See `requirements.txt` for the full list.

## Troubleshooting

### Type annotations on Python 3.9

If you encounter `TypeError: Unable to evaluate type annotation 'float | None'`, install `eval_type_backport`:

```bash
pip install eval_type_backport
```

### Asynchronous calls

`Runner.run()` is asynchronous. Call it with `await`:

```python
result = await Runner.run(agent, "Hello!")
```

## Notes

- Configure your OpenAI API key before running the examples.
- Some features may require paid OpenAI API access.
- Run the examples in a virtual environment.

## License

This project is for learning and research purposes.

## Contributing

Issues and pull requests are welcome.
