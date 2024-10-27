from django.contrib import admin
from django.urls import path
from dailydress import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path(r'clothes/', views.ClothesList.as_view(), name='clothers-list'),  # список одежду (GET),
    #
    # path(r'clothes/<int:pk>/', views.ClothesDetail.as_view(), name='clothes-detail'),  # получить одежду (GET),
    path(r'clothes/create/', views.ClothesDetail.as_view(), name='clothes-create'),  # добавление одежда (POST),
    path(r'clothes/update/<int:pk>/', views.ClothesDetail.as_view(), name='clothes-update'), # редактирование одежды (PUT),
    path(r'clothes/add/<int:pk>/', views.AddClothes.as_view(), name='add-clothes-to-style'), # добавление одежды в стиль (POST),
    #
    path(r'style/<int:pk>/', views.GetStyle.as_view(), name='get-style-by-id'), # получить лук (GET),
    path(r'style/create/', views.GetStyle.as_view(), name='get-style-by-id'), # получить лук (POST),
    path(r'history-list-styles/', views.ListStyles.as_view(), name='history-list-styles-by-username'), # получить историю луков (GET),
    #
    # # Users
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    # path('profile/', views.UserUpdateView.as_view(), name='profile'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
]
