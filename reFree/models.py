from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, AbstractUser
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from ckeditor.fields import RichTextField
from phonenumber_field.modelfields import PhoneNumberField

# make changes-->emailvalidation,imageField,relations
WORKEXP=(
    ('0','<1 year'),
    ('1','1-2 years'),
    ('2','2-5 years'),
    ('3','>5years'),
)

def user_directory_path(instance, filename): 
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename> 
    return 'user_{0}/{1}'.format(instance.user.phone_number, filename)

"""class UserProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, unique=True) 
    firstname =models.CharField(max_length= 50)
    lastname =models.CharField(max_length= 50)
    email = forms.EmailField(max_length=254)
    phonenumber=PhoneNumberField()
    password =forms.CharField(max_length= 50)
    confirmpassword =forms.CharField(max_length= 50)"""

class User(AbstractUser): 
    about = RichTextField(blank=True,null=True, ) 
    workExperience = models.CharField(max_length=1, choices=WORKEXP, default='1')
    phone_number=PhoneNumberField(default='DEFAULT VALUE')
    profile_photo = models.ImageField(upload_to='profile_photos/',null=True,blank =True)
    

    def __str__(self):
        return self.username

    """ emailsToSend = models.ForeignKey(self,on_delete=models.CASCADE);
        follows = models.ForeignKey(self,on_delete=models.CASCADE);"""

    class Meta :
        verbose_name_plural="User"

class Follow(models.Model):
    user_id = models.ForeignKey("User", related_name="following",on_delete=models.CASCADE,default='9999999999999')
    following_user_id = models.ForeignKey("User", related_name="followers",on_delete=models.CASCADE,default='999999999999')
    
    class Meta :
        verbose_name_plural="Follow"

class Company(models.Model): 
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    time = models.CharField(max_length=1, choices=WORKEXP)
    company = models.TextField()
    position = models.TextField()
    class Meta :
        verbose_name_plural="Company"

class SocialLinks(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    link = RichTextField(blank=True,null=True) 
    class Meta :
        verbose_name_plural="SocialLinks"

class Projects(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = RichTextField(blank=True,null=True)
    display = models.ImageField(upload_to ='projectdisplays/',null=True,blank =True) 
    creation = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return str(self.creation)

    class Meta :
        verbose_name_plural="Projects"   

class Like(models.Model):
    user_id = models.ForeignKey("User", related_name="person",on_delete=models.CASCADE)
    project_id = models.ForeignKey("Projects", related_name="project",on_delete=models.CASCADE)

    class Meta :
        verbose_name_plural="Like"

class Component(models.Model):
    project =models.ForeignKey(Projects,on_delete=models.CASCADE)
    description = RichTextField(blank=True,null=True)
    upload = models.ImageField(upload_to ='components/',null=True,blank =True) 
    class Meta :
        verbose_name_plural="Component"

class FinalDesign(models.Model):
    project = models.ForeignKey(Projects,on_delete=models.CASCADE)     
    finaldesign = models.ImageField(upload_to ='images/',null=True , blank=True)
    class Meta :
        verbose_name_plural="FinalDesign"
