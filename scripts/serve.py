from __future__ import annotations

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
BASE_PATH = "/multilinear-algebra-book/"


class PreviewHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path: str) -> str:
        if path.startswith(BASE_PATH):
            path = path[len(BASE_PATH):]
        elif path.startswith(BASE_PATH.strip("/")):
            path = path[len(BASE_PATH.strip("/")):]
        return super().translate_path(path)

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


def main() -> int:
    parser = argparse.ArgumentParser(description="Preview the generated website.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--directory", type=Path, default=SITE)
    args = parser.parse_args()

    preview_directory = args.directory.resolve()
    if not (preview_directory / "index.html").exists():
        raise SystemExit("site/index.html is missing. Run: python scripts/build.py all")

    handler = partial(PreviewHandler, directory=str(preview_directory))
    server = ThreadingHTTPServer((args.host, args.port), handler)
    print(f"Preview: http://{args.host}:{args.port}{BASE_PATH}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nPreview stopped.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
