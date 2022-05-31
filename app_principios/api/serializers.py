from rest_framework import serializers
from . import models as custom_models


# view
class UsuarioSerializer(serializers.ModelSerializer):

    class Meta:
        model = custom_models.Usuario
        fields = [
            "id",
            'username',
            'telefono',
            "tipo",
            "establecimiento",
            "direccion"
        ]


# Register Serializer
class RegistroSerializer(serializers.ModelSerializer):

    establecimiento = serializers.CharField(required=False)

    class Meta:
        model = custom_models.Usuario
        fields = [
            'username',
            'password',
            'telefono',
            'direccion',
            'establecimiento',
            'tipo',
        ]
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}

    def create(self, validated_data):
        user = custom_models.Usuario.objects.create_user(**validated_data)
        return user


class ProductoSerializer(serializers.ModelSerializer):

    vendedor = UsuarioSerializer(required=False)

    class Meta:
        model = custom_models.Producto
        fields = '__all__'

    def create(self, validated_data):

        producto_instance = custom_models.Producto.objects.create(
            **validated_data, vendedor=self.context['request'].user)
        producto_instance.save()
        return producto_instance


class OrdenSerializer(serializers.ModelSerializer):

    comprador = UsuarioSerializer(required=False)

    producto = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = custom_models.Orden
        fields = '__all__'

    def create(self, validated_data):
        id_prod = self.context["request"].data["producto"]
        prod = custom_models.Producto.objects.filter(id=id_prod).first()
        orden_instance = custom_models.Orden.objects.create(
            **validated_data, producto=prod, comprador=self.context['request'].user)
        orden_instance.save()
        return orden_instance

class listarOrdenSerializer(serializers.ModelSerializer):

    comprador = UsuarioSerializer()

    producto = ProductoSerializer()

    class Meta:
        model = custom_models.Orden
        fields = '__all__'