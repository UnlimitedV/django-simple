from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views


router = SimpleRouter()
router.register('product', views.ProductViewSet)
router.register('collection', views.CollectionViewSet)


urlpatterns = router.urls



# urlpatterns = [
#     path('product/', views.ProductList.as_view()),
#     path('product/<int:pk>/', views.ProductDetail.as_view()),
#     path('collection/', views.CollectionList.as_view()),
#     path('collection/<int:pk>/', views.CollectionDetail.as_view(), name='collection-detail'),
# ]
