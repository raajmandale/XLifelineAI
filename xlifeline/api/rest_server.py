from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

from ..service import XLifeline


lifeline = XLifeline()


class XLifelineHandler(BaseHTTPRequestHandler):
    server_version = "XLifelineHTTP/0.1"

    def _send_json(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0:
            return {}
        return json.loads(self.rfile.read(length).decode("utf-8"))

    def log_message(self, format: str, *args: object) -> None:
        return

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/health":
            self._send_json(200, {"status": "ok"})
            return
        self._send_json(404, {"error": "not_found"})

    def do_POST(self) -> None:  # noqa: N802
        try:
            data = self._read_json()
            if self.path == "/memory/save":
                key = data["key"]
                text = data["text"]
                manifest = lifeline.save_text(key, text)
                self._send_json(200, {"saved": True, "total_fragments": manifest["total_fragments"]})
            elif self.path == "/memory/load":
                key = data["key"]
                lossy = bool(data.get("lossy", False))
                self._send_json(200, lifeline.load_manifest(key, lossy=lossy))
            elif self.path == "/memory/verify":
                key = data["key"]
                lossy = bool(data.get("lossy", False))
                self._send_json(200, lifeline.verify(key, lossy=lossy))
            elif self.path == "/memory/simulate-loss":
                key = data["key"]
                percent = float(data.get("percent", 0.3))
                lossy = lifeline.simulate_loss(key, percent=percent)
                self._send_json(200, {"destroyed_indices": lossy.get("destroyed_indices", [])})
            elif self.path == "/memory/rebuild":
                key = data["key"]
                lossy = bool(data.get("lossy", False))
                result = lifeline.rebuild(key, lossy=lossy)
                payload = {
                    "integrity": result["integrity"],
                    "rebuilt_text": result.get("rebuilt_text"),
                    "repaired_text": result.get("repaired_text"),
                }
                self._send_json(200, payload)
            else:
                self._send_json(404, {"error": "not_found"})
        except KeyError as exc:
            self._send_json(400, {"error": f"missing_field:{exc.args[0]}"})
        except Exception as exc:
            self._send_json(500, {"error": str(exc)})


def main(host: str = "127.0.0.1", port: int = 8080) -> None:
    server = ThreadingHTTPServer((host, port), XLifelineHandler)
    print(f"XLifelineAI API running on http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
