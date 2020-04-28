from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from scraper.models import ScrapedData
from .df_response_lib import *
import json


# Create your views here.

@csrf_exempt
def webhook(request):
    # build a request object
    req = json.loads(request.body)
    print(req)
    print(type(req))
    # get action from json
    action = req.get('queryResult').get('action')
    print(action)
    if action == 'search':
        ful = fulfillment_response()
        dbdata = ScrapedData.objects.all()
        params = req.get('queryResult').get('parameters')
        queryparam = params.get('airline')
        for data in dbdata:
            if (data.airline_name.lower().find(queryparam.lower())) != -1:
                x = ful.fulfillment_text(data.about)
                ff_response = fulfillment_response()
                reply = ff_response.main_response(x, fulfillment_messages=None)
                return JsonResponse(reply, safe=False)

    elif action == 'get_biz':
        ful = fulfillment_response()
        dbdata = ScrapedData.objects.all()
        params = req.get('queryResult').get('parameters')
        queryparam = params.get('airline')
        for data in dbdata:
            if (data.airline_name.lower().find(queryparam.lower())) != -1:
                x = ful.fulfillment_text(data.biz_model)
                ff_response = fulfillment_response()
                reply = ff_response.main_response(x, fulfillment_messages=None)
                return JsonResponse(reply, safe=False)

    elif action == 'get_group':
        ful = fulfillment_response()
        dbdata = ScrapedData.objects.all()
        params = req.get('queryResult').get('parameters')
        queryparam = params.get('airline')
        for data in dbdata:
            if (data.airline_name.lower().find(queryparam.lower())) != -1:
                x = ful.fulfillment_text(data.group)
                ff_response = fulfillment_response()
                reply = ff_response.main_response(x, fulfillment_messages=None)
                return JsonResponse(reply, safe=False)

    elif action == 'get_network':
        ful = fulfillment_response()
        dbdata = ScrapedData.objects.all()
        params = req.get('queryResult').get('parameters')
        queryparam = params.get('airline')
        for data in dbdata:
            if (data.airline_name.lower().find(queryparam.lower())) != -1:
                x = ful.fulfillment_text(data.network)
                ff_response = fulfillment_response()
                reply = ff_response.main_response(x, fulfillment_messages=None)
                return JsonResponse(reply, safe=False)

    elif action == 'get_hub':
        ful = fulfillment_response()
        dbdata = ScrapedData.objects.all()
        params = req.get('queryResult').get('parameters')
        queryparam = params.get('airline')
        for data in dbdata:
            if (data.airline_name.lower().find(queryparam.lower())) != -1:
                x = ful.fulfillment_text(data.hub)
                ff_response = fulfillment_response()
                reply = ff_response.main_response(x, fulfillment_messages=None)
                return JsonResponse(reply, safe=False)

    elif action == 'get_territory':
        ful = fulfillment_response()
        dbdata = ScrapedData.objects.all()
        params = req.get('queryResult').get('parameters')
        queryparam = params.get('airline')
        for data in dbdata:
            if (data.airline_name.lower().find(queryparam.lower())) != -1:
                x = ful.fulfillment_text(data.territory)
                ff_response = fulfillment_response()
                reply = ff_response.main_response(x, fulfillment_messages=None)
                return JsonResponse(reply, safe=False)

    elif action == 'get_address':
        ful = fulfillment_response()
        dbdata = ScrapedData.objects.all()
        params = req.get('queryResult').get('parameters')
        queryparam = params.get('airline')
        for data in dbdata:
            if (data.airline_name.lower().find(queryparam.lower())) != -1:
                x = ful.fulfillment_text(data.address)
                ff_response = fulfillment_response()
                reply = ff_response.main_response(x, fulfillment_messages=None)
                return JsonResponse(reply, safe=False)

    elif action == 'get_iata':
        ful = fulfillment_response()
        dbdata = ScrapedData.objects.all()
        params = req.get('queryResult').get('parameters')
        queryparam = params.get('airline')
        for data in dbdata:
            if (data.airline_name.lower().find(queryparam.lower())) != -1:
                x = ful.fulfillment_text(data.iata_code)
                ff_response = fulfillment_response()
                reply = ff_response.main_response(x, fulfillment_messages=None)
                return JsonResponse(reply, safe=False)

    elif action == 'get_icao':
        ful = fulfillment_response()
        dbdata = ScrapedData.objects.all()
        params = req.get('queryResult').get('parameters')
        queryparam = params.get('airline')
        for data in dbdata:
            if (data.airline_name.lower().find(queryparam.lower())) != -1:
                x = ful.fulfillment_text(data.icao_code)
                ff_response = fulfillment_response()
                reply = ff_response.main_response(x, fulfillment_messages=None)
                return JsonResponse(reply, safe=False)

    elif action == 'get_ranking':
        ful = fulfillment_response()
        dbdata = ScrapedData.objects.all()
        params = req.get('queryResult').get('parameters')
        queryparam = params.get('airline')
        for data in dbdata:
            if (data.airline_name.lower().find(queryparam.lower())) != -1:
                x = ful.fulfillment_text(
                    'SKYTRAX 2019 ranking: ' + data.ranking + '/100\nSKYTRAX 2018 ranking: ' + data.prevrank + '/100')
                ff_response = fulfillment_response()
                reply = ff_response.main_response(x, fulfillment_messages=None)
                return JsonResponse(reply, safe=False)

    elif action == 'get_rating':
        ful = fulfillment_response()
        dbdata = ScrapedData.objects.all()
        params = req.get('queryResult').get('parameters')
        queryparam = params.get('airline')
        for data in dbdata:
            if (data.airline_name.lower().find(queryparam.lower())) != -1:
                x = ful.fulfillment_text('SKYTRAX rating: ' + data.ratingval + '/5 stars')
                ff_response = fulfillment_response()
                reply = ff_response.main_response(x, fulfillment_messages=None)
                return JsonResponse(reply, safe=False)
    else:
        fulfillmentText = {'fulfillmentText': 'no search parameters'}
        return JsonResponse(fulfillmentText, safe=False)
    fulfillmentText = {'fulfillmentText': 'no results'}
    x = JsonResponse(fulfillmentText, safe=False)
    print(x)
    return JsonResponse(fulfillmentText, safe=False)
