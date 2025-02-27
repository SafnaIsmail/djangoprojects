from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from shop.models import Category, Product

# Create your views here.
def allcategories(request):
    c = Category.objects.all()
    return render(request, 'category.html', {'c': c})

def allproducts(request, p):
    c = Category.objects.get(name=p)
    p = Product.objects.filter(category=c)
    return render(request, 'product.html', {'c': c, 'p': p})


def detail(request, p):
    product = Product.objects.get(name=p)
    return render(request, 'detail.html', {'p': product})


def user_login(request):
    if(request.method == 'POST'):
        name = request.POST['u']
        pas = request.POST['p']
        user = authenticate(username=name, password=pas)
        if user:
            login(request, user)
            return redirect('shop:allcat')
        else:
            messages.error(request, "Invalid credentails")
    return render(request, "login.html");

def register(request):
    if(request.method =='POST'):
        u = request.POST['u']
        p = request.POST['p']
        cp = request.POST['cp']
        e = request.POST['e']
        if(p==cp):
            u = User.objects.create_user(username=u, password=p, email=e,)
            u.save()
            return redirect('shop:allcat')
        else:
            return HttpResponse("Password not matching")
    return render(request, "register.html");

@login_required
def user_logout(request):
    logout(request)
    return user_login(request)
    return render(request, "login.html");
