import os
from google import genai
from google.genai import types
from tools.meal_tools import find_suitable_meal

# Initialize the Gemini client (reads os.environ["GEMINI_API_KEY"])
client = genai.Client()

# 1. Use the SDK's official types to build a clean schema contract
meal_tool_declaration = types.FunctionDeclaration(
    name="find_suitable_meal",
    description="Finds the meal closest to the target calories and checks the pantry for missing ingredients.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "calorie_target": types.Schema(
                type=types.Type.INTEGER,
                description="The target number of calories the user wants for the meal."
            )
        },
        required=["calorie_target"],
    ),
)

def run_agent_loop(user_prompt: str):
    print(f"User Prompt: '{user_prompt}'\n")
    print("🤖 Agent is reasoning...")

    # 2. Pass the explicit schema declaration into the model config
    response = client.models.generate_content(
        model='gemini-3.5-flash',
        contents=user_prompt,
        config={
            'tools': [types.Tool(function_declarations=[meal_tool_declaration])]
        }
    )

    # 3. Check if Gemini requested a tool execution
    if response.function_calls:
        for function_call in response.function_calls:
            print(f"🔧 Agent decided to call tool: {function_call.name}")
            print(f"📥 Arguments extracted by LLM: {function_call.args}")

            if function_call.name == "find_suitable_meal":
                calorie_target = function_call.args.get("calorie_target")
                
                # Execute your local Python function (the "muscle")
                tool_result = find_suitable_meal(calorie_target=calorie_target)
                print(f"📤 Tool Execution Result: {tool_result}\n")
                
                print("✨ Agent is formatting the final observation...")
                
                # 4. Feed the tool output back to Gemini to generate the final human response
                final_response = client.models.generate_content(
                    model='gemini-3.5-flash',
                    contents=[
                        user_prompt,
                        f"Tool Execution Result: {tool_result}"
                    ]
                )
                print(f"\nFinal Answer:\n{final_response.text}")
    else:
        print(f"\nFinal Answer:\n{response.text}")

if __name__ == "__main__":
    run_agent_loop("Hey, I need a meal plan around 300 calories today.")