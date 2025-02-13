from rest_framework import generics, permissions
from drf_api.permissions import IsOwnerOrReadOnly
from likes.models import Like
from likes.serializers import LikeSerializer


# API View, die zum Anzeigen und Erstellen von Likes dient
class LikeList(generics.ListCreateAPIView):
    # GET für alle, POST für eingeloggte User
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # Der zu nutzende Serializer für die Abfrage
    serializer_class = LikeSerializer
    # Holt alle Einträge aus der Datenbank
    queryset = Like.objects.all()

    # Standard-Methode von ListCreateAPIView, die dafür sorgt, dass
    # nur der Owner einen Like dalassen oder entfernen kann
    # Request ist dabei, muss NICHT übergeben werden
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# API View zum Anzeigen des einzelnen Likes
# Nur Owner kann löschen
class LikeDetail(generics.RetrieveDestroyAPIView):
    # Erlaubnis für den Owner, zu löschen
    # Alle Anderen können nur GETen
    permission_classes = [IsOwnerOrReadOnly]
    # Serializer für die Ansicht
    serializer_class = LikeSerializer
    # Holt alle Likes aus der Datenbank
    queryset = Like.objects.all()
