# from django import views
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from app.models import Customer,Product,Cart,OrderPlaced
from app.forms import CustomerCreationForm,CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# def home(request):
#  return render(request, 'app/home.html')

class home(View):
    def get(self,request):
        topwears=Product.objects.filter(category='TW')
        bottomwears=Product.objects.filter(category='BW')
        mobiles=Product.objects.filter(category='M')
        return render(request,'app/home.html',{'topwears':topwears,'bottomwears':bottomwears,'mobiles':mobiles})

# def product_detail(request):
#  return render(request, 'app/productdetail.html')

class product_detail(View):
    def get(self,request,pk):
        if request.user.is_authenticated:
            product=Product.objects.get(pk=pk)
            item_already_in_cart=False
            item_already_in_cart=Cart.objects.filter(Q(product=product.id)&Q(user=request.user)).exists()
            return render(request,'app/productdetail.html',{'product':product,'item_already_in_cart':item_already_in_cart})
        else:
            product=Product.objects.get(pk=pk)
            item_already_in_cart=False
            item_already_in_cart=Cart.objects.filter(Q(product=product.id)).exists()
            return render(request,'app/productdetail.html',{'product':product,'item_already_in_cart':item_already_in_cart})

@login_required
def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user=request.user
        cart=Cart.objects.filter(user=user)
        # print(cart)
        amount=0.0
        shippping_amount=70.0
        total_amount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user==user]
        # print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamount=(p.quantity*p.product.discounted_price)
                amount+=tempamount
                totalamount=amount+shippping_amount
            return render(request,'app/addtocart.html',{'carts':cart,'totalamount':totalamount,'amount':amount})
        else:
            return render(request,'app/emptycart.html')

def plus_cart(request):
    if request.method=="GET":
        prod_id=request.GET['prod_id']
        # print(prod_id)
        c=Cart.objects.get(Q(product=prod_id)&Q(user=request.user))
        c.quantity+=1
        c.save()
        amount=0.0
        shipping_amount=70.0
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount=(p.quantity*p.product.discounted_price)
            amount+=tempamount
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':amount+shipping_amount
        }
        return JsonResponse(data)

def minus_cart(request):
    if request.method=="GET":
        prod_id=request.GET['prod_id']
        # print(prod_id)
        c=Cart.objects.get(Q(product=prod_id)&Q(user=request.user))
        c.quantity-=1
        c.save()
        amount=0.0
        shipping_amount=70.0
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount=(p.quantity*p.product.discounted_price)
            amount+=tempamount
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':amount+shipping_amount
        }
        return JsonResponse(data)

def remove_cart(request):
    if request.method=="GET":
        prod_id=request.GET['prod_id']
        # print(prod_id)
        c=Cart.objects.get(Q(product=prod_id)&Q(user=request.user))
        c.delete()
        amount=0.0
        shipping_amount=70.0
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount=(p.quantity*p.product.discounted_price)
            amount+=tempamount
        data={
            'amount':amount,
            'totalamount':amount+shipping_amount
        }
        return JsonResponse(data)

def buy_now(request):
 return render(request, 'app/buynow.html')

# def profile(request):
#  return render(request, 'app/profile.html')

@login_required
def address(request):
    add=Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})

@login_required
def orders(request):
    op=OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{'order_placed':op})

def change_password(request):
 return render(request, 'app/changepassword.html')

def mobile(request,data=None):
    if data==None:
        mobiles=Product.objects.filter(category='M')
    elif data=='redmi' or data=='apple':
        mobiles=Product.objects.filter(category='M').filter(brand=data)
    elif data=='below':
        mobiles=Product.objects.filter(category='M').filter(discounted_price__lt=15000)
    elif data=='above':
        mobiles=Product.objects.filter(category='M').filter(discounted_price__gt=15000)
    return render(request, 'app/mobile.html',{'mobiles':mobiles})

def login(request):
 return render(request, 'app/login.html')

# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')

class CustomerRegistrationView(View):
    def get(self,request):
        form=CustomerCreationForm()
        return render(request,'app/customerregistration.html',{'form':form})
    def post(self,request):
        form=CustomerCreationForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulation!! Successfully Registered')
            form.save()
            form=CustomerCreationForm()
        return render(request,'app/customerregistration.html',{'form':form})

@login_required
def checkout(request):
    user=request.user
    add=Customer.objects.filter(user=user)
    cart_items=Cart.objects.filter(user=user)
    amount=0.0
    shipping_amount=70.0
    totalamount=0.0
    cart_product=[p for p in Cart.objects.all() if p.user==request.user]
    if cart_product:
        for p in cart_product:
            tempamount=(p.quantity*p.product.discounted_price)
            amount+=tempamount
        totalamount=amount+shipping_amount
    return render(request, 'app/checkout.html',{'add':add,'cart_items':cart_items,'totalamount':totalamount})

@login_required
def payment_done(request):
    user=request.user
    custid=request.GET.get('custid')
    customer=Customer.objects.get(id=custid)
    cart=Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
        c.delete()
    return redirect("orders")

@method_decorator(login_required,name="dispatch")
class ProfileView(View):
    def get(self,request):
        form=CustomerProfileForm()
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})

    def post(self,request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            usr=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            zipcode=form.cleaned_data['zipcode']
            state=form.cleaned_data['state']
            reg=Customer(user=usr,name=name,locality=locality,city=city,zipcode=zipcode,state=state)
            reg.save()
            messages.success(request,'Congratulations!! Your data is successfully updated')
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})