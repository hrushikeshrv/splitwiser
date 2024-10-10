from django.db import models

from users.models import User


class TransactionGroup(models.Model):
    name = models.CharField(max_length=48)
    users = models.ManyToManyField(User, related_name="transaction_groups")
    currency = models.CharField(max_length=4, default="$")
    # The joining code for the group
    code = models.CharField(max_length=7, unique=True)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    group = models.ForeignKey(
        TransactionGroup, on_delete=models.CASCADE, related_name="transactions"
    )

    # The total amount of the transaction. Each user that this transaction was
    # added for could have a different share, which is recorded in the associated
    # TransactionShare instance.
    amount = models.IntegerField()

    def __str__(self):
        if self.by:
            return f"Transaction by {self.by} for Group {self.group.name}"


class TransactionShare(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    transaction = models.ForeignKey(
        Transaction, on_delete=models.CASCADE, related_name="shares"
    )
    amount = models.IntegerField()
