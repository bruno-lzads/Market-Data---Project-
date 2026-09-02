from collections.abc import Sequence
from typing import Any

import requests
from requests import Session

from market_data.infrastructure.api.exceptions import (
    BrapiRequestError,
    BrapiResponseError,
)


class BrapiClient:
    """Cliente HTTP para a API de dados financeiros brapi."""

    HISTORICAL_PATH = "/api/v2/stocks/historical"

    def __init__(
        self,
        base_url: str,
        token: str | None = None,
        timeout_seconds: float = 10.0,
        session: Session | None = None,
    ) -> None:
        if not base_url.strip():
            raise ValueError("base_url não pode estar vazio")

        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds deve ser maior que zero")

        self._base_url = base_url.rstrip("/")
        self._token = token
        self._timeout_seconds = timeout_seconds
        self._session = session or requests.Session()

    def get_historical_data(
        self,
        symbols: Sequence[str],
        *,
        range_: str = "1mo",
        interval: str = "1d",
    ) -> dict[str, Any]:
        """Obtem dados históricos brutos de mercado para um ou mais símbolos."""

        normalized_symbols = self._normalize_symbols(symbols)

        params = {
            "symbols": ",".join(normalized_symbols),
            "range": range_,
            "interval": interval,
        }

        try:
            response = self._session.get(
                f"{self._base_url}{self.HISTORICAL_PATH}",
                params=params,
                headers=self._build_headers(),
                timeout=self._timeout_seconds,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            raise BrapiRequestError(
                "Falha ao obter dados históricos da brapi"
            ) from exc

        try:
            payload = response.json()
        except requests.exceptions.JSONDecodeError as exc:
            raise BrapiResponseError(
                "A Brapi retornou uma resposta que não é um JSON válido."
            ) from exc

        if not isinstance(payload, dict):
            raise BrapiResponseError(
                "A Brapi retornou uma estrutura JSON inesperada."
            )

        return payload

    def _build_headers(self) -> dict[str, str]:
        headers = {
            "Accept": "application/json",
        }

        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"

        return headers

    @staticmethod
    def _normalize_symbols(symbols: Sequence[str]) -> list[str]:
        normalized = [
            symbol.strip().upper()
            for symbol in symbols
            if symbol.strip()
        ]

        if not normalized:
            raise ValueError("Pelo menos um símbolo deve ser fornecido.")

        return normalized