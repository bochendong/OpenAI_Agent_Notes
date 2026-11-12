from agents import Agent, Runner, AgentOutputSchema

from model import Definition


definition_agent = Agent(
    name="definition_generator",
    instructions="""You write high-quality definitions of concepts in English.

Requirements:
1. Write accurate, clear, and complete definitions that capture the essential features of the concept.
2. Use standard terminology and notation for the discipline.
3. Keep definitions concise and avoid repetition.
4. Make the definition relevant to the given topic or context.

Follow the Definition model:
- definition: the definition text (required string)""",
    output_type = AgentOutputSchema(Definition, strict_json_schema=False),
)

