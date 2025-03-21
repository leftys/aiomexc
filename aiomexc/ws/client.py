from aiomexc.session.base import BaseSession


class MexcWsClient:
    def __init__(self, session: BaseSession):
        self.session = session
