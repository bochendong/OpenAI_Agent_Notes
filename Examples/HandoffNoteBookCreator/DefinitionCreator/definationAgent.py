from agents import Agent, Runner, AgentOutputSchema

from model import Definition

definition_agent = Agent(
    name="definition_generator",
    handoff_description="专业的概念定义生成器，负责生成准确、清晰、完整的概念定义",
    instructions="""你是一个专业的概念定义生成器。你的任务是生成高质量的概念定义。

                    要求：
                    1. 定义应该准确、清晰、完整，能够准确描述概念的本质特征
                    2. 定义应该使用标准的术语和符号，符合学科规范
                    3. 定义应该简洁明了，避免冗余
                    4. 确保定义与给定的知识点或上下文相关

                    输出格式必须符合 Definition 模型的要求：
                    - definition: 定义内容（必需，字符串格式）

                    注意：你只需要生成定义，不需要生成其他内容。""",
    output_type = AgentOutputSchema(Definition, strict_json_schema=False),
)

