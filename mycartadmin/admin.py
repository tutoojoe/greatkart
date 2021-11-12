from django.contrib import admin
from .models import BannerUpdate
from django.utils.html import format_html


# Register your models here.

class BannerUpdateAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html ('<img src="{}" width="30" style ="border-radius:5%>"'.format(object.banner_image.url))
    thumbnail.short_description = 'Banner Image'


    list_display = ('thumbnail', 'banner_name', 'valid_from', 'valid_to', 'is_active')
    list_display_links = ('thumbnail', 'banner_name')
    ordering            = ('-created_at',)


admin.site.register(BannerUpdate,BannerUpdateAdmin)
