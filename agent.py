# testwizard/agent.py

"""
This file serves as the main entry point for the Google ADK CLI.
It imports the fully constructed root agent from the 'agents' package
and assigns it to a variable named 'agent', which the CLI discovers and uses.
"""

from .agents.coordinator import root_agent


# The ADK CLI (`adk run`, `adk web`) looks for this 'agent' variable by convention.
agent = root_agent