"""CLI entry point. Run:  python main.py

Requires:  pip install anthropic python-dotenv
"""

from dotenv import load_dotenv

load_dotenv()

from agent import ResearchAgent


def main():
    print("Research agent ready. Type a question, or 'quit' to exit.\n")
    agent = ResearchAgent()  # one agent keeps memory across turns

    while True:
        try:
            user_input = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if user_input.lower() in {"quit", "exit"}:
            break
        if not user_input:
            continue

        answer = agent.run(user_input)
        print(f"\nagent> {answer}\n")


if __name__ == "__main__":
    main()
