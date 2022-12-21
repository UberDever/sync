#!/bin/python3

import logging
import requests
import json
from bs4 import BeautifulSoup


def strip_table(soup, indent=None):
    rows = soup.find_all("tr")

    headers = {}
    thead = soup.find("thead")
    if thead:
        thead = thead.find_all("th")
        for i in range(len(thead)):
            headers[i] = thead[i].text.strip().lower()
    data = []
    for row in rows:
        cells = row.find_all("td")
        if thead:
            items = {}
            if len(cells) > 0:
                for index in headers:
                    items[headers[index]] = cells[index].text
        else:
            items = []
            for index in cells:
                items.append(index.text.strip())
        if items:
            data.append(items)
    return data


def parse_method_summary(soup: BeautifulSoup):
    method_summary = soup.find('table', 'memberSummary')
    code = method_summary.find_all('code')
    for i, c in enumerate(code):
        signature = ""
        signature += c.text
        if i % 2 == 1:
            print(signature)
            signature = ""


def main():
    logging.getLogger().setLevel(logging.INFO)
    url = "https://docs.oracle.com/javase/9/docs/api/java/util/Arrays.html"
    resp = requests.get(url)
    if resp.ok:
        html = resp.text
        logging.debug(html)
        soup = BeautifulSoup(html, 'html.parser')
        parse_method_summary(soup)
    else:
        logging.critical(resp.status_code)
        logging.critical(resp.text)
        exit(-1)


main()
