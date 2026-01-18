import os
os.environ['OPENAI_API_KEY'] = 'sk-proj-********************************************************************************'

import sys
sys.path.insert(0, 'C:/Users/sabte/AppData/Local/Programs/Python/Python313/Lib/site-packages')
from swarm import Agent, Swarm, function_tool
Runner = Swarm  # Alias for compatibility

@function_tool
def add_task(title: str) -> str:
    return f'Added task: {title}'

agent = Agent(
    name='Test Agent',
    instructions='You are a todo assistant.',
    tools=[add_task]
)

import asyncio
async def test():
    result = await Runner.run(agent, 'add buy milk')
    print('Result:', result.final_output)

asyncio.run(test())
