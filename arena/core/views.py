from django.http import JsonResponse
from django.views import View


class JsonView(View):
    def get(self, request, *args, **kwargs):
        data = self.get_response_data()
        return JsonResponse(data)
