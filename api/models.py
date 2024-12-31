from django.db import models
from django.contrib.auth.models import User
class Notes(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,related_name='notes')
    body=models.TextField(null=True,blank=True)
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)


