from django.shortcuts import render,redirect
import boto3
import random
# Create your views here.
session = boto3.Session( aws_access_key_id='AKIAVR24HZ2UAQYHV2LL', aws_secret_access_key='jhgrkmmqJyKFN3mM7TkehWmnChl8X078ORAk/InZ')
s3 = session.resource('s3')
def Home(request):
    if request.method=='POST':
        img = request.FILES.get('img')
        object = s3.Object('imageapp123', img.name)
        data = object.put(Body=img.read(), ContentType = 'application/octet-stream')
        res = data.get('ResponseMetadata')
        if res.get('HTTPStatusCode') == 200:
            print('File Uploaded Successfully')
            return redirect("/")
        else:
            print('File Not Uploaded')
    else:
        image=s3.Bucket('imageapp123')
        img_lst=[]
        for i in image.objects.all():
            img_lst.append(i.key)
        random.shuffle(img_lst)
        return render(request,"index.html",{"img_lst":img_lst})
    return render(request,"index.html")

def ImageView(request, slug):
    return render(request,"imageview.html",{"img":slug})