from typing import Any

import aio_pika

from .base import BaseMQ
from configuration.config import settings


MQ_USER_EXCHANGE_NAME = "user"
MQ_USER_REGISTER_ROUTING_KEY = ".signup"


class UserQueue(BaseMQ):
    async def declare_user_exchange(self):
        user_exchange = await self.channel.declare_exchange(
            name=MQ_USER_EXCHANGE_NAME,
            type=aio_pika.ExchangeType.TOPIC,
        )
        return user_exchange

    async def publish_message(self, data: Any, routing_key: str):
        user_exchange = await self.declare_user_exchange()
        message_body = self.serialize_data(data)
        message = aio_pika.Message(
            body=message_body,
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
        )
        await user_exchange.publish(
            message=message,
            routing_key=routing_key,
        )


user_mq = UserQueue(settings.rmq.url)
