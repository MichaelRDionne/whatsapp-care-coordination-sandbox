from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from message_router import load_messages, route_messages


def main() -> None:
    messages = load_messages(ROOT / "synthetic-data" / "messages.json")
    print("CARE COORDINATION ROUTES")
    for route in route_messages(messages):
        print(f"- {route['id']} -> {route['queue']} [{route['priority']}]")
        print(f"  Guardrail: {route['guardrail']}")


if __name__ == "__main__":
    main()
