from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from rest_framework.decorators import action , api_view , renderer_classes,permission_classes
from reFree.models import User,Company,Projects,Component,FinalDesign,SocialLinks
from rest_framework import viewsets,permissions,status
from rest_framework.renderers import JSONRenderer , TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.decorators import action
from reFree.serializers import UserSerializer,CompanySerializer,SocialLinksSerializer,ProjectsSerializer,ComponentSerializer,FinalDesignSerializer
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth import authenticate, login,logout
from django.views import View
from reFree.forms import Signupform
from rest_framework.permissions import AllowAny
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
        var = request.data
        print(var)
        
        form = Signupform(request.POST)
        return Response({'data': 'User Created'})
        print(form.is_valid())
        
        if form.is_valid():
            user = form.save()
            return Response({'data': 'User Created'})

        return Response({'data': 'Invalid Username or Password'})

    @action(detail=False,methods=['get','post', 'options', ])
    def loginview(self, request):
        print(request)
        print(self.request)
        authorization_code = self.request.query_params.get('username')
        print(authorization_code)
        var = request.data
        print(var)
         
        form = AuthenticationForm(request, data=request.data)
        print(form.is_valid())
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password') 
            ) 
            print(user.username)
            if user is None:
                return Response({'data': 'Invalid Username or Password'})
              
            print(user.username)
            login(request, user)
            print(user.username)
            return Response({'data': 'User exists', 'username':self.request.user.username})
         # invalid username/ password # user does not exist in db
        return Response({'data': 'Invalid Username or Password'})  


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

class ComponentViewSet(viewsets.ModelViewSet):
   
    queryset = Component.objects.all()#.order_by('-date_joined')
    serializer_class = ComponentSerializer
    permission_classes = [permissions.IsAuthenticated]

class FinalDesignViewSet(viewsets.ModelViewSet):
    
    queryset = FinalDesign.objects.all()
    serializer_class = FinalDesignSerializer
    permission_classes = [permissions.IsAuthenticated]

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
"""class signup_view(View):
    def get(self, request):
        return render(request, 'signup.html', { 'form': UserCreationForm() })

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect(reverse('login'))

        return render(request, 'signup.html', { 'form': form })"""


"""class loginview(View):
    permission_classes = [AllowAny]
    def get(self, request):
        return render(request, 'loginview.html', { 'form':  AuthenticationForm() })

    #@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
    def post(self, request):
        print(request)
        print(self.request)
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password') """
     #       ) 
        #    print(user.username)
  #          if user is None:
  #              print(user.username)
  #              return Response({'data': 'User does not exist'})
              

        #    print(user.username)
 #           login(request, user)
 #           print(user.username)
 #           return Response({'data': 'User exists', 'username':self.request.user.username}) 
            
            #return HttpResponseRedirect(reverse('home.html',kwargs={'username' : user.username}))
            #return render({'form': form},status=status.HTTP_202_ACCEPTED)

            
            #return HttpResponse("<html>I am invalid user</html>")
       # return HttpResponse("<html>I am invalid user</html>")
        #return HttpResponse({'data':'User doesnot exists'},status = status.HTTP_401_UNAUTHORISED)
       # return Response({'form': form,'invalid_creds': True})

@action(detail=False,methods=['get',])
def logout_view(request):
    logout(request)
    return HttpResponse({'user': 'You have logged out'})

'''def logout_view(request):
        return render(request,'login.html')'''