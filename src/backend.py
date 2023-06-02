import boto3
import os

from botocore.config import Config
from sentry.nodestore.base import NodeStorage

class S3NodeStorage(NodeStorage):
    """
    An S3-based backend for storing node data.

    :param bucket: The name of the S3 bucket to use for storing data.
    :param aws_access_key_id: AWS access key ID. Optional, if not provided, will use AWS environment variables or IAM roles.
    :param aws_secret_access_key: AWS secret access key. Optional, if not provided, will use AWS environment variables or IAM roles.
    :param region_name: The name of the AWS region to connect to. Optional, if not provided, the default region will be used.
    :param endpoint_url: Alternative endpoint URL, if not connecting to the default S3 host. Optional, if not provided, the default S3 endpoint will be used.

    >>> S3NodeStorage(
    ...     bucket='my-s3-bucket',
    ...     aws_access_key_id='my-access-key',
    ...     aws_secret_access_key='my-secret-key',
    ...     region_name='us-west-1',
    ...     endpoint_url='http://my-s3-compatible-service:9000',
    ... )
    """

    def __init__(
        self,
        bucket,
        aws_access_key_id=None,
        aws_secret_access_key=None,
        region_name=None,
        endpoint_url=None,
    ):
        self.bucket = boto3.resource(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
            endpoint_url=endpoint_url,
            config=Config(
                retries={
                    'max_attempts': 10,
                    'mode': 'standard'
                }
            )
        ).Bucket(bucket)
        self.skip_deletes = '_SENTRY_CLEANUP' in os.environ

    def _get_bytes(self, id):
        obj = self.bucket.Object(id)
        try:
            return obj.get()['Body'].read()
        except self.bucket.meta.client.exceptions.NoSuchKey:
            return None

    def _set_bytes(self, id, data, ttl=None):
        self.bucket.put_object(Body=data, Key=id)

    def delete(self, id):
        if self.skip_deletes:
            return

        self.bucket.Object(id).delete()

    def delete_multi(self, id_list):
        if self.skip_deletes:
            return

        for id in id_list:
            self.delete(id)

    def cleanup(self, cutoff_timestamp):
        if self.skip_deletes:
            return

        for obj in self.bucket.objects.all():
            last_modified = obj.last_modified
            if last_modified and last_modified <= cutoff_timestamp:
                obj.delete()

    def bootstrap(self):
        pass
