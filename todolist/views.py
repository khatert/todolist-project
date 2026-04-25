import json
from bson import ObjectId
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import get_collection


def index(request):
    return render(request, 'todos/home.html')


@csrf_exempt
def todos(request):
    col = get_collection('todos')

    if request.method == 'GET':
        docs = list(col.find())
        for d in docs:
            d['id'] = str(d['_id'])
            del d['_id']
        return JsonResponse({'data': docs})

    if request.method == 'POST':
        body = json.loads(request.body)
        doc = {
            'title':     body.get('title'),
            'completed': False,
        }
        result = col.insert_one(doc)
        doc['id'] = str(result.inserted_id)
        del doc['_id']
        return JsonResponse({'data': doc})


@csrf_exempt
def todo_detail(request, todo_id):
    col = get_collection('todos')
    oid = ObjectId(todo_id)

    if request.method == 'GET':
        doc = col.find_one({'_id': oid})
        if not doc:
            return JsonResponse({'error': 'Not found'}, status=404)
        doc['id'] = str(doc['_id'])
        del doc['_id']
        return JsonResponse({'data': doc})

    if request.method == 'PUT':
        body = json.loads(request.body)
        col.update_one({'_id': oid}, {'$set': {'title': body.get('title')}})
        doc = col.find_one({'_id': oid})
        doc['id'] = str(doc['_id'])
        del doc['_id']
        return JsonResponse({'data': doc})

    if request.method == 'DELETE':
        col.delete_one({'_id': oid})
        return JsonResponse({'message': 'Deleted'})
