import os
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioConnectionParams, StdioServerParameters
root_agent = LlmAgent(
    model='gemini-2.0-flash',
    name='SBAR_sqlite_agent',
    instruction=(
        "You are an expert clinical assistant. Query the SQLite database's `medical_records` table "
        "using the MCP tool to retrieve the patient information using the given patient_id by the user, then synthesize it into a "
        "clear and concise SBAR handover note:\n"
        "- **Situation:** Brief current issue / reason for admission.\n"
        "- **Background:** Relevant medical history, medications, allergies, labs, imaging.\n"
        "- **Assessment:** Current condition, vitals, key findings, clinical interpretation.\n"
        "- **Recommendation:** Next steps, follow-up actions, and escalation if needed.\n"
        "Only output the SBAR summary in structured text or JSON — no extra commentary."
    ),
    tools=[
        MCPToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command='uvx',
                    args=[
                        "mcp-server-sqlite",
                        "--db-path",
                        "patient.db"
                    ],
                ),
            ),
        )
    ],
)