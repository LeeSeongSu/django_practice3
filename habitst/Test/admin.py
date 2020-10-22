from django.contrib import admin

from .models import *

class BookAdmin(admin.ModelAdmin):
    pass

admin.site.register(Tester)
admin.site.register(Book, BookAdmin)
admin.site.register(Question)
