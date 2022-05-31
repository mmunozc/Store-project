from rest_framework import viewsets, permissions, generics, status
from . import serializers as custom_serializers
from . import models as custom_models
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.http import Http404


# Get User API
class UserAPI(generics.RetrieveAPIView):

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = custom_serializers.UsuarioSerializer

    def get_object(self):
        return self.request.user


class UsersView(generics.ListAPIView):

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = custom_serializers.UsuarioSerializer

    def get_queryset(self):
        if self.request.user.tipo == "comprador":
            queryset = custom_models.Usuario.objects.all().filter(tipo="vendedor")
        else:
            queryset = custom_models.Usuario.objects.all().filter(tipo="comprador")
        return queryset


class RegistroView(generics.ListAPIView):

    serializer_class = custom_serializers.RegistroSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)  # JWT token
        return Response({
            "user": custom_serializers.RegistroSerializer(
                user,
                context=self.get_serializer_context()).data,
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        })


class ProductoView(viewsets.ModelViewSet):

    serializer_class = custom_serializers.ProductoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        vendedor = self.request.query_params.get("vendedor", None)
        queryset = custom_models.Producto.objects.filter(
            vendedor__establecimiento=vendedor)
        return queryset
    
    def delete(self, request):
        id_orden = self.request.query_params.get("id", None)
        if id_orden:
            try:
                instance = custom_models.Producto.objects.filter(id=id_orden)
                self.perform_destroy(instance)
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Http404:
                pass
        return Response(status=status.HTTP_404_NOT_FOUND)


class OrdenView(viewsets.ModelViewSet):

    serializer_class = custom_serializers.OrdenSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.tipo == "comprador":
            queryset = custom_models.Orden.objects.filter(
                comprador=self.request.user).filter(completado=False)
        else:
            queryset = custom_models.Orden.objects.filter(
                producto__vendedor=self.request.user).filter(completado=False)
        return queryset
    
    def list(self, request):
        queryset = self.get_queryset()
        if self.request.user.tipo == "comprador":
            serializer = custom_serializers.listarOrdenSerializer(queryset, many=True)
        else:
            serializer = custom_serializers.OrdenSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def delete(self, request):
        id_orden = self.request.query_params.get("id", None)
        if id_orden:
            try:
                instance = custom_models.Orden.objects.filter(id=id_orden)
                self.perform_destroy(instance)
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Http404:
                pass
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    def patch(self, request):
        id_orden = self.request.query_params.get("id", None)
        if id_orden:
            orden = custom_models.Orden.objects.filter(id=id_orden).first()
            orden.completado = True
            orden.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_404_NOT_FOUND)