from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from .models import Image
from .forms import ImageForm

@login_required
def detail_view(request, pk, slug):
    image = get_object_or_404(Image, pk=pk, slug=slug)
    return render(request, 'image/detail.html',
                  {
                      'image': image,
                  })


@login_required
def add_view(request):
    if request.method == 'POST':
        form = ImageForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.publisher = request.user
            instance.save()

            return redirect(instance)
    else:
        form = ImageForm(request.GET)
    return render(request, 'image/add.html',
                  {
                      'form': form,
                  })

def all_view(request):
    images = Image.objects.all()
    return render(request, 'image/all.html',
                  {
                      'section': 'images',
                      'images': images,
                  })