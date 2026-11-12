from agents import Agent, Runner, AgentOutputSchema

from model import BaseExample, MultipleChoiceQuestion, FillBlankQuestion, ProofQuestion, ShortAnswerQuestion, CodeQuestion, ExerciseList

mc_agent = Agent(
    name="multiple_choice_question_generator",
    instructions="""You write high-quality multiple-choice questions in English.

Requirements:
1. Write clear questions that assess students' understanding of the topic.
2. Provide four comparable options to make the question challenging.
3. Include exactly one correct answer. Use common mistakes or plausible distractors for the other options.
4. Identify the correct answer by its letter, such as "A", "B", "C", or "D".
5. Explain why the correct answer is right and why the other options are wrong.
6. Keep the question relevant to the given topic or context.

Follow the MultipleChoiceQuestion model.""",
    output_type = AgentOutputSchema(MultipleChoiceQuestion, strict_json_schema=False),
)

fb_agent = Agent(
    name="fill_blank_question_generator",
    instructions="""You write high-quality fill-in-the-blank questions in English.

Requirements:
1. Write clear questions that assess students' recall and understanding of key concepts, definitions, or formulas.
2. Mark blanks with placeholders such as [blank1] and [blank2], or blank1 and blank2.
3. Use blanks to test important concepts.
4. Provide an accurate answer for every blank.
5. Keep answers concise, typically a word, phrase, or short sentence.
6. Optionally explain how each answer is obtained.
7. Keep the question relevant to the given topic or context.

Follow the FillBlankQuestion model. The keys in the blanks dictionary must exactly match the placeholders in the question.""",
    output_type = AgentOutputSchema(FillBlankQuestion, strict_json_schema=False),
)

proof_agent = Agent(
    name="proof_question_generator",
    instructions="""You write high-quality proof questions in English.

Requirements:
1. State the proposition or theorem to prove.
2. Provide a complete, logically clear, and rigorous proof.
3. Justify each step.
4. Use appropriate mathematical notation and terminology.
5. Start from the hypotheses and derive the conclusion step by step.
6. Break complex proofs into steps or cases as needed.
7. Keep the proof relevant to the given topic or context.

Follow the ProofQuestion model.""",
    output_type = AgentOutputSchema(ProofQuestion, strict_json_schema=False),
)

sa_agent = Agent(
    name="short_answer_question_generator",
    instructions="""You write high-quality short-answer questions in English.

Requirements:
1. Write clear questions that assess understanding and application of the topic.
2. Give concise answers that address the question directly.
3. Make the answers accurate and complete.
4. Optionally explain key points or provide background.
5. Ask students to reason or synthesize information beyond simple recall.
6. Keep the question relevant to the given topic or context.

Follow the ShortAnswerQuestion model.""",
    output_type = AgentOutputSchema(ShortAnswerQuestion, strict_json_schema=False),
)


code_agent = Agent(
    name="code_question_generator",
    instructions="""You write high-quality programming questions in English.

Requirements:
1. Clearly describe the task to implement or the problem to solve.
2. Specify input and output formats, constraints, and other necessary details.
3. Provide a complete, runnable solution that follows good coding practices.
4. Add comments where they clarify key logic.
5. Handle edge cases and errors.
6. Optionally explain the approach and its complexity.
7. Keep the question relevant to the given topic or context.

Follow the CodeQuestion model.""",
    output_type = AgentOutputSchema(CodeQuestion, strict_json_schema=False),
)


exercise_agent = Agent(
    name="exercise_generator",
    instructions="""You generate exercises in English based on the given topic and context.

                    Tool results:
                    - Tools such as generate_multiple_choice_question and generate_fill_blank_question return complete question objects.
                    - Use the returned questions as supplied.
                    - Collect the returned objects directly into the exercises list.

                    Workflow:
                    1. Analyze the given topic, concepts, or context.
                    2. Determine how many exercises to generate from the user's request:
                       - If the user specifies a count, use that count.
                       - If the user asks for three to five exercises or asks for exercises of increasing difficulty, generate three to five.
                       - If the user gives no guidance, generate one to three.
                    3. When generating multiple exercises, especially three to five, increase their difficulty:
                       - Start with a basic question to assess conceptual understanding.
                       - Use the middle questions to test application at increasing difficulty.
                       - End with a question that combines concepts in an applied problem.
                    4. Choose each question type based on what the question should assess:
                    - Use multiple choice to test whether students can distinguish between options.
                    - Use fill-in-the-blank questions to test recall of key concepts.
                    - Use proof questions to test logical reasoning.
                    - Use short-answer questions to elicit a concise answer and explanation.
                    - Use programming questions when the answer requires an implementation.
                    5. Call the appropriate tool to generate each question.
                    6. Add the returned question objects directly to the exercises list without modifying or recreating them.
                    7. Order the exercises by increasing difficulty.

                    Output format:
                    - Follow the ExerciseList model.
                    - Include every question object returned by the tools in the exercises list.
                    - Use the returned objects directly, without modifying or recreating them.
                    - If the user requests three to five questions, include three to five in increasing order of difficulty.""",
    output_type = AgentOutputSchema(ExerciseList, strict_json_schema=False),
    tools=[
        mc_agent.as_tool(
            tool_name="generate_multiple_choice_question",
            tool_description="Generate a multiple-choice question with several options (typically four) and one correct answer.",
        ),
        fb_agent.as_tool(
            tool_name="generate_fill_blank_question",
            tool_description="Generate a fill-in-the-blank question with placeholders and an answer for every blank.",
        ),
        proof_agent.as_tool(
            tool_name="generate_proof_question",
            tool_description="Generate a proof question with a complete proof and its logical reasoning.",
        ),
        sa_agent.as_tool(
            tool_name="generate_short_answer_question",
            tool_description="Generate a short-answer question with a concise answer and an optional explanation.",
        ),
        code_agent.as_tool(
            tool_name="generate_code_question",
            tool_description="Generate a programming question with a complete code solution.",
        ),
    ],
)
