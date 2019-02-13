#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Webotron: Deploy websites with AWS.

Webotron automates the process of deploying websites in aws
- Configure AWS S3 list_buckets
    - Create them
    - Set them up for static website hosting
    - Deploy local files to them
- Configure DNS with AWS Route 53
- Configure a Content Delivery Network and SSL with AWS Cloudfront
"""


import boto3
import click

from bucket import BucketManager

session = None
bucket_manager = None

# -----------------click cli group
@click.group()
@click.option('--profile', default=None,
            help="Use a given AWS profile name.")
def cli(profile):
    """Webotron deploys websites to AWS."""
    global session
    global bucket_manager
    session_cfg = {}
    if profile:
        session_cfg['profile_name'] = profile

    session = boto3.Session(**session_cfg)
    bucket_manager = BucketManager(session)

# -------------------List buckets
@cli.command('list-buckets')
def list_buckets():
    """List all s3 buckets."""
#    for bucket in bucket_manager.s3.buckets.all():
    for bucket in bucket_manager.all_buckets():
        print(bucket)
    return
# ----------------- List bucket objects
@cli.command('list-bucket-objects')
@click.argument('bucket')
def list_bucket_objects(bucket):
    """List all objects in an s3 bucket."""
#    for obj in s3.Bucket(bucket).objects.all():
    for obj in bucket_manager.all_objects(bucket):
        print(obj.key)
    return
# ---------- setup-bucket
@cli.command('setup-bucket')
@click.argument('bucket')
def setup_bucket(bucket):
    """Create and configure S3 bucket."""
    s3_bucket = bucket_manager.init_bucket(bucket)
    bucket_manager.set_policy(s3_bucket)
    bucket_manager.configure_website(s3_bucket)

    return


# ------------ sync bucket contents
@cli.command('sync')
@click.argument('pathname', type=click.Path(exists=True))
@click.argument('bucket')
def sync(pathname, bucket):
    """Sync contents of PATHNAME to BUCKET."""
#    s3_bucket = s3.Bucket(bucket)
    bucket_manager.sync(pathname, bucket)
    print(bucket_manager.get_bucket_url(bucket_manager.s3.Bucket(bucket)))


if __name__ == '__main__':
    cli()
