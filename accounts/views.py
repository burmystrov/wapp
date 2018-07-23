# encoding: utf-8
from __future__ import unicode_literals

from django.contrib.auth import user_logged_in
from django.utils.translation import ugettext_lazy as _
from rest_auth.serializers import PasswordResetSerializer
from rest_framework import mixins, parsers, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from common.aggregates import Age
from common.permissions import UserObjectPermission
from common.utils import to_int
from geo_info.models import City

from .filters import UserFilter
from .models import Profile, User
from .serializers import (OAuthConnectSerializer, ProfileSerializer,
                          SignUpSerializer, UserSerializer)


class ListOnlyAdminMixin(object):
    def get_queryset(self):
        user = self.request.user
        assert hasattr(self, 'QS_FILTER_FIELD') and hasattr(self, 'manager')
        qs = (self.manager.all() if user.is_superuser else
              self.manager.filter(**{self.QS_FILTER_FIELD: user.id}))
        return qs.select_related()


class UserView(ListOnlyAdminMixin, ReadOnlyModelViewSet):
    #: Filters by `id` field using authorized user's id as value for it
    QS_FILTER_FIELD = 'id'
    manager = User.objects

    serializer_class = UserSerializer
    filter_class = UserFilter
    permission_classes = (IsAuthenticated,)


class ProfileView(ListOnlyAdminMixin, mixins.UpdateModelMixin,
                  ReadOnlyModelViewSet):
    #: Filters by `user_id` field using authorized user's id as value for it
    QS_FILTER_FIELD = 'user_id'
    manager = Profile.objects

    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated, UserObjectPermission)

    def get_queryset(self):
        qs = super(ProfileView, self).get_queryset()

        sex = self.request.query_params.get('sex')
        if sex:
            sex = Profile.get_sex_id_by_name(sex)
            if sex is not None:
                qs = qs.filter(sex=sex)

        country = self.request.query_params.get('country')
        if country:
            qs = qs.filter(city__in=City.objects.filter(country__name=country))

        city = self.request.query_params.get('city')
        if city:
            qs = qs.filter(city__in=City.objects.filter(name=city))

        age_from = self.request.query_params.get('age_from')
        age_to = self.request.query_params.get('age_to')

        if age_from is not None or age_to is not None:
            qs = qs.annotate(age=Age('date_birth'))

            if age_from is not None:
                age_from = to_int(age_from)
                qs = qs.filter(age__gte=age_from)

            if age_to is not None:
                age_to = to_int(age_to)
                qs = qs.filter(age__lte=age_to)

        return qs


class ObtainAuthToken(GenericAPIView):
    parser_classes = (parsers.FormParser, parsers.JSONParser,)
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        user_logged_in.send(
            sender=user.__class__, request=self.request, user=user
        )
        return Response({'token': token.key, 'user_id': user.id})


class SignUpView(mixins.CreateModelMixin, GenericAPIView):
    serializer_class = SignUpSerializer

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return Response(
                {'error': _('You cannot register an account being logged in')},
                status=status.HTTP_400_BAD_REQUEST
            )
        return self.create(request, *args, **kwargs)


class OAuthConnectView(ObtainAuthToken):
    serializer_class = OAuthConnectSerializer


class PasswordResetView(GenericAPIView):

    """
    Calls Django Auth PasswordResetForm save method.

    Accepts the following POST parameters: email
    Returns the success/fail message.
    """

    serializer_class = PasswordResetSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        # Create a serializer with request.data
        serializer = self.get_serializer(data=request.data)
        try:
            user = User.objects.get(email=request.data.get('email'))
        except User.DoesNotExist:
            return Response(
                {'error': 'User does not exist'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        message_success = 'Password reset e-mail has been sent.' \
            if user.user_settings.lang == 'en' \
            else 'Cообщение для восстановление пароля было отправлено.'
        return Response(
            {'success': message_success},
            status=status.HTTP_200_OK
        )
