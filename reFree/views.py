from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from rest_framework.decorators import action , api_view , renderer_classes,permission_classes
from reFree.models import User,Company,Projects,Component,FinalDesign,SocialLinks
from django.views.generic import ListView,DetailView
from rest_framework import viewsets,permissions,status
from rest_framework.renderers import JSONRenderer , TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.decorators import action
from reFree.serializers import UserSerializer,CompanySerializer,SocialLinksSerializer,ProjectsSerializer,ComponentSerializer,FinalDesignSerializer
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth import authenticate, login,logout
from django.views import View
from rest_framework.permissions import AllowAny
import operator
#from django_project import helpers

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()#.order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    @action(detail=False,methods=['post', 'options', ])
    def signupview(self, request):
        print(request)
        print(self.request)
        authorization_code = self.request.query_params.get('username')
        print(authorization_code)
        userdata = request.data
        print(userdata)

        u1 = User.objects.filter(username = userdata['username'])
        u2 = User.objects.filter(email = userdata['email'])

        if len(u1)!=0:
            return Response({'data': 'Username already taken!'})
        if len(u2)!=0:
            return Response({'data': 'Email already taken!'})

        newuser = User(username = userdata['username'], 
            first_name = userdata['firstname'], 
            last_name = userdata['lastname'], 
            email = userdata['email'],
            password = userdata['password'],
            phone_number = userdata['phone_number']
            )
        newuser.save()
        return Response({'data': 'User Created'})
       
    @action(detail=False,methods=['get','post', 'options', ])
    def loginview(self, request):
        print(request)
        print(self.request)
        authorization_code = self.request.query_params.get('username')
        print(authorization_code)
        userdata = request.data
        print(userdata)       
        u1 = User.objects.filter(username = userdata['username'])       
        if len(u1)==0:
            return Response({'data': 'Invalid Username'})
        try : 
            u2 = User.objects.get(username=userdata['username'],password = userdata['password'])
            if u2 is not None :
                login(request, u2)
                return Response({'data':'User logged in','username':u2.username})
            else :
                return Response({'data': 'Invalid password'})
        except User.DoesNotExist : 
            return Response({'data':'Invalid password'})
    
    @action(detail=False,methods=['get',])
    def logoutview(request):
        logout(request)
        return Response({'data': 'User has logged out'})

    @action(detail=False , methods=['get',])
    def currentuser(self , request ):
        if self.request.user.is_anonymous:
            return Response({'userId':0})
        return Response({'userId':self.request.user.id})

    @action(detail=False , methods=['get',])
    def userlist(self , request ):
        if self.request.user.is_anonymous:
            return Response({'UserList':0})
        
        querysets = User.objects.all()
        users = querysets.order_by('username')[:]
        ordered = sorted(users, key=operator.attrgetter('first_name'))
        serializer = UserSerializer(ordered,many =True)
        print(serializer.data)
        return Response(serializer.data)

class CompanyViewSet(viewsets.ModelViewSet):
   
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]

class SocialLinksViewSet(viewsets.ModelViewSet):
    
    queryset = SocialLinks.objects.all()#.order_by('-date_joined')
    serializer_class = SocialLinksSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProjectsViewSet(viewsets.ModelViewSet):
    
    queryset = Projects.objects.all()
    serializer_class = ProjectsSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False , methods=['get',])
    def projectlist(self , request ):
        if self.request.user.is_anonymous:
            return Response({'ProjectList':0})
        
        querysets = Projects.objects.filter(user = self.request.user.id)
        projs = querysets.order_by('likes')[:8]
        ordered = sorted(projs, key=operator.attrgetter('name'))
        serializer = ProjectsSerializer(ordered,many =True)
        print(serializer.data)
        return Response(serializer.data)

class ComponentViewSet(viewsets.ModelViewSet):
   
    queryset = Component.objects.all()#.order_by('-date_joined')
    serializer_class = ComponentSerializer
    permission_classes = [permissions.IsAuthenticated]

class FinalDesignViewSet(viewsets.ModelViewSet):
    
    queryset = FinalDesign.objects.all()
    serializer_class = FinalDesignSerializer
    permission_classes = [permissions.IsAuthenticated]
    def display_projects(request): 
  
        if request.method == 'GET': 
            # getting all the projects. 
            projects = FinalDesign.objects.all()  
            return Response(serializer.data) 

'''def home(request):
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
    return render(request,'home.html',context)'''

class HomeView(ListView): 
    model = Projects
    template_name = 'home.html'