class CustomizeAgent(BaseModel):
    name: str
    instructions: str

AGENT_SAVE_PATH = './agent_database'

def to_json(agent: Agent):
    return json.dump({"name": agent.name, "instruction": agent.instruction})
class Manager():
    def __init__(self, name:str, instruction:str)->None:
        self.name = name
        self.instruction = instruction
        self.agent_generator = Agent(name, instruction, output_type=CustomizeAgent)

    async def generlize_new_agent(self, instruction):
        result = await Runner.run(self.agent, f"{instruction}")

        newAgents = Agent(result.final_output.name, result.final_output.instructions)