from django.db import models


class FavoriteBook(models.Model):
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE
    )

    composition_id = models.BigIntegerField(
        null=False,
        blank=False,
        default=0
    )