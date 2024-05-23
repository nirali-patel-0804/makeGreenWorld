from django.contrib import admin
from core.models import Category, SubCategory, Vendor, Product, ProductImages, ProductReview, CartOrder, CartOrderItems, Add
from django.http import HttpResponse

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table,TableStyle
from reportlab.lib import colors

def download_pdf(self, request, queryset):
    model_name = self.model.__name__
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={model_name}.pdf'
    
    pdf = canvas.Canvas(response, pagesize=letter)
    pdf.setTitle('PDF Report')
    
    order_queryset = queryset.order_by('id')
    
    headers = [field.verbose_name for field in self.model._meta.fields]
    data = [headers]
    
    for obj in order_queryset:
        data_row = [str(getattr(obj, field.name)) for field in self.model._meta.fields]
        data.append(data_row)
    
    table = Table(data)
    table.setStyle(TableStyle(
        [
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('GRID', (0,0), (-1,-1), 1, colors.black)
        ]
    ))
    
    canvas_width = 600
    canvas_height = 600
    
    table.wrapOn(pdf, canvas_width, canvas_height)
    table.drawOn(pdf, 40, canvas_height - len(data))
    
    pdf.save()
    return response

download_pdf.short_description =  "Report"
    
class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages
    actions = [download_pdf]
    
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = ['user', 'title', 'product_image', 'price', 'featured', 'product_status']
    
    actions = [download_pdf]
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'category_image']
    actions = [download_pdf]
    
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['title',  'category']
    actions = [download_pdf]
class VendorAdmin(admin.ModelAdmin):
    list_display = ['title', 'vendor_image']
    actions = [download_pdf]
class CartOrderAdmin(admin.ModelAdmin):
    list_editable = ['paid_status','product_status']
    list_display = ['user', 'price', 'paid_status', 'order_date', 'product_status']
    actions = [download_pdf]
class CartOrderItemsAdmin(admin.ModelAdmin):
    list_display = ['order', 'invoice_no', 'item', 'image', 'qty', 'price', 'total']
    actions = [download_pdf]
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'review', 'rating']
    actions = [download_pdf]

class AddAdmin(admin.ModelAdmin):
    list_editable = ['address','status']
    list_display = ['user', 'address', 'status']
    
    
    
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(CartOrder, CartOrderAdmin)
admin.site.register(CartOrderItems, CartOrderItemsAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Add, AddAdmin)