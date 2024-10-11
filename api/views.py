from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import TransactionGroup, Transaction, TransactionShare


class GroupPaymentSummary(APIView):
    """
    Returns how much each user has paid and owes in a transaction group
    """
    def get(self, request, pk):
        if not request.user.is_authenticated:
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)
        if not request.user.transaction_groups.filter(pk=self.kwargs['pk']).exists():
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)
        transaction_group = TransactionGroup.objects.prefetch_related('transactions', 'transactions__shares', 'users').get(pk=self.kwargs['pk'])
        data = {
            'unknown_user': {
                'amount_paid': 0,
                'amount_owed': 0,
                'n_transactions': 0
            }
        }
        for user in transaction_group.users.all():
            data[user.username] = {
                'amount_paid': 0,
                'amount_owed': 0,
                'n_transactions': 0
            }
        for transaction in transaction_group.transactions.all():
            for share in transaction.shares.all():
                username = share.user.username
                if share.user.username not in data:
                    username = 'unknown_user'
                data[username]['amount_paid'] += share.amount_paid
                data[username]['amount_owed'] += share.amount_owed
                data[username]['n_transactions'] += 1
        return Response(data, status=status.HTTP_200_OK)


class TestView(APIView):
    pass
