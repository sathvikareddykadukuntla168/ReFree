from django.contrib import admin
from .models import User,Company,Projects,Component,FinalDesign,SocialLinks

# Register your models here.
admin.site.register(User)
admin.site.register(Component)
admin.site.register(Company)
admin.site.register(FinalDesign)
admin.site.register(SocialLinks)
admin.site.register(Projects)