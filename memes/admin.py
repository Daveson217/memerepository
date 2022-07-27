from django.contrib import admin
from .models import Meme

class SaverAdmin(admin.ModelAdmin):
    list_display = ('id', '')
    list_filter = ('lga', 'state', 'saving_frequency', 'bank', 'agent')

#admin.site.register(Saver, SaverAdmin)
