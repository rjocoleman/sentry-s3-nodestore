# Sentry S3 Nodestore

Sentry S3 Nodestore is an S3-based backend for storing node data in Sentry. It provides a scalable and reliable storage solution for event payloads.

## Installation

You can install the `sentry-s3-nodestore` package using pip:

```bash
pip install git+https://github.com/rjocoleman/sentry-s3-nodestore.git
```

## Configuration

To use the S3 Nodestore backend in Sentry, you need to update your Sentry configuration (`sentry/sentry.conf.py`) with the following settings:

1. Create the S3 bucket.

2. Set the `SENTRY_NODESTORE` option to `'backend.S3NodeStorage'`.

3. Set the `SENTRY_NODESTORE_OPTIONS` dictionary with the necessary configuration options. Here's an example configuration:

```python
SENTRY_NODESTORE = 'backend.S3NodeStorage'

SENTRY_NODESTORE_OPTIONS = {
    'bucket': 'my-s3-bucket',
    'aws_access_key_id': 'my-access-key',
    'aws_secret_access_key': 'my-secret-key',
    'region_name': 'us-west-1',
    'endpoint_url': 'http://my-s3-compatible-service:9000', # for using an non-AWS S3-like object store
}
```

Make sure to replace the values in the `SENTRY_NODESTORE_OPTIONS` dictionary with your actual S3 bucket name, region, AWS access key ID, and AWS secret access key.

## Usage

Once you have installed the package and configured Sentry, it will automatically use the S3 Nodestore backend for storing event data.

For more information on using and configuring Sentry, refer to the [Sentry documentation](https://develop.sentry.dev/self-hosted/#configuration).

## Note

This repo is unrelated to https://github.com/ewdurbin/sentry-s3-nodestore and the [PyPi package](https://pypi.org/project/sentry-s3-nodestore/) of the same name.
