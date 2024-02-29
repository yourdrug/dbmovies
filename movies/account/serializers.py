from djoser.serializers import UserSerializer

from account.models import Account


class CurrentUserInfoSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = Account
        fields = (
            'id',
            'username',
            'image',
            'email',
            'is_critic'
        )

    def update_image(self, instance, validated_data):
        image = validated_data.get('image', None)
        if image:
            instance.image = image
        instance.save()
        return instance
