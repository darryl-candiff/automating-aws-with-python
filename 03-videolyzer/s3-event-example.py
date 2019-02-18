event['Records'][0]['s3']
event['Records'][0]['s3']['s3SchemaVersion']
event['Records'][0]['s3']['bucket']['name']
event['Records'][0]['s3']['object']['key']
import urllib
urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
