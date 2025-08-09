from typing import Any
import asyncio

from aiohttp import (
    ClientSession,
    ClientWebSocketResponse,
    WSMsgType,
    WSServerHandshakeError,
    ConnectionTimeoutError,
)

from aiomexc.ws.messages import PING, subscription
from aiomexc.exceptions import (
    MexcWsConnectionClosed,
    MexcWsConnectionNotEstablished,
    MexcWsUnknownMessageTypeError,
    MexcWsConnectionTimeoutError,
    MexcWsConnectionHandshakeError,
)

from .base import BaseWsSession, EventMessage, ConnectionMessage


class AiohttpWsSession(BaseWsSession):
    def __init__(
        self,
        session: ClientSession,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.http_session = session
        self.ws_session: ClientWebSocketResponse | None = None

    async def connect(self, url: str) -> None:
        if self.ws_session is not None and not self.ws_session.closed:
            return

        try:
            self.ws_session = await self.http_session.ws_connect(
                url,
                autoping=False,
                autoclose=True,
            )
        except WSServerHandshakeError as e:
            raise MexcWsConnectionHandshakeError(e.status) from e
        except ConnectionTimeoutError as e:
            raise MexcWsConnectionTimeoutError("Connection timeout") from e

    async def subscribe(self, streams: list[str]) -> None:
        if self.ws_session is None or self.ws_session.closed:
            raise MexcWsConnectionNotEstablished()
        
        # Send streams in batches of at most 30 items
        batch_size = 30
        for i in range(0, len(streams), batch_size):
            batch = streams[i:i+batch_size]
            msg = self.dump_message(subscription(batch))
            print(f'Sending subscription message for batch {i//batch_size + 1}/{(len(streams) + batch_size - 1)//batch_size}', msg)
            await self.ws_session.send_str(msg)
            # Small delay between batches to avoid overwhelming the server
            if i + batch_size < len(streams):
                await asyncio.sleep(1.0)

    async def receive(self) -> EventMessage | ConnectionMessage:
        if self.ws_session is None or self.ws_session.closed:
            raise MexcWsConnectionNotEstablished()

        msg = await self.ws_session.receive()

        if msg.type == WSMsgType.TEXT:
            return ConnectionMessage(self.load_json_message(msg.data))

        elif msg.type == WSMsgType.BINARY:
            return EventMessage(self.load_message(msg.data))

        elif msg.type in (WSMsgType.CLOSE, WSMsgType.CLOSING, WSMsgType.CLOSED):
            # print('Received CLOSE message', msg)
            raise MexcWsConnectionClosed()

        raise MexcWsUnknownMessageTypeError(f"Unknown message type: {msg.type}")

    async def ping(self) -> None:
        if self.ws_session is None or self.ws_session.closed:
            raise MexcWsConnectionNotEstablished()

        await self.ws_session.send_str(PING)

    async def close(self) -> None:
        if self.ws_session is None or self.ws_session.closed:
            raise MexcWsConnectionNotEstablished()

        await self.ws_session.close()
