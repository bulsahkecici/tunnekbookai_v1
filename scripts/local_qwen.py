import argparse
import json
import sys
import urllib.request
from pathlib import Path
from urllib.parse import urlparse


DEFAULT_API_BASE = "http://127.0.0.1:1234/v1"
DEFAULT_MODEL = "qwen3.6-35b-a3b-mlx"


def validate_local_endpoint(api_base: str) -> str:
    parsed = urlparse(api_base)

    if parsed.hostname not in {"127.0.0.1", "localhost", "::1"}:
        raise RuntimeError("REMOTE_ENDPOINT_REJECTED")

    return api_base.rstrip("/")


def load_text(path: str | None) -> str:
    if not path:
        return ""

    p = Path(path)

    if not p.exists():
        raise FileNotFoundError(path)

    return p.read_text(encoding="utf-8")


def call_qwen(
    prompt: str,
    model: str,
    api_base: str,
    system_prompt: str | None = None,
) -> str:

    api_base = validate_local_endpoint(api_base)

    messages = []

    if system_prompt:
        messages.append(
            {
                "role": "system",
                "content": system_prompt,
            }
        )

    messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    body = {
        "model": model,
        "system_prompt": system_prompt or "",
        "input": prompt,
        "temperature": 0.2,
        "store": False,
    }

    base = api_base.rstrip("/")
    if base.endswith("/v1"):
        base = base[:-3]

    request = urllib.request.Request(
        f"{base}/api/v1/chat",
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=600) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body_text = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {body_text}") from exc

    output = data.get("output", [])
    messages = [
        item.get("content", "").strip()
        for item in output
        if isinstance(item, dict)
        and item.get("type") == "message"
        and isinstance(item.get("content"), str)
    ]

    if not messages:
        raise RuntimeError("LM Studio native response has no message output")

    return messages[-1]


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "prompt",
        nargs="?",
        help="Prompt text",
    )

    parser.add_argument(
        "--prompt-file",
        help="Prompt file path",
    )

    parser.add_argument(
        "--input",
        help="Optional input/evidence file",
    )

    parser.add_argument(
        "--system",
        help="Optional system prompt file",
    )

    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
    )

    parser.add_argument(
        "--api-base",
        default=DEFAULT_API_BASE,
    )

    parser.add_argument(
        "--output",
        help="Write result to file",
    )

    args = parser.parse_args()

    prompt = args.prompt or ""

    if args.prompt_file:
        prompt = load_text(args.prompt_file)

    if not prompt:
        raise RuntimeError("PROMPT_REQUIRED")

    if args.input:
        input_text = load_text(args.input)

        prompt = (
            f"{prompt}\n\n"
            "===== INPUT =====\n"
            f"{input_text}\n"
            "===== END INPUT =====\n"
        )

    system_prompt = load_text(args.system) if args.system else None

    result = call_qwen(
        prompt=prompt,
        model=args.model,
        api_base=args.api_base,
        system_prompt=system_prompt,
    )

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(result + "\n", encoding="utf-8")
        print(f"written={output_path}")
    else:
        print(result)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
