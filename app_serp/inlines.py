from django.contrib import admin
from . import models

class TopicInline(admin.TabularInline):
    model = models.TopicModel