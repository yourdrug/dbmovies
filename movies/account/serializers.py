from djoser.serializers import UserSerializer

from account.models import Account


class CurrentUserInfoSerializer(UserSerializer):

    class Meta(UserSerializer.Meta):
        model = Account
        fields = (
            'id',
            'username',
            'image',
            'email'
        )
