import asyncio
from typing import List, Dict, Any
from app.config import settings
from app.agent.tool_registry import ToolRegistry
from app.agent.llm_interface import OllamaLLM
from app.memory.memory_handler import MemoryHandler


class AgentLoop:
    def __init__(self):
        self.tools = ToolRegistry()
        self.llm = OllamaLLM()
        self.memory = MemoryHandler()

    async def run(self, session_id: str, user_prompt: str, history: List[Dict[str, Any]]):
        tool_history = []

        for step in range(settings.agent_max_iterations):
            context = await self.memory.retrieve(session_id, history)
            prompt = self._make_prompt(user_prompt, context)
            response = await self.llm.generate(prompt)

            tool_call = self.tools.parse_tool_call(response)
            if tool_call:
                output = await self.tools.invoke(tool_call)
                tool_history.append({"tool": tool_call["name"], "args": tool_call.get("args"), "output": output})
                await self.memory.save_tool_result(session_id, tool_call, output)

                if tool_call.get("finish", False):
                    return output, tool_history

                user_prompt = output + "\nContinue."
                continue

            # no tool selected -> final answer
            await self.memory.save_final_response(session_id, response)
            return response, tool_history

        final = "Sorry, I could not complete the task after multiple steps."
        await self.memory.save_final_response(session_id, final)
        return final, tool_history

    def _make_prompt(self, user_prompt: str, context: str) -> str:
        return f"You are an AI agent. User: {user_prompt}\nContext: {context}\nAvailable tools: {self.tools.list_tools()}\nRespond with a tool call or final answer."
