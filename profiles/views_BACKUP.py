from django.shortcuts import render # noqa
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Profile
from rest_framework import status
from .serializers import ProfileSerializers
from drf_api.permissions import IsOwnerOrReadOnly


# APIView sorgt dafür, dass Profile im DRF (Browser) angezeigt werden
class ProfileList(APIView):
    # GET-Anfrage-Verarbeitung für die Profile
    def get(self, request):
        # Nimmt die Profile aus der Datenbanke
        profiles = Profile.objects.all()
        # Wählt den Serializer aus, übergibt Profile zum Prüfen und
        # many=True, weil es viele Werte sind, nicht nur einer.
        # Request wird als Prop übergeben
        serializer = ProfileSerializers(
            profiles,
            many=True,
            context={'request': request}
            )
        return Response(serializer.data)


# ProfileDetail ist eine eigene URL
class ProfileDetail(APIView):
    # Wählt den Serializer für die View
    serializer_class = ProfileSerializers
    # Sorgt dafür, dass nur der Owner bearbeiten, aber alle die Daten sehen
    permission_classes = [IsOwnerOrReadOnly]

    # PK wird in der URL übergeben und hier verwendet
    def get_object(self, pk):
        try:
            profile = Profile.objects.get(pk=pk)
            self.check_object_permissions(self.request, profile)
            return profile
        except Profile.DoesNotExist:
            raise Http404

    # GET-Methode für diese View
    def get(self, request, pk):
        # Ruft die get_object-Methode oben auf und gibt den PK an
        # PK ist in der URL als <int:pk> und muss angegeben werden
        profile = self.get_object(pk)
        # Wählt den Serializer aus, übergibt Profile zum Prüfen und
        # many=True, weil es viele Werte sind, nicht nur einer.
        # Request wird als "Prop" übergeben
        serializer = ProfileSerializers(
            profile,
            context={'request': request}
            )
        return Response(serializer.data)

    # PUT-Methode für diese View, PK ist in der URL
    def put(self, request, pk):
        # Ruft die get_object-Methode oben auf und gibt den PK an
        # PK ist in der URL als <int:pk> und muss angegeben werden
        profile = self.get_object(pk)
        # Wählt den Serializer aus, übergibt Profile zum Prüfen und
        # many=True, weil es viele Werte sind, nicht nur einer.
        # Request wird als "Prop" übergeben
        serializer = ProfileSerializers(
            profile,
            data=request.data,
            context={'request': request}
            )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
