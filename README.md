# 🤖 Gemini Agentic Lab: Pilot Implementation
## Suitable Meal Agent

A lightweight, zero-framework Python implementation demonstrating the core mechanics of an **AI Agent Loop** using the official Google Genai SDK (`google-genai`) and Gemini.

---

## 🧭 Learning Scope
This project moves away from traditional deterministic control flows (`if/else`, hardcoded APIs) and explores foundational agentic concepts:
1. **Perception & Intent Extraction:** Translating natural language requests into structured parameters via LLM reasoning.
2. **Tool / Skill Execution:** Allowing the LLM to dynamically trigger local Python functions (acting as the agent's "muscle").
3. **Observation & Reflection:** Feeding tool execution outputs back into the chat history for final formatting and response generation.

---

## 🎯 Agent Skill & Purpose
* **Skill Name:** `find_suitable_meal`
* **Purpose:** Acts as a smart nutrition and inventory assistant. Given a user's target calorie constraint (e.g., *"I need a meal around 600 calories"*), the agent:
  1. Searches local meal data for the closest caloric match.
  2. Cross-references the kitchen inventory to check for missing ingredients.
  3. Returns a structured report detailing nutritional values and grocery status.

---

## 🛠️ Technical Architecture & Implementation

Unlike projects that hide mechanics behind massive orchestration libraries, this lab implements a **raw agent loop** in native Python.

### Directory Structure
```text
google
├── agent.py            # Agent code (google-genai)
├── data
│   └── mock_pantry.py  # Available ingredients from the kitchen (mock data)
└── tools
    └── meal_tools.py   # Local Python functions (the agent's tools)
```

### How the Agent Loop Works (`agent.py`)

1. **Model Call with Tools:** The script sends the user prompt to `gemini-3.5-flash` alongside an explicitly defined schema contract (`types.FunctionDeclaration`).
2. **Function Interception:** If Gemini decides a tool is required, it parses the arguments (e.g., `{'calorie_target': 600}`) and returns a function call request.
3. **Deterministic Execution:** Python intercepts the request, runs the local `find_suitable_meal` function, and fetches the result.
4. **Final Response Formatting:** The tool output is handed back to Gemini to convert the raw data into a polished, human-readable response.

---

## 🚀 Getting Started

### 1. Prerequisites & Environment Setup

Ensure you have Python 3.10+ installed. Clone the repository and set up your environment:

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

```

### 2. Configure API Key

Export your Gemini API key directly in your terminal session:

```bash
export GEMINI_API_KEY="your_actual_api_key_here"

```

### 3. Run the Agent Loop

Navigate to your agent directory and execute the script:

```bash
cd google
python3 agent.py

```
