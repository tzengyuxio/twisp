import re
from datetime import datetime

import tika
from tika import parser
from .utils import minguo_to_ad, Transaction

row_pattern = r"^(\d{3}/\d{2}/\d{2}) (\d{3}/\d{2}/\d{2})\s(.*\n?.*)\s{1,2}(-?\d+(?:,\d{3})*(?:\.\d+)?) (\d{4})? ([A-Z]{2})? ([A-Z]{3})? (\d+(?:,\d{3})*(?:\.\d+)?)?\s?$"


def pdf_to_text_tika(filename):
    return parser.from_file(filename)["content"]


def liberate_data_table(text):
    rows = []
    m = re.search(r'卡號末四碼:(\d{4})', text)
    card_no = m.group(0)
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
        desc = " | ".join([x.strip() for x in m[2].split("\n")])
        convert_date = None
        if m[4]:
            yy, mm, dd = trans_date.year, int(m[4][:2]), int(m[4][2:])
            convert_date = datetime(yy, mm, dd).date()
            if convert_date < trans_date:
                print("[EXCEPT]", m)
                convert_date = datetime(yy + 1, mm, dd).date()
        country = m[5] if m[5] else None
        currency = m[6] if m[6] else None
        row = Transaction(
            trans_date,
            post_date,
            desc,
            country,
            m[3],
            convert_date,
            currency,
            m[7],
            card_no,
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
