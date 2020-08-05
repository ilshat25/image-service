from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import LocalUserEditForm

# Create your views here.
@login_required
def dashboard_view(request):
    return render(request, 'localuser/dashboard.html', 
                {
                    'section': 'dashboard',
                })

@login_required
def edit_view(request):
    user = request.user
    if request.method == 'POST':
        form = LocalUserEditForm(request.POST, files=request.FILES, instance=user)
        if form.is_valid():
            form.save()
    else:
        form = LocalUserEditForm(instance=user)
    return render(request, 'localuser/edit.html',
                {
                    'form': form,
                })