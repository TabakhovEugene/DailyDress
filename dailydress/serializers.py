from rest_framework import serializers

from .models import Cloth, Style


class ClothListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cloth
        fields = ["id_cloth", "user", "type", "sub_type", "color", "temp_range", "weather", "like_rate", "picture_url"]

class ClothDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cloth
        fields = ["id_cloth", "user", "type", "sub_type", "color", "temp_range", "weather", "like_rate", "picture_url"]

class StyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Style
        fields = ["id_style", "user", "date_for_style"]