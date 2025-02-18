from rest_framework import serializers
from .models import Post
from likes.models import Like


class PostSerializers(serializers.ModelSerializer):
    # Angabe der Werte, die überprüft werden sollen
    # Greift auf das Profil eines Owners zu und sucht dessen Namne raus
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    like_id = serializers.SerializerMethodField()
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()

    # DRF-Funktion zur Überprüfung eines Wertes
    # validate_EIGENSCHAFT ist immer die Syntax und value immer benötigt
    """def validate_image(self, value):
        # Dateigröße
        image_info = cloudinary.api.resource(value.public_id)
        if image_info['bytes'] > 1024 * 1024 * 2:
            raise serializers.ValidationError(
                'Image size larger than 2 MB!'
            )
        # Breite
        if value.image.width > 4096:
            raise serializers.ValidationError(
                'Image width large than 4096 pixels!'
            )
        # Höhe
        if value.image.height > 4096:
            raise serializers.ValidationError(
                'Image height large than 4096 pixels!'
            )
        return value"""

    # DRF-Methode zur Überprüfung des SerializerMethodFields
    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_like_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            like = Like.objects.filter(
                owner=user, post=obj
            ).first()
            return like.id if like else None
        return None

    class Meta:
        model = Post
        fields = [
            'id', 'owner', 'is_owner', 'profile_id',
            'profile_image', 'created_at', 'updated_at',
            'title', 'content', 'image', 'image_filter',
            'like_id', 'likes_count', 'comments_count',
        ]
