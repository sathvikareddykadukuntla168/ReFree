"""csnpro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
"""from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('reFree/',include('reFree.urls')),
]"""

from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from rest_framework import routers
from reFree import views 
from django.views.generic.base import TemplateView

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'companies', views.CompanyViewSet)
router.register(r'socialLinks', views.SocialLinksViewSet)
router.register(r'projects', views.ProjectsViewSet)
router.register(r'component', views.ComponentViewSet)
router.register(r'finalDesign', views.FinalDesignViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    url(r'^home/$', TemplateView.as_view(template_name='home.html'), name='home'),
   # path('signup/',views.signup_view.as_view(),name='signup'),
    path('profile/', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
] 
