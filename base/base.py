import json
from typing import List, Union
from urllib.parse import urlparse
from pandas import json_normalize
import pandas as pd


class URL(str):
    def __new__(cls, content: str):
        instance = super().__new__(cls, content)
        instance._validate()
        return instance

    def _validate(self) -> None:
        if not self.__is_valid_url(self):
            raise ValueError(f"Invalid URL: {self}")

    @staticmethod
    def __is_valid_url(url: str) -> bool:
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False


class Price(int):
    def __new__(cls, value: Union[int, str]):
        if isinstance(value, str):
            value = cls._convert_to_int(value)
        instance = super().__new__(cls, value)
        instance._validate()
        return instance

    @staticmethod
    def _convert_to_int(value: str) -> int:
        try:
            return int(value)
        except ValueError:
            raise ValueError(f"Cannot convert {value} to an integer.")

    def _validate(self) -> None:
        if not self.__is_valid_price(self):
            raise ValueError(f"Invalid Price: {self}")

    @staticmethod
    def __is_valid_price(price: int) -> bool:
        return price >= 0


class RestCountriesException(Exception): ...


class EbayScraperException(Exception): ...


class PandasJSONConverter:

    def convert(self, data: List[dict]) -> pd.DataFrame:
        return json_normalize(data)


class EbayItem:
    def __init__(
        self,
        images: List[str],
        title: str,
        url: str,
        seller: str,
        price: Union[str, int],
        delivery_price: Union[str, int],
    ):
        self.images: List[URL] = [URL(image) for image in images]
        self.title: str = title
        self.url: URL = URL(url)
        self.seller: str = seller
        self.price: Union[str, int] = price
        self.delivery_price: Union[str, int] = delivery_price

    def print(self) -> None:
        fields = self.__dict__.items()
        data = f'{", ".join([f"{k}={v}" for k, v in fields if not k.startswith("_")])}'
        print(f"{self.__class__.__name__}({data})")

    def json(self) -> dict:
        fields = self.__dict__.items()
        return {k: v for k, v in fields if not k.startswith("_")}

    def write(self, filename: str = None) -> None:
        if not filename:
            filename = self.title.replace(' ', '-') + '.json'
        with open(filename, "w") as file:
            json.dump(self.json(), file, indent=4)
