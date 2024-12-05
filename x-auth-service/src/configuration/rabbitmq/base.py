import json
from typing import Any

import aio_pika
from pydantic import BaseModel


class BaseMQ:
    """Base class for RabbitMQ"""
    def __init__(self, mq_url: str) -> None:
        self.mq_url = mq_url
        self.connection = None
        self.channel = None

    async def mq_connect(self):
        self.connection = await aio_pika.connect_robust(url=self.mq_url)
        self.channel = await self.connection.channel()

    async def mq_close_connection(self):
        await self.connection.close()

    @staticmethod
    def serialize_data(data: Any) -> bytes:
        def custom_serializer(obj):
            if isinstance(obj, BaseModel):
                return obj.model_dump()
        return json.dumps(data, default=custom_serializer).encode()

    @staticmethod
    def deserialize_data(data: bytes) -> Any:
        return json.loads(data)
