from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Video, VideoReaction
from .forms import VideoForm


# ✅ Agora apenas usuários logados podem ver a home
@login_required
def home(request):
    videos = Video.objects.all().order_by('-created_at')
    return render(request, 'videos/home.html', {'videos': videos})


# ✅ Protege também a página de detalhes
@login_required
def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    video.views += 1
    video.save(update_fields=['views'])

    # Verifica se o usuário já reagiu
    user_reaction = VideoReaction.objects.filter(user=request.user, video=video).first()

    return render(request, 'videos/video_detail.html', {
        'video': video,
        'user_reaction': user_reaction.reaction if user_reaction else None
    })


@login_required
def like_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    reaction, created = VideoReaction.objects.get_or_create(user=request.user, video=video)

    if not created and reaction.reaction == 'like':
        reaction.delete()
        video.likes -= 1
    else:
        if reaction.reaction == 'dislike':
            video.dislikes -= 1
        reaction.reaction = 'like'
        reaction.save()
        video.likes += 1

    video.save(update_fields=['likes', 'dislikes'])
    return JsonResponse({'likes': video.likes, 'dislikes': video.dislikes})


@login_required
def dislike_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    reaction, created = VideoReaction.objects.get_or_create(user=request.user, video=video)

    if not created and reaction.reaction == 'dislike':
        reaction.delete()
        video.dislikes -= 1
    else:
        if reaction.reaction == 'like':
            video.likes -= 1
        reaction.reaction = 'dislike'
        reaction.save()
        video.dislikes += 1

    video.save(update_fields=['likes', 'dislikes'])
    return JsonResponse({'likes': video.likes, 'dislikes': video.dislikes})


@login_required
def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.uploaded_by = request.user
            video.save()
            return redirect('home')
    else:
        form = VideoForm()
    return render(request, 'videos/upload.html', {'form': form})
