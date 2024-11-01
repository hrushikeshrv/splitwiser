from datetime import datetime

from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, reverse
from django.utils.timezone import now
from django.views.generic import View, DetailView, ListView, CreateView

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


class TransactionGroupCreateView(LoginRequiredMixin, View):
    def post(self, request):
        name = request.POST.get("name", "Shared Group")
        currency = request.POST.get("currency", "$")
        group = TransactionGroup.objects.create(name=name, currency=currency)
        group.users.add(request.user)
        # TODO: Generate a code for the group
        return HttpResponseRedirect(
            reverse("core:transaction_group_detail", kwargs={"pk": group.pk})
        )


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
        is_internal_payment = request.POST.get("internal-payment", "false") == "true"
        transaction_amount = int(request.POST.get("amount", 0)) * 100
        transaction_date = datetime.strptime(request.POST["date"], "%Y-%m-%dT%H:%M")
        transaction_group = TransactionGroup.objects.get(pk=pk)
        try:
            transaction_by = User.objects.get(username=request.POST.get("by"))
        except User.DoesNotExist:
            return HttpResponseRedirect(
                reverse("core:transaction_group_detail", kwargs={"pk": pk})
            )

        if is_internal_payment:
            transaction_name = "Internal Payment"
        else:
            transaction_name = request.POST.get("name")
            if not transaction_name:
                transaction_name = "Shared Transaction"

        transaction = Transaction.objects.create(
            title=transaction_name,
            date=transaction_date,
            by=transaction_by,
            group=transaction_group,
            amount=transaction_amount,
            is_internal_payment=is_internal_payment,
        )

        if is_internal_payment:
            try:
                transaction_for = User.objects.get(username=request.POST.get("for"))
            except User.DoesNotExist:
                transaction.delete()
                return HttpResponseRedirect(
                    reverse("core:transaction_group_detail", kwargs={"pk": pk})
                )
            TransactionShare.objects.create(
                user=transaction_by,
                transaction=transaction,
                amount_paid=transaction_amount,
                amount_owed=0,
            )
            TransactionShare.objects.create(
                user=transaction_for,
                transaction=transaction,
                amount_paid=0,
                amount_owed=transaction_amount,
            )
        else:
            shared_usernames = request.POST.getlist("for", [])
            amount_owed = transaction_amount / len(shared_usernames)
            for username in shared_usernames:
                amount_paid = 0
                if username == request.POST.get("by", ""):
                    amount_paid = transaction_amount
                TransactionShare.objects.create(
                    user=User.objects.get(username=username),
                    transaction=transaction,
                    amount_paid=amount_paid,
                    amount_owed=amount_owed,
                )
        return HttpResponseRedirect(
            reverse("core:transaction_group_detail", kwargs={"pk": pk})
        )


class JoinTransactionGroupView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "core/transaction_group_join.html")

    def post(self, request):
        code = request.POST.get("code")
        try:
            group = TransactionGroup.objects.get(code=code)
            group.users.add(request.user)
            group.save()
            return HttpResponseRedirect(
                reverse("core:transaction_group_detail", kwargs={"pk": group.pk})
            )
        except TransactionGroup.DoesNotExist:
            return render(
                request,
                "core/transaction_group_join.html",
                {"error": "Invalid group code"},
            )
        except Exception as e:
            return render(
                request,
                "core/transaction_group_join.html",
                {"error": "An error occurred while joining the group"},
            )


def test_view(request, *args, **kwargs):
    return HttpResponse("Hello World")
