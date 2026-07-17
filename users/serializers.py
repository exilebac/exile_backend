import re
from rest_framework import serializers
from .models import CustomUser
from django.utils import timezone

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    
    class Meta:
        model = CustomUser
        fields = [
            'id','full_name','username','email','password','confirm_password',
            'phone_number','birth_date','profession','speciality','country','city',
            'last_login_time','last_login_ip'
        ]
        read_only_fields = ['username','last_login_time','last_login_ip']

    def validate_password(self, value):
        # Regex: min 8 chars, 1 maj, 1 min, 1 digit, 1 special
        pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$'
        if not re.match(pattern, value):
            raise serializers.ValidationError(
                "Le mot de passe doit contenir au moins 8 caractères, "
                "une majuscule, une minuscule, un chiffre et un caractère spécial."
            )
        return value

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        if (timezone.now().date().year - data['birth_date'].year) < 18:
            raise serializers.ValidationError("Vous devez avoir au moins 18 ans.")
        return data
    
   
    def create(self, validated_data):
      validated_data.pop('confirm_password')
      password = validated_data.pop('password')
      user = CustomUser(**validated_data)
      user.set_password(password)   # ✅ mot de passe hashé
      user.save()
      return user
    
    def update(self, instance, validated_data):
       password = validated_data.pop('password', None)
       if password:
        instance.set_password(password)
       return super().update(instance, validated_data)

    

    




