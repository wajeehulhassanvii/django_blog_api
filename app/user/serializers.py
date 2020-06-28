from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'first_name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    # overrigding create function of ModelSerializer
    def create(self, validated_data):
        """Create a new user with encrypted pass and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        # default valule for pop here is None
        # meaning if the value isn't there then itd return None
        password = validated_data.pop('password', None)
        # super gives model serializer update func
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serialzier for user authentication object"""
    # authenticate workshelps in authentication
    email = serializers.CharField()
    password = serializers.CharField(
        style={'imput_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            reques=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs
