from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from cc.forms import UserForm
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages



# Create your views here.
def index(request):
    return render(request,'cc/index.html')

def register(request):

    registered = False
    prereg = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST )


        # Check to see both forms are valid
        if user_form.is_valid():
            user = user_form.save(commit=False)

            if User.objects.filter(email=user.email).exists():
                prereg = True
                print('Already Exists!!')
            else:
                # Save User Form to Database
                user = user_form.save()

                # Hash the password
                user.set_password(user.password)
                user.username = user.email

                # Update with Hashed password
                user.save()


                # Registration Successful!
                registered = True



        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    if registered== True:

        return render(request,'cc/register.html',
                          {'user_form':user_form,
                           'registered':registered,
                           'username':user.username,
                           })
    else:
        return render(request,'cc/register.html',
                          {'user_form':user_form,
                           'registered':registered,
                           
                           })

def user_login(request):

    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request,user)
                # Send the user back to some page.
                # In this case their homepage.
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            messages.error(request,'Invalid login details supplied. Please try again')

    else:
        #Nothing has been provided for username or password.
        return HttpResponseRedirect(reverse('index'))
    return HttpResponseRedirect(reverse('index'))


@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return HttpResponseRedirect(reverse('index'))