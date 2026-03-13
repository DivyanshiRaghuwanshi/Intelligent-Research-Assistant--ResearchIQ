import logging

from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, AIMessage
from langchain.agents import create_agent

from config.config import MAX_HISTORY_MESSAGES

logger = logging.getLogger(__name__)

from langchain.agents.middleware import AgentMiddleware

class TrimMessagesMiddleware(AgentMiddleware):

    def before_model(self, state):
        messages = state.get("messages", [])
        if len(messages) > MAX_HISTORY_MESSAGES:
            state["messages"] = messages[-MAX_HISTORY_MESSAGES:]
        return state


def build_agent(response_llm, tools, system_prompt, memory):
    """Builds a LangGraph ReAct agent with InMemorySaver and message trimming."""
    try:
        return create_agent(
            model=response_llm,
            tools=tools,
            checkpointer=memory,
            system_prompt=system_prompt,
            middleware=[TrimMessagesMiddleware()],
        )
    except Exception as e:
        raise RuntimeError(f"Failed to build agent: {e}")


def run_agent(agent, user_message, thread_id="default"):
    """Sends a message to the agent and returns the reply string."""
    try:
        result = agent.invoke(
            {"messages": [HumanMessage(content=user_message)]},
            config={"configurable": {"thread_id": thread_id}},
        )
        for msg in reversed(result.get("messages", [])):
            if isinstance(msg, AIMessage) and msg.content:
                content = msg.content

                if isinstance(content, list):
                    content = "\n".join(
                        part["text"] for part in content if part.get("type") == "text"
                    )

                return content
        return "I could not generate a response. Please try again."
    except Exception as e:
        logger.error(f"Agent error (thread={thread_id}): {e}")
        raise RuntimeError(f"Agent error: {e}")

