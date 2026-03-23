from django.urls import path
from .views import (
    ProcessMassValuesView,
    SimulationWithMassView,
    SimulationWithoutMassView,
    ResultadosView,
    DeletarSimulacaoView,
)

urlpatterns = [
    path(
        "simulation_with_mass/",
        SimulationWithMassView.as_view(),
        name="simulation_with_mass",
    ),
    path(
        "simulation_without_mass/",
        SimulationWithoutMassView.as_view(),
        name="simulation_without_mass",
    ),
    path(
        "process_mass_values/<int:id>/",
        ProcessMassValuesView.as_view(),
        name="process_mass_values",
    ),
    path("resultados/", ResultadosView.as_view(), name="resultados_view"),
    path(
        "deletar_simulacao/<int:id>/",
        DeletarSimulacaoView.as_view(),
        name="deletar_simulacao",
    ),
]
