from agentopera.chatflow.agents import AssistantAgent
from agents.model_client_factory import get_shared_model_client
from agentopera.core import UserMessage, SystemMessage
import os

class ExplainerAgent(AssistantAgent):
    def __init__(self):
        model_name = os.environ.get("MODEL_NAME", "deepseek-chat-v3-0324")
        model_client = get_shared_model_client()
        model_client.model = model_name

        self.system_message_text = (
                "You are a professional smart contract security analyst. "
                "When analyzing vulnerability reports from automated tools (e.g., Slither, Mythril, Solhint), "
                "you must clearly explain each issue and propose specific fixes.\n\n"
                "🔹 For each tool, summarize findings by severity (High, Medium, Low, Info).\n"
                "🔹 For each finding, include:\n"
                "  1. Explanation (in simple language)\n"
                "  2. Risk or impact if unaddressed\n"
                "  3. Recommended fix or mitigation (including code if possible)\n"
                "  4. Best practices to prevent it in future code"
            )

        super().__init__(
            name="explainer_agent",
            model_client=model_client,
            system_message=self.system_message_text
        )

    async def on_messages(self, messages):
        input_text = messages[-1].content

        prompt = f"""
Analyze the following smart contract findings.

🔧 Format:
Group findings by tool name (e.g., Slither, Mythril, Solhint).
Within each tool, group by severity (e.g., High, Medium, Low, Info).

For each issue:
1. Explain what the issue means (simply).
2. Describe the security or functional risk.
3. Recommend a fix or code change to solve the issue.
4. Offer any best practices that prevent it.

Input starts here:
{input_text}
"""

        result = await self._model_client.create([
            SystemMessage(content=self.system_message_text),
            UserMessage(content=prompt, source="user")
        ])
        return result.content
