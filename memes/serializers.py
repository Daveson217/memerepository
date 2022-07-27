# 3rd party
from rest_framework import serializers

# App
from .models import Meme

class MemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meme
        fields = ['title', 'image', 'tags']