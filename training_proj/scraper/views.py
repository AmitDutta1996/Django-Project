from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from .forms import ScrapeLinksForm as slf
from .models import ScrapedData, ScrapeLinks, ScrapedReviewData
from . import scraper_engine as se
from django.core import serializers
from django.http import JsonResponse
# Create your views here.

@login_required
@permission_required('scraper.change_scrapelinks')
def scraperlink(request):
    if request.method == 'POST':
        form = slf(request.POST)
        if form.is_valid():
            flag = False
            dbdata = ScrapeLinks.objects.all()
            name = form.cleaned_data.get('airline_name')
            link = form.cleaned_data.get('link')
            rew_url = form.cleaned_data.get('review_url')
            img_url = form.cleaned_data.get('image_url')
            for data in dbdata:
                if (data.airline_name == name) | (data.link == link) | (data.image_url == img_url):
                    data.delete()
                    data = ScrapeLinks(airline_name=name, link=link, review_url=rew_url, image_url=img_url)
                    data.save()
                    flag = True

            if not flag:
                form.save()

            messages.success(request, f'New Scrape Data Added for {name}!')
            se.scraper({name:link},img_url,rew_url)
            return redirect('scraperdata')
    else:
        form = slf()
    return render(request, 'scraper/scraper.html', {'form': form})


@login_required
@permission_required('scraper.change_scrapelinks')
def scraperdataview(request):
    data = ScrapedData.objects.all()
    return render(request, 'scraper/viewdata.html', {'data': data})


@login_required
def scraperdash(request):
    data = ScrapedData.objects.all()
    return render(request, 'scraper/dashboard.html', {'data': data})

@login_required
def reviewstats(request):
    return render(request, 'scraper/reviewstats.html', {})

@login_required
def pivot_data(request):
    dataset = ScrapedReviewData.objects.all()
    data = serializers.serialize('json', dataset)
    return JsonResponse(data, safe=False)