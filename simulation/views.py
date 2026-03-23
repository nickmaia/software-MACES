from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, render, redirect
from .models import Resultado, Simulacao
from GA.GA_with_MLP import get_molecule_with_mass, get_molecule_without_mass
import time

class SimulationWithMassView(LoginRequiredMixin, TemplateView):
    template_name = "simulation/simulacao_com_massa.html"

    def post(self, request, *args, **kwargs):
        # Obter nome da simulação do formulário
        nome_simulacao = request.POST.get("nome_simulacao")

        # Obter e converter valores de massa e intensidade do formulário diretamente para float
        massas = list(map(float, request.POST.getlist("mass")))
        intensidades = list(map(float, request.POST.getlist("intensity")))

        # Ordenar os valores de intensidade em ordem decrescente
        valores_ordenados = sorted(zip(intensidades, massas), reverse=True)

        # Pegar os 10 maiores valores de intensidade e suas respectivas massas
        maiores_valores = valores_ordenados[:10]
        maiores_intensidades = [valor[0] for valor in maiores_valores]
        maiores_massas = [valor[1] for valor in maiores_valores]
        massa_alvo = request.POST.get("massa_alvo")

        # Criar uma nova simulação associada ao usuário autenticado
        simulacao = Simulacao.objects.create(nome=nome_simulacao, usuario=request.user)

        
        massa_alvo = float(massa_alvo)
        # Calcular o tempo de execução da função de cálculo com massa
        start_time = time.time()
        # Calcular o tempo de execução da função de cálculo com massa 
        resultado_calculado = get_molecule_with_mass(
            maiores_massas, maiores_intensidades, massa_alvo
        )
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"#########################Tempo de execução: {execution_time:.2f} segundos")

        # Calcular a soma total das chances
        total_chances = sum(
            detalhes["chance"] for detalhes in resultado_calculado.values()
        )
        # Criar os resultados com base nos valores calculados
        for molecula, detalhes in resultado_calculado.items():
            chance_porcentagem = (detalhes["chance"] / total_chances) * 100
            Resultado.objects.create(
                simulacao=simulacao,
                massa=detalhes["mass"],
                resultado=molecula,
                chance=chance_porcentagem,
            )

        return redirect("process_mass_values", id=simulacao.id)


class SimulationWithoutMassView(LoginRequiredMixin, TemplateView):
    template_name = "simulation/simulacao_sem_massa.html"

    def post(self, request, *args, **kwargs):
        # Obter nome da simulação do formulário
        nome_simulacao = request.POST.get("nome_simulacao")

        # Obter e converter valores de massa e intensidade do formulário diretamente para float
        massas = list(map(float, request.POST.getlist("mass")))
        intensidades = list(map(float, request.POST.getlist("intensity")))

        # Ordenar os valores de intensidade em ordem decrescente
        valores_ordenados = sorted(zip(intensidades, massas), reverse=True)

        # Pegar os 10 maiores valores de intensidade e suas respectivas massas
        maiores_valores = valores_ordenados[:10]
        maiores_intensidades = [valor[0] for valor in maiores_valores]
        maiores_massas = [valor[1] for valor in maiores_valores]

        # Criar uma nova simulação associada ao usuário autenticado
        simulacao = Simulacao.objects.create(nome=nome_simulacao, usuario=request.user)

        # Chamar a função de cálculo sem massa
        resultado_calculado = get_molecule_without_mass(
            maiores_massas, maiores_intensidades
        )

        # Calcular a soma total das chances
        total_chances = sum(
            detalhes["chance"] for detalhes in resultado_calculado.values()
        )

        # Criar os resultados com base nos valores calculados
        for molecula, detalhes in resultado_calculado.items():
            chance_porcentagem = (detalhes["chance"] / total_chances) * 100
            Resultado.objects.create(
                simulacao=simulacao,
                massa=detalhes["mass"],
                resultado=molecula,
                chance=chance_porcentagem,
            )

        return redirect("process_mass_values", id=simulacao.id)


class ResultadosView(LoginRequiredMixin, TemplateView):
    template_name = "simulation/resultados_list.html"

    def get(self, request, *args, **kwargs):
        # Filtra as simulações pelo usuário autenticado
        simulacoes = Simulacao.objects.filter(usuario=request.user).order_by(
            "-data_criacao"
        )
        return render(request, self.template_name, {"simulacoes": simulacoes})


class ProcessMassValuesView(LoginRequiredMixin, TemplateView):
    template_name = "simulation/resultados.html"

    def get(self, request, id, *args, **kwargs):
        simulacao = get_object_or_404(Simulacao, id=id, usuario=request.user)
        resultados = Resultado.objects.filter(simulacao=simulacao)
        return render(
            request,
            self.template_name,
            {"simulacao": simulacao, "resultados": resultados},
        )


class DeletarSimulacaoView(LoginRequiredMixin, TemplateView):
    def post(self, request, id, *args, **kwargs):
        simulacao = get_object_or_404(Simulacao, id=id, usuario=request.user)
        simulacao.delete()
        return redirect("resultados_view")
