from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'firstname', 'lastname')
        
class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'email', 'firstname', 'lastname', 'password', 'password2')
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
    def create(self, validated_data):
        username = validated_data['email']
        email = username
        password = validated_data['password']
        password2 = validated_data['password2']
        firstname = validated_data['firstname']
        lastname = validated_data['lastname']
        
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
                
        user = User.objects.create_user(username, email, password, password2, firstname, lastname)
        return user