from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.conf import settings

from .models import Image
from .forms import ImageForm
from common.decorators import ajax_required
from action.utisl import create_action

import redis

r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)

@ajax_required
@require_POST
@login_required
def like_view(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
                create_action(request.user, 'liked image', image)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'error'})


def detail_view(request, pk, slug):
    image = get_object_or_404(Image, pk=pk, slug=slug)
    total_views = r.incr(f'image:{image.id}:views')
    r.zincrby('image_ranking', 1, image.id)
    return render(request, 'image/detail.html',
                  {
                      'section': 'images',
                      'image': image,
                      'total_views': total_views,
                  })


@login_required
def add_view(request):
    if request.method == 'POST':
        form = ImageForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.publisher = request.user
            instance.save()

            create_action(request.user, 'bookmarked image', instance)

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