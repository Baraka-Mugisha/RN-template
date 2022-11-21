from rest_framework import mixins, viewsets
from rest_framework.generics import CreateAPIView

from home.api.v1.users.models import User
from home.api.v1.users.serializers import SignupSerializer, VerifyPhoneNumberSerializer, UserViewSetSerializer


class SignupView(CreateAPIView):
    serializer_class = SignupSerializer


class VerifyPhoneNumber(CreateAPIView):
    serializer_class = VerifyPhoneNumberSerializer


class UserViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = UserViewSetSerializer
    lookup_field = "phone_number"
    lookup_url_kwarg = "phone_number"

    def get_queryset(self):
        # Filtering users will happen here
        return User.objects.filter(is_active=True)

    def perform_destroy(self, instance: User):
        instance.is_active = False
        instance.save()
