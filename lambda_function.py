import boto3, os, io
from urllib.parse import unquote_plus
from PIL import Image

s3 = boto3.client('s3')
THUMB_BUCKET = os.environ['THUMB_BUCKET']

def lambda_handler(event, context):
    rec = event['Records'][0]['s3']
    bucket = rec['bucket']['name']
    key = unquote_plus(rec['object']['key'])

    obj = s3.get_object(Bucket=bucket, Key=key)
    img = Image.open(io.BytesIO(obj['Body'].read()))
    fmt = img.format or 'JPEG'

    img.thumbnail((150, 150))
    buf = io.BytesIO()
    img.save(buf, format=fmt)
    buf.seek(0)

    s3.put_object(Bucket=THUMB_BUCKET, Key='thumb-' + key,
                  Body=buf, ContentType=obj['ContentType'])
    return {'status': 'done'}
