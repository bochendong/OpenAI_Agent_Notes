from agents import Agent, Runner, AgentOutputSchema

from model import Section
from DefinitionCreator.definationAgent import definition_agent
from TheoremCreator.theoremAgent import theorem_agent
from SummaryCreator.summaryAgent import summary_agent
from ExerciseCreator.exerciseAgent import exercise_agent


section_agent = Agent(
    name="section_generator",
    instructions="""You create complete sections in English based on the given topic and context.

                    Tool results:
                    - The tools return complete content objects.
                    - Use the returned objects as supplied.
                    - Assemble those objects directly into a Section.

                    Section structure, in order:
                    1. One definition (Definition), generated with definition_agent.
                    2. Zero or more theorems (Theorem), generated with theorem_agent.
                    3. Three to five examples or exercises (Examples) of increasing difficulty, generated with exercise_agent.
                    4. One summary (Summary), generated with summary_agent.

                    Workflow:
                    1. Analyze the given topic, concepts, and context.
                    2. Generate the section title (section_title) and introduction (introduction).
                    3. Call definition_agent to generate one Definition.
                    4. Decide whether the topic needs any theorems:
                       - If needed, use theorem_agent to generate the relevant theorems.
                    5. Call exercise_agent to generate three to five examples or exercises:
                       - Explicitly request three to five exercises.
                       - Arrange them in increasing order of difficulty.
                       - Start with basic concepts and progress toward applied questions.
                    6. Call summary_agent to generate the section summary:
                       - Pass the previously generated definition, theorems, and exercises as context.
                       - Base the summary on the full section content.
                       - In the input to generate_summary, specify:
                         * The section definition.
                         * The theorems included, if any.
                         * The exercises included.
                         * That the summary should cover this material.
                    7. Assemble the content into a Section with these fields:
                       - section_title: a title based on the context.
                       - introduction: an introduction based on the context.
                       - definition: the definition field returned by definition_agent.
                       - theorems: the list of zero or more theorems returned by theorem_agent.
                       - examples: the list of three to five exercises returned by exercise_agent.
                       - summary: the summary field returned by summary_agent.

                    Output format:
                    - Follow the Section model.
                    - Use the returned tool objects directly, without modifying or recreating them.
                    - Order the content as definition, theorems, examples, and summary.
                    - Include three to five examples in increasing order of difficulty.""",
    output_type = AgentOutputSchema(Section, strict_json_schema=False),
    tools=[
        definition_agent.as_tool(
            tool_name="generate_definition",
            tool_description="Generate one accurate, clear, and complete definition that captures the essential features of the concept.",
        ),
        theorem_agent.as_tool(
            tool_name="generate_theorem",
            tool_description="Generate a theorem statement and proof for the concept. Each section may include zero or more theorems. Examples are generated separately for the section.",
        ),
        exercise_agent.as_tool(
            tool_name="generate_exercises",
            tool_description="Generate a list of three to five exercises in increasing order of difficulty.",
        ),
        summary_agent.as_tool(
            tool_name="generate_summary",
            tool_description="Generate one accurate, comprehensive summary of the section's core topics. Include the previously generated definition, theorems, and exercises in the input.",
        ),
    ],
)

