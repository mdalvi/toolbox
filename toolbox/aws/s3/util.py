import boto3


def upload_file(bucket_name, source_path, destination_path, file_name):
    """

    :param bucket_name: Name of bucket (e.g. s3-my-bucket)
    :param source_path: Fully qualified path including file name at source
    :param destination_path: destination path without bucket name and file name
    :param file_name: Desired named of file at destination
    :return: None
    """
    s3_resource = boto3.resource('s3')
    s3_resource.Object(bucket_name, destination_path + file_name).upload_file(source_path)


def download_file(bucket_name, source_path, destination_path, file_name):
    """

    :param bucket_name: Name of bucket (e.g. s3-my-bucket)
    :param source_path: Fully qualified path including file name at source
    :param destination_path: destination path to save file
    :param file_name: Desired named of file at destination
    :return: None
    """
    s3_resource = boto3.resource('s3')
    s3_resource.meta.client.download_file(bucket_name, source_path, destination_path + file_name)


def list_files(bucket_name, source_path):
    """
    :param bucket_name: Name of bucket (e.g. s3-my-bucket)
    :param source_path: S3 key without the bucket name
    :return: list
    """
    s3 = boto3.resource("s3")
    s3_bucket = s3.Bucket(bucket_name)
    return [f.key for f in s3_bucket.objects.filter(Prefix=source_path).all()]
