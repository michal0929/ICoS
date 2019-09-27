
from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Course)
admin.site.register(Chapter)
admin.site.register(TextBlock)
admin.site.register(YTLink)
admin.site.register(FileUpload)

