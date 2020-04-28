from .models import ScrapedData, ScrapedReviewData
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uopen
from textblob import TextBlob
from requests import get
from contextlib import closing


class rank:
    def __init__(self, pos, airline, prev):
        self.position = pos
        self.airline = airline
        self.prevpos = prev


class rating:
    def __init__(self, airline, region, ratingval):
        self.airline = airline
        self.region = region
        self.rating = ratingval


class details:
    def __init__(self, airline, biz, network, group, hub, territory, address, iata, icao, about, url):
        self.airline = airline
        self.biz = biz
        self.network = network
        self.group = group
        self.hub = hub
        self.territory = territory
        self.address = address
        self.iata = iata
        self.icao = icao
        self.about = about
        self.url = url


class sentiment:
    def __init__(self, pol, sub):
        self.pol = pol
        self.sub = sub


def rankingscraper():
    scrap_url = 'https://www.worldairlineawards.com/worlds-top-100-airlines-2019/'
    client = uopen(scrap_url)
    page_html = client.read()
    client.close()
    page_soup = soup(page_html, 'html.parser')
    containers = page_soup.find_all('div', {'class': 'row mb-2 awards-list'})
    ranklist = []
    for container in containers:
        pos = container.div.div.h6.text
        name = container.h4.text
        prevpos = container.find('span', {'class': 'font-weight-bold'}).text
        rankval = rank(pos, name, prevpos)
        ranklist.append(rankval)

    return ranklist


def ratingscraper():
    scrap_url = 'https://skytraxratings.com/airlines?set_posts_per_page=50'
    client = uopen(scrap_url)
    page_html = client.read()
    client.close()
    page_soup = soup(page_html, 'html.parser')
    containers = page_soup.find_all('div', {'class': 'pageportal__content'})
    ratinglist = []
    for container in containers:
        name = container.h2.text
        reg = container.findAll('div', {'class': 'clearfix'})[1].text.strip()
        ratingval = str(5 - len(container.findAll('i', {'class': 'fa-star-o'})))
        rate = rating(name, reg, ratingval)
        ratinglist.append(rate)

    scrap_url = 'https://skytraxratings.com/airlines/page/2?set_posts_per_page=50'
    client = uopen(scrap_url)
    page_html = client.read()
    client.close()
    page_soup = soup(page_html, 'html.parser')
    containers = page_soup.find_all('div', {'class': 'pageportal__content'})
    for container in containers:
        name = container.h2.text
        reg = container.findAll('div', {'class': 'clearfix'})[1].text.strip()
        ratingval = str(5 - len(container.findAll('i', {'class': 'fa-star-o'})))
        rate = rating(name, reg, ratingval)
        ratinglist.append(rate)

    scrap_url = 'https://skytraxratings.com/airlines/page/3?set_posts_per_page=50'
    client = uopen(scrap_url)
    page_html = client.read()
    client.close()
    page_soup = soup(page_html, 'html.parser')
    containers = page_soup.find_all('div', {'class': 'pageportal__content'})
    for container in containers:
        name = container.h2.text
        reg = container.findAll('div', {'class': 'clearfix'})[1].text.strip()
        ratingval = str(5 - len(container.findAll('i', {'class': 'fa-star-o'})))
        rate = rating(name, reg, ratingval)
        ratinglist.append(rate)
    return ratinglist


def detailscraper(url):
    scrap_url = url
    client = uopen(scrap_url)
    page_html = client.read()
    client.close()
    page_soup = soup(page_html, 'html.parser')
    container = page_soup.find_all('div', {'class': 'about_title_1m1'})
    airline = container[0].h1.text
    container = page_soup.find_all('div', {'class': 'about_bizmodel_xTg'})
    biz = container[0].text
    container = page_soup.find_all('div', {'class': 'about_network_1dQ'})
    network = container[0].text
    container = page_soup.find_all('div', {'class': 'about_group_Vsc'})
    group = container[0].a.text
    container = page_soup.find_all('div', {'class': 'about_box_2_w'})
    iata = container[1].text.split(': ')[1]
    icao = container[2].text.split(': ')[1]
    hub = container[3].text.split(': ')[1]
    terrirory = container[4].text.split(': ')[1]
    site_url = str(container[5].a).split(' ')[2].split('"')[1]
    if (len(container) < 9):
        address = container[6].text.split(': ')[1]
        about = container[7].p.text.strip()
    else:
        address = container[7].text.split(': ')[1]
        about = container[8].p.text.strip()

    detail = details(airline, biz, network, group, hub, terrirory, address, iata, icao, about, site_url)
    return detail


