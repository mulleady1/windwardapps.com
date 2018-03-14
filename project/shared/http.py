from django.http import JsonResponse

class JsonSuccessResponse(JsonResponse):
    def __init__(self, data={}, **kwargs):
        data['success'] = True
        super(JsonSuccessResponse, self).__init__(data, **kwargs)

class JsonErrorResponse(JsonResponse):
    status_code = 400
    def __init__(self, data={}, **kwargs):
        data['success'] = False
        super(JsonErrorResponse, self).__init__(data, **kwargs)
