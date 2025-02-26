from rest_framework import serializers
from .models import Profile
from follower.models import Follower


class ProfileSerializers(serializers.ModelSerializer):
    # Nimmt den Owner-Wert eines Profils, Zugriff möglich, weil FK gesetzt
    owner = serializers.ReadOnlyField(source='owner.username')
    # SerializerMethodField ist für die Prüfung eines Wertes da
    is_owner = serializers.SerializerMethodField()
    # SerializerMethodField für die Prüfung der IDs, die followen
    following_id = serializers.SerializerMethodField()
    # Anzahl der Posts mithilfe der views.py
    posts_count = serializers.ReadOnlyField()
    # Anzahl der Follower

    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    def get_followers_count(self, obj):
        return Follower.objects.filter(followed=obj.owner).count()

    def get_following_count(self, obj):
        return Follower.objects.filter(owner=obj.owner).count()

    # Ruft den Context ab und vergleicht den Request mit dem Owner
    # obj muss immer benutzt werden und ist das Objekt, das geprüft wird
    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_following_id(self, obj):
        # Ruft den User aus dem Request ab
        # Request wurde als Context gesendet
        user = self.context['request'].user
        if user.is_authenticated:
            # Guckt, ob die Person ein Follower ist
            following = Follower.objects.filter(
                owner=user, followed=obj.owner
            ).first()
            # Gibt zurück, ob man folgt
            # Kann in React abgerufen werden
            return following.id if following else None
        return None

    # Gibt das Model an, das beim Serializer benutzt werden soll
    class Meta:
        model = Profile
        fields = [
            'id',
            'owner',
            'created_at',
            'updated_at',
            'name',
            'content',
            'image',
            'is_owner',
            'following_id',
            'posts_count',
            'followers_count',
            'following_count',
        ]
