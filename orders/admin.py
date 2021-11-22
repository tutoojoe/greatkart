from django.contrib import admin
from .models import Payment, Order, OrderProduct
# Register your models here.

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    
    extra = 0
    readonly_fields = ['payment', 'user', 'product', 'quantity','ordered']




class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number','full_name','phone','email','city','order_total','tax','status','is_ordered']
    list_filter = ['status', 'is_ordered','coupon_use_status']
    search_fields = ['order_number','first_name','last_name','phone','email']
    list_per_page = 20
    fieldsets           = ()
    inlines = [OrderProductInline]


admin.site.register(Payment)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderProduct)

