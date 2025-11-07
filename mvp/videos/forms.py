from django import forms
from .models import Video

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'subject', 'thumbnail', 'thumbnail_url', 'video_file', 'video_url']
    
    def clean(self):
        cleaned_data = super().clean()
        video_file = cleaned_data.get('video_file')
        video_url = cleaned_data.get('video_url')
        thumb_file = cleaned_data.get('thumbnail')
        thumb_url = cleaned_data.get('thumbnail_url')

        if not thumb_file and not thumb_url:
            raise forms.ValidationError("Envie uma miniatura ou insira o link da miniatura.")

        if not video_file and not video_url:
            raise forms.ValidationError("Envie um vídeo ou insira o link do vídeo.")

        return cleaned_data
