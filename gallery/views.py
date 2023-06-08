from django.shortcuts import render,redirect
import boto3
import random
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .Image_Verification import ImageVerification
import uuid
from textblob import TextBlob
from .mongodb import insert_record

# Create your views here.
session = boto3.Session( aws_access_key_id='', aws_secret_access_key='')
s3 = session.resource('s3')
def Home(request):
    if request.method=='POST':
        
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

@login_required
def ImageUpload(request):
    if request.method=='POST':
        img = request.FILES.get('img')
        img_name = request.POST.get("img_name")
        img_desc = request.POST.get("img_desc")
        # validation checks goes here
        img_verf_obj = ImageVerification()
        if not img_verf_obj.moderate_text(img_name):
            messages.info(request,"Watch your Text")
            return redirect("/upload")
        image_name = uuid.uuid4().hex[:6].upper()+img.name
        object = s3.Object('imageapp123', image_name)
        data = object.put(Body=img.read(), ContentType = 'application/octet-stream')
        res = data.get('ResponseMetadata')
        if res.get('HTTPStatusCode') == 200:
            print('File Uploaded Successfully')
            if img_verf_obj.moderate_image(image_name):
                messages.info(request,"Explicit Image found")
                return redirect('/upload')
                try:
                    s3.Object('imageapp123', image_name).delete()
                except Exception as e:
                    raise Exception(e)
            img_tags = list(TextBlob(img_desc).noun_phrases) + img_verf_obj.label_detection(image_name)
            image_doc = {"author": request.user.username, 
                            "name": image_name,
                            "desc": img_desc,
                            "tags": img_tags
                            }
            insert_record(image_doc)

            return redirect("/")
        else:
            messages.info(request,"Image Upload Failed!!")
    return render(request,"upload_image.html")

