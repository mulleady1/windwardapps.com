from django.http import JsonResponse
from django.views.generic.edit import FormView

class JsonSuccessResponse(JsonResponse):
    def __init__(self, data={}, **kwargs):
        data['success'] = True
        super(JsonSuccessResponse, self).__init__(data, **kwargs)

class JsonErrorResponse(JsonResponse):
    status_code = 400
    def __init__(self, data={}, **kwargs):
        data['success'] = False
        super(JsonErrorResponse, self).__init__(data, **kwargs)

class AjaxFormView(FormView):
    def form_valid(self, form):
        return JsonSuccessResponse()

    def form_invalid(self, form):
        return JsonErrorResponse({ 'errors': form.errors })
