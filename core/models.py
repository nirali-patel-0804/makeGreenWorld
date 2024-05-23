from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User


STATUS_CHOICE = (
    ("process", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
)

STATUS = (
    ("draft", "Draft"),
    ("disabled", "Disabled"),
    ("rejected", "Rejected"),
    ("in_review", "In Review"),
    ("published", "Published"),
)

RATING = (
    ("1", "★"),
    ("2", "★★"),
    ("3", "★★★"),
    ("4", "★★★★"),
    ("5", "★★★★★"),
)

# Create your models here.
def user_directory_path(instance,filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=30, prefix="cat")
    title=models.CharField(max_length=100,default="Food")
    image = models.ImageField(upload_to="category",default="category.jpg")
    
    class Meta:
        verbose_name_plural="Categories"
        
    def category_image(self):
        return mark_safe('<img src="%s" width="70" height="70"/>' % (self.image.url))
    
    def __str__(self):
        return self.title
    
    
class SubCategory(models.Model):
    sid = ShortUUIDField(unique=True, length=10, max_length=30)
    title=models.CharField(max_length=100,default="Food")
    image = models.ImageField(upload_to="category",default="category.jpg")
    
    
    category = models.ForeignKey(Category,on_delete=models.SET_NULL, null=True)
    
    class Meta:
        verbose_name_plural="Sub Categories"
        
    def subcategory_image(self):
        return mark_safe('<img src="%s" width="70" height="70"/>' % (self.image.url))
    
    def __str__(self):
        return self.title
    
    


class Vendor(models.Model):
    vid = ShortUUIDField(unique=True, length=10, max_length=30, prefix="Ven")
    title = models.CharField(max_length=100,default="Nestify")
    image = models.ImageField(upload_to=user_directory_path,default="Vendor.jpg")
    description = models.TextField(null=True, blank=True,default="I  am vendor")
    address = models.CharField(max_length=100,default="Ahmedabad")
    contact = models.CharField(max_length=100,default="+123(555) 555")
    chat_resp_time = models.CharField(max_length=100,default="100")
    shipping_on_time = models.CharField(max_length=100,default="100")
    authentic_rating = models.CharField(max_length=100,default="100")
    days_return = models.CharField(max_length=100,default="100")
    warranty_period = models.CharField(max_length=100,default="100")
    
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    
    class Meta:
        verbose_name_plural="Vendors"
        
    def vendor_image(self):
        return mark_safe('<img src="%s" width="70" height="70"/>' % (self.image.url))
    
    def __str__(self):
        return self.title
    
class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=30)
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100, default="Fresh Pear")
    
    image = models.ImageField(upload_to=user_directory_path, default="product.jpg")
    description = models.TextField(null=True, blank=True, default="This is the product")
    
    price = models.DecimalField(max_digits=11, decimal_places=2, default="1.99")
    old_price = models.DecimalField(max_digits=11, decimal_places=2, default="2.99")
    
    specification = models.TextField(null=True, blank=True)
    stock_count = models.CharField(max_length=100, default="100")
    life = models.CharField(max_length=100, default="1")
    

    tags = models.CharField(max_length=100, default="Plants")
    
    product_status = models.CharField(choices=STATUS, max_length=10, default="in_review")
    
    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)
    
    sku = ShortUUIDField(unique=True, length=4, max_length=30, prefix="sku")
    
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name_plural="Products"
        
    def product_image(self):
        return mark_safe('<img src="%s" width="70" height="70"/>' % (self.image.url))
    
    def __str__(self):
        return self.title
    
    def get_percentage(self):
        new_price = (self.price / self.old_price) * 100
        return new_price
    
class ProductImages(models.Model):
    images = models.ImageField(upload_to="product-images", default="product.jpg")
    product = models.ForeignKey(Product, related_name = "p_images", on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural="Product Images"
        
        
############################## Cart, Order , OrderItems , Address ##################
        
class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    price = models.DecimalField(max_digits=11, decimal_places=2, default="0.00")
    
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS_CHOICE, max_length=30, default="process")
    
    class Meta:
        verbose_name_plural="Cart Order"
        
class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=200)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    qty = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=11, decimal_places=2, default="1.99")
    total = models.DecimalField(max_digits=11, decimal_places=2, default="1.99")

    class Meta:
        verbose_name_plural="Cart Order Items" 
        
    def order_image(self):
        return mark_safe('<img src="/media/%s" width="70" height="70"/>' % (self.image))
    
############################## Product Review, wishlists, Address ##################

class ProductReview(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL, null=True,related_name="review")
    review = models.TextField()
    rating = models.TextField(choices=RATING,default=None)
    date = models.DateTimeField(auto_now_add=True)
     
    class Meta:
         verbose_name_plural="Product Reviews"
        
    def __str__(self):
        return self.product.title
    
    def get_rating(self):
        return self.rating

   

    

class Add(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    mobile = models.CharField(max_length=10, null=True)
    address = models.CharField(max_length=100, null=True)
    status = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural="Address"
    
     