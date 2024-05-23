from django.urls import path, include
from core.views import index
from core.views import about
from core.views import product_list_view,order_detail,make_address_deault,checkout_view,customer_dashboard,payment_completed_view,payment_failed_view,delete_item_from_cart,update_item_from_cart,add_to_cart,cart_view,product_category_list_view,product_detail_view,ajax_add_review,search_view,filter_product

app_name="core"

urlpatterns=[
    path("",index,name="index"),
    path("about/",about,name="about"),
    path("shop/",product_list_view,name="product"),
    path("product/<pid>/",product_detail_view,name="product-detail"),
    path("subcategory/<sid>",product_category_list_view,name="product-category-list"),
    path("ajax-add-review/<pid>/", ajax_add_review, name="ajax-add-review"),
    path("search/", search_view, name="search"),
    path("filter-product/",filter_product,name="filter-product"),
    path("add-to-cart/",add_to_cart,name="add-to-cart"),
    path("cart/",cart_view,name="cart"),
    path("delete-from-cart/",delete_item_from_cart,name="delete-from-cart"),
    path("update-cart/",update_item_from_cart,name="update-cart"),
    path("checkout/",checkout_view,name="checkout"),
    path("make-default-address/",make_address_deault,name="make-default-address"),

    
    #payment paypal
    path('paypal/',include('paypal.standard.ipn.urls')),
    
    #payment complated
    path('payment-completed/',payment_completed_view,name="payment-completed"),
    
    #payment fail
    path('payment-failed/',payment_failed_view,name="payment-failed"),
    path('dashboard/',customer_dashboard,name="dashboard"),
    path("dashboard/order/<int:id>",order_detail,name="order-detail"),
    
   
    
   
]