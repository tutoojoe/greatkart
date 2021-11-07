from django.contrib import admin
from django.utils.html import format_html
from accounts.models import Account, Address, UserProfile
from django.contrib.auth.admin import UserAdmin
# Register your models here.


# class AddressInline(admin.TabularInline):
#     model = Address
#     extra = 0
#     readonly_fields = ['full_name', 'mobile', 'address_line1', 'city','district','state','pincode']

class AccountAdmin(UserAdmin):
    list_display        = ('email','first_name','last_name','username','last_login','is_active','date_joined')
    # Making the below links clickable
    list_display_links  = ('email', 'first_name', 'username')
    filter_horizontal   = ()
    list_filter         = ()
    fieldsets           = ()

    readonly_fields     = ('last_login','date_joined',)
    ordering            = ('-date_joined',)
    # inlines             = [AddressInline]


class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html ('<img src="{}" width="30" style ="border-radius:5%>"'.format(object.profile_picture.url))
    thumbnail.short_description = 'Profile Picture'


    list_display = ('thumbnail', 'user', 'city', 'state','country')



admin.site.register(Account,AccountAdmin)
admin.site.register(Address)
admin.site.register(UserProfile,UserProfileAdmin)

