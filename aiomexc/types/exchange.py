from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class ExchangeSymbol:
    symbol: str
    status: str
    baseAsset: str
    baseAssetPrecision: int
    quoteAsset: str
    quotePrecision: int
    quoteAssetPrecision: int
    baseCommissionPrecision: int
    quoteCommissionPrecision: int
    orderTypes: List[str]
    isSpotTradingAllowed: bool
    isMarginTradingAllowed: bool
    quoteAmountPrecision: str
    baseSizePrecision: str
    permissions: List[str]
    filters: List[Any]
    maxQuoteAmount: str
    makerCommission: str
    takerCommission: str
    quoteAmountPrecisionMarket: str
    maxQuoteAmountMarket: str
    fullName: str
    tradeSideType: int
    contractAddress: str
    st: bool

@dataclass
class ExchangeInfoType:
    timezone: str
    serverTime: int
    rateLimits: List[Any]
    exchangeFilters: List[Any]
    symbols: List[ExchangeSymbol]
