from django.urls import path
from .views import (
    BikeServiceView, 
    ResultadosBuscaView, 
    get_cities_by_country, 
    salvar_avaliacao,
    LugarCreateView, 
    SobreServicoView,
    ComentarioCreateView, 
    ComentarioUpdateView, 
    ComentarioDeleteView, 
    ComentarioLugarListView,
    ComentarioUpdateEstrelasView
)

urlpatterns = [
    path('', BikeServiceView.as_view(), name='check_bike_service'),
    path('resultados/<str:city>/<str:country>/', ResultadosBuscaView.as_view(), name='resultados_busca'),
    path('cadastrar/', LugarCreateView.as_view(), name='cadastrar_lugar'),
    path('sobre/', SobreServicoView.as_view(), name='sobre_servico'),

    path('lugares/<int:lugar_id>/comentarios/', ComentarioLugarListView.as_view(), name='comentario_lugar_list'),
    path('lugares/<int:lugar_id>/comentarios/novo/', ComentarioCreateView.as_view(), name='comentario_create'),
    path('comentarios/<int:pk>/editar/', ComentarioUpdateView.as_view(), name='comentario_update'),
    path('comentarios/<int:pk>/deletar/', ComentarioDeleteView.as_view(), name='comentario_delete'),


    path('comentario/<int:pk>/alterar-estrelas/', ComentarioUpdateEstrelasView.as_view(), name='comentario_update_estrelas'),


    path('comentarios/<int:comentario_id>/avaliacao/', salvar_avaliacao, name='salvar_avaliacao'),

    path('get-cities/', get_cities_by_country, name='get_cities_by_country'),
]
