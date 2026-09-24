"""Chat with the agent: cd sierra && python -m problem_5_agent_debug"""
from datetime import date

from . import Agent, demo_db

if __name__ == "__main__":
    today = date.today()
    agent = Agent(demo_db(today), today=today)
    print("Try: 'my email is sam@example.com', 'where is order #1001?', 'refund order #1003'. Ctrl-D to quit.")
    while True:
        try:
            text = input("you> ")
        except EOFError:
            break
        print("agent>", agent.handle(text))
        for msg in agent.state.history[-4:]:
            if msg.role == "tool":
                print(f"   [tool {msg.tool_name}] {msg.content}")
