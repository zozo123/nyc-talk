"""Minimal Boat API client. Secrets stay in the environment."""
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any


class BoatError(RuntimeError):
    def __init__(self, payload: Any):
        self.payload = payload
        super().__init__(str(payload))


class Boat:
    def __init__(self, key: str | None = None, base: str | None = None):
        self.key = key or os.environ["BOAT_API_KEY"]
        self.base = (base or os.environ.get("BOAT_API_BASE", "https://boat.dev/api/v1")).rstrip("/")

    def _request(self, method: str, path: str, body: dict | None = None,
                 query: dict | None = None, extra_headers: dict | None = None,
                 timeout: int = 90) -> dict:
        url = self.base + path
        if query:
            url += "?" + urllib.parse.urlencode(query)
        data = None if body is None else json.dumps(body).encode()
        headers = {
            "Authorization": "Bearer " + self.key,
            "Accept": "application/json",
        }
        if data is not None:
            headers["Content-Type"] = "application/json"
        if extra_headers:
            headers.update(extra_headers)
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                raw = response.read()
                return json.loads(raw) if raw else {}
        except urllib.error.HTTPError as error:
            raw = error.read()
            try:
                payload = json.loads(raw)
            except json.JSONDecodeError:
                payload = {"status": error.code, "message": raw.decode("utf-8", "replace")}
            raise BoatError(payload) from error

    def create(self, *, name: str, ttl: int, no_env: bool, idempotency: str) -> dict:
        return self._request(
            "POST", "/sandboxes",
            {"name": name, "ttlSeconds": ttl, "noEnv": no_env, "type": "default"},
            extra_headers={"Idempotency-Key": idempotency},
        )

    def get(self, sandbox_id: str) -> dict:
        return self._request("GET", f"/sandboxes/{sandbox_id}")

    def wait_ready(self, sandbox_id: str, timeout: int = 180) -> dict:
        deadline = time.time() + timeout
        delay = 1.0
        last = {}
        while time.time() < deadline:
            last = self.get(sandbox_id)
            sandbox = last.get("sandbox") or last
            state = sandbox.get("state")
            if state in {"ready", "idle", "running"}:
                return last
            if state in {"error", "deleted"}:
                raise BoatError(last)
            time.sleep(delay)
            delay = min(delay * 1.5, 5)
        raise TimeoutError(f"sandbox {sandbox_id} not ready: {last}")

    def write_file(self, sandbox_id: str, path: str, content: str) -> dict:
        return self._request("PUT", f"/sandboxes/{sandbox_id}/files",
                             {"path": path, "content": content, "encoding": "utf8"})

    def command(self, sandbox_id: str, command: str, timeout_seconds: int = 30) -> dict:
        return self._request(
            "POST", f"/sandboxes/{sandbox_id}/commands",
            {"command": command, "timeoutSeconds": timeout_seconds},
            timeout=timeout_seconds + 30,
        )

    def stop(self, sandbox_id: str) -> dict:
        return self._request("POST", f"/sandboxes/{sandbox_id}/stop", {})
