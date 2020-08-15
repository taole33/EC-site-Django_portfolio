from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.template.response import TemplateResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render
from django.views.generic import View

from merchandise.models import Product
import requests

@require_POST
def cart_add(request, product_id):
    if not Product.objects.filter(id=product_id).exists():
        raise Http404
    cart = request.session.get('cart')
    if cart:
        cart.append(product_id)
        request.session['cart'] = cart
    else:
        request.session['cart'] = [product_id]
    return HttpResponseRedirect(reverse('product_list'))


def cart_list(request):
    cart = request.session.get('cart') 
    if cart:
        products = []
        for product_id in cart:
            try:
                product = Product.objects.get(id=product_id)
                products.append(product)
            except Product.DoesNotExist:
                pass
    else:
        products = []
    
    total_price = 0
    for product in products:
        total_price += product.price
    request.session['total_price'] = total_price
    
    return TemplateResponse(request, 'cart/list.html',
                            {'products': products,
                             'total_price':total_price})

@require_POST
def cart_delete(request,product_id):
    cart = request.session.get('cart')
    if cart:
        filtered = []
        for p in cart:
            if p != product_id:
                filtered.append(p)
        request.session['cart'] = filtered
    return HttpResponseRedirect(reverse('cart_list'))


@require_POST
def payment(request):
    total_price = request.session.get('total_price')
    payjp_token = request.POST.get('payjp-token')

    request_url = 'https://api.pay.jp/v1/charges'
    params = {
        'amount': total_price,
        'currency': 'jpy',
        'card': payjp_token
        }

    requests.post(request_url, params, auth=("WRITE_HERE_secretkey", ""))
    request.session['cart'] = None
    return render(request, 'cart/pay_done.html',{'total_price':total_price} )
