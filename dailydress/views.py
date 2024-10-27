from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import condition
from rest_framework import status
from rest_framework.response import Response
from random import random
from math import sqrt

from .models import Style, Cloth, StyleCloth
from rest_framework.views import APIView

from .serializers import ClothListSerializer, ClothDetailSerializer, StyleSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.views import APIView
from random import randint

from .weather import get_weather_forecast

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Пользователь с таким именем уже существует'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Неверные учетные данные'}, status=status.HTTP_401_UNAUTHORIZED)


class UserLogoutView(APIView):
    def post(self, request):
        try:
            # Получаем токен из заголовка Authorization
            token = request.META.get('HTTP_AUTHORIZATION').split()[1]
            token_obj = RefreshToken(token)
            token_obj.blacklist()  # Добавляем токен в черный список
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ClothesList(APIView):
    serializer_class = ClothListSerializer
    # Вывод всех вещей
    def get(self, request):
        hats = Cloth.objects.filter(user = request.user, type='Головные уборы')
        outerwear = Cloth.objects.filter(user = request.user, type='Верхняя одежда')
        undergarments = Cloth.objects.filter(user = request.user, type='Нижняя одежда')
        tops = Cloth.objects.filter(user = request.user, type='Топы и футболки')
        shoes = Cloth.objects.filter(user = request.user, type='Обувь')
        accessories = Cloth.objects.filter(user = request.user, type='Аксессуары')

        hats_serializer = self.serializer_class(hats, many=True)
        outerwear_serializer = self.serializer_class(outerwear, many=True)
        undergarments_serializer = self.serializer_class(undergarments, many=True)
        tops_serializer = self.serializer_class(tops, many=True)
        shoes_serializer = self.serializer_class(shoes, many=True)
        accessories_serializer = self.serializer_class(accessories, many=True)

        response = {}
        response['hats'] = hats_serializer.data
        response['outerwear'] = outerwear_serializer.data
        response['undergarments'] = undergarments_serializer.data
        response['tops'] = tops_serializer.data
        response['shoes'] = shoes_serializer.data
        response['accessories'] = accessories_serializer.data

        return Response(response, status=status.HTTP_200_OK)

