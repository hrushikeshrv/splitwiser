from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View


class IndexView(View):
    def get(self, request):
        if request.user.is_authenticated:
            pass
        return render(request, 'core/index.html')


def test_view(request, *args, **kwargs):
    return HttpResponse("Hello World")
