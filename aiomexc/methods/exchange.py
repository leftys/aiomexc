from dataclasses import dataclass
from http import HTTPMethod
from aiomexc.types.exchange import ExchangeInfoType
from .base import MexcMethod

@dataclass(kw_only=True)
class GetExchangeInfo(MexcMethod):
    __returning__ = ExchangeInfoType
    __api_http_method__ = HTTPMethod.GET
    __api_method__ = "exchangeInfo"
    __requires_auth__ = False

    # No parameters required for this endpoint
