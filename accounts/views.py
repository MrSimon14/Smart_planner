from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

def register(request):
    #register a new user
    if request.method != 'POST':
        #show empty form
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            #login and go to main page
            login(request, new_user)
            return redirect('smart_planner:index')
        
    #empty or incorrect form
    context = {'form': form}
    return  render(request, 'registration/register.html', context)