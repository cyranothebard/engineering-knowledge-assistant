from __future__ import annotations

import argparse
import json

from app.settings import get_settings
from rag.service import KnowledgeAssistantService


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Engineering Knowledge Assistant CLI")
    parser.add_argument("command", choices=["build-index", "ask"], help="Command to run")
    parser.add_argument("--question", help="Question to answer when using the ask command")
    parser.add_argument("--language", choices=["en", "de"], help="Optional response language override")
    parser.add_argument("--rebuild", action="store_true", help="Rebuild the vector index")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    service = KnowledgeAssistantService(get_settings())

    if args.command == "build-index":
        build_info = service.build_or_load_index(rebuild=True)
        print(json.dumps(build_info, indent=2))
        return

    if not args.question:
        raise SystemExit("--question is required for the ask command")

    service.build_or_load_index(rebuild=args.rebuild)
    answer = service.ask(args.question, preferred_language=args.language)
    print(json.dumps(answer.model_dump(mode="json"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
