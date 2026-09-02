from pprint import pprint

from market_data.infrastructure.api.brapi_client import BrapiClient
from market_data.infrastructure.api.exceptions import BrapiClientError
from market_data.application.mappers.brapi_historical_mapper import (map_brapi_historical_data,)


def main() -> None:
    client = BrapiClient(
        base_url="https://brapi.dev",
        timeout_seconds=10.0,
    )

    try:
        payload = client.get_historical_data(
            ["PETR4"],
            range_="1mo",
            interval="1d",
        )
        prices = map_brapi_historical_data(payload)

        for price in prices[:5]:
            print(price)
            
    except BrapiClientError as exc:
        print(f"Failed to communicate with brapi: {exc}")
        raise SystemExit(1) from exc

    pprint(payload)


if __name__ == "__main__":
    main()

