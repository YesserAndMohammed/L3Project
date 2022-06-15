from base64 import encode
from django.shortcuts import render,redirect
from .models import *
from .forms import *
import json

from tensorflow import keras
import string

model = keras.models.load_model("./models/Best10.h5")

with open("./models/dictionary.txt", "r") as f:
    word_index = eval(f.read())



def review_encode(s):
    encoded = [1]
    for word in s:
        if word.lower() in word_index:
            encoded.append(word_index[word.lower()])
        else:
            encoded.append(2)
    return encoded



def clean(s):
    new_string = s.translate(str.maketrans('', '', string.punctuation))
    return new_string

def getPrediction(s):
    encode = clean(s)
    #print(encode)
    encode = encode.split()
    #print(encode)
    encode = review_encode(encode)
    #print(encode)
    encode = keras.preprocessing.sequence.pad_sequences([encode], value=word_index["<PAD>"], padding="post", maxlen=250)
    #print(encode)
    predict = model.predict(encode)
    #print(type(predict[0][0]))
    return predict[0][0]


def dashboard(request):
    
    form = PostForm(request.POST , request.FILES)
    if request.method == "POST":
        #print("i'm posting...")
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            k = getPrediction(post.body)
            
            print(k)
            if(k >0.8):
                return redirect("Mymedia:warning")
            elif(k <0.5):
                post.save()
                return redirect("Mymedia:dashboard")
            else :
                post.approved = False
                post.save()
                return redirect("Mymedia:suspe")
            
             

    return render(request, "Mymedia/dashboard.html", {"form": form})




def profile_list(request):
    profiles = Profile.objects.exclude(user=request.user)
    return render(request, "Mymedia/profile_list.html", {"profiles": profiles})

def warning(request):
    return render(request, "Mymedia/warning.html")

def suspe(request):
    return render(request, "Mymedia/suspe.html")




def profile(request, pk):
    if not hasattr(request.user, 'profile'):
        missing_profile = Profile(user=request.user)
        missing_profile.save()

    profile = Profile.objects.get(pk=pk)
    if request.method == "POST":
        current_user_profile = request.user.profile
        data = request.POST
        action = data.get("follow")
        if action == "follow":
            current_user_profile.follows.add(profile)
        elif action == "unfollow":
            current_user_profile.follows.remove(profile)
        current_user_profile.save()

    return render(request, "Mymedia/profile.html", {"profile": profile})



def Myprofile(request, pk):   
    profile = Profile.objects.get(pk=pk)
    form = PostForm(request.POST , request.FILES)

    if request.method == "POST":
        current_user_profile = request.user.profile
        data = request.POST
        action = data.get("follow")
        if action == "follow":
            current_user_profile.follows.add(profile)
        elif action == "unfollow":
            current_user_profile.follows.remove(profile)
        current_user_profile.save()
        post = form.save(commit=False)
        post.user = request.user
        k = getPrediction(post.body)
        print(k)
        if(k >0.8):
                return redirect("Mymedia:warning")
        elif(k<0.5):
                post.save()
                return redirect("Mymedia:dashboard")
        else :
                post.approved = False
                post.save()
                return redirect("Mymedia:suspe")            

    return render(request, "Mymedia/Myprofile.html", {"profile": profile , "form": form})









    