def reviewAnalyzer(url):
    scrap_url = url
    with closing(get(scrap_url, stream=True)) as resp:
        page_html = resp.content
    page_soup = soup(page_html, 'html.parser')
    containers = page_soup.find_all('div', {'class': 'text_content'})
    returnlist = []
    for container in containers:
        if len(container.text.split('|')) > 1:
            x = container.text.split('|')[1].strip()
        else:
            x = container.text.split('|')[0].strip()
        blob = TextBlob(x)
        item = sentiment(blob.polarity,blob.subjectivity)
        returnlist.append(item)
    return returnlist


def removeReviewScrape(airline):
    ScrapedReviewData.objects.filter(airline_name__iexact=airline).delete()


def scraper(links,image_url,review_url):

    print('scraping top 100 airline ranking')
    rankinglist = rankingscraper()
    print('scraping airline rating')
    ratinglist = ratingscraper()
    results = []
    for key in links.keys():
        print('scraping details of ' + key)
        details = detailscraper(links[key])
        rank = ''
        prevrankval = ''
        ratingval = ''
        for r in rankinglist:
            if getattr(r, 'airline').find(key) > -1:
                rank = getattr(r, 'position')
                prevrankval = getattr(r, 'prevpos')
        for r in ratinglist:
            if getattr(r, 'airline').find(key) > -1:
                ratingval = getattr(r, 'rating')

        data = ScrapedData(airline_name=getattr(details, 'airline'), biz_model=getattr(details, 'biz'),
                           network=getattr(details, 'network'),
                           group=getattr(details, 'group'),
                           hub=getattr(details, 'hub'), territory=getattr(details, 'territory'),
                           address=getattr(details, 'address'),
                           iata_code=getattr(details, 'iata'),
                           icao_code=getattr(details, 'icao'), about=getattr(details, 'about'), ranking=rank,
                           prevrank=prevrankval,
                           ratingval=ratingval, image_url=image_url, site_url=getattr(details, 'url'),source_url=links[key])
        results.append(data)

    for r in results:
        dbdata = ScrapedData.objects.all()
        save = False
        for item in dbdata:
            if item.airline_name == r.airline_name:
                item.biz_model=r.biz_model
                item.network=r.network
                item.group=r.group
                item.hub=r.hub
                item.territory=r.territory
                item.address=r.address
                item.iata_code=r.iata_code
                item.icao_code=r.icao_code
                item.about=r.about
                item.ranking=r.ranking
                item.prevrank=r.prevrank
                item.image_url=r.image_url
                item.site_url=r.site_url
                item.source_url=r.source_url
                item.save()
                print(item.airline_name + ' updated')
                print('Fetching reviews of ' + item.airline_name)
                sentiments = reviewAnalyzer(review_url)
                removeReviewScrape(item.airline_name)
                for x in sentiments:
                    y = ScrapedReviewData(airline_name=item.airline_name, polarity=str(x.pol), subjectivity=str(x.sub))
                    y.save()
                save = True
                break

        if not save:
            r.save()
            print(r.airline_name + ' saved')
            print('Fetching reviews of ' + r.airline_name)
            sentiments = reviewAnalyzer(review_url)
            removeReviewScrape(r.airline_name)
            for x in sentiments:
                y = ScrapedReviewData(airline_name=r.airline_name, polarity=str(x.pol), subjectivity=str(x.sub))
                y.save()
