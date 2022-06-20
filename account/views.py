from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from account.forms import UserForm

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)
            return redirect('/')
    else:
        form = UserForm()
    return render(request, 'account/signup.html', {'form': form})
