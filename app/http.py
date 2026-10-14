from django.http import JsonResponse


class JsonSuccessResponse(JsonResponse):
    def __init__(self, data=None, **kwargs):
        super().__init__({**(data or {}), 'success': True}, **kwargs)


class JsonErrorResponse(JsonResponse):
    status_code = 400

    def __init__(self, data=None, **kwargs):
        super().__init__({**(data or {}), 'success': False}, **kwargs)
