from django.contrib.auth.models import User
from factory import SubFactory, fuzzy
from factory.django import DjangoModelFactory

from wingtel.subscriptions import models


class UserFactory(DjangoModelFactory):
    username = fuzzy.FuzzyText()
    email = fuzzy.FuzzyText(suffix="@mail.ru")

    class Meta:
        model = User


class SubscriptionFactory(DjangoModelFactory):
    user = SubFactory(UserFactory)

    class Meta:
        model = models.Subscription
