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
from domain import DomainManager
from certificate import CertificateManager
from cdn import DistributionManager
import util

session = None
bucket_manager = None
domain_manager = None
certificate_manager = None
dist_manager = None

# -----------------click cli group
@click.group()
@click.option('--profile', default=None,
                help = "Use a given AWS profile name.")
def cli(profile):
    """Webotron deploys websites to AWS."""
    global session
    global bucket_manager
    global domain_manager
    global certificate_manager
    global dist_manager

    session_cfg = {}
    if profile:
        session_cfg['profile_name'] = profile

    session = boto3.Session(**session_cfg)
    bucket_manager = BucketManager(session)
    domain_manager = DomainManager(session)
    certificate_manager = CertificateManager(session)
    dist_manager = DistributionManager(session)

# -------------------List buckets
@cli.command('list-buckets')
def list_buckets():
    """List all s3 buckets."""
#    for bucket in bucket_manager.s3.buckets.all():
    for bucket in bucket_manager.all_buckets():
        print(bucket)

# ----------------- List bucket objects
@cli.command('list-bucket-objects')
@click.argument('bucket')
def list_bucket_objects(bucket):
    """List all objects in an s3 bucket."""
#    for obj in s3.Bucket(bucket).objects.all():
    for obj in bucket_manager.all_objects(bucket):
        print(obj.key)

# ---------- setup-bucket
@cli.command('setup-bucket')
@click.argument('bucket')
def setup_bucket(bucket):
    """Create and configure S3 bucket."""
    s3_bucket = bucket_manager.init_bucket(bucket)
    bucket_manager.set_policy(s3_bucket)
    bucket_manager.configure_website(s3_bucket)



# ------------ sync bucket contents
@cli.command('sync')
@click.argument('pathname', type=click.Path(exists=True))
@click.argument('bucket')
def sync(pathname, bucket):
    """Sync contents of PATHNAME to BUCKET."""
#    s3_bucket = s3.Bucket(bucket)
    bucket_manager.sync(pathname, bucket)
    print(bucket_manager.get_bucket_url(bucket_manager.s3.Bucket(bucket)))


@cli.command('setup-domain')
@click.argument('domain')
def setup_domain(domain):
    """Configure DOMAIN to point to the BUCKET."""
    bucket = bucket_manager.get_bucket(domain)

    zone = domain_manager.find_hosted_zone(domain) \
        or domain_manager.create_hosted_zone(domain)

    endpoint = util.get_endpoint(bucket_manager.get_region_name(bucket))

    a_record = domain_manager.create_s3_domain_record(zone, domain, endpoint)
    print("Domain configured: http://{}".format(domain))


@cli.command('find-cert')
@click.argument('domain')
def find_cert(domain):
    """Find certificates for domain."""
    print(certificate_manager.find_matching_cert(domain))

@cli.command('setup-cdn')
@click.argument('domain')
@click.argument('bucket')
def setup_cdn(domain, bucket):
    """Setup CDN for s3 hosted websites."""
#    print("before find_matching_dist.")
    dist = dist_manager.find_matching_dist(domain)
#    print("after find_matching_dist.")
#    print(dist)

    if not dist:
#        print("before certificate_manager.find_matching_cert(domain)")
        cert = certificate_manager.find_matching_cert(domain)
#        print("after certificate_manager.find_matching_cert(domain)")
#        print(cert)
        if not cert: # SSL is not optional at this time
            print("Error: no matching cert found.")
            return

        dist = dist_manager.create_dist(domain, cert)
#        print("waiting for distribution deployment...")
        dist_manager.await_deploy(dist)

    zone = domain_manager.find_hosted_zone(domain) \
        or domain_manager.create_hosted_zone(domain)

    a_record = domain_manager.create_cf_domain_record(zone, domain, dist['DomainName'])
    print("Domain configured: https://{}".format(domain))

    return

if __name__ == '__main__':
    cli()
