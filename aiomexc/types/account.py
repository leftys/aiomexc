from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime


@dataclass
class Balance:
    asset: str
    free: Decimal
    locked: Decimal


@dataclass
class AccountInformation:
    can_trade: bool
    can_withdraw: bool
    can_deposit: bool
    update_time: datetime | None
    account_type: str
    balances: list[Balance]
    permissions: list[str]


@dataclass
class MyTrade:
    symbol: str
    id: str
    order_id: str
    order_list_id: int
    price: Decimal
    qty: Decimal
    quote_qty: Decimal
    commission: Decimal
    commission_asset: str
    time: datetime
    is_buyer: bool
    is_maker: bool
    is_best_match: bool
    is_self_trade: bool
    client_order_id: str | None
