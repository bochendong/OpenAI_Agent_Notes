from agents import Agent, Runner, AgentOutputSchema

from model import Summary


summary_agent = Agent(
    name="summary_generator",
    instructions="""You write high-quality section summaries in English.

Requirements:
1. Cover the section's core topics accurately and comprehensively.
2. Organize the summary clearly, grouping related topics where helpful.
3. Highlight key ideas and difficult points.
4. Keep the summary concise and avoid repetition.
5. Help readers review and understand the material quickly.
6. Choose formats that suit the section, such as:
   - A list of key topics
   - A concept map
   - A reference list of important formulas
   - Study suggestions
   - Frequently asked questions
7. Keep the summary relevant to the section.

Follow the Summary model:
- summary: the summary text (required string)""",
    output_type = AgentOutputSchema(Summary, strict_json_schema=False),
)

