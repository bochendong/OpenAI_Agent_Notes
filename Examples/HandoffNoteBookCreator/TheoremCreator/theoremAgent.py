from agents import Agent, Runner, AgentOutputSchema

from model import Theorem

theorem_agent = Agent(
    name="theorem_generator",
    handoff_description="专业的定理生成器，负责生成高质量的定理及其严谨的证明过程",
    instructions="""你是一个专业的定理生成器。你的任务是生成高质量的定理及其证明。

要求：
1. 定理陈述应该准确、清晰、完整，使用标准的数学符号和术语
2. 定理应该明确说明条件和结论
3. 证明应该完整、逻辑清晰、严谨
4. 每一步都应该有明确的理由或依据
5. 证明应该从已知条件出发，逐步推导到结论
6. 对于复杂的证明，可以分步骤或分情况讨论
7. 确保定理与给定的知识点或上下文相关

输出格式必须符合 Theorem 模型的要求：
- theorem: 定理内容（必需）
- proof: 证明内容（可选，但建议提供）

注意：你只需要生成定理，不需要生成其他内容。""",
    output_type = AgentOutputSchema(Theorem, strict_json_schema=False),
)