class ClothesDetail(APIView):
    serializer_class = ClothDetailSerializer
    # Добавление новой одежды
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Изменение конкретной одежды
    def put(self, request, pk, format=None):
        cloth = get_object_or_404(Cloth, id_cloth=pk)
        serializer = self.serializer_class(cloth, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AddClothes(APIView):
    # Добавление вещи в лук
    def post(self, request, id_cloth):
        if not Style.objects.filter(user=request.user, id_style=request.id_style).exists():
            new_style = Style()
            new_style.user = request.user
            new_style.save()

        style_id = Style.objects.filter(user=request.user, id_style=request.id_style).first().id_style

        if Cloth.objects.filter(id_cloth=id_cloth).exists():
            new_style_cloth = StyleCloth()
            new_style_cloth.id_cloth = id_cloth
            new_style_cloth.id_style = style_id
            new_style_cloth.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({'error':'Одежда не найдена'}, status=status.HTTP_400_BAD_REQUEST)

class GetStyle(APIView):
    # Просмотр лука
    def get(self, request, id_style):
        # Здесь будет автоматическое формирование лука


        style = Style.objects.filter(user=request.user, id_style=id_style)
        serializer = StyleSerializer(style)
        response = serializer.data

        current_clothes = Cloth.objects.filter(
            cloth__id_style=id_style
        )

        clothes_serializer = ClothListSerializer(current_clothes, many=True)
        response['clothes'] = clothes_serializer.data

        return Response(response, status=status.HTTP_200_OK)

    def post(self, request):
        clothes = Cloth.objects.filter(user=request.user)
        temp, condition, today = get_weather_forecast()
        new_style = Style()
        new_style.user = request.user
        new_style.date_for_style = today
        new_style.save()

        def get_clothes(clothes, temp, condition):
            if 'rain' in condition or 'wet' in condition:
                condition = 'Дождь'
            elif condition == 'clear':
                condition = 'Солнечно'
            else:
                condition = ''

            def weather_filter(cloth: Cloth) -> bool:
                if condition == 'Солнечно':
                    if cloth.type in ['Головные уборы', 'Обувь']:
                        return cloth.weather in ['', 'Солнечно']
                    return cloth.weather == ''
                elif condition == 'Дождь':
                    if cloth.type == 'Верхняя одежда':
                        return cloth.weather in ['Дождь']
                    elif cloth.type == 'Обувь':
                        return cloth.weather in ['', 'Дождь']
                    return cloth.weather == ''
                else:
                    return cloth.weather == ''

            def temp_filter(cloth:Cloth) -> bool:
                return cloth.temp_range[0] <= temp <= cloth.temp_range[1]

            filtered_clothes = [cloth for cloth in clothes if weather_filter(cloth) and temp_filter(cloth)]

            grouped_clothes = {}
            for cloth in filtered_clothes:
                if cloth.type not in grouped_clothes:
                    grouped_clothes[cloth.type] = []
                grouped_clothes[cloth.type].append(cloth)

            # Функция для выбора одежды с учётом like_rate
            def weighted_random_choice(items: list[Cloth]) -> Cloth:
                massive = [0] * len(items)
                for i in range(len(items)):
                    massive[i] = (((items[i].temp_range[0] - temp) ** 2 + (items[i].temp_range[1] - temp) ** 2) / sqrt(2)) + (10 - items[i].like_rate)
                minimum = min(massive)
                ind = massive.index(minimum)
                if random() < 0.2:
                    return items[ind]
                else:
                    return items[randint(0, len(items) - 1)]


            selected_clothes = []

            # Обязательные категории для выбора
            for category in ['Обувь', 'Нижняя одежда', 'Футболки']:
                if category in grouped_clothes:
                    selected_clothes.append(weighted_random_choice(grouped_clothes[category]))

            # Обработка верхней одежды в зависимости от погоды
            if condition == 'Дождь':
                # Добавляем верхнюю одежду, подходящую для дождя
                if 'Верхняя одежда' in grouped_clothes:
                    rain_outerwear = [item for item in grouped_clothes['Верхняя одежда'] if 'Дождь' in item.weather]
                    if rain_outerwear:
                        selected_clothes.append(weighted_random_choice(rain_outerwear))
            else:
                if temp < 5:
                    for category in ['Верхняя одежда']:
                        if category in grouped_clothes:
                            selected_clothes.append(weighted_random_choice(grouped_clothes[category]))
                elif 5 <= temp <= 15:
                    for category in ['Верхняя одежда', 'Толстовки и свитеры']:
                        if category in grouped_clothes:
                            selected_clothes.append(weighted_random_choice(grouped_clothes[category]))
                elif 15 < temp <= 25:
                    if 'Толстовки и свитеры' in grouped_clothes:
                        selected_clothes.append(weighted_random_choice(grouped_clothes['Толстовки и свитеры']))

            # Добавляем аксессуары в зависимости от погоды
            used_accessories = set()
            if condition == 'Дождь':
                if 'Аксессуары' in grouped_clothes:
                    # Фильтруем аксессуары подходящие для дождя (зонтики)
                    rain_accessories = [item for item in grouped_clothes['Аксессуары'] if 'Зонтик' in item.sub_type]
                    if rain_accessories:
                        chosen_accessory = weighted_random_choice(rain_accessories)
                        selected_clothes.append(chosen_accessory)
                        used_accessories.add(chosen_accessory.sub_type)

            if temp < 5:
                if 'Аксессуары' in grouped_clothes:
                    # Фильтруем аксессуары подходящие для холода (перчатки, шарфы, снуды)
                    cold_accessories = [item for item in grouped_clothes['Аксессуары'] if
                                        item.sub_type in ['Перчатки', 'Шарф',
                                                          'Снуд'] and item.sub_type not in used_accessories]
                    for accessory_type in ['Перчатки', 'Шарф', 'Снуд']:
                        specific_accessories = [item for item in cold_accessories if item.sub_type == accessory_type]
                        if specific_accessories:
                            chosen_accessory = weighted_random_choice(specific_accessories)
                            selected_clothes.append(chosen_accessory)
                            used_accessories.add(accessory_type)

            if condition == 'Солнечно':
                if 'Головные уборы' in grouped_clothes:
                    # Фильтруем головные уборы подходящие для солнца (кепки, панамки)
                    sun_hats = [item for item in grouped_clothes['Головные уборы'] if
                                item.sub_type in ['Кепка', 'Панамка']]
                    if sun_hats:
                        selected_clothes.append(weighted_random_choice(sun_hats))

            # Возвращаем итоговый список выбранной одежды
            return selected_clothes

        select_clothes = get_clothes(clothes, temp, condition)

        for cloth in select_clothes:
            new_style_cloth = StyleCloth()
            new_style_cloth.cloth_id = cloth.id_cloth
            new_style_cloth.style_id = new_style.id_style
            new_style_cloth.save()

        # Логика передачи вещей в лук
        style_serializer = StyleSerializer(new_style)
        response = style_serializer.data

        current_clothes = Cloth.objects.filter(
            cloth__style=new_style.id_style
        )

        clothes_serializer = ClothListSerializer(current_clothes, many=True)
        response['clothes'] = clothes_serializer.data

        return Response(response, status=status.HTTP_200_OK)



class ListStyles(APIView):
    def get(self, request):
        if 'date' in request.data and 'status' in request.data:
            styles = Style.objects.filter(date_for_style__gte=request.data['date'])
        else:
            styles = Style.objects.all()
        styles_serializer = StyleSerializer(styles, many=True)
        response = styles_serializer.data

        for style_data in response:
            id_style = style_data['id_style']
            current_clothes = Cloth.objects.filter(
                cloth__id_style=id_style
            )

            clothes_serializer = ClothListSerializer(current_clothes, many=True)
            style_data['clothes'] = clothes_serializer.data

        return Response(response, status=status.HTTP_200_OK)