import boto3
import datetime
import pytz
import pytest
from botocore.exceptions import NoCredentialsError, NoRegionError
from moto import mock_s3
from src.backend import S3NodeStorage

@pytest.fixture
def storage():
    with mock_s3():
        bucket_name = 'my-s3-bucket'
        bucket_region = 'us-west-1'
        s3_client = None
        nodestore = S3NodeStorage(bucket=bucket_name, region_name=bucket_region)

        try:
            s3_client = boto3.client('s3', region_name=bucket_region)
            s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': bucket_region})
        except (NoCredentialsError, NoRegionError):
            pytest.skip('AWS credentials or region not found')

        yield nodestore

def test_get(storage):
    storage.set('key1', 'value1')
    storage.set('key2', 'value2')

    result = storage.get('key1')
    assert result == 'value1'

    result = storage.get('key2')
    assert result == 'value2'

    result = storage.get('key3')
    assert result is None

def test_set(storage):
    storage.set('key1', 'value1')
    result = storage.get('key1')
    assert result == 'value1'

    storage.set('key2', 'value2')
    result = storage.get('key2')
    assert result == 'value2'

def test_get_multi(storage):
    storage.set('key1', 'value1')
    storage.set('key2', 'value2')
    storage.set('key3', 'value3')

    result = storage.get_multi(['key1', 'key2'])
    assert result == {'key1': 'value1', 'key2': 'value2'}

    result = storage.get_multi(['key2', 'key3', 'key4'])
    assert result == {'key2': 'value2', 'key3': 'value3', 'key4': None}

    result = storage.get_multi(['key4', 'key5'])
    assert result == {'key4': None, 'key5': None}

def test_delete(storage):
    storage.set('key1', 'value1')
    storage.set('key2', 'value2')

    storage.delete('key1')
    result = storage.get('key1')
    assert result is None

    result = storage.get('key2')
    assert result == 'value2'

    storage.delete('key2')
    result = storage.get('key2')
    assert result is None

def test_delete_multi(storage):
    storage.set('key1', 'value1')
    storage.set('key2', 'value2')
    storage.set('key3', 'value3')

    storage.delete_multi(['key1', 'key2'])
    result = storage.get('key1')
    assert result is None

    result = storage.get('key2')
    assert result is None

    result = storage.get('key3')
    assert result == 'value3'

def test_cleanup(storage):
    storage.set('key1', 'value1')
    storage.set('key2', 'value2')
    storage.set('key3', 'value3')

    cutoff_timestamp = datetime.datetime.now(pytz.utc) - datetime.timedelta(days=1)
    storage.cleanup(cutoff_timestamp)

    result = storage.get('key1')
    assert result == 'value1'

    result = storage.get('key2')
    assert result == 'value2'

    result = storage.get('key3')
    assert result == 'value3'

    cutoff_timestamp = datetime.datetime.now(pytz.utc) + datetime.timedelta(days=1)
    storage.cleanup(cutoff_timestamp)

    result = storage.get('key1')
    assert result is None

    result = storage.get('key2')
    assert result is None

    result = storage.get('key3')
    assert result is None
