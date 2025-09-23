import asyncio
import json
import re
import os # <-- Add this import
from google.adk.runners import Runner
from google.genai import types
from google.adk.sessions import InMemorySessionService
from dotenv import load_dotenv

# Import the fully assembled root agent from our coordinator module
from .agents.coordinator import root_agent

# Use a shared session service for the application
session_service = InMemorySessionService()

# Get the directory where this main.py script is located ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

async def main():
    print("--- Starting Autonomous Test Suite Generation System ---")
    
    # 1. Load the source code we want to test using an absolute path
    source_file_path = os.path.join(SCRIPT_DIR, "sample_code.py") 
    try:
        with open(source_file_path, "r") as f: 
            source_code_to_test = f.read()
    except FileNotFoundError:
        print(f"Error: `{source_file_path}` not found. Please ensure the file exists.")  
        return

    # 2. Instantiate the ADK Runner with our master agent
    runner = Runner(
        app_name="autotest_suite_generator",
        agent=root_agent,
        session_service=session_service
    )
    
    # 3. Create a session for this run
    session = await runner.session_service.create_session(
        app_name="autotest_suite_generator",
        user_id="end_user"
    )

    # 4. Format the initial user request as a JSON object
    initial_request = json.dumps({
        "source_code": source_code_to_test,
        "language": "python"
    })
    
    print(f"\n[USER REQUEST] Generating tests for:\n---\n{source_code_to_test}\n---\n")

    user_message = types.Content(
        role="user",
        parts=[types.Part(text=initial_request)]
    )

    # 5. Run the agent system and stream the process
    final_output = ""
    print("\n--- SYSTEM EXECUTION LOG ---")
    async for event in runner.run_async(
        user_id=session.user_id,
        session_id=session.id,
        new_message=user_message
    ):
        author = event.author
        content_text = ""
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    content_text += part.text + "\n"
        
        if content_text.strip():
            print(f"[{author}]: {content_text.strip()}")

        if event.is_final_response():
            final_output = content_text.strip()
            
    print("\n--- SYSTEM EXECUTION COMPLETE ---")
    print("\n--- FINAL RESULT ---")
    
    print(final_output)

    python_code_match = re.search(r"```python\n([\s\S]+?)\n```", final_output, re.DOTALL)
    if python_code_match:
        final_code = python_code_match.group(1).strip()
        
        # Save the file inside the testwizard directory using an absolute path
        output_file_path = os.path.join(SCRIPT_DIR, "final_test_suite.py")  
        with open(output_file_path, "w") as f: # 
            f.write(final_code)
        print(f"\n--- Final test suite saved to `{output_file_path}` ---")  
    else:
        print("\n--- Could not extract a Python code block to save to file. ---")


if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())