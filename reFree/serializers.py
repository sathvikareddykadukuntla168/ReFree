from reFree.models import User,Company,Projects,Component,FinalDesign,SocialLinks
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['firstname', 'lastname', 'phone_number','about','workExperience']

class CompanySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Company
        fields = ['user', 'time','company','position']

class SocialLinksSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SocialLinks
        fields = ['user', 'name','link']

class ProjectsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Projects
        fields = ['user', 'name','description','likes']

class ComponentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Component
        fields = ['project','description','upload']

class FinalDesignSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FinalDesign
        fields = ['project']

