
from celery.decorators import task
from celery.utils.log import get_task_logger
from PIL import Image

from feedback.emails import send_feedback_email
import boto
import boto.s3
import sys
from boto.s3.key import Key
import os
logger = get_task_logger(__name__)


@task(name="send_feedback_email_task")
def send_feedback_email_task(email, message):
    """sends an email when feedback form is filled successfully"""
    logger.info("Sent feedback email")
    return send_feedback_email(email, message)
            

@task()
def amazon_uploader():
    AWS_S3_ACCESS_KEY_ID='AMAZON_ID'
    AWS_S3_SECRET_ACCESS_KEY='AMAZON_KEY' 
    AWS_STORAGE_BUCKET_NAME='development-branch'
    SECRET_KEY='A long string with many different types of characters'
    bucket_name = 'development-branch'
    testfile = 'IMAGE_PATH'
    conn = boto.connect_s3(AWS_S3_ACCESS_KEY_ID,AWS_S3_SECRET_ACCESS_KEY)
    bucket = conn.get_bucket('development-branch')
    k = Key(bucket)
    key_name = 'my test file2'
    path = '/tmp/'
#path = '/candidate-photos/hello' this make a directory inside candidate-photos as well. 
    full_key_name = os.path.join(path, key_name)
    k = bucket.new_key(full_key_name)
    return k.set_contents_from_filename(testfile)

@task()
def create_thumb():
    AWS_S3_ACCESS_KEY_ID='AMAZON_ID'
    AWS_S3_SECRET_ACCESS_KEY='AMAZON_KEY' 
    AWS_STORAGE_BUCKET_NAME='development-branch'
    SECRET_KEY='A long string with many different types of characters'
    bucket_name = 'development-branch'
    src_file = 'IMAGE_PATH'
    conn = boto.connect_s3(AWS_S3_ACCESS_KEY_ID,AWS_S3_SECRET_ACCESS_KEY)
    bucket = conn.get_bucket('development-branch')
    k = Key(bucket)
    key_name = 'my test file2'
    path = '/candidate-photos/'
#path = '/candidate-photos/hello' this make a directory inside candidate-photos as well. 
    size = 128, 128
    im = Image.open(src_file)
    im.thumbnail(size)
    im.save(src_file + ".thumbnail", "JPEG")
    full_key_name = os.path.join(path, key_name)
    k = bucket.new_key(full_key_name)
    return k.set_contents_from_filename(src_file + ".thumbnail")
