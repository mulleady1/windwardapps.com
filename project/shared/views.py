from django.views.generic.edit import FormView

from .http import JsonSuccessResponse, JsonErrorResponse

class AjaxFormView(FormView):
    def form_valid(self, form):
        return JsonSuccessResponse()

    def form_invalid(self, form):
        return JsonErrorResponse({ 'errors': form.errors })
