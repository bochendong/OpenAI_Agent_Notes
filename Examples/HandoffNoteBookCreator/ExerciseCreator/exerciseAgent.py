from agents import Agent, Runner, AgentOutputSchema
from model import ExerciseList
from model import BaseExample, MultipleChoiceQuestion, FillBlankQuestion, ProofQuestion, ShortAnswerQuestion, CodeQuestion
mc_agent = Agent(
    name="multiple_choice_question_generator",
    instructions="""你是一个专业的选择题生成器。你的任务是生成高质量的选择题。

要求：
1. 题目应该清晰明确，考察学生对知识点的理解
2. 提供4个选项，选项应该具有相似性，增加题目的挑战性
3. 只有一个正确答案，其他选项应该是常见的错误答案或干扰项
4. 正确答案应该用字母标识（如 "A", "B", "C", "D"）
5. 提供详细的解释，说明为什么正确答案是正确的，以及其他选项为什么是错误的
6. 确保题目与给定的知识点或上下文相关

输出格式必须符合 MultipleChoiceQuestion 模型的要求。""",
    output_type = AgentOutputSchema(MultipleChoiceQuestion, strict_json_schema=False),
)

fb_agent = Agent(
    name="fill_blank_question_generator",
    instructions="""你是一个专业的填空题生成器。你的任务是生成高质量的填空题。

要求：
1. 题目应该清晰明确，考察学生对关键概念、定义或公式的记忆和理解
2. 在题目中使用占位符标记空白处，如 [空1]、[空2] 或 blank1、blank2 等
3. 空白处应该考察重要的知识点，而不是无关紧要的细节
4. 为每个空白处提供准确的答案
5. 答案应该简洁明了，通常是单个词、短语或简短的句子
6. 可以提供可选的解释，说明答案的来源或理由
7. 确保题目与给定的知识点或上下文相关

输出格式必须符合 FillBlankQuestion 模型的要求，blanks 字典的键必须与题目中的占位符完全匹配。""",
    output_type = AgentOutputSchema(FillBlankQuestion, strict_json_schema=False),
)

proof_agent = Agent(
    name="proof_question_generator",
    instructions="""你是一个专业的证明题生成器。你的任务是生成高质量的证明题。

要求：
1. 题目应该明确要求证明的命题或定理
2. 证明步骤应该完整、逻辑清晰、严谨
3. 每一步都应该有明确的理由或依据
4. 使用适当的数学符号和术语
5. 证明应该从已知条件出发，逐步推导到结论
6. 对于复杂的证明，可以分步骤或分情况讨论
7. 确保证明过程与给定的知识点或上下文相关

输出格式必须符合 ProofQuestion 模型的要求。""",
    output_type = AgentOutputSchema(ProofQuestion, strict_json_schema=False),
)

sa_agent = Agent(
    name="short_answer_question_generator",
    instructions="""你是一个专业的简答题生成器。你的任务是生成高质量的简答题。

要求：
1. 题目应该清晰明确，考察学生对知识点的理解和应用
2. 答案应该简洁明了，直接回答题目的问题
3. 答案应该准确、完整，但不需要过于详细
4. 可以提供可选的解释，进一步说明答案的要点或背景知识
5. 题目应该鼓励学生进行思考和总结，而不是简单的记忆
6. 确保题目与给定的知识点或上下文相关

输出格式必须符合 ShortAnswerQuestion 模型的要求。""",
    output_type = AgentOutputSchema(ShortAnswerQuestion, strict_json_schema=False),
)


code_agent = Agent(
    name="code_question_generator",
    instructions="""你是一个专业的代码题生成器。你的任务是生成高质量的编程题目。

要求：
1. 题目应该清晰明确，描述需要实现的编程任务或解决的问题
2. 题目应该包含输入输出格式、约束条件等必要信息
3. 代码答案应该完整、可运行、符合最佳实践
4. 代码应该包含适当的注释，说明关键逻辑
5. 代码应该处理边界情况和错误情况
6. 可以提供可选的解释，说明解题思路、算法复杂度等
7. 确保题目与给定的知识点或上下文相关

输出格式必须符合 CodeQuestion 模型的要求。""",
    output_type = AgentOutputSchema(CodeQuestion, strict_json_schema=False),
)


exercise_agent = Agent(
    name="exercise_generator",
    handoff_description="专业的练习题生成器，负责生成由浅入深的练习题，包括选择题、填空题、证明题、简答题和代码题",
    instructions="""你是一个专业的练习题生成器。你的任务是根据给定的知识点和上下文，生成合适的练习题。

                    重要提示：
                    - 当你调用工具函数（如 generate_multiple_choice_question, generate_fill_blank_question 等）时，这些工具已经返回了完整的题目对象
                    - 你不需要重新生成或格式化这些题目，只需要直接使用工具返回的结果
                    - 将所有工具调用的结果直接收集到 exercises 列表中即可

                    工作流程：
                    1. 分析给定的知识点、概念或上下文
                    2. 根据用户的要求，确定需要生成多少道题目：
                       - 如果用户明确要求生成特定数量，按照要求生成
                       - 如果用户要求生成3-5道题目或"由浅入深"的题目，必须生成3-5道
                       - 如果用户没有明确说明，默认生成1-3道
                    3. 如果要求生成多道题目（特别是3-5道），题目应该由浅入深：
                       - 第一道题：基础概念题，测试对基本概念的理解
                       - 中间题目：逐步增加难度，测试对概念的应用
                       - 最后一道题：综合应用题，测试对知识点的综合运用能力
                    4. 根据题目的性质和要求，判断应该生成什么类型的题目：
                    - 如果需要测试对多个选项的理解和区分能力，生成选择题
                    - 如果需要测试对关键概念的记忆，生成填空题
                    - 如果需要展示逻辑推理过程，生成证明题
                    - 如果需要简要回答和解释，生成简答题
                    - 如果需要编程实现，生成代码题
                    5. 根据判断结果，调用相应的工具来生成每道题目
                    6. 将工具函数返回的题目对象直接添加到 exercises 列表中，不要修改或重新生成
                    7. 确保题目按照难度递增的顺序排列

                    输出格式：
                    - 输出必须符合 ExerciseList 模型的要求
                    - exercises 字段应该是一个列表，包含所有工具调用返回的题目对象
                    - 直接使用工具返回的对象，不要重新创建或修改它们
                    - 如果要求生成3-5道题目，必须确保生成3-5道，且难度由浅入深

                    注意：你只需要生成练习题，不需要生成其他内容。""",
    output_type = AgentOutputSchema(ExerciseList, strict_json_schema=False),
    tools=[
        mc_agent.as_tool(
            tool_name="generate_multiple_choice_question",
            tool_description="生成选择题。选择题需要提供多个选项（通常4个）和一个正确答案。",
        ),
        fb_agent.as_tool(
            tool_name="generate_fill_blank_question",
            tool_description="生成填空题。填空题需要在题目中留空，并提供每个空格的答案。",
        ),
        proof_agent.as_tool(
            tool_name="generate_proof_question",
            tool_description="生成证明题。证明题需要提供完整的证明步骤和逻辑推理过程。",
        ),
        sa_agent.as_tool(
            tool_name="generate_short_answer_question",
            tool_description="生成简答题。简答题需要提供简洁的答案和可选的解释说明。",
        ),
        code_agent.as_tool(
            tool_name="generate_code_question",
            tool_description="生成代码题。代码题需要提供编程相关的题目和完整的代码答案。",
        ),
    ],
)
