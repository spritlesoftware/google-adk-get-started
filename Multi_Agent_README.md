# Multi-Agent - Google ADK Example

This example demonstrates setting up a **Multi-Agent** environment using **Google ADK**,  
with policy rules stored in a local SQLite database.

---

## 📦 Installation

### 1. Download Example Script and Policy Dataset
```bash
wget https://raw.githubusercontent.com/spritlesoftware/google-adk-get-started/refs/heads/master/csv_to_policy_db.py
wget https://raw.githubusercontent.com/spritlesoftware/google-adk-get-started/refs/heads/master/policy_rules.csv
````

---

### 2. Generate the Policy Database

Run the script to convert the CSV file into a SQLite database:

```bash
python3 csv_to_policy_db.py
```

This will create a `policy.db` file in your project directory.

---

## 🛠 Create the Multi-Agent Project

### 3. Create Directory and Files

```bash
mkdir multi_agent
echo "from . import agent" > multi_agent/__init__.py
touch multi_agent/agent.py
touch multi_agent/.env
```

---

### 4. Configure Environment Variables

Edit `multi_agent/.env` and set your configuration:

```env
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=your_google_api_key_here
```

---

### 5. Add Agent Code

Open the following link and copy the contents into `multi_agent/agent.py`:

🔗 [Multi-Agent Code](https://github.com/spritlesoftware/google-adk-get-started/blob/master/multi_agent/agent.py)

---

## 🚀 Run the Multi-Agent

After setup, run the agent with:

```bash
adk web
```
