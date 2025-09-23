from google.adk.agents import LlmAgent
from ..tools.code_analysis_tools import analyze_code_structure

# This agent is highly specialized. Its instructions are very direct to prevent
# the LLM from trying to analyze the code itself, which can lead to errors.
# We want it to reliably delegate the task to our deterministic tool.
code_analyzer_agent = LlmAgent(
    name="CodeAnalyzer",
    description="Performs deep, accurate static analysis of source code by parsing it into a structured format.",
    model="gemini-2.5-flash", # Or any capable model
    instruction="""
    You are a specialized agent for static code analysis. Your sole responsibility is to receive a block of source code and call the `analyze_code_structure` tool.
    You must correctly identify the programming language from the user's request or file context and pass both the language and the source code to the tool.
    Do NOT attempt to analyze, summarize, or explain the code yourself. Only call the tool.
    """,
    tools=[
        analyze_code_structure
    ]
)