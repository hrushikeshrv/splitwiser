from django.db import models
from django.utils.timezone import now

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
    class Meta:
        ordering = ("-date",)

    title = models.CharField(max_length=64, default="Shared Transaction")
    date = models.DateTimeField(default=now)
    by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    group = models.ForeignKey(
        TransactionGroup, on_delete=models.CASCADE, related_name="transactions"
    )
    is_internal_payment = models.BooleanField(default=False)

    # The total amount of the transaction. Each user that this transaction was
    # added for could have a different share, which is recorded in the associated
    # TransactionShare instance.
    amount = models.IntegerField()

    def __str__(self):
        return self.title

    def get_share_count(self) -> int:
        """Return the number of people this transaction was shared with"""
        return self.shares.count()

    def get_amount(self) -> str:
        """
        Returns the string representation of the amount by simply dividing the amount
        by 100
        """
        return str(self.amount / 100)


class TransactionShare(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    transaction = models.ForeignKey(
        Transaction, on_delete=models.CASCADE, related_name="shares"
    )
    # The amount the user paid for the transaction
    amount_paid = models.IntegerField()
    # The amount the user owed for their own share of the
    # transaction. This means that the user should get back
    # amount_paid - amount_owed from the group.
    amount_owed = models.IntegerField()

    def __str__(self):
        if self.user:
            return f"{self.user.username} paid {self.amount_paid} for {self.transaction.title} and owed {self.amount_owed}"
        return f"[deleted user] paid {self.amount_paid} for {self.transaction.title} and owed {self.amount_owed}"

    def get_amount_paid(self) -> str:
        """
        Returns the string representation of the amount by simply dividing the amount
        paid by 100
        """
        return str(self.amount_paid / 100)

    def get_amount_owed(self) -> str:
        """
        Returns the string representation of the amount by simply dividing the amount
        owed by 100
        """
        return str(self.amount_owed / 100)
