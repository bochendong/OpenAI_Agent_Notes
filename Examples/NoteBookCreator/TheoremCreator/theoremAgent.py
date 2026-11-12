from agents import Agent, Runner, AgentOutputSchema

from model import Theorem


theorem_agent = Agent(
    name="theorem_generator",
    instructions="""You write high-quality theorems and proofs in English.

Requirements:
1. State the theorem accurately, clearly, and completely using standard mathematical notation and terminology.
2. State the hypotheses and conclusion explicitly.
3. Write a complete, logically clear, and rigorous proof.
4. Justify each step.
5. Start from the hypotheses and derive the conclusion step by step.
6. Break complex proofs into steps or cases as needed.
7. Make the theorem relevant to the given topic or context.

Follow the Theorem model:
- theorem: the theorem statement (required)
- proof: the proof (optional, but recommended)""",
    output_type = AgentOutputSchema(Theorem, strict_json_schema=False),
)

