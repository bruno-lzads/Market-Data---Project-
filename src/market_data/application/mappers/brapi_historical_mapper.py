from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from typing import Any

from market_data.application.exceptions import DataMappingError
from market_data.domain.entities.historical_price import HistoricalPrice


def map_brapi_historical_data(
    payload: dict[str, Any],
) -> list[HistoricalPrice]:
    """Map a raw brapi historical response into normalized OHLCV records."""

    results = payload.get("results")

    if not isinstance(results, list):
        raise DataMappingError(
            "Expected 'results' to be a list"
        )

    prices: list[HistoricalPrice] = []

    for result in results:
        if not isinstance(result, dict):
            raise DataMappingError(
                "Expected each result to be an object"
            )

        prices.extend(_map_result(result))

    return prices


def _map_result(result: dict[str, Any]) -> list[HistoricalPrice]:
    symbol = result.get("symbol")

    if not isinstance(symbol, str) or not symbol.strip():
        raise DataMappingError(
            "Expected result to contain a valid symbol"
        )

    data = result.get("data")

    if not isinstance(data, dict):
        raise DataMappingError(
            f"Expected data object for symbol {symbol}"
        )

    historical_data = data.get("historicalDataPrice")

    if not isinstance(historical_data, list):
        raise DataMappingError(
            f"Expected historicalDataPrice list for symbol {symbol}"
        )

    return [
        _map_price(symbol, item)
        for item in historical_data
    ]


def _map_price(
    symbol: str,
    item: Any,
) -> HistoricalPrice:
    if not isinstance(item, dict):
        raise DataMappingError(
            f"Expected historical price for {symbol} to be an object"
        )

    try:
        timestamp = int(item["date"])

        observed_at = datetime.fromtimestamp(
            timestamp,
            tz=timezone.utc,
        )

        open_price = _to_decimal(item["open"])
        high_price = _to_decimal(item["high"])
        low_price = _to_decimal(item["low"])
        close_price = _to_decimal(item["close"])

    except (KeyError, TypeError, ValueError, InvalidOperation) as exc:
        raise DataMappingError(
            f"Invalid historical price for symbol {symbol}"
        ) from exc

    volume = _to_optional_int(item.get("volume"))

    return HistoricalPrice(
        symbol=symbol.strip().upper(),
        observed_at=observed_at,
        open=open_price,
        high=high_price,
        low=low_price,
        close=close_price,
        volume=volume,
    )


def _to_decimal(value: Any) -> Decimal:
    if value is None:
        raise ValueError("Price must not be null")

    return Decimal(str(value))


def _to_optional_int(value: Any) -> int | None:
    if value is None:
        return None

    return int(value)