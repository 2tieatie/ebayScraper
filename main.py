from ebayscaper.ebayscraper import EbayScraper

es = EbayScraper()

item = es.get_item("https://www.ebay.com/itm/256569817595?itmmeta=01J32Z98B62BPXNF9FC3S6F7KS&hash=item3bbcc0b9fb%3Ag%3AH00AAOSwvJlmkBLk")

item.print()
print(item.json())
item.write()

