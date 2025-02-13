from django.http import Http404
# Permissions ist wichtig, damit der Login erkannt wird
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post
from .serializers import PostSerializers
from drf_api.permissions import IsOwnerOrReadOnly


# APIView sorgt dafür, dass Posts im DRF (Browser) angezeigt werden
class PostList(APIView):

    # Vorgabe von APIView, um den Serializer auszuwählen
    serializer_class = PostSerializers

    # Vorgabe des DRF, um die Zugriffsrechte zu verwalten
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]

    # GET-Anfrage in dieser View wird verarbeitet
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializers(
            posts,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

    # POST-Anfrage in dieser View wird verarbeitet
    def post(self, request):
        serializer = PostSerializers(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
                )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


# PostDetail View ist in der URL definiert
class PostDetail(APIView):
    # Berechtigung, damit nur der Owner bearbeiten kann
    permission_classes = [
        IsOwnerOrReadOnly
    ]
    serializer_class = PostSerializers

    # Funktion, um einen Post zu bekommen, NICHT der URL-Part
    # Dient zur Kontrolle, ob ein Post existiert
    def get_object(self, pk):
        try:
            # Einen Post nach PK suchen
            post = Post.objects.get(pk=pk)
            self.check_object_permissions(self.request, post)
            return post
        except Post.DoesNotExist:
            raise Http404

    # GET-Anfrage, PK wird in der URL übergeben (<int:pk>)
    def get(self, request, pk):
        post = self.get_object(pk)
        # Überprüft mit diesem Serializer den einen Post
        # Post wird übergeben, Request auch
        serializer = PostSerializers(
            post,
            context={
                'request': request
                }
        )
        return Response(serializer.data)

    # PUT-Anfrage, PK wird in der URL übergeben (<int:pk>)
    def put(self, request, pk):
        post = self.get_object(pk)
        # Überprüft mit diesem Serializer den einen Post
        # Post wird übergeben, Request auch
        serializer = PostSerializers(
            post,
            # Daten, die gesendet worden sind
            data=request.data,
            context={
                'request': request
            }
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
