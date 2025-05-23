import os
from typing import Any
from uuid import uuid4

import pytest
from dotenv import load_dotenv
from langinfra.base.models.model_input_constants import MODEL_PROVIDERS_DICT
from langinfra.base.models.openai_constants import (
    OPENAI_MODEL_NAMES,
    OPENAI_REASONING_MODEL_NAMES,
)
from langinfra.components.agents.agent import AgentComponent
from langinfra.components.tools.calculator import CalculatorToolComponent
from langinfra.custom import Component
from langinfra.utils.constants import MESSAGE_SENDER_AI, MESSAGE_SENDER_NAME_AI

from tests.base import ComponentTestBaseWithClient, ComponentTestBaseWithoutClient
from tests.unit.mock_language_model import MockLanguageModel

# Load environment variables from .env file


class TestAgentComponent(ComponentTestBaseWithoutClient):
    @pytest.fixture
    def component_class(self):
        return AgentComponent

    @pytest.fixture
    def file_names_mapping(self):
        return []

    async def component_setup(self, component_class: type[Any], default_kwargs: dict[str, Any]) -> Component:
        component_instance = await super().component_setup(component_class, default_kwargs)
        # Mock _should_process_output method
        component_instance._should_process_output = lambda output: False  # noqa: ARG005
        return component_instance

    @pytest.fixture
    def default_kwargs(self):
        return {
            "_type": "Agent",
            "add_current_date_tool": True,
            "agent_description": "A helpful agent",
            "agent_llm": MockLanguageModel(),
            "handle_parsing_errors": True,
            "input_value": "",
            "max_iterations": 10,
            "system_prompt": "You are a helpful assistant.",
            "tools": [],
            "verbose": True,
            "session_id": str(uuid4()),
            "sender": MESSAGE_SENDER_AI,
            "sender_name": MESSAGE_SENDER_NAME_AI,
        }

    async def test_build_config_update(self, component_class, default_kwargs):
        component = await self.component_setup(component_class, default_kwargs)
        frontend_node = component.to_frontend_node()
        build_config = frontend_node["data"]["node"]["template"]
        # Test updating build config for OpenAI
        component.set(agent_llm="OpenAI")
        updated_config = await component.update_build_config(build_config, "OpenAI", "agent_llm")
        assert "agent_llm" in updated_config
        assert updated_config["agent_llm"]["value"] == "OpenAI"
        assert isinstance(updated_config["agent_llm"]["options"], list)
        assert len(updated_config["agent_llm"]["options"]) > 0
        assert all(provider in updated_config["agent_llm"]["options"] for provider in MODEL_PROVIDERS_DICT)
        assert "Custom" in updated_config["agent_llm"]["options"]

        # Verify model_name field is populated for OpenAI

        assert "model_name" in updated_config
        model_name_dict = updated_config["model_name"]
        assert isinstance(model_name_dict["options"], list)
        assert len(model_name_dict["options"]) > 0  # OpenAI should have available models
        assert "gpt-4o" in model_name_dict["options"]

        # Test Anthropic
        component.set(agent_llm="Anthropic")
        updated_config = await component.update_build_config(build_config, "Anthropic", "agent_llm")
        assert "agent_llm" in updated_config
        assert updated_config["agent_llm"]["value"] == "Anthropic"
        assert isinstance(updated_config["agent_llm"]["options"], list)
        assert len(updated_config["agent_llm"]["options"]) > 0
        assert all(provider in updated_config["agent_llm"]["options"] for provider in MODEL_PROVIDERS_DICT)
        assert "Anthropic" in updated_config["agent_llm"]["options"]
        assert updated_config["agent_llm"]["input_types"] == []
        options = updated_config["model_name"]["options"]
        assert any("sonnet" in option.lower() for option in options), f"Options: {options}"

        # Test updating build config for Custom
        updated_config = await component.update_build_config(build_config, "Custom", "agent_llm")
        assert "agent_llm" in updated_config
        assert updated_config["agent_llm"]["value"] == "Custom"
        assert isinstance(updated_config["agent_llm"]["options"], list)
        assert len(updated_config["agent_llm"]["options"]) > 0
        assert all(provider in updated_config["agent_llm"]["options"] for provider in MODEL_PROVIDERS_DICT)
        assert "Custom" in updated_config["agent_llm"]["options"]
        assert updated_config["agent_llm"]["input_types"] == ["LanguageModel"]

        # Verify model_name field is cleared for Custom
        assert "model_name" not in updated_config


class TestAgentComponentWithClient(ComponentTestBaseWithClient):
    @pytest.fixture
    def component_class(self):
        return AgentComponent

    @pytest.fixture
    def file_names_mapping(self):
        return []

    @pytest.mark.api_key_required
    async def test_agent_component_with_calculator(self):
        # Mock inputs
        load_dotenv()

        # Now you can access the environment variables
        api_key = os.getenv("OPENAI_API_KEY")
        tools = [CalculatorToolComponent().build_tool()]  # Use the Calculator component as a tool
        input_value = "What is 2 + 2?"

        temperature = 0.1

        # Initialize the AgentComponent with mocked inputs
        agent = AgentComponent(
            tools=tools,
            input_value=input_value,
            api_key=api_key,
            model_name="gpt-4o",
            llm_type="OpenAI",
            temperature=temperature,
            _session_id=str(uuid4()),
        )

        response = await agent.message_response()
        assert "4" in response.data.get("text")

    @pytest.mark.api_key_required
    async def test_agent_component_with_all_openai_models(self):
        # Mock inputs
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        tools = [CalculatorToolComponent().build_tool()]  # Use the Calculator component as a tool
        input_value = "What is 2 + 2?"

        # Iterate over all OpenAI models
        for model_name in OPENAI_MODEL_NAMES + OPENAI_REASONING_MODEL_NAMES:
            # Initialize the AgentComponent with mocked inputs
            agent = AgentComponent(
                tools=tools,
                input_value=input_value,
                api_key=api_key,
                model_name=model_name,
                llm_type="OpenAI",
                _session_id=str(uuid4()),
            )

            response = await agent.message_response()
            assert "4" in response.data.get("text"), f"Failed for model: {model_name}"
