from tools.slither_tool import slither_tool
from tools.mythril_tool import mythril_tool
from tools.solhint_tool import solhint_tool

TOOL_REGISTRY = {
    "slither": slither_tool,
    "mythril": mythril_tool,
    "solhint": solhint_tool,
}
