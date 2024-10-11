from datetime import datetime

from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, reverse
from django.utils.timezone import now
from django.views.generic import View, DetailView, ListView

from users.models import User
from core.models import TransactionGroup, Transaction, TransactionShare


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
            return HttpResponseRedirect(reverse("core:transaction_group_list"))
        return render(request, "core/index.html")


class TransactionGroupListView(ListView):
    model = TransactionGroup
    template_name = "core/transaction_group_list.html"
    context_object_name = "transaction_groups"

    def get_queryset(self):
        return self.request.user.transaction_groups.all()


# A detail view for a transaction group is actually a list view for
# transactions in the transaction group
class TransactionGroupDetailView(UserPassesTestMixin, ListView):
    template_name = "core/transaction_group_detail.html"
    context_object_name = "transactions"
    paginate_by = 20

    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        return self.request.user.in_group(pk=int(self.kwargs["pk"]))

    def get_queryset(self):
        return (
            TransactionGroup.objects.get(pk=self.kwargs["pk"])
            .transactions.prefetch_related("shares", "group__users")
            .all()
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["transaction_group"] = TransactionGroup.objects.get(
            pk=self.kwargs["pk"]
        )
        return context


class TransactionCreateView(UserPassesTestMixin, View):
    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        return self.request.user.in_group(pk=int(self.kwargs["pk"]))

    def post(self, request, pk):
        transaction_name = request.POST.get('name')
        if not transaction_name:
            transaction_name = 'Shared Transaction'
        transaction_amount = int(request.POST.get('amount', 0)) * 100

        transaction = Transaction.objects.create(
            title=transaction_name,
            date=datetime.strptime(request.POST['date'], '%Y-%m-%dT%H:%M'),
            by=User.objects.get(username=request.POST.get('by')),
            group=TransactionGroup.objects.get(pk=pk),
            amount=transaction_amount,
        )
        shared_usernames = request.POST.getlist('for', [])
        amount_owed = transaction_amount / len(shared_usernames)
        for username in shared_usernames:
            amount_paid = 0
            if username == request.POST.get('by', ''):
                amount_paid = transaction_amount
            TransactionShare.objects.create(
                user=User.objects.get(username=username),
                transaction=transaction,
                amount_paid=amount_paid,
                amount_owed=amount_owed,
            )
        return HttpResponseRedirect(reverse('core:transaction_group_detail', kwargs={"pk": pk}))


class JoinTransactionGroupView(View):
    def get(self, request):
        return render(request, "core/transaction_group_join.html")


def test_view(request, *args, **kwargs):
    return HttpResponse("Hello World")
