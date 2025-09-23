import re
from typing import Any, Dict, List
from pydantic import BaseModel, Field

# Pydantic models define the strict JSON schema for our test scenarios.
# This ensures data consistency between the TestCaseDesigner and TestImplementer agents.
class TestScenario(BaseModel):
    """Represents a single abstract test scenario."""
    description: str = Field(..., description="A clear, concise description of what is being tested.")
    expected_outcome: str = Field(..., description="The expected result or behavior of the code under this test scenario.")

# --- (Replace the old function with this new one) ---
def generate_test_scenarios(natural_language_output: str) -> List[Dict[str, Any]]:
    """
    Takes a natural-language string of test scenarios from an LLM and parses
    it into a structured JSON array of test scenario objects.

    This parser is flexible and can handle two common formats:
    1. A block-based format with "SCENARIO:" and "EXPECTED:" tags.
    2. A bullet-point format with "Description:" and "Expected Outcome:" tags.

    Args:
        natural_language_output: A string containing test scenarios.

    Returns:
        A list of dictionaries, where each dictionary conforms to the TestScenario schema.
    """
    scenarios = []
    
    # Split the output into individual scenario blocks. The LLM might use '---' or just newlines.
    # We will split by '---' first, and if that yields only one block, we'll try splitting by "Scenario".
    scenario_blocks = natural_language_output.strip().split('---')
    if len(scenario_blocks) < 2:
        # The LLM might not be using '---', let's try a more robust split based on "Scenario X:"
        scenario_blocks = re.split(r'\*\s*Scenario \d+:', natural_language_output)

    for block in scenario_blocks:
        if not block.strip():
            continue

        description = None
        expected_outcome = None

        # Pattern 1: Look for "Description:" and "Expected Outcome:" (the format the LLM is using)
        # We use re.DOTALL to allow '.' to match newlines, and re.IGNORECASE for flexibility.
        desc_match_v2 = re.search(r"(?:Description|SCENARIO):\s*(.*?)(?:\n\s*-\s*(?:Inputs|Expected Outcome|EXPECTED):|$)", block, re.DOTALL | re.IGNORECASE)
        outcome_match_v2 = re.search(r"Expected Outcome|EXPECTED:\s*(.*)", block, re.DOTALL | re.IGNORECASE)
        
        if desc_match_v2 and outcome_match_v2:
            description = desc_match_v2.group(1).strip()
            expected_outcome = outcome_match_v2.group(1).strip()
        else:
            # Pattern 2: Fallback to the original "SCENARIO:" and "EXPECTED:" format
            desc_match_v1 = re.search(r"SCENARIO:\s*(.+?)\s*EXPECTED:", block, re.DOTALL | re.IGNORECASE)
            outcome_match_v1 = re.search(r"EXPECTED:\s*(.+)", block, re.DOTALL | re.IGNORECASE)
            if desc_match_v1 and outcome_match_v1:
                description = desc_match_v1.group(1).strip()
                expected_outcome = outcome_match_v1.group(1).strip()

        if description and expected_outcome:
            try:
                # Validate data against the Pydantic model
                scenario_obj = TestScenario(
                    description=description,
                    expected_outcome=expected_outcome
                )
                # Append the validated data as a dictionary
                scenarios.append(scenario_obj.model_dump())
            except Exception as e:
                # Skip blocks that fail validation
                print(f"Warning: Skipping scenario block due to validation error: {e}\nBlock content:\n{block}")

    if not scenarios:
        raise ValueError("Could not parse any valid scenarios from the provided text.")

    return scenarios