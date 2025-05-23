import aio_pika

from configuration.config import settings
from database.session import connector
from dto.user import UserCreateDTO
from repositories.user_repository import UserRepository
from services.user_service import UserService

from .base import BaseMQ

MQ_USER_EXCHANGE_NAME = "user"
MQ_USER_QUEUE_NAME = "user_queue"

bindings_keys = [".signup"]


class UserQueue(BaseMQ):
    async def declare_queue(self):
        user_exchange = await self.channel.declare_exchange(
            name=MQ_USER_EXCHANGE_NAME,
            type=aio_pika.ExchangeType.TOPIC,
        )
        queue = await self.channel.declare_queue(
            name=MQ_USER_QUEUE_NAME,
            durable=True,
        )
        for binding_key in bindings_keys:
            await queue.bind(user_exchange, routing_key=binding_key)
        return queue

    async def callback(
        self,
        msg: aio_pika.IncomingMessage,
    ):
        # msg_data = self.deserialize_data(msg.body)
        async with connector.get_session() as session:
            user_repo = UserRepository(session=session)
            user_service = UserService(repository=user_repo)
            if msg.routing_key == ".signup":
                user = UserCreateDTO.model_validate_json(msg.body)
                await user_service.create_user(user=user)
        await msg.ack()

    async def consume_messages(self):
        await self.channel.set_qos(prefetch_count=1)
        queue = await self.declare_queue()

        async with queue.iterator() as iterator:
            message: aio_pika.IncomingMessage
            async for message in iterator:
                await self.callback(message)


user_queue = UserQueue(
    mq_url=settings.rmq.url,
)
