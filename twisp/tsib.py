import re
from collections import namedtuple
from datetime import datetime

import tika
from tika import parser
from .utils import minguo_to_ad

row_pattern = r"^(\d{3}/\d{2}/\d{2}) (\d{3}/\d{2}/\d{2})\s(.*\n?.*)\s{1,2}(-?\d+(?:,\d{3})*(?:\.\d+)?) (\d{4})? ([A-Z]{2})? ([A-Z]{3})? (\d+(?:,\d{3})*(?:\.\d+)?)?\s?$"

Record = namedtuple(
    "Record",
    [
        "trans_date",
        "post_date",
        "details",
        "amount",
        "translation_date",
        "country",
        "currency",
        "foreign_currency_amount",
    ],
)


def pdf_to_text_tika(filename):
    return parser.from_file(filename)["content"]


def liberate_data_table(text):
    rows = []
    text = re.sub(
        r"^(\d{3}/\d{2}/\d{2} \d{3}/\d{2}/\d{2})", r"\n\1", text, flags=re.MULTILINE
    )
    matches = re.findall(row_pattern, text, re.MULTILINE)
    for m in matches:
        trans_date = datetime.fromisoformat(minguo_to_ad(m[0])).date()
        post_date = datetime.fromisoformat(minguo_to_ad(m[1])).date()
        # if (post_date - trans_date).days > 7:
        #     dd = (post_date - trans_date).days
        #     print('[EXCEPT] [{:3d}] {}'.format(dd, m))
        details = " | ".join([x.strip() for x in m[2].split("\n")])
        translation_date = None
        if m[4]:
            yy, mm, dd = trans_date.year, int(m[4][:2]), int(m[4][2:])
            translation_date = datetime(yy, mm, dd).date()
            if translation_date < trans_date:
                print("[EXCEPT]", m)
                translation_date = datetime(yy + 1, mm, dd).date()
        country = m[5] if m[5] else None
        currency = m[6] if m[6] else None
        row = Record(
            trans_date,
            post_date,
            details,
            m[3],
            translation_date,
            country,
            currency,
            m[7],
        )
        rows.append(row)
    return rows


class CreditCardParser:
    """An parser for TSIB credit card e-statement PDF file"""

    def __init__(self):
        tika.initVM()

    def identify(self, filename):
        pass

    @staticmethod
    def extract(filename):
        text = pdf_to_text_tika(filename)
        rows = liberate_data_table(text)
        for r in rows:
            print(r)
