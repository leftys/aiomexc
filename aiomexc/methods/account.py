from dataclasses import dataclass
from http import HTTPMethod

from aiomexc.types import AccountInformation, MyTrade
from .base import MexcMethod


@dataclass(kw_only=True)
class GetAccountInformation(MexcMethod):
    __returning__ = AccountInformation
    __api_http_method__ = HTTPMethod.GET
    __api_method__ = "account"
    __requires_auth__ = True


@dataclass(kw_only=True)
class GetMyTrades(MexcMethod):
    __returning__ = list[MyTrade]
    __api_http_method__ = HTTPMethod.GET
    __api_method__ = "myTrades"
    __requires_auth__ = True

    symbol: str
    limit: int = 100
