from django.contrib.auth import get_user_model, authenticate
# explanation for gettext and ugettext and ugettext_lazy
# https://simpleisbetterthancomplex.com/tips/2016/10/17/django-tip-18-translations.html
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        # pop will retrieve and remove the password property from validated_data
        # since we want to update password with hash not with raw password
        # and giving NONE default value if it's not defined in the property
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


# we are inheriting from the more standard Serializer
class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""

    # fields that we want to validate
    email = serializers.CharField()
    # input_type is for the browsable API text field style
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )

        # if authentication fails, it will not return a user
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs