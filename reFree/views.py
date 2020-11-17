from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.core.mail import BadHeaderError, send_mail
from rest_framework.decorators import action , api_view , renderer_classes,permission_classes
from reFree.models import User,Follow,Company,Projects,Component,FinalDesign,SocialLinks
from django.views.generic import ListView,DetailView
from rest_framework import viewsets,permissions,status
from rest_framework.renderers import JSONRenderer , TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.decorators import action
from reFree.serializers import UserSerializer,FollowSerializer,CompanySerializer,SocialLinksSerializer,ProjectsSerializer,ComponentSerializer,FinalDesignSerializer
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

        newuser = User.objects.create_user(username = userdata['username'], 
            first_name = userdata['firstname'], 
            last_name = userdata['lastname'], 
            email = userdata['email'],
            password = userdata['password'],
            phone_number = userdata['phone_number']
            )
        newuser.save()
        login(request , newuser)
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
            #u2 = User.objects.get(username=userdata['username'],password = userdata['password'])
            u2 = authenticate(request , username=userdata['username'] , password=userdata['password'])
            if u2 is not None :
                login(request, u2)
                return Response({'data':'User logged in','username':u2.username})
            else :
                return Response({'data': 'Invalid password'})
        except User.DoesNotExist : 
            return Response({'data':'Invalid password'})
            
    @action(detail=False , methods=['get',])
    def currentuser(self , request ):
        if self.request.user.is_anonymous:
            return Response({'userId':0})
        return Response({'userId':self.request.user.id })

    @action(detail=False,methods=['get',])
    def logoutview(request):
        logout(request)
        return Response({'data': 'User has logged out'})

    @action(detail=False , methods=['get',])
    def userlist(self , request ):
        if self.request.user.is_anonymous:
            queryset = User.objects.none()
            serializer = UserSerializer(queryset , many=True)
            return Response(serializer.data)
        
        querysets = User.objects.all()
        users = querysets.order_by('workExperience', 'username')[:]
        # ordered = sorted(users, key=operator.attrgetter('first_name'))
        serializer = UserSerializer(users,many =True)
        print(serializer.data)
        return Response(serializer.data)
    
    # whom user is following
    @action(detail=False , methods=['get',])
    def followinglist(self , request ):
        if self.request.user.is_anonymous:
            queryset = User.objects.none()
            serializer = UserSerializer(queryset , many=True)
            return Response(serializer.data)
    
        user = User.objects.get(id=self.request.user.id )      
        querysets = user.following.all()
        # users = querysets.order_by('workExperience', 'username')[:]
        # ordered = sorted(users, key=operator.attrgetter('first_name'))
        serializer = FollowSerializer(querysets,many =True)
        print(serializer.data)
        return Response(serializer.data)

    #who all are following this user
    @action(detail=False , methods=['get',])
    def followerslist(self , request ):
        if self.request.user.is_anonymous:
            queryset = User.objects.none()
            serializer = UserSerializer(queryset , many=True)
            return Response(serializer.data)
    
        user = User.objects.get(id=self.request.user.id )      
        querysets = user.followers.all()
        # users = querysets.order_by('workExperience', 'username')[:]
        # ordered = sorted(users, key=operator.attrgetter('first_name'))
        serializer = FollowSerializer(querysets,many =True)
        print(serializer.data)
        return Response(serializer.data)
    
    # filters
    @action(detail=False , methods=['get',])
    def userfilteredlist(self , request ):
        usersdata = request.data
        print(usersdata)
        lists = []
        if(usersdata['a']==1):
            lists += User.objects.filter('workExperience'==0)
        if(usersdata['b']==1):
            lists += User.objects.filter('workExperience'==1)
        if(usersdata['c']==1):
            lists = User.objects.filter('workExperience'==2)
        if(usersdata['d']==1):
            lists += User.objects.filter('workExperience'==3)
        if(usersdata['fff']==1):
            lists += followerslist(self,request)

        users = lists.order_by('workExperience', 'username')[:]
        serializer = UserSerializer(users,many =True)
        print(serializer.data)
        return Response(serializer.data)

    '''@action(detail=False , methods=['get',])
    def usersfiltered(self , request ):
        userdata = request.data
        if self.request.user.is_anonymous:
            return Response({'UserList':0})
        
        querysets = User.objects.filter(userdata['workExperience'])
        users = querysets.order_by('username')[:]
    #    ordered = sorted(users, key=operator.attrgetter('first_name'))
        serializer = UserSerializer(users,many =True)
        print(serializer.data)
        return Response(serializer.data)'''

    @action(detail=False , methods=['get',])
    def send_email(self, request):
        """subject = request.POST.get('subject', '')
        from_email = request.POST.get('from_email', '') """
       
        subject = 'ReFree: New Post Uploaded'
        message = 'Check out new post uploaded by the person you follow!'
        from_email = 'refree6914@gmail.com'
        user = User.objects.get(id=self.request.user.id )      
        querysets = user.followers.all()

        to_email = []
        for obj in querysets :
            print(querysets)
            x = querysets[0]
            uss = x.user_id
            ''' objectt = User.objects.get(id=uss)'''
            to_email.append(uss.email)

        try:
            send_mail(subject, message, from_email,to_email)

        except BadHeaderError:
            return Response({'data':'Invalid header found.'})

        return Response({'data':'Emails sent succesfully!.'})

