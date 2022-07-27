# Django
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# 3rd party
from taggit.managers import TaggableManager
from cloudinary.models import CloudinaryField

class Meme(models.Model):
    title = models.CharField(max_length=100, blank=True) 
    # type = models.CharField(
    #     choices=[
    #         ('gif', 'gif'),
    #         ('image', 'image'),    
    #     ], blank=False)
    tags = TaggableManager()    
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True) # User who added this meme
    image = CloudinaryField('image')
    date_added = models.DateTimeField(auto_now_add=True)
       
    class Meta:
        verbose_name = _("Meme")
        verbose_name_plural = _("Memes")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Meme_detail", kwargs={"pk": self.pk})