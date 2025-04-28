from django.contrib import admin
from ekart_app.models import Categories,Types,Brands,Products,Images,Reviews,ActualStock,TempStock,Carts,Orders,Shipping,Addresses,Highlighted_Products

class CategoriesAdmin(admin.ModelAdmin):
    list_display=('category_name',)
    def category_name(self, instance):
        return instance.cat_name

class TypesAdmin(admin.ModelAdmin):
    list_display=('type_name',)
    def get_form(self, request, typeObj=None, **kwargs):
        form = super(TypesAdmin, self).get_form(request, typeObj, **kwargs)
        form.base_fields['cat_fk'].label_from_instance = lambda callObj: "{}. {}".format(callObj.id, callObj.cat_name)
        return form

class BrandsAdmin(admin.ModelAdmin):
    list_display=('brand_name',)

class ProductsAdmin(admin.ModelAdmin):
    list_display=('name','brand_name','type_name')
    def brand_name(self, instance):
        return instance.brand_fk.brand_name
    def type_name(self, instance):
        return instance.type_fk.type_name

    def get_form(self, request, prodObj=None, **kwargs):
        form = super(ProductsAdmin, self).get_form(request, prodObj, **kwargs)
        form.base_fields['brand_fk'].label_from_instance = lambda callObj: "{}. {}".format(callObj.id, callObj.brand_name)
        form.base_fields['type_fk'].label_from_instance = lambda callObj2: "{}. {}".format(callObj2.id, callObj2.type_name)
        return form

class ImagesAdmin(admin.ModelAdmin):
    list_display=('id','product_image','product_name','main_image')
    def product_name(self, instance):
        return instance.product_fk.name
    def main_image(self, instance):
        return instance.main_img

    def get_form(self, request, imageObj=None, **kwargs):
        form = super(ImagesAdmin, self).get_form(request, imageObj, **kwargs)
        form.base_fields['product_fk'].label_from_instance = lambda callObj: "{}. {}".format(callObj.id, callObj.name)
        return form

class ReviewsAdmin(admin.ModelAdmin):
    list_display=('user_name','product_name','id')
    def user_name(self, instance):
        return instance.user_fk.username
    def product_name(self, instance):
        return instance.product_fk.name

class AStockAdmin(admin.ModelAdmin):
    list_display=('product_name','actual_quantity','id')
    def product_name(self, instance):
        return instance.product_fk.name
    def actual_quantity(self, instance):
        return instance.act_quant

    def get_form(self, request, stockObj=None, **kwargs):
        form = super(AStockAdmin, self).get_form(request, stockObj, **kwargs)
        form.base_fields['product_fk'].label_from_instance = lambda callObj: "{}. {}".format(callObj.id, callObj.name)
        return form

class OrdersAdmin(admin.ModelAdmin):
    list_display=('id','user_name','product_name')
    def user_name(self, instance):
        return instance.user_fk.username
    def product_name(self, instance):
        return instance.product_fk.name

    def get_form(self, request, orderObj=None, **kwargs):
        form = super(OrdersAdmin, self).get_form(request, orderObj, **kwargs)
        form.base_fields['product_fk'].label_from_instance = lambda callObj: "{}. {}".format(callObj.id, callObj.name)
        return form

class ShippingAdmin(admin.ModelAdmin):
    list_display=('order_id','shipping_status','user_name','product_name')
    def order_id(self, instance):
        return ("Order : "+ instance.order_id.id)
    def user_name(self, instance):
        return instance.order_id.user_fk.username
    def product_name(self, instance):
        return instance.order_id.product_fk.name

    def get_form(self, request, shpObj=None, **kwargs):
        form = super(ShippingAdmin, self).get_form(request, shpObj, **kwargs)
        form.base_fields['order_id'].label_from_instance = lambda callObj: "{} {}".format("Ord ID :", callObj.id)
        return form

class AddressAdmin(admin.ModelAdmin):
    list_display=('user','address')
    def user(self,instance):
        return instance.user_fk.username
    def get_form(self, request, addrObj=None, **kwargs):
        form = super(AddressAdmin, self).get_form(request, addrObj, **kwargs)
        form.base_fields['user_fk'].label_from_instance = lambda callObj: "{}. {}".format(callObj.id, callObj.username)
        return form

class HighlightAdmin(admin.ModelAdmin):
    list_display=('products','stock')
    def products(self, instance):
        return instance.product_fk.name
    def stock(self, instance):
        currentStock=ActualStock.objects.get(product_fk=instance.product_fk)
        return currentStock.act_quant
    def get_form(self, request, highObj=None, **kwargs):
        form = super(HighlightAdmin, self).get_form(request, highObj, **kwargs)
        form.base_fields['product_fk'].label_from_instance = lambda callingObj: "{}. {}".format(callingObj.id, callingObj.name)
        return form

admin.site.register(Categories, CategoriesAdmin),
admin.site.register(Types,TypesAdmin),
admin.site.register(Brands, BrandsAdmin),
admin.site.register(Products, ProductsAdmin),
admin.site.register(Images, ImagesAdmin),
admin.site.register(Reviews, ReviewsAdmin),
admin.site.register(ActualStock, AStockAdmin),
# admin.site.register(TempStock),
# admin.site.register(Carts),
admin.site.register(Orders, OrdersAdmin),
admin.site.register(Shipping, ShippingAdmin),
admin.site.register(Addresses, AddressAdmin),
admin.site.register(Highlighted_Products, HighlightAdmin)