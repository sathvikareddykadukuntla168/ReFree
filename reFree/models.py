from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from ckeditor.fields import RichTextField

# make changes-->emailvalidation,imageField,relations

WORKEXP=(
    ('0','<1 year'),
    ('1','1-2 years'),
    ('2','2-5 years'),
    ('3','>5years'),
)
def user_directory_path(instance, filename): 
	# file will be uploaded to MEDIA_ROOT / user_<id>/<filename> 
	return 'user_{0}/{1}'.format(instance.user.id, filename)

class User(models.Model): 
    firstname =models.CharField(max_length= 50)
    lastname =models.CharField(max_length= 50)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    #def custom_validate_email(value):
    #    if <custom_check>:
    #        raise ValidationError('Email format is incorrect')
    # email = models.EmailField(max_length=254, blank=False, unique=True, validators=[validate_email, custom_validate_email)
    about = RichTextField(blank=True,null=True) 
    workExperience = models.CharField(max_length=1, choices=WORKEXP)
    def __str__(self):
        return self.firstname
    #emailsToSend = models.ForeignKey('self',on_delete=models.CASCADE, null=True, blank=True)
    # follows = models.ForeignKey('self',on_delete=models.CASCADE, null=True, blank=True)
    class Meta :
        verbose_name_plural="User"

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
    likes = models.IntegerField()
    class Meta :
        verbose_name_plural="Projects"   

class Component(models.Model):
    project =models.ForeignKey(Projects,on_delete=models.CASCADE)
    description = RichTextField(blank=True,null=True)
    upload = models.ImageField(upload_to = user_directory_path) 
    class Meta :
        verbose_name_plural="Component"

class FinalDesign(models.Model):
    project = models.ForeignKey(Projects,on_delete=models.CASCADE) 
    #def user_directory_path2(instance, filename): 
	    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename> 
	    #return 'user_{0}/{1}'.format(instance.user.id, filename)
	#upload = models.ImageField(upload_to = user_directory_path2)
    class Meta :
        verbose_name_plural="FinalDesign"