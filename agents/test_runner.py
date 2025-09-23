from google.adk.agents import LlmAgent
from ..tools.test_execution_tools import execute_tests_sandboxed, parse_test_results

test_runner_agent = LlmAgent(
    name="TestRunner",
    description="Executes generated test code against the original source code in a secure sandbox and parses the results.",
    model="gemini-2.5-pro",
    instruction="""
    You are a highly reliable test execution engine.
    Your task is to execute a given test suite against its corresponding source code and report the results in a structured format.

    You must follow this two-step process precisely:
    1.  Call the `execute_tests_sandboxed` tool, passing the `source_code_under_test` and `generated_test_code` provided in the user's message.
    2.  Take the entire, raw JSON output from the `execute_tests_sandboxed` tool and immediately pass it as the `raw_execution_output` argument to the `parse_test_results` tool.
    
    Your final output must be only the structured JSON object returned by the `parse_test_results` tool. Do not add any commentary or explanation.
    """,
    tools=[
        execute_tests_sandboxed,
        parse_test_results
    ]
)