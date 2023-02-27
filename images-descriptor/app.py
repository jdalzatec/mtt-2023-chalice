import json
import os
from datetime import datetime, timezone
from uuid import uuid4

import boto3
from chalice import Chalice, Response, BadRequestError, Rate
from chalicelib.model import ImageModel
from chalicelib.utils import is_a_valid_image

s3_client = boto3.client('s3')
bucket_name = os.environ['BUCKET_NAME']
app = Chalice(app_name='images-descriptor')


@app.route('/images', methods=['GET'])
def get_images():
    return [json.loads(image.to_json()) for image in ImageModel.scan()]


@app.route('/images/{image_id}', methods=['GET'])
def get_image(image_id):
    try:
        image = ImageModel.get(image_id)
        return json.loads(image.to_json())
    except ImageModel.DoesNotExist:
        return Response(body=None, status_code=404)


@app.route('/images/{image_id}', methods=['DELETE'])
def delete_image(image_id):
    try:
        image = ImageModel.get(image_id)
        s3_client.delete_object(Bucket=bucket_name, Key=image.get_file_name())
        image.delete()
        return Response(body=None, status_code=200)
    except ImageModel.DoesNotExist:
        return Response(body=None, status_code=404)


@app.route('/images', methods=['POST'], content_types=['image/png', 'image/jpg', 'image/jpeg'])
def upload_image():
    image_bytes = app.current_request.raw_body
    if not is_a_valid_image(image_bytes):
        raise BadRequestError('Invalid image')

    image_id = str(uuid4())
    content_type = app.current_request.headers['Content-Type']
    image_extension = content_type.split('/')[-1]

    image = ImageModel(id=image_id, extension=image_extension, created_at=datetime.utcnow(), concepts=None)
    image.save()

    s3_client.put_object(
        Body=image_bytes,
        Bucket=bucket_name,
        Key=image.get_file_name(),
        ContentType=content_type,
    )
    return {'image_id': image_id}


@app.route('/images/{image_id}/download_url', methods=['GET'])
def get_download_url(image_id):
    try:
        image = ImageModel.get(image_id)
        url = s3_client.generate_presigned_url(
            'get_object', Params={'Bucket': bucket_name, 'Key': image.get_file_name()}, ExpiresIn=3600
        )
        return {'url': url}
    except ImageModel.DoesNotExist:
        return Response(body=None, status_code=404)


@app.schedule(Rate(1, unit=Rate.HOURS))
def clean_old_info():
    now = datetime.utcnow().replace(tzinfo=timezone.utc)
    for image in ImageModel.scan():
        created_at = image.created_at
        delta_time = now - created_at
        delta_seconds = delta_time.seconds
        if delta_seconds > 0:
            s3_client.delete_object(Bucket=bucket_name, Key=image.get_file_name())
            image.delete()
