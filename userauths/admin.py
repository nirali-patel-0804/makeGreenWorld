from django.contrib import admin
from userauths.models import User
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
class UserAdmin(admin.ModelAdmin):
    list_display = ['email','username', 'first_name', 'last_name', 'phone', 'address']
    actions = [download_pdf]
    
admin.site.register(User, UserAdmin)
