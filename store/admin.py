from django.contrib import admin
from django.utils.html import format_html
from .models import Product, ProductGallery,Variation,ReviewRating
import admin_thumbnails

@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1



class ProductAdmin(admin.ModelAdmin):
    list_display        = ('product_name','mrp_price','price','stock','category',)
    prepopulated_fields = {'slug': ('product_name',)}
 
    inlines             = [ProductGalleryInline]

    def thumbnail(self, object):
        return format_html ('<img src="{}" width="30" style ="border-radius:50%>"'.format(object.images.url))
    thumbnail.short_description = 'Product Image'
    
    
class VariationAdmin(admin.ModelAdmin):
    list_display        = ('product','variation_category','variation_value','is_active',)
    list_editable       = ('is_active',)
    list_filter         = ('product','variation_category','variation_value','is_active',)

# Register your models here.

admin.site.register(Product,ProductAdmin)

admin.site.register(Variation,VariationAdmin)

admin.site.register(ReviewRating)

admin.site.register(ProductGallery)