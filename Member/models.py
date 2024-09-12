from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.
class Members(models.Model):
  id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=50)
  email = models.CharField(max_length=50)
  password = models.CharField(max_length=1000)
  phone = models.CharField(max_length=50, null=True)
  verify_status = models.BooleanField(null=True)
  photo = models.CharField(max_length=150, null=True)
  description = models.CharField(max_length=1500, null=True)
  role = models.ForeignKey("Roles", on_delete=models.CASCADE, null=True)

  def set_password(self, raw_password):  
    self.password = make_password(raw_password)

  def check_password(self, raw_password):  
    return check_password(raw_password, self.password)
  
class Roles(models.Model):
  id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=50)