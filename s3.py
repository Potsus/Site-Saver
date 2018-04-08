import boto3
from botocore.client import Config

from json import loads
from utils import cprint

from config import S3_BUCKET

BUCKET = S3_BUCKET

class s3Connect():

    def __init__(self):

        # Credentials are now being stored in the ~/.aws folder where boto knows to look for them
        # still need to find a better way to set them without having them in the repo
        self.client = boto3.client('s3', config=Config(signature_version='s3v4'))

        self.BUCKET = BUCKET
        cprint('Using bucket: %s' % self.BUCKET, 'info')


    def moveInS3(self, filekey, destination, bucket):
        filename = filekey.split('/')[-1]
        self.client.copy_object(Bucket=bucket, CopySource=bucket+'/'+filekey, Key=destination+filename)
        self.client.delete_object(Bucket=bucket, Key=filekey)
        return destination+filekey

    def getFileFromS3(self, filename, localFile):
        self.client.download_file(self.BUCKET, filename, localFile)

    def readS3File(self, filename):
        data = self.client.get_object(Bucket=self.BUCKET, Key=filename)
        body = data['Body'].read(data['ContentLength'])
        return body

    def getMetaData(self, metaFile):
        data = self.readS3File(metaFile)
        data = loads(bytes.decode(data))
        return data['metadata']

    def clearFolder(self, folder):
        out = []
        keys = self.getKeys()
        for key in keys:
            if key.startswith(folder):
                out.append(self.client.delete_object(Bucket=self.BUCKET, Key=key))
        return out


    def getKeys(self):
        b = self.client.list_objects(Bucket=self.BUCKET)
        out = []
        if 'Contents' in b: 
                files = b['Contents']
                for file in files:
                    out.append(file['Key'])
        return out

    def mv(self, oldKey, newKey):
        self.client.copy_object(Bucket=self.BUCKET, CopySource=self.BUCKET+'/'+oldKey, Key=newKey)
        self.client.delete_object(Bucket=self.BUCKET, Key=oldKey)

    def uploadData(self, data, remoteFile):
        o = self.client.put_object(Bucket=self.BUCKET, Key=remoteFile, Body=str(data))
        return o.get('ResponseMetadata').get('HTTPStatusCode') == 200

    def uploadFile(self, localFile, remoteFile):
        data = open(localFile, 'rb')
        o = self.client.put_object(Bucket=self.BUCKET, Key=remoteFile, Body=data)
        return o.get('ResponseMetadata').get('HTTPStatusCode') == 200

    def getDownloadUrl(self, remoteFile):
        url = self.client.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': self.BUCKET,
                'Key': remoteFile
            },
            ExpiresIn=86400
        )
        print(url)
        return url

