from django.shortcuts import render
from django.http import HttpResponse
from .models import User,Company,Projects,Component,FinalDesign,SocialLinks

def home(request):
    user=User.objects.all()[:]
    company=Company.objects.all()[:]
    projects=Projects.objects.all()[:]
    component=Component.objects.all()[:]
    finalDesign=FinalDesign.objects.all()[:]
    socialLinks=SocialLinks.objects.all()[:]
    context={
        'user': user,
        'company':company,
        'component':component,
        'projects':projects,
        'finalDesign':finalDesign,
        'socialLinks':socialLinks
    }
    return render(request,'home.html',context)