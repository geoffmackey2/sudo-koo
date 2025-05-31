from django.http import HttpResponse
from django.template import loader
from django.conf import settings
import boto3
import os

def index(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())

def ads_txt(request):
    s3 = boto3.client('s3', aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'), region_name='us-east-2')
    try:
        response = s3.get_object(Bucket=os.environ.get('AWS_STORAGE_BUCKET_NAME'), Key='ads.txt')
        content = response['Body'].read().decode('utf-8')
        return HttpResponse(content, content_type='text/plain')
    except Exception as e:
        return HttpResponse(f"Error: {e}", status=500)