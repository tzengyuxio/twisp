from datetime import datetime
from typing import NamedTuple


# CTCB(台幣消費明細): 帳單結帳日, 上期帳單金額, +本期帳款, +循環利息, -已繳款金額, -調整／退款, =本期應繳總金額
# ESUN(帳務資訊):    繳款幣別, 上期未繳餘額, 本期新增款項, 本期應繳總金額, 本期最低應繳金額
# TSIB(帳務資訊):    帳單結帳日, 帳單截止日, 上期應繳總額, -已繳退款總額, =前期餘額, +本期新增款項, =本期累計應繳金額, 本期最低應繳金額

# CITI: 簽帳日, 入帳日(起息日), 交易項目(外幣幣別,金額,折算日), 消費地區, 金額
# CTCB: 消費日, 入帳起息日, 消費暨收費摘要表,   台幣金額, 卡號末四碼, 消費地, 外幣折算日, 幣別, 消費地金額
# ESUN: 交易日期, 入帳日期, 交易項目／交易國家與地區, 外幣折算日, 幣別／金額, 繳款幣別, 金額
# TSIB: 消費日, 入帳起息日, 消費明細,        新臺幣金額,           外幣折算日, 消費地, 幣別, 外幣金額

class Transaction(NamedTuple):
    """
    A transaction is usually a row of credit card e-statement table.

    Attributes:
        trans_date: 消費日, 交易日期, 簽帳日
        post_date: 入帳起息日, 入帳日期, 入帳日(起息日)
        description: 交易項目, 消費暨收費摘要表, 消費明細
        country_area: 消費地, 交易國家與地區, 消費地區
        amount: 台幣金額, 新臺幣金額, 金額
        convert_date: 外幣折算日, 折算日
        foreign_currency: foreign currency, 幣別, 外幣幣別
        foreign_currency_amount: 消費地金額, 外幣金額
        card_no: 卡號末四碼
    """
    trans_date: datetime.date
    post_date: datetime.date
    description: str
    country_area: str
    amount: int
    convert_date: datetime.date
    foreign_currency: str
    foreign_currency_amount: float
    card_no: str


def minguo_to_ad(s):
    words = s.split("/")
    words[0] = str(int(words[0]) + 1911)
    return "-".join(words)
