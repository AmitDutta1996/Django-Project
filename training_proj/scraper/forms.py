from django.forms import ModelForm
from .models import ScrapeLinks


class ScrapeLinksForm(ModelForm):
    class Meta:
        model = ScrapeLinks
        fields = ['airline_name', 'link', 'review_url', 'image_url']