class FollowViewSet(viewsets.ModelViewSet):
   
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

class CompanyViewSet(viewsets.ModelViewSet):
   
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False , methods=['get',])
    def usercompanies(self , request):
        userId = self.request.query_params.get('userId')
        querysets = Company.objects.filter(user=userId)
        serializeddata = CompanySerializer(querysets , many=True)
        return Response(serializeddata.data)


class SocialLinksViewSet(viewsets.ModelViewSet):
    
    queryset = SocialLinks.objects.all()#.order_by('-date_joined')
    serializer_class = SocialLinksSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False , methods=['get',])
    def userlinks(self , request):
        userId = self.request.query_params.get('userId')
        querysets = SocialLinks.objects.filter(user=userId)
        serializeddata = SocialLinksSerializer(querysets , many=True)
        return Response(serializeddata.data)


class ProjectsViewSet(viewsets.ModelViewSet):
    
    queryset = Projects.objects.all()
    serializer_class = ProjectsSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False , methods=['get',])
    # trendinglist
    def projectlist(self , request ):
        if self.request.user.is_anonymous:
            queryset = Projects.objects.none()
            serializer =ProjectsSerializer(queryset , many=True)
            return Response(serializer.data)
        
        querysets = Projects.objects.filter(user = self.request.user.id)
        projs = querysets.order_by('likes')[:8]
        ordered = sorted(projs, key=operator.attrgetter('name'))
        serializer = ProjectsSerializer(ordered,many =True)
        print(serializer.data)
        return Response(serializer.data)


    @action(detail=False , methods=['get',])
    def userprojects(self , request):
        querysets = Projects.objects.filter(user=self.request.user.id)
        serializeddata = ProjectsSerializer(querysets , many=True)
        return Response(serializeddata.data)


class ComponentViewSet(viewsets.ModelViewSet):
   
    queryset = Component.objects.all()#.order_by('-date_joined')
    serializer_class = ComponentSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False , methods=['get',])
    def display_components(request):
        userdata = request.data
        if request.method == 'GET': 
            # getting all the projects. 
            component = Component.objects.filter(projects = userdata['projects']) 
            serializeddata = FinalDesignSerializer(component , many=True)
            return Response(serializeddata.data)

class FinalDesignViewSet(viewsets.ModelViewSet):
    
    queryset = FinalDesign.objects.all()
    serializer_class = FinalDesignSerializer
    permission_classes = [permissions.IsAuthenticated]

    def display_projects(request):
        userdata = request.data
        if request.method == 'GET': 
            # getting all the projects. 
            projects = FinalDesign.objects.filter(projects = userdata['projects']) 
            serializeddata = FinalDesignSerializer(projects , many=True)
            return Response(serializeddata.data) 

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

'''def logout_view(request):
        return render(request,'login.html')'''

