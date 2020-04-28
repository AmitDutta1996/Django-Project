# Generated by Django 3.0.4 on 2020-04-10 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0008_auto_20200401_2311'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScrapedReviewData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('airline_name', models.CharField(max_length=100)),
                ('polarity', models.CharField(max_length=100)),
                ('subjectivity', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='scrapelinks',
            name='review_url',
            field=models.CharField(default='https://www.airlinequality.com/review-pages/a-z-airline-reviews/', max_length=1000),
        ),
    ]