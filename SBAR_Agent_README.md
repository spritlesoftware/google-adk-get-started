# SBAR Agent - Google ADK Example

This project demonstrates building an **SBAR Agent** using the **Google Agent Development Kit (ADK)**.  
The agent works with a local SQLite database populated from a CSV file.

---

## 📦 Installation

### 1. Install Required Python Package
We need `pysqlite3-binary` for SQLite support and  `mcp-server-sqlite` for Sqlite MCQ:

```bash
pip3 install pysqlite3-binary
pip3 install mcp-server-sqlite 
````

---

## 📂 Prepare Data

### 2. Download Example Script and Dataset

Download the CSV-to-database script and the example patient dataset:

```bash
wget https://raw.githubusercontent.com/spritlesoftware/google-adk-get-started/refs/heads/master/csv_to_db.py
wget https://raw.githubusercontent.com/spritlesoftware/google-adk-get-started/refs/heads/master/sbar_notes_emergency_room_patients_week.csv
```

---

### 3. Generate the Database

Run the script to convert the CSV file into a SQLite database:

```bash
python3 csv_to_db.py
```

This will create a `patients.db` file in your project directory.

---

## 🛠 Create the SBAR Agent

### 4. Create Project Directory and Files

```bash
mkdir sbar_agent
echo "from . import agent" > sbar_agent/__init__.py
touch sbar_agent/agent.py
touch sbar_agent/.env
```

---

### 5. Configure Environment Variables

Open `sbar_agent/.env` and set your configuration:

```env
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=your_google_api_key_here
```

---

### 6. Add the Agent Code

Open the following link and copy the code into `sbar_agent/agent.py`:

🔗 [SBAR Agent Code](https://github.com/spritlesoftware/google-adk-get-started/blob/master/sbar_agent/agent.py)

---

## 🚀 Run the Agent

After setting up, you can run your SBAR agent with:

```bash
adk web
```
