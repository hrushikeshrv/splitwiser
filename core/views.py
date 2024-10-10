from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, reverse
from django.views.generic import View, DetailView

from users.models import User
from core.models import TransactionGroup


class IndexView(View):
    def get(self, request):
        if request.user.is_authenticated:
            groups = request.user.transaction_groups.all()
            if len(groups) == 1:
                return HttpResponseRedirect(
                    reverse(
                        "core:transaction_group_detail", kwargs={"pk": groups[0].pk}
                    )
                )
        return render(request, "core/index.html")


class TransactionGroupDetailView(DetailView):
    model = TransactionGroup
    template_name = "core/transaction_group_detail.html"
    context_object_name = "transaction_group"


def test_view(request, *args, **kwargs):
    return HttpResponse("Hello World")
