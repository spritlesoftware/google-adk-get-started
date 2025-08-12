# Google ADK - Get Started

## Create the Project Directory
```
mkdir google-adk-get-started
````

---

## First Agent Setup

### 1. Create the `single_agent` directory and files

```bash
mkdir single_agent/
echo "from . import agent" > single_agent/__init__.py
touch single_agent/agent.py
touch single_agent/.env
```

---

### 2. Configure `.env`

Copy and paste the following into `single_agent/.env`:

```env
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=
```

---

### 3. Add the Agent Code

Open the following link and copy the contents of `agent.py`:

🔗 [multi\_tool\_agent/agent.py](https://github.com/spritlesoftware/google-adk-get-started/blob/master/single_agent/agent.py)

Paste the copied code into:

```
single_agent/agent.py
```
