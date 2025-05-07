from contextlib import asynccontextmanager
from io import BytesIO
from typing import Union

from aiobotocore.session import get_session

from configuration.config import settings


class S3StorageService:
    def __init__(
        self,
        access_key: str,
        secret_key: str,
        endpoint_url: str,
        bucket_name: str,
    ):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
        }
        self.bucket_name = bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def upload_file(
        self,
        destination_path: str,
        content: Union[str, bytes],
    ) -> None:
        if isinstance(content, bytes):
            buffer = BytesIO(content)
        else:
            buffer = BytesIO(content.encode("utf-8"))
        async with self.get_client() as client:
            await client.put_object(
                Bucket=self.bucket_name,
                Key=destination_path,
                Body=buffer,
            )

    async def get_file(self, key: str):
        async with self.get_client() as client:
            response = await client.get_object(Bucket=self.bucket_name, Key=key)
            data: bytes = await response["Body"].read()
            return data

    async def delete_file(self, key: str):
        async with self.get_client() as client:
            await client.delete_object(Bucket=self.bucket_name, Key=key)


s3_service = S3StorageService(
    access_key=settings.s3.access_key,
    secret_key=settings.s3.secret_key,
    endpoint_url=settings.s3.endpoint_url,
    bucket_name=settings.s3.bucket_name,
)
