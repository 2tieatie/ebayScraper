import lxml
import requests
from lxml import html
from lxml.etree import XMLSyntaxError
from typing import Union

from base.base import URL, EbayScraperException, EbayItem


class EbayScraper:

    TITLE_XPATH = '//h1[@class="x-item-title__mainTitle"]/span'
    PRICE_XPATH = '//div[@class="x-price-primary"]/span'
    IMAGES_XPATH = '//div[@class="ux-image-grid no-scrollbar"]//img'
    SELLER_XPATH = '//div[@class="x-sellercard-atf__info__about-seller"]//span'
    DELIVERY_PRICE = '//div[@class="ux-labels-values col-12 ux-labels-values--shipping"]/div[2]//span'

    @staticmethod
    def __parse_element(
        path: str, html_content: html.HtmlElement, all_elements: bool = False
    ) -> Union[html.Element, list[html.Element]]:
        elements = html_content.xpath(path)
        if not elements:
            if all_elements:
                return elements
            return None

        if all_elements:
            return elements
        return elements[0]

    def __make_request(self, url: URL) -> html.HtmlElement:
        response = requests.get(str(url))

        if response.status_code != 200:
            raise EbayScraperException(
                f"Request to {url} failed with status code {response.status_code}"
            )

        try:
            tree = html.fromstring(response.content)
        except XMLSyntaxError as e:
            raise EbayScraperException(f"Failed to parse HTML from {url}: {e}")

        return tree

    def get_item(self, url: str):
        tree = self.__make_request(URL(url))
        title = self.__parse_element(self.TITLE_XPATH, tree)
        if title is not None:
            title = title.text.strip()

        price = self.__parse_element(self.PRICE_XPATH, tree)
        if price is not None:
            price = price.text.strip()

        seller = self.__parse_element(self.SELLER_XPATH, tree)
        if seller is not None:
            seller = seller.text.strip()

        delivery_price = self.__parse_element(self.DELIVERY_PRICE, tree)
        if delivery_price is not None:
            delivery_price = delivery_price.text.strip()

        images: list[html.Element] = self.__parse_element(self.IMAGES_XPATH, tree, all_elements=True)
        images = [image.get('src') for image in images if image.get('src')]

        ebay_item = EbayItem(title=title, images=images, price=price, delivery_price=delivery_price, seller=seller, url=url)
        return ebay_item
