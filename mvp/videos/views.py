from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models import Sum, Count, Q
from django.core.paginator import Paginator
from .models import Video, VideoReaction
from .forms import VideoForm


@login_required
def home(request):
    """Home com busca, filtros, ordenação e paginação."""
    videos = Video.objects.all()

    # --- BUSCA ---
    query = request.GET.get('q')
    if query:
        videos = videos.filter(
            Q(title__icontains=query) |
            Q(subject__icontains=query) |
            Q(description__icontains=query) |
            Q(uploaded_by__username__icontains=query) |
            Q(uploaded_by__email__icontains=query)
        )

    # --- FILTROS ---
    selected_filter = request.GET.get('filter')
    if selected_filter:
        videos = videos.filter(
            Q(subject__icontains=selected_filter) |
            Q(uploaded_by__username__icontains=selected_filter) |
            Q(uploaded_by__email__icontains=selected_filter)
        )

    # --- UNIVERSIDADE via domínio do e-mail ---
    for v in videos:
        if v.uploaded_by.email:
            domain = v.uploaded_by.email.split('@')[-1]
            domain = domain.replace('.edu.br', '').replace('.edu', '')
            v.university = domain.upper()
        else:
            v.university = "N/A"

    # --- ORDENAÇÃO ---
    sort_option = request.GET.get('sort', 'date')
    if sort_option == 'title':
        videos = videos.order_by('title')
    elif sort_option == 'views':
        videos = videos.order_by('-views')
    elif sort_option == 'likes':
        videos = videos.order_by('-likes')
    else:
        videos = videos.order_by('-created_at')

    # --- PAGINAÇÃO ---
    paginator = Paginator(videos, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # --- DADOS PARA OS SELECTS ---
    subjects = Video.objects.values_list('subject', flat=True).distinct()
    professors = Video.objects.values_list('uploaded_by__username', flat=True).distinct()
    universities = set([
        u.uploaded_by.email.split('@')[-1].replace('.edu.br', '').replace('.edu', '').upper()
        for u in Video.objects.exclude(uploaded_by__email__isnull=True)
    ])

    context = {
        'videos': page_obj,
        'page_obj': page_obj,
        'query': query or "",
        'selected_filter': selected_filter or "",
        'sort_option': sort_option,
        'subjects': subjects,
        'professors': professors,
        'universities': sorted(universities),
    }

    return render(request, 'videos/home.html', context)


# --- RESTANTE DO CÓDIGO EXISTENTE ---
@login_required
def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    video.views += 1
    video.save(update_fields=['views'])
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
    edit_id = request.GET.get("edit")
    if edit_id:
        video = get_object_or_404(Video, id=edit_id, uploaded_by=request.user)
        if request.method == "POST":
            form = VideoForm(request.POST, request.FILES, instance=video)
            if form.is_valid():
                form.save()
                return redirect("my_videos")
        else:
            form = VideoForm(instance=video)
        return render(request, "videos/upload.html", {
            "form": form,
            "is_edit": True,
            "video": video,
        })
    if request.method == "POST":
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.uploaded_by = request.user
            video.save()
            return redirect("my_videos")
    else:
        form = VideoForm()
    return render(request, "videos/upload.html", {"form": form, "is_edit": False})


@login_required
def my_videos(request):
    if request.user.user_type != 'professor':
        return render(request, 'videos/erro_acesso.html', {'mensagem': 'Apenas professores podem acessar esta página.'})
    videos = Video.objects.filter(uploaded_by=request.user).order_by('-created_at')
    return render(request, 'videos/my_videos.html', {'videos': videos})


@login_required
def delete_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    if video.uploaded_by != request.user:
        return HttpResponseForbidden("Você não tem permissão para excluir este vídeo.")
    if request.method in ["DELETE", "POST"]:
        video.delete()
        return JsonResponse({"success": True, "message": "Vídeo excluído com sucesso!"})
    return JsonResponse({"success": False, "message": "Método inválido."}, status=400)


@login_required
def stats_view(request):
    if request.user.user_type != 'professor':
        return render(request, 'videos/erro_acesso.html', {'mensagem': 'Apenas professores podem acessar esta página.'})
    videos = Video.objects.filter(uploaded_by=request.user)
    total_videos = videos.count()
    total_views = videos.aggregate(Sum('views'))['views__sum'] or 0
    total_likes = videos.aggregate(Sum('likes'))['likes__sum'] or 0
    total_dislikes = videos.aggregate(Sum('dislikes'))['dislikes__sum'] or 0
    top_videos = videos.order_by('-views')[:5]
    context = {
        'total_videos': total_videos,
        'total_views': total_views,
        'total_likes': total_likes,
        'total_dislikes': total_dislikes,
        'top_videos': top_videos,
    }
    return render(request, 'videos/stats.html', context)


@login_required
def video_stats(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    if video.uploaded_by != request.user:
        return HttpResponseForbidden("Você não tem permissão para visualizar as estatísticas deste vídeo.")
    total_views = video.views
    likes = video.likes
    dislikes = video.dislikes
    total_reactions = likes + dislikes
    engagement_rate = (total_reactions / total_views * 100) if total_views > 0 else 0
    like_ratio = (likes / total_reactions * 100) if total_reactions > 0 else 0
    context = {
        'video': video,
        'views': total_views,
        'likes': likes,
        'dislikes': dislikes,
        'engagement_rate': round(engagement_rate, 1),
        'like_ratio': round(like_ratio, 1),
    }
    return render(request, 'videos/video_stats.html', context)
