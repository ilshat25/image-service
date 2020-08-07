from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.conf import settings

from image.models import Image
from .models import Contact
from .forms import LocalUserEditForm
from common.decorators import ajax_required
from action.utisl import create_action
from action.models import Action

import redis

r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)

@login_required
def dashboard_view(request):

    # Actions
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id', flat=True)
    if following_ids:
        actions = actions.filter(user__id__in=following_ids)
    actions = actions[:10]
    
    # Ranked images
    image_ranking = r.zrange('image_ranking', 0, -1, desc=True)[:5]
    image_ranking_ids = [int(id) for id in image_ranking]
    most_viewed = list(Image.objects.filter(
        id__in=image_ranking_ids
    ))
    most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))
    return render(request, 'localuser/dashboard.html', 
                {
                    'section': 'dashboard',
                    'most_viewed_images': most_viewed,
                    'actions': actions,
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
            
def people_view(request):
    people = get_user_model().objects.exclude(pk=request.user.pk)
    return render(request, 'localuser/people.html',
                  {
                      'section': 'people',
                      'users': people,
                  })

def user_detail_view(request, pk, username):
    user = get_object_or_404(get_user_model(),  
                            pk=pk, 
                            username=username)
    return render(request, 'localuser/user_detail.html', 
                 {
                     'section': 'people',
                     'user': user,
                 })

@require_POST
@ajax_required
@login_required
def follow_view(request):
    user_pk = request.POST.get('id')
    action = request.POST.get('action')
    if user_pk and action:
        try:
            print(action)
            user = get_user_model().objects.get(pk=user_pk)
            if action == 'follow':
                Contact.objects.create(user_from=request.user,
                                        user_to=user)
                create_action(request.user,'is following', user)
            else:
                Contact.objects.filter(user_from=request.user,
                                    user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except: pass
    return JsonResponse({'status': 'error'})
    