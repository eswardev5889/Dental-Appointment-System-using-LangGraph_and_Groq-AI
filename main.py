"""
Dental Appointment System — powered by LangGraph + GPT-OSS-120B (Groq)
"""

from dotenv import load_dotenv
load_dotenv()

from langchain_core.messages import (
    HumanMessage,
    AIMessageChunk,
)

from dental_agent.agent import dental_graph


BANNER = """
╔══════════════════════════════════════════════════════════╗
║         Dental Appointment Management System             ║
║         Powered by LangGraph + GPT-OSS-120B (Groq)       ║
╚══════════════════════════════════════════════════════════╝
"""


def run():

    print(BANNER)

    history = []

    while True:

        try:
            user_input = input("\nYou: ").strip()

        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in {"quit", "exit", "bye"}:
            print("Goodbye!")
            break

        history.append(
            HumanMessage(content=user_input)
        )

        print("\nAgent: ", end="", flush=True)

        final_messages = None

        try:

            for event_type, data in dental_graph.stream(
                {"messages": history},
                stream_mode=["messages", "values"],
                config={"recursion_limit": 20},
            ):

                if event_type == "messages":

                    chunk, meta = data

                    if (
                        isinstance(chunk, AIMessageChunk)
                        and chunk.content
                        and not getattr(chunk, "tool_calls", None)
                    ):
                        print(chunk.content, end="", flush=True)

                elif event_type == "values":
                    final_messages = data.get("messages", [])

        except Exception as exc:

            print(f"\nError: {exc}")

            history.pop()

            continue

        print()

        if final_messages:

            history = final_messages

            last_message = final_messages[-1]

            if getattr(last_message, "content", None):
                print(last_message.content)


if __name__ == "__main__":
    run()