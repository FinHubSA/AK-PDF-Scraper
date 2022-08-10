def pdf_upload(path_to_pdf, name):

    from boto3 import session

    # from botocore.client import Config

    ACCESS_ID = "JSGEKRRXM3EMPGON3PXO"
    SECRET_KEY = "XXX"

    # Initiate session
    session = session.Session()
    client = session.client(
        "s3",
        region_name="FRA1",
        endpoint_url="https://aaronskit-cloudstorage.fra1.digitaloceanspaces.com",
        aws_access_key_id=ACCESS_ID,
        aws_secret_access_key=SECRET_KEY,
    )

    # Upload a file to your Space
    client.upload_file(
        path_to_pdf,
        "aaronskit-cloudstorage",
        name,
        ExtraArgs={"ACL": "public-read", "StorageClass": "REDUCED_REDUNDANCY"},
    )
