from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import get_object_or_404

import json

from .models import Item

from .serializers import ItemSerializer
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse


# List and Create

@csrf_exempt

def item_list(request):

    if request.method == 'GET':

        items = Item.objects.all()   #taking all data from Item Table

        serializer = ItemSerializer(items, many=True)   # converting Table data----> Python Data
        Json_data= JSONRenderer().render(serializer.data)

        return HttpResponse(Json_data, content_type='application/json')  


    elif request.method == 'POST':

        data = json.loads(request.body)

        serializer = ItemSerializer(data=data)

        if serializer.is_valid():

            serializer.save()
            res={'msg':'data created successfully'}
            json_data=JSONRenderer().render(res)

            return HttpResponse(json_data, content_type='application/json')

        json_data=JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data, content_type='application/json')


# Retrieve, Update, and Delete

@csrf_exempt

def item_detail(request, pk):

    item = get_object_or_404(Item, pk=pk)


    if request.method == 'GET':

        serializer = ItemSerializer(item)

        Json_data= JSONRenderer().render(serializer.data)

        return HttpResponse(Json_data, content_type='application/json')  


    elif request.method == 'PUT':

        data = json.loads(request.body)

        serializer = ItemSerializer(item, data=data)

        if serializer.is_valid():

            serializer.save()

            res={'msg':'data created successfully'}
            json_data=JSONRenderer().render(res)

            return HttpResponse(json_data, content_type='application/json')

        json_data=JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data, content_type='application/json')


    elif request.method == 'DELETE':

        item.delete()

        return JsonResponse({'message': 'Item deleted'}, status=204)