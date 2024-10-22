from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView, FormView
from django.http import JsonResponse, HttpResponseRedirect
from .models import Lugar, Comentario
from .forms import BikeSearchForm
import requests


def get_cities_by_country(request):
    """
    Retorna cidades disponíveis para um país usando a API CityBikes.
    """
    country = request.GET.get("country", None)
    if country:
        url = "http://api.citybik.es/v2/networks"
        response = requests.get(url)
        if response.status_code == 200:
            networks = response.json().get("networks", [])
            cities = set(
                network["location"]["city"]
                for network in networks
                if network["location"]["country"].lower() == country.lower()
            )
            return JsonResponse({"cities": list(cities)})
    return JsonResponse({"cities": []})


class BikeServiceView(FormView):
    """
    Renderiza e processa o formulário de busca de bike-sharing.
    """
    template_name = "bike/check_bike_service.html"
    form_class = BikeSearchForm

    def form_valid(self, form):
        """
        Redireciona para resultados após validação do formulário.
        """
        city = form.cleaned_data["city"]
        country = form.cleaned_data["country"]
        return HttpResponseRedirect(
            reverse(
                "resultados_busca",
                kwargs={
                    "city": city,
                    "country": country,
                },
            )
        )


class ResultadosBuscaView(TemplateView):
    """
    Exibe resultados de serviços de bike-sharing para cidade e país específicos.
    """
    template_name = "bike/resultados_busca.html"

    def get_context_data(self, **kwargs):
        """
        Obtém dados de contexto para a página de resultados.
        """
        context = super().get_context_data(**kwargs)
        city = self.kwargs["city"]
        country = self.kwargs["country"]

        response = requests.get("http://api.citybik.es/v2/networks")
        if response.status_code == 200:
            networks = response.json().get("networks", [])
            bikes_data = [
                network
                for network in networks
                if network["location"]["city"].lower() == city.lower()
                and network["location"]["country"].lower() == country.lower()
            ]

            for bike in bikes_data:
                network_id = bike["id"]
                network_response = requests.get(
                    f"http://api.citybik.es/v2/networks/{network_id}"
                )
                if network_response.status_code == 200:
                    bike["stations"] = (
                        network_response.json().get("network", {}).get("stations", [])
                    )
                else:
                    bike["stations"] = []

            context["bikes_data"] = bikes_data
        else:
            context["bikes_data"] = []

        lugares = Lugar.objects.all()
        lugares_data = [
            {
                "nome": lugar.nome,
                "descricao": lugar.descricao,
                "latitude": lugar.latitude,
                "longitude": lugar.longitude,
                "tipo": lugar.get_tipo_display(),
                "comentarios_url": reverse("comentario_lugar_list", args=[lugar.id]),
            }
            for lugar in lugares
        ]
        context["lugares_data"] = lugares_data

        context["city"] = city
        context["country"] = country
        return context


class LugarCreateView(CreateView):
    """
    Cria um novo lugar no banco de dados.
    """
    model = Lugar
    fields = ["nome", "descricao", "latitude", "longitude", "tipo"]
    template_name = "bike/cadastrar_lugar.html"
    success_url = reverse_lazy("check_bike_service")


class SobreServicoView(TemplateView):
    """
    Exibe a página inicial sobre o serviço.
    """
    template_name = "bike/home.html"


class ComentarioLugarListView(ListView):
    """
    Exibe a lista de comentários de um lugar.
    """
    model = Comentario
    template_name = "bike/comentarios/comentario_lugar_list.html"
    context_object_name = "comentarios"

    def get_queryset(self):
        lugar_id = self.kwargs.get("lugar_id")
        return Comentario.objects.filter(lugar_id=lugar_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lugar_id"] = self.kwargs.get("lugar_id")
        return context


class ComentarioCreateView(CreateView):
    """
    Cria um novo comentário para um lugar.
    """
    model = Comentario
    fields = ["texto"]
    template_name = "bike/comentarios/comentario_form.html"

    def form_valid(self, form):
        lugar_id = self.kwargs["lugar_id"]
        form.instance.lugar_id = lugar_id
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lugar_id"] = self.kwargs["lugar_id"]
        return context

    def get_success_url(self):
        lugar_id = self.kwargs["lugar_id"]
        return reverse_lazy("comentario_lugar_list", kwargs={"lugar_id": lugar_id})


class ComentarioUpdateView(UpdateView):
    """
    Atualiza um comentário existente.
    """
    model = Comentario
    fields = ["texto"]
    template_name = "bike/comentarios/comentario_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lugar_id"] = self.object.lugar_id
        return context

    def get_success_url(self):
        return reverse_lazy("comentario_lugar_list", kwargs={"lugar_id": self.object.lugar_id})


class ComentarioDeleteView(DeleteView):
    model = Comentario
    template_name = "bike/comentarios/comentario_confirm_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lugar_id'] = self.object.lugar_id  # Certifique-se de que lugar_id está disponível
        return context

    def get_success_url(self):
        return reverse_lazy("comentario_lugar_list", kwargs={"lugar_id": self.object.lugar_id})
