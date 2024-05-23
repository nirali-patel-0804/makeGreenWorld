from core.models import Category, SubCategory, Vendor, Product, ProductImages, ProductReview, CartOrder, CartOrderItems, Add
from django.db.models import Min,Max
def default(request):
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    min_max_price = Product.objects.aggregate(Min("price") , Max("price"))
    
    return{
        'categories':categories,
        'subcategories':subcategories,
        'min_max_price':min_max_price
    }