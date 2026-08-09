import re
from rest_framework import serializers
from .models import CustomUser
from django.utils import timezone

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    phone_number = serializers.CharField(required=False, allow_blank=True)
    gender = serializers.CharField(required=False, allow_blank=True)
    username = serializers.CharField(required=False, allow_blank=True)

    
    class Meta:
        model = CustomUser
        fields = [
            'id','full_name','username','email','password','confirm_password',
            'phone_number','birth_date','gender','profession','speciality','country','city',
            'last_login_time','last_login_ip'
        ]
        read_only_fields = ['last_login_time','last_login_ip']

    def validate_password(self, value):
        # Validation simplifiée: min 8 caractères
        if len(value) < 8:
            raise serializers.ValidationError(
                "Le mot de passe doit contenir au moins 8 caractères."
            )
        return value

    def validate(self, data):
        # Valider qu'au moins email ou phone_number est fourni
        email = data.get('email', '')
        phone_number = data.get('phone_number', '')
        
        if not email and not phone_number:
            raise serializers.ValidationError("Vous devez fournir un email ou un numéro de téléphone.")
        
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        
        birth_date = data.get('birth_date')
        if birth_date and (timezone.now().date().year - birth_date.year) < 18:
            raise serializers.ValidationError("Vous devez avoir au moins 18 ans.")
        return data
    
   
    def create(self, validated_data):
      validated_data.pop('confirm_password')
      password = validated_data.pop('password')

      # Générer username automatiquement basé sur full_name si non fourni (CamelCase)
      if 'username' not in validated_data or not validated_data['username']:
          full_name = validated_data.get('full_name', '')
          # Séparer prénom et nom
          name_parts = full_name.strip().split()
          if len(name_parts) >= 2:
              # Prendre le premier mot comme prénom et le reste comme nom
              first_name = name_parts[0].capitalize()
              last_name = ''.join(part.capitalize() for part in name_parts[1:])
              username = f"@{first_name}{last_name}"
          else:
              # Si seulement un mot, l'utiliser comme prénom
              username = f"@{name_parts[0].capitalize() if name_parts else 'User'}"

          # Nettoyer: retirer caractères spéciaux sauf @
          username = re.sub(r'[^a-zA-Z0-9@]', '', username)

          # Ajouter un suffixe numérique si le username existe déjà
          base_username = username
          counter = 1
          while CustomUser.objects.filter(username=username).exists():
              username = f"{base_username}{counter}"
              counter += 1
          validated_data['username'] = username

      user = CustomUser(**validated_data)
      user.set_password(password)   # ✅ mot de passe hashé
      user.save()
      return user
    
    def update(self, instance, validated_data):
       password = validated_data.pop('password', None)
       if password:
        instance.set_password(password)
       return super().update(instance, validated_data)

    

    




