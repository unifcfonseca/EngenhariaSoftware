from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Video
from .forms import VideoForm

def home(request):
    videos = Video.objects.all().order_by('-created_at')
    return render(request, 'videos/home.html', {'videos': videos})

@login_required
def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST)
        if form.is_valid():
            video = form.save(commit=False)
            video.uploaded_by = request.user
            video.save()
            return redirect('home')
    else:
        form = VideoForm()
    return render(request, 'videos/upload.html', {'form': form})
