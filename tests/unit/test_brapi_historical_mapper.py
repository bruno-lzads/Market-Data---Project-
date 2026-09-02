from datetime import datetime, timezone
from decimal import Decimal

import pytest

from market_data.application.exceptions import DataMappingError
from market_data.application.mappers.brapi_historical_mapper import (
    map_brapi_historical_data,
)


def test_maps_historical_price() -> None:
    payload = {
        "results": [
            {
                "symbol": "PETR4",
                "data": {
                    "historicalDataPrice": [
                        {
                            "date": 1722470400,
                            "open": 37.10,
                            "high": 38.80,
                            "low": 36.95,
                            "close": 38.52,
                            "volume": 1234567,
                            "adjustedClose": 38.40,
                        }
                    ]
                },
            }
        ]
    }

    result = map_brapi_historical_data(payload)

    assert len(result) == 1

    price = result[0]

    assert price.symbol == "PETR4"
    assert price.observed_at == datetime.fromtimestamp(
        1722470400,
        tz=timezone.utc,
    )
    assert price.open == Decimal("37.1")
    assert price.high == Decimal("38.8")
    assert price.low == Decimal("36.95")
    assert price.close == Decimal("38.52")
    assert price.volume == 1234567


from datetime import datetime, timezone
from decimal import Decimal

import pytest

from market_data.application.exceptions import DataMappingError
from market_data.application.mappers.brapi_historical_mapper import (
    map_brapi_historical_data,
)


def test_maps_historical_price() -> None:
    payload = {
        "results": [
            {
                "symbol": "PETR4",
                "data": {
                    "historicalDataPrice": [
                        {
                            "date": 1722470400,
                            "open": 37.10,
                            "high": 38.80,
                            "low": 36.95,
                            "close": 38.52,
                            "volume": 1234567,
                            "adjustedClose": 38.40,
                        }
                    ]
                },
            }
        ]
    }

    result = map_brapi_historical_data(payload)

    assert len(result) == 1

    price = result[0]

    assert price.symbol == "PETR4"
    assert price.observed_at == datetime.fromtimestamp(
        1722470400,
        tz=timezone.utc,
    )
    assert price.open == Decimal("37.1")
    assert price.high == Decimal("38.8")
    assert price.low == Decimal("36.95")
    assert price.close == Decimal("38.52")
    assert price.volume == 1234567


def test_maps_multiple_symbols() -> None:
    payload = {
        "results": [
            {
                "symbol": "PETR4",
                "data": {
                    "historicalDataPrice": [
                        {
                            "date": 1722470400,
                            "open": 37,
                            "high": 39,
                            "low": 36,
                            "close": 38,
                            "volume": 1000,
                        }
                    ]
                },
            },
            {
                "symbol": "VALE3",
                "data": {
                    "historicalDataPrice": [
                        {
                            "date": 1722470400,
                            "open": 60,
                            "high": 62,
                            "low": 59,
                            "close": 61,
                            "volume": 2000,
                        }
                    ]
                },
            },
        ]
    }

    result = map_brapi_historical_data(payload)

    assert len(result) == 2
    assert result[0].symbol == "PETR4"
    assert result[1].symbol == "VALE3"


def test_accepts_missing_volume() -> None:
    payload = {
        "results": [
            {
                "symbol": "PETR4",
                "data": {
                    "historicalDataPrice": [
                        {
                            "date": 1722470400,
                            "open": 37,
                            "high": 39,
                            "low": 36,
                            "close": 38,
                        }
                    ]
                },
            }
        ]
    }

    result = map_brapi_historical_data(payload)

    assert result[0].volume is None


def test_rejects_missing_results() -> None:
    payload = {}

    with pytest.raises(
        DataMappingError,
        match="Expected 'results' to be a list",
    ):
        map_brapi_historical_data(payload)


def test_rejects_missing_historical_data() -> None:
    payload = {
        "results": [
            {
                "symbol": "PETR4",
                "data": {},
            }
        ]
    }

    with pytest.raises(
        DataMappingError,
        match="historicalDataPrice",
    ):
        map_brapi_historical_data(payload)


def test_rejects_empty_symbol() -> None:
    payload = {
        "results": [
            {
                "symbol": "",
                "data": {
                    "historicalDataPrice": []
                },
            }
        ]
    }

    with pytest.raises(
        DataMappingError,
        match="valid symbol",
    ):
        map_brapi_historical_data(payload)


def test_rejects_null_open_price() -> None:
    payload = {
        "results": [
            {
                "symbol": "PETR4",
                "data": {
                    "historicalDataPrice": [
                        {
                            "date": 1722470400,
                            "open": None,
                            "high": 39,
                            "low": 36,
                            "close": 38,
                            "volume": 100,
                        }
                    ]
                },
            }
        ]
    }

    with pytest.raises(
        DataMappingError,
        match="Invalid historical price for symbol PETR4",
    ):
        map_brapi_historical_data(payload)