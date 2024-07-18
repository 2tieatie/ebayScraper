from typing import Optional, List

import pandas as pd
import requests
from urllib.parse import urlencode
from base.base import RestCountriesException, PandasJSONConverter


class RestCountries:
    BASE_URL = "https://restcountries.com/v3.1/"

    def __init__(self):
        self.converter = PandasJSONConverter()

    def _make_request(self, endpoint: str, params: Optional[dict] = None) -> List[dict]:
        url = f"{self.BASE_URL}{endpoint}"
        if params:
            url += f"?{urlencode(params)}"

        response = requests.get(url)
        if response.status_code != 200:
            raise RestCountriesException(
                f"API request failed: {response.status_code} - {response.text}"
            )

        return response.json()

    def _extract_relevant_fields(self, data: List[dict]) -> pd.DataFrame:
        records = []
        for country in data:
            country_name = country.get("name", {}).get("common", "N/A")
            capital = country.get("capital", ["N/A"])[0]
            flag_url = country.get("flags", {}).get("png", "N/A")
            records.append(
                {"Country": country_name, "Capital": capital, "Flag URL": flag_url}
            )
        return pd.DataFrame(records)

    def get_all(self) -> pd.DataFrame:
        result = self._make_request("all")
        return self._extract_relevant_fields(result)

    def get_by_name(self, name: str) -> pd.DataFrame:
        result = self._make_request(f"name/{name}")
        return self._extract_relevant_fields(result)

    def get_by_code(self, code: str) -> pd.DataFrame:
        result = self._make_request(f"alpha/{code}")
        return self._extract_relevant_fields(result)

    def get_by_codes(self, codes: List[str]) -> pd.DataFrame:
        params = {"codes": ",".join(codes)}
        result = self._make_request("alpha", params)
        return self._extract_relevant_fields(result)

    def get_by_currency(self, currency: str) -> pd.DataFrame:
        result = self._make_request(f"currency/{currency}")
        return self._extract_relevant_fields(result)

    def get_by_demonym(self, demonym: str) -> pd.DataFrame:
        result = self._make_request(f"demonym/{demonym}")
        return self._extract_relevant_fields(result)

    def get_by_language(self, language: str) -> pd.DataFrame:
        result = self._make_request(f"lang/{language}")
        return self._extract_relevant_fields(result)

    def get_by_capital(self, capital: str) -> pd.DataFrame:
        result = self._make_request(f"capital/{capital}")
        return self._extract_relevant_fields(result)

    def get_by_region(self, region: str) -> pd.DataFrame:
        result = self._make_request(f"region/{region}")
        return self._extract_relevant_fields(result)

    def get_by_subregion(self, subregion: str) -> pd.DataFrame:
        result = self._make_request(f"subregion/{subregion}")
        return self._extract_relevant_fields(result)

    def get_by_translation(self, translation: str) -> pd.DataFrame:
        result = self._make_request(f"translation/{translation}")
        return self._extract_relevant_fields(result)

    def get_independent(self, status: bool = True) -> pd.DataFrame:
        params = {"status": str(status).lower()}
        result = self._make_request("independent", params)
        return self._extract_relevant_fields(result)


