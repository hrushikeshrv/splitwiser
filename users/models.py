from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """ """

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, unique=True, blank=True, null=True)

    def in_group(self, pk: int) -> bool:
        """
        Returns true if user is in group with the passed pk
        """
        return self.transaction_groups.filter(pk=pk).exists()
