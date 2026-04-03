from typing import Dict, Any, Optional
from .tools.web_search import web_search
from .tools.sql_executor import sql_query
from .tools.python_executor import run_python
from .tools.api_caller import call_api


class ToolRegistry:
    def __init__(self):
        self.available_tools = {
            "web_search": web_search,
            "sql_query": sql_query,
            "python_exec": run_python,
            "api_call": call_api,
        }

    def list_tools(self):
        return list(self.available_tools.keys())

    def parse_tool_call(self, text: str) -> Optional[Dict[str, Any]]:
        # common text format: TOOL_NAME: {"arg": "value"}
        lines = text.strip().splitlines()
        if not lines:
            return None

        first = lines[0].strip()
        if ":" not in first:
            return None

        name, argstr = first.split(":", 1)
        name = name.strip()
        if name not in self.available_tools:
            return None

        args = {}
        import json
        try:
            args = json.loads(argstr.strip())
        except Exception:
            args = {"query": argstr.strip()}

        return {"name": name, "args": args}

    async def invoke(self, tool_call: Dict[str, Any]) -> Any:
        name = tool_call.get("name")
        args = tool_call.get("args", {})
        tool = self.available_tools.get(name)
        if not tool:
            raise ValueError(f"Tool {name} is not available")
        return await tool(**args)
