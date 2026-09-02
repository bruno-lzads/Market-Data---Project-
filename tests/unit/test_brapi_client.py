from typing import Any

import pytest
import requests

from market_data.infrastructure.api.brapi_client import BrapiClient
from market_data.infrastructure.api.exceptions import (
    BrapiRequestError,
    BrapiResponseError,
)


class FakeResponse:
    def __init__(
        self,
        payload: Any,
        *,
        status_error: requests.HTTPError | None = None,
        json_error: Exception | None = None,
    ) -> None:
        self._payload = payload
        self._status_error = status_error
        self._json_error = json_error

    def raise_for_status(self) -> None:
        if self._status_error:
            raise self._status_error

    def json(self) -> Any:
        if self._json_error:
            raise self._json_error

        return self._payload


class FakeSession:
    def __init__(
        self,
        response: FakeResponse | None = None,
        request_error: requests.RequestException | None = None,
    ) -> None:
        self._response = response
        self._request_error = request_error
        self.last_request: dict[str, Any] | None = None

    def get(
        self,
        url: str,
        *,
        params: dict[str, str],
        headers: dict[str, str],
        timeout: float,
    ) -> FakeResponse:
        self.last_request = {
            "url": url,
            "params": params,
            "headers": headers,
            "timeout": timeout,
        }

        if self._request_error:
            raise self._request_error

        if self._response is None:
            raise AssertionError("FakeSession não possui resposta configurada.")

        return self._response


def test_get_historical_data_returns_raw_payload() -> None:
    payload = {
        "results": [
            {
                "symbol": "PETR4",
            }
        ]
    }
    session = FakeSession(response=FakeResponse(payload))

    client = BrapiClient(
        base_url="https://brapi.dev/",
        token="test-token",
        timeout_seconds=5.0,
        session=session,  # type: ignore[arg-type]
    )

    result = client.get_historical_data(
        [" petr4 ", "vale3"],
        range_="1mo",
        interval="1d",
    )

    assert result == payload
    assert session.last_request == {
        "url": "https://brapi.dev/api/v2/stocks/historical",
        "params": {
            "symbols": "PETR4,VALE3",
            "range": "1mo",
            "interval": "1d",
        },
        "headers": {
            "Accept": "application/json",
            "Authorization": "Bearer test-token",
        },
        "timeout": 5.0,
    }


def test_get_historical_data_does_not_send_authorization_without_token() -> None:
    session = FakeSession(response=FakeResponse({"results": []}))

    client = BrapiClient(
        base_url="https://brapi.dev",
        session=session,  # type: ignore[arg-type]
    )

    client.get_historical_data(["PETR4"])

    assert session.last_request is not None
    assert session.last_request["headers"] == {
        "Accept": "application/json",
    }


def test_get_historical_data_rejects_empty_symbols() -> None:
    client = BrapiClient(base_url="https://brapi.dev")

    with pytest.raises(
        ValueError,
        match="Pelo menos um símbolo deve ser fornecido.",
    ):
        client.get_historical_data([])


def test_get_historical_data_wraps_request_errors() -> None:
    session = FakeSession(
        request_error=requests.Timeout("request timed out")
    )

    client = BrapiClient(
        base_url="https://brapi.dev",
        session=session,  # type: ignore[arg-type]
    )

    with pytest.raises(BrapiRequestError) as error:
        client.get_historical_data(["PETR4"])

    assert isinstance(error.value.__cause__, requests.Timeout)


def test_get_historical_data_rejects_non_object_json() -> None:
    session = FakeSession(response=FakeResponse(["unexpected", "list"]))

    client = BrapiClient(
        base_url="https://brapi.dev",
        session=session,  # type: ignore[arg-type]
    )

    with pytest.raises(
        BrapiResponseError,
        match="estrutura JSON inesperada",
    ):
        client.get_historical_data(["PETR4"])