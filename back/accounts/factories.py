import factory
import factory.fuzzy as fuz

from accounts.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = fuz.FuzzyText(length=12, prefix="test user ")
