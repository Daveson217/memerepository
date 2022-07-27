# 3rd party
from rest_framework import generics

# App
from .models import Meme
from .serializers import MemeSerializer
# Create your views here.

class MemeListCreateAPIView(generics.ListCreateAPIView):
    queryset = Meme.objects.all()
    serializer_class = MemeSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return super(MemeListCreateAPIView, self).create(request, *args, **kwargs)        