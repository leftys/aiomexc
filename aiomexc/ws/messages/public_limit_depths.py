from typing import cast
from dataclasses import dataclass

from aiomexc.ws.proto import PushMessage
from aiomexc.ws.proto.public_limit_depths import (
    PublicLimitDepthItemMessage as ProtoPublicLimitDepthItemMessage,
    PublicLimitDepthsMessage as ProtoPublicLimitDepthsMessage,
)

from .base import BaseMessage


@dataclass
class PublicLimitDepthItemMessage(BaseMessage):
    price: str
    quantity: str

    @classmethod
    def from_proto(
        cls, message: ProtoPublicLimitDepthItemMessage
    ) -> "PublicLimitDepthItemMessage":
        return cls(
            price=message.price,
            quantity=message.quantity,
        )


@dataclass
class PublicLimitDepthsMessage(BaseMessage):
    asks: list[PublicLimitDepthItemMessage]
    bids: list[PublicLimitDepthItemMessage]
    event_type: str
    version: str
    symbol: str
    time: int

    @classmethod
    def from_proto(cls, message: PushMessage) -> "PublicLimitDepthsMessage":
        assert message.public_limit_depths is not None, "public_limit_depths is None"
        proto: ProtoPublicLimitDepthsMessage = message.public_limit_depths

        return cls(
            asks=[PublicLimitDepthItemMessage.from_proto(it) for it in proto.asks],
            bids=[PublicLimitDepthItemMessage.from_proto(it) for it in proto.bids],
            event_type=proto.event_type,
            version=proto.version,
            symbol=cast(str, message.symbol),
            time=cast(int, message.send_time),
        )
