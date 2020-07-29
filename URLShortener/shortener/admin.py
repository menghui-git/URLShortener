from django.contrib import admin

from shortener.models import URL


class URLAdmin(admin.ModelAdmin):
    list_display = ('id', 'hash', 'url', 'created_at')


admin.site.register(URL, URLAdmin)
