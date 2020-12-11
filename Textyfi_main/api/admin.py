from django.contrib import admin
from .models import wordcounterModel,ratereviewModel,grammarModel
# Register your models here.
admin.site.register(wordcounterModel)
admin.site.register(ratereviewModel)
admin.site.register(grammarModel)