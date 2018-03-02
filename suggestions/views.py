from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from .models import Suggestion
from .models import Preference
from django import forms
from django.core import serializers
import json

def index(request):
    if request.user.is_authenticated:
        # Assume some values about the view
        thumbs_up_icon = "/static/img/grey_thumbs_up_medium.png"
        thumbs_down_icon = "/static/img/grey_thumbs_down_medium.png"
        src = ""
        selected_video = ""

        # Just get the first liked video...
        obj = Preference.objects.filter(user=request.user, preference='1')
        if obj:
            src = "https://www.youtube.com/embed/" + obj[0].video
            thumbs_up_icon = "/static/img/green_thumbs_up_medium.png"
            selected_video = obj[0].video
        
        template = loader.get_template('suggestions/index.html')
        
        context = { 'src' : src, 'thumbs_up_icon': thumbs_up_icon, 'thumbs_down_icon': thumbs_down_icon, 'selected_video': selected_video, 'video_list' : Suggestion.objects.all() }
        return HttpResponse(template.render(context, request))
    else:
        # Redirect to login if not logged in
        return redirect("/login/")

def get_preferences(request):
    if request.user.is_authenticated:
        
        # Print all preferences
        res = ""
        for obj in Preference.objects.filter(user=request.user):
            res += "Id: " + obj.video + " pref: " + obj.preference

        return HttpResponse(res)
    return HttpResponse('error')

def get_preference(request):
    if request.user.is_authenticated and request.is_ajax() and request.POST.get('video') != None:
        
        # Get a single preference
        obj = Preference.objects.filter(user=request.user, video=request.POST.get('video'))
        if obj:
            return HttpResponse(obj[0].preference)
        else:
            return HttpResponse('0')
    else:
        return HttpResponse('error')

def set_preference(request):
    if request.user.is_authenticated and request.is_ajax() and request.POST.get('video') != None:

        # Set a preference
        obj = Preference.objects.filter(user=request.user, video=request.POST.get('video'))
        if obj:
            obj.update(preference=request.POST.get('preference'))
        else:
            p = Preference(user=request.user, name='', video=request.POST.get('video'), preference=request.POST.get('preference'))
            p.save()
        return HttpResponse('ok')
    else:
        return HttpResponse('error')

def set_suggestions(request):
    if request.FILES:
        jsonfile = request.FILES['json_file']

        movies = json.load(jsonfile.open())

        for movie in movies:
            # Sanitize JSON
            for key, value in movie.items():
                if value == None:
                    movie[key] = ""

            obj = Suggestion.objects.filter(name=movie["title"], video=movie["ytid"])

            # Avoid duplicates
            if obj:
                continue
            
            s = Suggestion(name=movie["title"], video=movie["ytid"],
                           rated=movie["rated"], released=movie["released"],
                           runtime=movie["runtime"], genres=movie["genres"],
                           director=movie["director"], writer=movie["writer"],
                           actors=movie["actors"], plot=movie["plot"],
                           languages=movie["languages"], country=movie["country"],
                           awards=movie["awards"])

            s.save()
        
        return redirect("/suggestions/")
    else:
        return HttpResponse('Error')

def get_video_details(request):
    if request.user.is_authenticated and request.is_ajax() and request.POST.get('video') != None:
        
        obj = Suggestion.objects.filter(video=request.POST.get('video'))

        print(obj)
        print(obj[0].name)
        print(obj[0].rated)
        print(obj[0].country)
        print(obj[0].director)

        data = serializers.serialize("json", obj)
        print(data)

        if obj:
            return HttpResponse(data)
        else:
            return HttpResponse('')
    else:
        return HttpResponse('error')


