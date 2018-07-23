# encoding: utf-8
from __future__ import unicode_literals

from django.conf import settings
from rauth import OAuth2Service

from ..models import User, OAuthAccount


class RequiredFieldsException(Exception):
    pass


class ProviderException(Exception):
    pass


class UnableRetrieveRequiredData(Exception):
    pass


class BaseProvider(object):
    USERNAME_LEN = 16
    BASE_URL = None
    AUTHORIZE_URL = None
    ACCESS_TOKEN_URL = None
    FIELDS = ['fullname', 'sex', 'date_birth']

    def __init__(self, name):
        self.name = name

        client_id, client_secret = self.get_id_and_secret()
        self.service = OAuth2Service(
            client_id, client_secret, name, self.ACCESS_TOKEN_URL,
            self.AUTHORIZE_URL, self.BASE_URL
        )

    def get_id_and_secret(self):
        """Gets credentials to connect with provider."""
        oauth = settings.OAUTH.get(self.name, {})
        return oauth.get('client_id'), oauth.get('client_secret')

    def me(self, session):
        """Makes request to provider to get user's data.
        :param session:
        :return: requests instance
        """
        return session.get('me')

    def normalize_me(self, data):
        raise NotImplementedError

    def connect(self, access_token, extra_attrs):
        """Logs in/Signs up user based on data given by provider.
        :return: User instance
        """
        session = self.service.get_session(access_token)

        me = self.me(session)
        if me.status_code != 200:
            raise ProviderException

        norm_data = self.normalize_me(me.json())
        uid = norm_data.pop('id')
        if not uid:
            raise UnableRetrieveRequiredData

        user = self.get_user(uid)
        if user:
            return user
        else:
            email = norm_data.pop('email')

            if not email:
                raise UnableRetrieveRequiredData

            # Binds provider with existing user
            rel_user = self.associate(uid, email)
            if rel_user:
                return rel_user

            for field_name in self.FIELDS:
                val = extra_attrs.get(field_name)
                if val:
                    norm_data[field_name] = val

            self.check_required_fields(norm_data)
            return self.signup(uid, email, norm_data)

    def check_required_fields(self, norm_data):
        required = [f for f in self.FIELDS if not norm_data.get(f)]
        if required:
            raise RequiredFieldsException(required)

    def associate(self, uid, email):
        """Associates provider's account with user by email.
        :return: User instance
        """
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user:
            OAuthAccount.objects.create(user=user, provider=self.name, uid=uid)
            return user

    def signup(self, uid, email, data):
        """Creates user based on data provided by provider.
        :param uid: User ID
        :param email: Email given by provider
        :param data: extra data
        :return: User instance
        """
        kwargs = {
            'username': self.get_username(uid),
            'email': email,
            'password': None,
            'fullname': data.get('fullname'),
            'sex': data.get('sex'),
            'date_birth': data.get('date_birth')
        }

        user = User.objects.create_user(**kwargs)
        OAuthAccount.objects.create(
            user=user, provider=self.name, uid=uid
        )
        return user

    @staticmethod
    def get_username(uid):
        """Generates not reserved username based on uid from provider.
        :param uid: User ID
        :return: username
        """
        username = uid
        i = 1
        while User.objects.filter(username=username).exists():
            username = '{}_{}'.format(uid[:BaseProvider.USERNAME_LEN], i)
            i += 1
        return username

    @staticmethod
    def get_user(uid):
        """Gets user by provider's UID if it's present.
        :param uid: User ID
        :return: User instance
        """
        try:
            return OAuthAccount.objects.get(uid=uid).user
        except OAuthAccount.DoesNotExist:
            return None
