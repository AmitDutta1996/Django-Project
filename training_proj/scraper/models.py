from django.db import models


# Create your models here.

class ScrapedData(models.Model):
    airline_name = models.CharField(max_length=100)
    biz_model = models.CharField(max_length=100)
    network = models.CharField(max_length=100)
    group = models.CharField(max_length=100)
    hub = models.CharField(max_length=100)
    territory = models.CharField(max_length=100)
    address = models.CharField(max_length=1000)
    iata_code = models.CharField(max_length=50)
    icao_code = models.CharField(max_length=50)
    about = models.CharField(max_length=10000)
    ranking = models.CharField(max_length=50)
    prevrank = models.CharField(max_length=50)
    ratingval = models.CharField(max_length=50)
    image_url = models.CharField(max_length=500,default='default.jpg')
    site_url = models.CharField(max_length=500,default='www.ibsplc.com')
    source_url=models.CharField(max_length=500,default='www.ibsplc.com')


class ScrapeLinks(models.Model):
    airline_name = models.CharField(max_length=100)
    link = models.CharField(max_length=1000)
    review_url = models.CharField(max_length=1000,default='https://www.airlinequality.com/review-pages/a-z-airline-reviews/')
    image_url = models.CharField(max_length=5000,default='default.jpg')


class ScrapedReviewData(models.Model):
    airline_name = models.CharField(max_length=100)
    polarity = models.CharField(max_length=100)
    subjectivity = models.CharField(max_length=100)
