from typing import Protocol, List

import pandas as pd


class IScraper(Protocol):

    def _make_request(self): ...


class IURL(Protocol):
    def _validate(self): ...

    def __is_valid_url(self): ...


class IPrice(Protocol):

    def _validate(self) -> None: ...


class IPandasJSONConverter(Protocol):
    def convert(self, data: List[dict]) -> pd.DataFrame: ...


class IEbayItem(Protocol):
    def print(self) -> None: ...

    def json(self) -> dict: ...

    def write(self, filename: str) -> None: ...
