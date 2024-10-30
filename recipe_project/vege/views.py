from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required


@login_required(login_url="login/")
def recipes(request):
    if request.method == 'POST':
        data=request.POST

        recipe_name = data.get('recipe_name')
        recipes_description = data.get('recipe_description')
        recipe_image=request.FILES.get('recipe_image')
        
        Recipe.objects.create(
            recipe_name=recipe_name,
            recipe_description=recipes_description,
            recipe_image=recipe_image,
        )
        return redirect('/recipe_table/')
    context={'page': 'recipes'}
    return render(request,'recipes.html',context)

# Create your views here.
@login_required(login_url="login/")
def recipe_table(request):
    #start of view data process 
    queryset=Recipe.objects.all() # added recipes to the queryset

    if request.GET.get('search'):
        queryset=queryset.filter(recipe_name__icontains=request.GET.get('search'))
        
    context={'receipes':queryset,'page': 'recipes_table'}

    return render(request, 'recipe_table.html',context)

@login_required(login_url="login/")
def delete_recipe(request,id):
    queryset=Recipe.objects.get(id=id)
    queryset.delete()
    return redirect('/')

@login_required(login_url="login/")
def update_recipe(request,id):
    queryset=Recipe.objects.get(id=id)
    if request.method == 'POST':
        data=request.POST

        recipe_name = data.get('recipe_name')
        recipes_description = data.get('recipe_description')
        recipe_image=request.FILES.get('recipe_image')

        queryset.recipe_name=recipe_name
        queryset.recipe_description=recipes_description

        if recipe_image:
            queryset.recipe_image=recipe_image

        queryset.save()

        return redirect('/')
    context={'receipe':queryset}
    return render(request,'update_recipe.html',context)

# authentication start
def login_page(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.info(request, 'invalid username !!!!!')
            return redirect('/login')
        
        user=authenticate(username=username,password=password)
        
        if user is None:
            messages.info(request, 'invalid password !!!!!')
            return redirect('/login')
        else:
            login(request,user)
            return redirect('/')
    return render(request,'login.html')


def logout_page(request):
    logout(request)
    return redirect('/login')
def register_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=User.objects.filter(username=username)

        if user.exists():
            messages.info(request, 'Username already taken')
            return redirect('/register')
        
        user=User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            # here we didn't added passsword bcoz we need to encrypt the password for sercurity purpose
            # for that reason we need to call methond on objects
        )
        user.set_password(password)
        user.save()
        messages.info(request,'Account created successfully')
        return redirect('/register')

    return render(request,'register.html')