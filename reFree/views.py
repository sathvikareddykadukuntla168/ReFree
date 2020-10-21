from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse
from reFree.models import User,Company,Projects,Component,FinalDesign,SocialLinks
from rest_framework import viewsets
from rest_framework import permissions
from reFree.serializers import UserSerializer,CompanySerializer,SocialLinksSerializer,ProjectsSerializer,ComponentSerializer,FinalDesignSerializer
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth import authenticate, login
from django.views import View


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()#.order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

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
class signup_view(View):
    def get(self, request):
        return render(request, 'signup.html', { 'form': UserCreationForm() })

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect(reverse('login'))

        return render(request, 'signup.html', { 'form': form })


class login_view(View):
    def get(self, request):
        return render(request, 'login.html', { 'form':  AuthenticationForm })

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )

            if user is None:
               """ return render(
                    request,
                    'login.html',
                    { 'form': form, 'invalid_creds': True }
                )"""
            return redirect(reverse('home'))

            try:
                form.confirm_login_allowed(user)
            except ValidationError:
                return render(
                    request,
                    'login.html',
                    { 'form': form, 'invalid_creds': True }
                )
            login(request, user)
        return HttpResponse("<html>I am invalid user</html>")

        
def logout_view(request):
        return render(request,'login.html')
