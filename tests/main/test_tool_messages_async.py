import itertools
from typing import List

import pytest
from pydantic import Field

from langroid.agent.chat_agent import ChatAgent, ChatAgentConfig
from langroid.agent.tool_message import ToolMessage
from langroid.cachedb.redis_cachedb import RedisCacheConfig
from langroid.language_models.openai_gpt import OpenAIGPTConfig
from langroid.parsing.parser import ParsingConfig
from langroid.prompts.prompts_config import PromptsConfig
from langroid.utils.configuration import Settings, set_global


class CountryCapitalMessage(ToolMessage):
    request: str = "country_capital"
    purpose: str = "To check whether <city> is the capital of <country>."
    country: str = "France"
    city: str = "Paris"
    result: str = "yes"  # or "no"

    @classmethod
    def examples(cls) -> List["CountryCapitalMessage"]:
        return [
            cls(country="France", city="Paris", result="yes"),
            cls(country="France", city="Marseille", result="no"),
        ]


class FileExistsMessage(ToolMessage):
    request: str = "file_exists"
    purpose: str = "To check whether a certain <filename> is in the repo."
    filename: str = Field(..., description="File name to check existence of")
    result: str = "yes"  # or "no"

    @classmethod
    def examples(cls) -> List["FileExistsMessage"]:
        return [
            cls(filename="README.md", result="yes"),
            cls(filename="Dockerfile", result="no"),
        ]


class PythonVersionMessage(ToolMessage):
    request: str = "python_version"
    purpose: str = "To check which version of Python is needed."
    result: str = "3.9"

    @classmethod
    def examples(cls) -> List["PythonVersionMessage"]:
        return [
            cls(result="3.7"),
            cls(result="3.8"),
        ]


DEFAULT_PY_VERSION = "3.9"


class MessageHandlingAgent(ChatAgent):
    def file_exists(self, message: FileExistsMessage) -> str:
        return "yes" if message.filename == "requirements.txt" else "no"

    def python_version(self, PythonVersionMessage) -> str:
        return DEFAULT_PY_VERSION

    def country_capital(self, message: CountryCapitalMessage) -> str:
        return (
            "yes" if (message.city == "Paris" and message.country == "France") else "no"
        )


cfg = ChatAgentConfig(
    name="test-langroid",
    vecdb=None,
    llm=OpenAIGPTConfig(
        type="openai",
        cache_config=RedisCacheConfig(fake=False),
    ),
    parsing=ParsingConfig(),
    prompts=PromptsConfig(),
    use_functions_api=False,
    use_tools=True,
)
agent = MessageHandlingAgent(cfg)

# Define the range of values each variable can have
use_vals = [True, False]
handle_vals = [True, False]
force_vals = [True, False]
message_classes = [None, FileExistsMessage, PythonVersionMessage]

# Get the cartesian product
cartesian_product = list(
    itertools.product(message_classes, use_vals, handle_vals, force_vals)
)

agent.enable_message(FileExistsMessage)
agent.enable_message(PythonVersionMessage)

NONE_MSG = "nothing to see here"

FILE_EXISTS_MSG = """
Ok, thank you.
{
"request": "file_exists",
"filename": "test.txt"
} 
Hope you can tell me!
"""

PYTHON_VERSION_MSG = """
great, please tell me this --
{
"request": "python_version"
}/if you know it
"""


BAD_FILE_EXISTS_MSG = """
Ok, thank you.
{
"request": "file_exists"
} 
Hope you can tell me!
"""


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "use_functions_api",
    [True, False],
)
@pytest.mark.parametrize(
    "message_class, prompt, result",
    [
        (
            FileExistsMessage,
            "You have to find out whether the file 'requirements.txt' exists",
            "yes",
        ),
        (
            PythonVersionMessage,
            "Find out about the python version",
            "3.9",
        ),
        (
            CountryCapitalMessage,
            "You have to check whether Paris is the capital of France",
            "yes",
        ),
    ],
)
async def test_llm_tool_message(
    test_settings: Settings,
    use_functions_api: bool,
    message_class: ToolMessage,
    prompt: str,
    result: str,
):
    """
    Test whether LLM is able to GENERATE message (tool) in required format, and the
    agent handles the message correctly.
    Args:
        test_settings: test settings from conftest.py
        use_functions_api: whether to use LLM's functions api or not
            (i.e. use the langroid ToolMessage tools instead).
        message_class: the message class (i.e. tool/function) to test
        prompt: the prompt to use to induce the LLM to use the tool
        result: the expected result from agent handling the tool-message
    """
    set_global(test_settings)
    agent = MessageHandlingAgent(cfg)
    agent.config.use_functions_api = use_functions_api
    agent.config.use_tools = not use_functions_api
    agent.enable_message(FileExistsMessage)
    agent.enable_message(PythonVersionMessage)
    agent.enable_message(CountryCapitalMessage)

    llm_msg = await agent.llm_response_forget_async(prompt)
    tool_name = message_class.default_value("request")
    if use_functions_api:
        assert llm_msg.function_call.name == tool_name
    else:
        tools = agent.get_tool_messages(llm_msg)
        assert len(tools) == 1
        assert isinstance(tools[0], message_class)

    agent_result = agent.handle_message(llm_msg)
    assert result.lower() in agent_result.lower()
