from agentopera.chatflow.agents import AssistantAgent
from agents.model_client_factory import get_shared_model_client

class StaticAnalyzerAgent(AssistantAgent):
    def __init__(self, custom_tools=None):
        model_client = get_shared_model_client()

        super().__init__(
            name="static_analyzer",
            model_client=model_client,
            tools=custom_tools or [],
            system_message="You are a Solidity smart contract auditor. Use Slither, Mythril and Solhint to identify vulnerabilities and return concise reports."
        )
