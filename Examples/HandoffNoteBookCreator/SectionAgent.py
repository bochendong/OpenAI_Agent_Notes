from agents import Agent, Runner, AgentOutputSchema

from model import Section
from DefinitionCreator.definationAgent import definition_agent
from TheoremCreator.theoremAgent import theorem_agent
from SummaryCreator.summaryAgent import summary_agent
from ExerciseCreator.exerciseAgent import exercise_agent


section_agent = Agent(
    name="section_generator",
    instructions="""你是一个专业的章节生成器。你的任务是根据给定的知识点和上下文，创建完整的章节内容。

                    重要提示：
                    - 当你调用工具函数时，这些工具已经返回了完整的内容对象
                    - 你不需要重新生成或格式化这些内容，只需要直接使用工具返回的结果
                    - 将所有工具调用的结果直接组织到 Section 结构中即可

                    章节结构要求（按顺序）：
                    1. 一个定义（Definition）：使用 generate_definition 工具生成定义
                    2. 0到多个定理（Theorem）：使用 generate_theorem 工具生成定理
                    3. 3-5个由浅入深的例子/练习题（Examples）：使用 generate_exercises 工具生成练习题，难度应该逐步递增
                    4. 一个总结（Summary）：使用 generate_summary 工具生成章节总结

                    工作流程：
                    1. 分析给定的章节主题、知识点和上下文
                    2. 生成章节标题（section_title）和介绍（introduction）
                    3. 调用 generate_definition 工具生成一个定义（Definition）：
                       - 将章节主题、知识点和上下文传递给工具
                       - 工具会返回 Definition 对象（包含 definition 字段）
                       - 从返回的 Definition 对象中提取 definition 字段并保存
                    4. 根据知识点，判断是否需要生成定理：
                       - 如果需要，调用 generate_theorem 工具生成定理
                       - 将之前生成的定义和上下文传递给工具
                       - 工具会返回 Theorem 对象（包含 theorem 和 proof 字段）
                       - 将返回的 Theorem 对象添加到 theorems 列表中
                       - 如果需要多个定理，可以多次调用 generate_theorem 工具，每次调用都会返回一个 Theorem 对象
                       - 如果不需要定理，theorems 列表保持为空
                    5. 调用 generate_exercises 工具生成3-5个例子/练习题：
                       - 将之前生成的定义、定理（如果有）和完整的上下文传递给工具
                       - 明确要求生成3-5道题目，且难度由浅入深
                       - 工具会返回 ExerciseList 对象（包含 exercises 列表）
                       - 从返回的 ExerciseList 对象中提取 exercises 列表并保存
                    6. 调用 generate_summary 工具生成章节总结：
                       - 重要：必须将之前生成的所有内容作为上下文传递给工具：
                         * 章节的定义是什么
                         * 章节包含哪些定理（如果有）
                         * 章节包含哪些练习题
                         * 总结应该涵盖这些内容
                       - 工具会返回 Summary 对象（包含 summary 字段）
                       - 从返回的 Summary 对象中提取 summary 字段并保存
                    7. 将所有内容组织到 Section 结构中（按顺序）：
                       - section_title: 章节标题（根据上下文生成）
                       - introduction: 章节介绍（根据上下文生成）
                       - definition: 从 generate_definition 工具返回的 Definition 对象中提取 definition 字段
                       - theorems: 从 generate_theorem 工具返回的 Theorem 对象组成的列表（0到多个）
                       - examples: 从 generate_exercises 工具返回的 ExerciseList 对象中提取 exercises 列表（3-5个）
                       - summary: 从 generate_summary 工具返回的 Summary 对象中提取 summary 字段

                    输出格式：
                    - 输出必须符合 Section 模型的要求
                    - 直接使用工具返回的对象，不要重新创建或修改它们
                    - 组织结构顺序：definition → theorems → examples → summary
                    - examples 应该包含3-5道由浅入深的题目""",
    output_type = AgentOutputSchema(Section, strict_json_schema=False),
    tools=[
        definition_agent.as_tool(
            tool_name="generate_definition",
            tool_description="生成定义。定义应该准确、清晰、完整，能够准确描述概念的本质特征。每个章节需要一个定义。",
        ),
        theorem_agent.as_tool(
            tool_name="generate_theorem",
            tool_description="生成定理。定理包含定理陈述和证明。每个章节可以有0到多个定理。",
        ),
        exercise_agent.as_tool(
            tool_name="generate_exercises",
            tool_description="生成练习题列表。必须生成3-5道题目，题目应该由浅入深，难度逐步递增。",
        ),
        summary_agent.as_tool(
            tool_name="generate_summary",
            tool_description="生成章节总结。总结应该全面、准确，涵盖章节的核心知识点。每个章节需要一个总结。在调用此工具时，必须将之前生成的定义、定理和练习题的内容作为输入的一部分，以便生成准确的总结。",
        ),
    ],
)

