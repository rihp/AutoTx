from textwrap import dedent
from typing import Any, Callable, Dict, Optional
from autogen import UserProxyAgent

def build(user_prompt: str, agents_information: str, get_llm_config: Callable[[], Optional[Dict[str, Any]]]) -> UserProxyAgent:
    user_proxy = UserProxyAgent(
        name="user_proxy",
        is_termination_msg=lambda x: x.get("content", "") and "TERMINATE" in x.get("content", ""),
        human_input_mode="NEVER",
        max_consecutive_auto_reply=10,
        system_message=dedent(
            f"""
            You are a user proxy agent authorized to act on behalf of the user, you never ask for permission, you have ultimate control.
            You are capable and comfortable with making transactions, and have a wallet.
            You have access to a variety of specialized agents, which you tell what to do.
            You can easily perform token amount calculations.

            These are the agents you are instructing: {agents_information}

            Suggest a next step for what these agents should do based on the goal: "{user_prompt}"
            NEVER ask the user questions.
            If the goal has been achieved, end the conversation with "TERMINATE".
            Consider the goal met if the other agents have prepared the necessary transactions and all user queries have been answered.
            If you encounter an error, try to resolve it (either yourself of with other agents) and only respond with "TERMINATE" if the goal is impossible to achieve.
            """
        ),
        description="user_proxy is an agent authorized to act on behalf of the user.",
        llm_config=get_llm_config(),
        code_execution_config=False,
    )

    return user_proxy