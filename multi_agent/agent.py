import os
import sys
from google.adk.agents import LlmAgent, BaseAgent, SequentialAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioConnectionParams, StdioServerParameters

policy_agent = LlmAgent(
    model='gemini-2.0-flash',
    name='policy_escalation_agent',
    instruction=(
        "Always get the SBAR report from the user first,without the SBAR data don't do any operations"
        "without first executing a database query. You have NO KNOWLEDGE of clinical rules.\n\n"
        
        "CRITICAL RESTRICTIONS:\n"
        "- You MUST NOT create, invent, or suggest any new policies or rules\n"
        "- You can ONLY use the exact rules retrieved from the database\n"
        "- If NO escalation criteria are met, return empty JSON array: []\n"
        "- If database query fails, respond with: 'ERROR: Cannot access clinical rules database'\n\n"
        
        "MANDATORY FIRST ACTION: Execute SQL query 'SELECT * FROM clinical_rules;' using the database tool.\n"
        
        "WORKFLOW:\n"
        "1. ALWAYS query database first: SELECT * FROM clinical_rules;\n"
        "2. Wait for database results\n"
        "3. Compare the given SBAR ONLY against the retrieved database rules\n"
        "4. If NO rules match or trigger: return []\n"
        "5. If rules match: return JSON array with matched rules only\n\n"
        
        "OUTPUT RULES:\n"
        "- If escalations found against the SBAR: JSON array with objects\n"
        "- If NO escalations found: []\n"
        "- Never create rules that don't exist in database\n"
        "- Never suggest new policies or criteria\n\n"
        
        "You are a database-dependent system that only applies existing rules to SBAR and gives the final JSON."
    ),
    tools=[
        MCPToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command='uvx',
                    args=[  
                        "mcp-server-sqlite", 
                        "--db-path",
                        "policy_rules.db"
                    ],
                ),
            ),
        )
    ],
)

patient_agent = LlmAgent(
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
                        "sbar_notes_emergency_room_patients_week.db"
                    ],
                ),
            ),
        )
    ],
)

summary_agent = LlmAgent(
    model='gemini-2.0-flash',
    name='summary_consolidation_agent',
    instruction=(
        "You are a clinical data consolidation agent that creates final structured reports.\n\n"
        
        "ROLE:\n"
        "- Consolidate the outputs from the previous agents into a single, well-formatted JSON response.\n"
        "- Cross-verify the escalation rules provided by the policy agent against the SBAR (Situation, Background, Assessment, Recommendation) data.\n"
        "- Remove any escalation entries that are not justified or supported by the SBAR data.\n"
        "- Ensure only relevant, SBAR-supported escalations remain in the final output.\n\n"
        
        "INPUT EXPECTATIONS:\n"
        "- SBAR data from the patient agent (structured clinical handover)\n"
        "- Escalation rules from the policy agent (JSON array of matched policies)\n\n"
        
        "OUTPUT FORMAT - MUST BE VALID JSON:\n"
        "{\n"
        "  \"patient_id\": \"<original_patient_id>\",\n"
        "  \"sbar\": {\n"
        "    \"situation\": \"<situation_text>\",\n"
        "    \"background\": \"<background_text>\",\n"
        "    \"assessment\": \"<assessment_text>\",\n"
        "    \"recommendation\": \"<recommendation_text>\"\n"
        "  },\n"
        "  \"escalations\": [\n"
        "    // Array of escalation objects from policy agent, filtered to only include SBAR-supported cases\n"
        "  ],\n"
        "  \"summary\": {\n"
        "    \"total_escalations\": <count>,\n"
        "    \"priority_level\": \"<LOW|MEDIUM|HIGH|CRITICAL>\",\n"
        "    \"requires_immediate_attention\": <boolean>,\n"
        "    \"next_actions\": [\"<action1>\", \"<action2>\"]\n"
        "  },\n"
        "}\n\n"
        
        "PRIORITY LEVELS:\n"
        "- CRITICAL: Life-threatening conditions requiring immediate intervention\n"
        "- HIGH: Urgent conditions requiring prompt attention within hours\n"
        "- MEDIUM: Important conditions requiring attention within 24 hours\n"
        "- LOW: Stable conditions with routine follow-up\n\n"
        
        "VALIDATION RULES:\n"
        "- Only use data provided by previous agents.\n"
        "- Do not invent or add new clinical information.\n"
        "- Ensure JSON is properly formatted and valid.\n"
        "- Base priority level on the filtered escalation list and SBAR clinical severity.\n"
        "- If SBAR data contradicts or does not support an escalation, remove that escalation from the output.\n"
        "- Include timestamp in ISO format.\n\n"
        
        "ERROR HANDLING:\n"
        "- If SBAR data is missing: include error in summary.\n"
        "- If escalation data is missing: set escalations to [].\n"
        "- Always produce valid JSON even with partial data."
    ),
)


root_agent = SequentialAgent(
    name="SBAR_Agent",
    sub_agents=[     
        patient_agent,
        policy_agent,
        summary_agent,
    ],
    description=(
        "Executes a three-step SBAR handover workflow for a given patient:\n"
        "1. **Patient Agent**: Queries the patient database and generates a structured SBAR summary "
        "containing Situation, Background, Assessment, and Recommendation.\n"
        "2. **Policy Agent**: Retrieves escalation policy rules from the policy database and applies "
        "them to the SBAR data to identify any matching escalation triggers.\n"
        "3. **Summary Agent**: Consolidates all outputs into a final structured JSON report with "
        "priority assessment and actionable recommendations.\n\n"
        
        "The final output is a comprehensive JSON object containing:\n"
        "- 'sbar': the generated SBAR summary\n"
        "- 'escalations': a JSON array of matched policy rules (or [] if none)\n"
        "- 'summary': consolidated assessment with priority level and next actions\n\n"
        
        "COORDINATION INSTRUCTION:\n"
        "Each agent in the sequence receives the cumulative output from all previous agents, "
        "ensuring proper data flow and context preservation throughout the workflow. "
        "No invented content allowed—only database-derived facts and rule-based assessments."
    )
)