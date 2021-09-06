from django.http import JsonResponse


# JsonResponse 可以直接将字典返回成json串

def test_cors(request):
    return JsonResponse({'msg': 'CORS is ok'})
