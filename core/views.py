from django.shortcuts import redirect,render
from django.http import HttpResponseRedirect
from django.urls import reverse
from core.models import Category, SubCategory, Vendor, Product, ProductImages, ProductReview, CartOrder, CartOrderItems, Add
from core.forms import ProductReviewForm
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib import messages

from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from paypal.standard.forms import PayPalPaymentsForm

# Create your views here.
def index(request):
    products = Product.objects.all().order_by("-id")
    
    context = {
        "products":products
    }
    return render(request,'core/index.html', context)

def product_list_view(request):
    products = Product.objects.filter(product_status="published")
    
    context = {
        "products":products
    }
    return render(request,'core/product.html', context)

def product_category_list_view(request,sid):
    subcategory = SubCategory.objects.get(sid=sid)
    products = Product.objects.filter(product_status="published", subcategory=subcategory)
    
    context = {
        "subcategory":subcategory,
        "products":products
    }
    return render(request,'core/subcategory-product-list.html', context)

def product_detail_view(request,pid):
    product = Product.objects.get(pid=pid)
    p_image = product.p_images.all()
    products = Product.objects.filter(subcategory=product.subcategory).exclude(pid=pid)
    
    review = ProductReview.objects.filter(product=product).order_by("-date")
    review_form = ProductReviewForm()
    context = {
        "product":product,
        "p_image":p_image,
        "review_form":review_form,
        "review":review,
        "products":products,
    }
    return render(request,'core/product-detail.html', context)

def ajax_add_review(request,pid):
    product = Product.objects.get(pid=pid)
    user = request.user
    
    review= ProductReview.objects.create(
        user=user,
        product=product,
        review=request.POST['review'],
        rating=request.POST['rating'],
        
    )
    
    context={
        'user':user.username,
        'review':request.POST['review'],
        'rating':request.POST['rating'],
    }
    return JsonResponse(
        {'bool':True,
        'context':context}
    )
    
def search_view(request):
    query = request.GET.get("q")
    
    products = Product.objects.filter(title__icontains=query).order_by("-date")
    
    context = {
        "products":products,
        "query":query,
    }
    return render(request,'core/search.html', context)

def filter_product(request):
    subcategories = request.GET.getlist("subcategory[]")
    min_price= request.GET['min_price']
    max_price= request.GET['max_price']
    
    products=Product.objects.filter(product_status="published").order_by("-id").distinct()
    products = products.filter(price__gte=min_price)
    products = products.filter(price__lte=max_price)
    
    
    if len(subcategories)>0:
        products = products.filter(subcategory__id__in = subcategories).distinct()
        
    context = render_to_string("core/async/product-list.html",{"products":products})
    return JsonResponse({"context":context})
    
def about(request):
    return render(request,'core/about.html')

@login_required
def add_to_cart(request):
    cart_product ={}

    qty = int(request.GET.get('qty', 0))
    if qty <= 0:
        return JsonResponse({"error": "Quantity must be greater than zero"})

    cart_product[str(request.GET['id'])]={
        'title':request.GET['title'],
        'qty': qty,
        'price':request.GET['price'],
        'image':request.GET['image'],
        'pid':request.GET['pid'],
    }

    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj']=cart_data
            
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj'] = cart_product 
    return JsonResponse({"data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj'])})

@login_required
def cart_view(request):
    cart_total_amount=0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            
            cart_total_amount += int(item['qty']) * float(item['price'])
           
        return render(request, "core/cart.html",{"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})
    else:
        messages.warning(request,"your cart is empty!..")
        return redirect("core:index") 
@login_required    
def delete_item_from_cart(request):
    product_id = str(request.GET['id'])
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data
        cart_total_amount=0
        if 'cart_data_obj' in request.session:
            for p_id, item in request.session['cart_data_obj'].items():
                cart_total_amount += int(item['qty']) * float(item['price'])    

        context = render_to_string("core/async/cart-list.html",{"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})
        return JsonResponse({"data":context, 'totalcartitems': len(request.session['cart_data_obj'])})
    
@login_required
def update_item_from_cart(request):
    product_id = str(request.GET['id'])
    product_qty = int(request.GET['qty'])

    if product_qty <= 0:
        if 'cart_data_obj' in request.session and product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del cart_data[product_id]
            request.session['cart_data_obj'] = cart_data
    else:
        if 'cart_data_obj' in request.session and product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[product_id]['qty'] = product_qty
            request.session['cart_data_obj'] = cart_data

    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

    context = render_to_string("core/async/cart-list.html",{"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})
    return JsonResponse({"data":context, 'totalcartitems': len(request.session['cart_data_obj'])})

@login_required
def checkout_view(request):
    if 'cart_data_obj' in request.session and len(request.session['cart_data_obj']) >= 6:
        cart_total_amount = 0
        total_amount = 0
        for p_id, item in request.session['cart_data_obj'].items():
            total_amount += int(item['qty']) * float(item['price'])
            
        order = CartOrder.objects.create(
            user=request.user,
            price=total_amount
        ) 
        
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
            
            cart_order_product = CartOrderItems.objects.create(
                order=order,
                invoice_no="INVOICE_NO-" + str(order.id),
                item=item['title'],
                image=item['image'],
                qty=item['qty'],
                price=item['price'],
                total=float(item['qty']) * float(item['price'])
            )
    
        host = request.get_host()
        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': cart_total_amount,
            'item_name': "Order-Item-No-" + str(order.id),
            'invoice': "INVOICE_NO-" + str(order.id),
            'currency_code': "USD",
            'notify_url': 'http://{}{}'.format(host, reverse("core:paypal-ipn")),
            'return_url': 'http://{}{}'.format(host, reverse("core:payment-completed")),
            'cancel_url': 'http://{}{}'.format(host, reverse("core:payment-failed")),
        }
        
        paypal_payment_button = PayPalPaymentsForm(initial=paypal_dict)
        
        return render(request, "core/checkout.html", {
            "cart_data": request.session['cart_data_obj'],
            'totalcartitems': len(request.session['cart_data_obj']),
            'cart_total_amount': cart_total_amount,
            'paypal_payment_button': paypal_payment_button
        })
    else:
        messages.warning(request, 'Your cart must have at least 6 products to checkout.')
        return HttpResponseRedirect(reverse("core:product"))

@login_required
def payment_completed_view(request):
    cart_total_amount=0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
    return render(request, "core/payment-completed.html", {"cart_data":request.session['cart_data_obj'],'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})

@login_required
def payment_failed_view(request):
    return render(request, 'core/payment-failed.html')

@login_required
def customer_dashboard(request):
    orders =  CartOrder.objects.filter(user=request.user).order_by("-id")
    address = Add.objects.filter(user=request.user)
    
    if request.method == "POST":
        address = request.POST.get("address")
        mobile = request.POST.get("mobile")
        
        new_address = Add.objects.create(
            user = request.user,
            address=address,
            mobile=mobile,
        )
        messages.success(request, "Address added Successfully.")
        return redirect("core:dashboard")
    
    context = {
        "orders" : orders,
        "address" : address
    }
    return render(request, 'core/dashboard.html',context)

def order_detail(request, id):
    order =  CartOrder.objects.get(user=request.user, id=id)
    order_items =  CartOrderItems.objects.filter(order=order)
    
    context = {
        "order_items" : order_items
    }
    return render(request, 'core/order-detail.html',context)
    
def make_address_deault(request):
    id = request.GET['id']
    Add.objects.update(status=False)
    Add.objects.filter(id=id).update(status=True)
    return JsonResponse({"boolean":True})


