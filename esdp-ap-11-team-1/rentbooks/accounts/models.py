from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    age = models.PositiveIntegerField(verbose_name="Возраст")

    REQUIRED_FIELDS = ["phone", "age"]

    email = models.EmailField(blank=True, verbose_name="Email")
    first_name = models.CharField(max_length=30, blank=True, verbose_name="Имя")
    last_name = models.CharField(max_length=30, blank=True, verbose_name="Фамилия")
    gender = models.CharField(max_length=10, blank=True, verbose_name="Пол")
    education = models.CharField(max_length=100, blank=True, verbose_name="Образование")
    city = models.CharField(max_length=50, blank=True, verbose_name="Город")
    address = models.TextField(blank=True, verbose_name="Адрес")
    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True,
        verbose_name="Аватар",
    )

    def __str__(self):
        return self.username


class Estimation(models.Model):
    owner = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    put_ratio = models.ManyToManyField(
        to=get_user_model(),
        related_name="has_estimation",
        through="UsersEstimates",
        verbose_name="Estimator_ratio",
    )
    aver_ratio = models.DecimalField(
        max_digits=7, decimal_places=2, default=0.00, verbose_name="Общая оценка"
    )


class UsersEstimates(models.Model):
    estimator = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    estimation = models.ForeignKey(Estimation, on_delete=models.CASCADE, default=0)
    ratio = models.PositiveIntegerField(default=0, verbose_name="Оценка пользователя")


class TelegramUser(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, null=False)
    id_telegram = models.IntegerField(null=False)
    confirm = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.user.id} {self.confirm}"


class CompositionTest(models.Model):
    name = models.CharField(max_length=20)
    author = models.CharField(max_length=20)
    description = models.CharField(max_length=20)
    rent_qte = models.IntegerField()
    language = models.CharField(max_length=20)
    id_genre = models.CharField(max_length=20)
    is_visible = models.CharField(max_length=20)
