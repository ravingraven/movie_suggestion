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
    """Create the suggestions GUI"""
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
        
        context = { 'src' : src, 
                    'thumbs_up_icon': thumbs_up_icon, 
                    'thumbs_down_icon': thumbs_down_icon, 
                    'selected_video': selected_video, 
                    'video_list' : Suggestion.objects.all() 
                  }

        return HttpResponse(template.render(context, request))
    else:
        # Redirect to login if not logged in
        return redirect("/login/")

def get_preferences(request):
    """Get the preferences for the current user as a CSV"""
    if request.user.is_authenticated:
    
        # Print all preferences
        res = ""
        for obj in Preference.objects.filter(user=request.user):
            if obj.preference != '0':
                res += obj.video + "," + obj.preference + "</br>"
        return HttpResponse(res)
    else:
        return redirect("/login/")


def get_preference(request):
    """Get the preference of a movie"""
    if request.user.is_authenticated and request.is_ajax() and request.POST.get('video') != None:
        
        # Get a single preference
        obj = Preference.objects.filter(user=request.user, video=request.POST.get('video'))
        if obj:
            return HttpResponse(obj[0].preference)
        else:
            # Return neutral on unknown
            return HttpResponse('0')
    else:
        return HttpResponse('error')

def set_preference(request):
    """Set the preference of a movie"""
    if request.user.is_authenticated and request.is_ajax() and request.POST.get('video') != None:

        # Set a preference
        obj = Preference.objects.filter(user=request.user, video=request.POST.get('video'))
        
        # Either add new or update a preference
        # TODO: This saves neutral preferences as well, maybe we don't want that...
        if obj:
            obj.update(preference=request.POST.get('preference'))
        else:
            p = Preference(user=request.user, name='', video=request.POST.get('video'), preference=request.POST.get('preference'))
            p.save()
        return HttpResponse('ok')
    else:
        return HttpResponse('error')

def set_suggestions(request):
    """Add new suggestions over a JSON file"""
    if request.FILES:
        jsonfile = request.FILES['json_file']

        # Load JSON file
        movies = json.load(jsonfile.open())

        # Add all entries to the suggestions object
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
        return HttpResponse('error')

def get_video_details(request):
    """Get the details of a video"""
    if request.user.is_authenticated and request.is_ajax() and request.POST.get('video') != None:
        
        # Get the video from the Suggestion model
        obj = Suggestion.objects.filter(video=request.POST.get('video'))

        # If found, serialize it in JSON format and send it to the front end
        if obj:
            data = serializers.serialize("json", obj)

            return HttpResponse(data)
        else:
            return HttpResponse('')
    else:
        return HttpResponse('error')


