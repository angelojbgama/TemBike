from django.urls import path
from .views import BikeServiceView, ResultadosBuscaView, get_cities_by_country, LugarCreateView, SobreServicoView


from .views import ComentarioListView, ComentarioCreateView, ComentarioUpdateView, ComentarioDeleteView, ComentarioLugarListView

urlpatterns = [
    path('', BikeServiceView.as_view(), name='check_bike_service'),
    path('resultados/<str:city>/<str:country>/', ResultadosBuscaView.as_view(), name='resultados_busca'),
    path('cadastrar/', LugarCreateView.as_view(), name='cadastrar_lugar'),
    path('sobre/', SobreServicoView.as_view(), name='sobre_servico'),
    
    
    path('comentarios/', ComentarioListView.as_view(), name='comentario_list'),
    path('comentarios/novo/', ComentarioCreateView.as_view(), name='comentario_create'),
    path('comentarios/<int:pk>/editar/', ComentarioUpdateView.as_view(), name='comentario_update'),
    path('comentarios/<int:pk>/deletar/', ComentarioDeleteView.as_view(), name='comentario_delete'),
    path('lugares/<int:lugar_id>/comentarios/', ComentarioLugarListView.as_view(), name='comentario_list_lugar'),

    
    path('get-cities/', get_cities_by_country, name='get_cities_by_country'),

]
