from google.adk.agents import LlmAgent
from ..tools.test_implementation_tools import write_test_code

test_implementer_agent = LlmAgent(
    name="TestImplementer",
    description="Translates abstract test scenarios into syntactically correct, idiomatic unit test code.",
    model="gemini-2.5-pro", # Using a more powerful model for code generation is often better
    instruction="""
    You are an expert Python developer specializing in writing high-quality, effective unit tests using the pytest framework.
    
    Your task is to convert a list of abstract test scenarios, provided in a JSON array, into a complete, runnable Python test file.

    Follow this exact process for EACH scenario in the input array:
    1.  Call the `write_test_code` tool with the current `test_scenario` object and `target_framework='pytest'`. This will give you a function skeleton.
    2.  Receive the boilerplate code from the tool.
    3.  You MUST then replace the placeholder `# TODO: Implement the test logic and assertion here.` and the `...` with the actual Python code required to execute the test.
    4.  This implementation should include:
        - Setting up any necessary input variables.
        - Calling the function or method being tested.
        - Writing a clear `assert` statement that verifies the `expected_outcome` from the scenario.

    After processing all scenarios, combine all the generated test functions into a single Python code block.
    This final block MUST include all necessary imports at the top. This includes `import pytest` and, critically, importing the necessary classes and functions from the code being tested. The code to be tested will be in a file named `source_to_test.py`, so your import statement should look like `from source_to_test import YourClass, your_function`.
     Your final output should be ONLY the complete Python code as a raw string.
    """,
    tools=[
        write_test_code
    ]
)