import boto3
from better_profanity import profanity
class ImageVerification:
    def __init__(self):
        self.status = ""
        self.session = boto3.Session( aws_access_key_id='', aws_secret_access_key='')
    def label_detection(self,photo):
        client = self.session.client('rekognition',region_name="us-east-1")

        response = client.detect_labels(Image={'S3Object':{'Bucket':"imageapp123",'Name':photo}},
        MaxLabels=10,
        )
        detected_labels = []
        for label in response['Labels']:
            detected_labels.append(label['Name'])
        return detected_labels
    
    def moderate_image(self,photo):
    
        client = self.session.client('rekognition',region_name="us-east-1")

        response = client.detect_moderation_labels(Image={'S3Object':{'Bucket':"imageapp123",'Name':photo}})

        # print('Detected labels for ' + photo)
        # for label in response['ModerationLabels']:
        #     print (label['Name'] + ' : ' + str(label['Confidence']))
        #     print (label['ParentName'])
        return len(response['ModerationLabels'])>0
    
    def moderate_text(self,text):
        return profanity.contains_profanity(text)
