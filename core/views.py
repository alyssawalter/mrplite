from django.shortcuts import render


def homepage(request):
    return render(request, 'core/homepage.html')


# when user signs in, they are redirected here
def dashboard(request):
    return render(request, "core/dashboard.html")
