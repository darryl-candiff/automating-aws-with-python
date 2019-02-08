import boto3
import click

session = boto3.Session(profile_name='pythonAutomation')
s3 = session.resource('s3')

#########click cli group
@click.group()
def cli():
    "Webotron deploys websites to AWS"
    pass
### List buckets
@cli.command('list-buckets')

def list_buckets():
    "List all s3 buckets"
    for bucket in s3.buckets.all():
        print(bucket)
### List bucket objects
@cli.command('list-bucket-objects')
@click.argument('bucket')
def list_bucket_objects(bucket):
    "List all objects in an s3 bucket"
    for obj in s3.Bucket(bucket).objects.all():
        print(obj.key)

if __name__ == '__main__':
    cli()
