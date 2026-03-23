from django.db import models

from accounts.models import User


class Simulacao(models.Model):
    nome = models.CharField(max_length=255)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"Simulação {self.nome} - {self.data_criacao.strftime('%Y-%m-%d %H:%M:%S')}"
        )


class Resultado(models.Model):
    simulacao = models.ForeignKey(
        Simulacao, related_name="resultados", on_delete=models.CASCADE
    )
    massa = models.FloatField()
    resultado = models.CharField(max_length=255)
    chance = models.FloatField()

    def __str__(self):
        return f"Resultado {self.id} - Massa: {self.massa}"
