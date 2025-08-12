# Google ADK - Get Started

## Create the Project Directory
```
mkdir google-adk-get-started
````

---

## First Agent Setup

### 1. Create the `multi_tool_agent` directory and files

```bash
mkdir multi_tool_agent/
echo "from . import agent" > multi_tool_agent/__init__.py
touch multi_tool_agent/agent.py
touch multi_tool_agent/.env
```

---

### 2. Configure `.env`

Copy and paste the following into `multi_tool_agent/.env`:

```env
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=
```

---

### 3. Add the Agent Code

Open the following link and copy the contents of `agent.py`:

🔗 [multi\_tool\_agent/agent.py](https://github.com/spritlesoftware/google-adk-get-started/blob/master/multi_tool_agent/agent.py)

Paste the copied code into:

```
multi_tool_agent/agent.py
```
