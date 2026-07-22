"""Shared HTTP client behavior for Messenger API wrappers."""

from __future__ import annotations

from typing import Any, Mapping

import requests


class BaseApiClient:
    """Base class with shared request behavior."""

    def __init__(
        self,
        page_access_token: str,
        *,
        timeout: float = 30.0,
        session: requests.Session | None = None,
    ) -> None:
        if not isinstance(page_access_token, str) or not page_access_token.strip():
            raise ValueError("page_access_token must be a non-empty string")
        if timeout <= 0:
            raise ValueError("timeout must be greater than 0")

        self._page_access_token = page_access_token
        self._timeout = timeout
        self._session = session or requests.Session()

    def get_access_token(self) -> str:
        return self._page_access_token

    def _post_json(self, url: str, body: Mapping[str, Any]) -> dict[str, Any]:
        response = self._session.post(
            url,
            params={"access_token": self.get_access_token()},
            json=body,
            timeout=self._timeout,
        )
        return response.json()

    def _post_multipart(self, url: str, data: Any, content_type: str) -> dict[str, Any]:
        response = self._session.post(
            url,
            params={"access_token": self.get_access_token()},
            data=data,
            headers={"content-type": content_type},
            timeout=self._timeout,
        )
        return response.json()
