from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Video
from .forms import VideoForm


def home(request):
    """Página inicial que lista todas as aulas."""
    videos = Video.objects.all().order_by('-created_at')
    return render(request, 'videos/home.html', {'videos': videos})


def video_detail(request, video_id):
    """Exibe os detalhes de uma aula específica."""
    video = get_object_or_404(Video, id=video_id)
    # Incrementa contador de visualizações
    video.views += 1
    video.save(update_fields=['views'])
    return render(request, 'videos/video_detail.html', {'video': video})


@login_required
def upload_video(request):
    """Permite o upload de uma nova aula."""
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
