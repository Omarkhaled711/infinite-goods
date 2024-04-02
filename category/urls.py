from django.urls import path, include
urlpatterns = [
    path('api/v1/', include('category.api.v1.urls')),
]
