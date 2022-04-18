from minio import Minio
from minio.error import S3Error

class MinioClient:
    def __init__(self):

        self.load_params()

        print(f"Create MINIO client for {self.params['host']}")
        self.client = Minio(
            self.params["host"],
            #access_key="Q3AM3UQ867SPQQA43P2F",
            #secret_key="zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG",
        )

        found = self.client.bucket_exists(self.params["bucket_name"])
        if not found:
            self.client.make_bucket(self.params["bucket_name"])
        else:
            print(f"Bucket {self.params['bucket_name']} already exists")

    def load_params(self):
        self.params={
            "host":"localhost",
            "bucket_name":"test",
        }

    def get_file(self, objectpath):
        try:
            response = self.client.get_object(
                self.params['bucket_name'],
                objectpath,
            )
            return response.read()
        finally:
            response.close()
            response.release_conn()
