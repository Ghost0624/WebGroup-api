from rest_framework import serializers
from Member.models import Members, Roles

class MemberSerializer(serializers.ModelSerializer):
  role_name = serializers.CharField(source='role.name', read_only=True)
  class Meta:  
    model = Members  
    fields = ('name', 'password', 'email', 'phone', 'photo', 'description', 'role_name')  
    extra_kwargs = {  
        'password': {'write_only': True}  
    }  

  def create(self, validated_data):  
    password = validated_data.pop('password', None)  
    instance = self.Meta.model(**validated_data)  
    if password is not None:  
      instance.set_password(password)  
    instance.save()  
    return instance

class RoleSerializer(serializers.ModelSerializer):
  class Meta:
    model=Roles
    fields=('name')