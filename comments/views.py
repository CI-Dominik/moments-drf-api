from rest_framework import generics, permissions
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Comment
from .serializers import CommentSerializer, CommentDetailSerializer


# Sorgt dafür, dass die GET- und POST-Methode nicht nötigt ist
# LIST steht quasi für GET und Create für POST
class CommentList(generics.ListCreateAPIView):
    # Serializer, der benutzt wird
    serializer_class = CommentSerializer
    # Zugang nur für eingeloggte Nutzer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # Holt alle Inhalte aus der Datenbank, um sie anzuzeigen
    queryset = Comment.objects.all()

    # Methode, um Daten in einer Datenbank zu POSTen
    # Owner wird auf den Owner des Requests gesetzt
    # Request muss NICHT übergeben werden und ist automatisch dabei
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    # Berechtigung nur für den Owner oder zum Lesen
    permission_classes = [IsOwnerOrReadOnly]
    # Setzt den Serializer
    # Sorgt dafür, dass nicht jedes Mal die ID übergeben werden muss
    # -> Siehe:
    #   class CommentDetailSerializer(CommentSerializer):
    #       post = serializers.ReadOnlyField(source='post.id')
    serializer_class = CommentDetailSerializer
    # Ruft die Daten aus der Datenbank ab
    queryset = Comment.objects.all()
