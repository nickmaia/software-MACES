# MACES

**MACES** (Molecular Analysis and Composition Estimation System) é um software para análise estrutural de moléculas orgânicas a partir de espectros de massas. O projeto combina redes neurais artificiais do tipo MLP com algoritmos genéticos para estimar massa molecular e composição elementar, oferecendo suporte computacional para problemas de determinação estrutural em química, farmácia e áreas correlatas.

## Visão geral

A interpretação de espectros de massas é uma etapa essencial na caracterização de pequenas moléculas, mas pode ser trabalhosa, demorada e fortemente dependente de conhecimento especializado. O MACES foi desenvolvido para automatizar parte desse processo por meio de técnicas de aprendizado de máquina e otimização evolutiva.

O sistema foi concebido como uma ferramenta científica com aplicação em:

- Química orgânica.
- Química medicinal.
- Farmácia.
- Análise de metabólitos.
- Caracterização de compostos orgânicos.

## Objetivo do software

O objetivo do MACES é estimar propriedades moleculares de compostos orgânicos a partir de espectros de massas, com foco em:

- Predição de massa molecular.
- Estimativa de composição elementar.
- Refinamento das soluções por algoritmo genético.
- Apoio à análise estrutural de pequenas moléculas.

## Contribuição científica

A principal contribuição científica do MACES está na integração de duas abordagens computacionais em um único fluxo de análise:

1. **Redes neurais MLP** para predição inicial de massa molecular e composição molecular.
2. **Algoritmo genético** para refinamento das soluções preditas, considerando balanço de massa e proximidade em relação à saída da rede neural.

Essa abordagem híbrida transforma um processo tradicionalmente manual em um pipeline reproduzível e orientado por dados, contribuindo para o desenvolvimento de software científico aplicado à espectrometria de massas.

## Metodologia

A metodologia do MACES segue um fluxo sistemático que vai desde a coleta e preparação dos dados até a modelagem com redes neurais artificiais e o refinamento por algoritmo genético. Inicialmente, os espectros de massas foram extraídos da base **MassBank of North America (MoNA)** e submetidos a um processo rigoroso de pré-processamento para garantir qualidade, consistência e padronização dos registros utilizados no estudo.

Foram selecionados exclusivamente espectros provenientes de análises de cromatografia líquida acoplada à espectrometria de massas (CL-EM), totalizando inicialmente **160.993 espectros**. Após remoção de redundâncias, exclusão de registros sem informações essenciais e descarte de espectros com formatação inconsistente ou sem identificação molecular adequada, obteve-se um conjunto final de **26.579 espectros**.

Esses dados foram divididos em três subconjuntos:

- **Treinamento:** 17.010 espectros
- **Teste:** 5.316 espectros
- **Validação:** 4.253 espectros

As variáveis de entrada utilizadas no treinamento corresponderam aos **10 picos mais intensos** de cada espectro e às suas respectivas abundâncias relativas. Para garantir homogeneidade na escala dos dados, foi aplicada normalização com **StandardScaler**.

### Redes neurais

Foram desenvolvidos dois modelos de redes neurais artificiais do tipo **Multilayer Perceptron (MLP)**, ambos com duas camadas ocultas contendo **526 neurônios** cada.

- **MLP 1:** modelo de regressão para predição da massa molecular.
- **MLP 2:** modelo para predição da composição molecular, utilizando também a massa predita como atributo adicional.

Os modelos foram treinados com:

- Função de perda: **Mean Squared Error (MSE)**
- Otimizador: **Adam**
- Taxa de aprendizado inicial: **0.005**
- Número de épocas: **1000**

Durante o treinamento, foram monitoradas métricas como perda, acurácia, acurácia perfeita e erro absoluto médio (**MAE**).

### Algoritmo genético

Após a predição inicial com as redes neurais, foi implementado um algoritmo genético com o objetivo de refinar a composição molecular estimada. Nesse contexto, cada indivíduo da população representa uma composição molecular candidata, codificada como um vetor de valores em ponto flutuante.

O algoritmo genético foi estruturado com os seguintes operadores e estratégias:

- **Seleção:** Tournament Selection
- **Cruzamento:** Simulated Binary Crossover (SBX)
- **Mutação:** Polynomial Mutation
- **Estratégias adicionais:** elitismo e niching em série

A função de avaliação foi desenvolvida para equilibrar dois critérios principais:

1. **Precisão do balanço de massa**
2. **Proximidade da solução em relação à predição da MLP**

### Função de avaliação

A massa total da solução candidata é calculada por:

$$
M_{solução} = \sum_{i=1}^{n} n_i \cdot m_i
$$

em que $M_{solução}$ representa a massa total da solução candidata, $n_i$ é o número de unidades do componente $i$, e $m_i$ é a massa molar do componente $i$.

A diferença absoluta entre a massa da solução candidata e a massa ideal esperada é dada por:

$$
\Delta M = \left| M_{solução} - M_{ideal} \right| 
$$

Em seguida, calcula-se a distância de Manhattan entre a solução analisada e a solução predita pela rede neural:

$$
D_{Manhattan} = \sum_{i=1}^{n} \left| n_i - b_i \right| 
$$

em que $n_i$ representa o valor do componente $i$ na solução candidata e $b_i$ representa o valor correspondente predito pela MLP.

A diferença relativa por componente é calculada por:

$$
P_{relativa,i} = \frac{\left|n_i - b_i\right|}{b_i} 
$$

Com base nessa diferença relativa, define-se o multiplicador de penalização:

$$
M = 1 + \sum_{i=1}^{n}
\begin{cases}
P_{relativa,i} + MLP\_WEIGHT, & \text{se } P_{relativa,i} \geq 1 \\
P_{relativa,i} - 0.5 + MLP\_WEIGHT, & \text{se } 0.5 \leq P_{relativa,i} < 1
\end{cases} 
$$

Esse termo penaliza soluções que se afastam significativamente da composição estimada pela rede neural, favorecendo candidatos mais coerentes com a predição inicial.

Por fim, o score final utilizado pelo algoritmo genético é dado por:

$$
S = \left( \left| M_{sol} - M_{ideal} \right| \times MASS_{WEIGHT} \times M \right) + M 
$$

em que $S$ representa o valor da função objetivo a ser minimizado. Essa formulação integra o erro de massa e a divergência em relação à predição da MLP, conduzindo o algoritmo genético para soluções mais viáveis e quimicamente consistentes.

### Síntese do fluxo metodológico

De forma resumida, o pipeline do MACES pode ser descrito da seguinte forma:

1. Coleta de espectros no MoNA.
2. Pré-processamento e filtragem dos dados.
3. Extração dos principais picos espectrais.
4. Treinamento da MLP para predição de massa molecular.
5. Treinamento da MLP para predição de composição molecular.
6. Refinamento da solução com algoritmo genético.
7. Geração da composição molecular final estimada.

## Resultados

Os resultados obtidos no estudo mostraram desempenho promissor:

- Acurácia de **0.96** na predição de presença ou ausência de componentes moleculares.
- Redução do **MAE de 3.25 para 2.30** quando o algoritmo genético foi aplicado em cenários com massa previamente conhecida.
- Aumento da acurácia perfeita para **0.11** no cenário com massa atribuída.
- Limitações observadas quando a massa precisava ser predita, com aumento do MAE de **3.95 para 4.85**.

<img width="672" height="411" alt="{4F8BFA1E-36DF-4487-8463-8C3B1F897562}" src="https://github.com/user-attachments/assets/0bf06b48-860d-4d58-b158-7fd2b3c37c85" />
<img width="674" height="429" alt="{67CB1EE8-DA0D-4827-83A1-3A15C603A0CF}" src="https://github.com/user-attachments/assets/61d13c7f-b4e3-4943-a5f4-4317175a12fb" />


Esses resultados indicam que a integração entre MLP e algoritmo genético é especialmente útil quando há informação prévia da massa do composto.

<img width="620" height="707" alt="{7448722E-5E8B-4339-BAB6-B71368FABC5E}" src="https://github.com/user-attachments/assets/15b80f83-4e75-4996-b56e-29ec6e34cb86" />


## Tecnologias utilizadas

- Python
- Django
- Django REST Framework
- PyTorch
- DEAP
- NumPy
- torchvision
- torchaudio
- pandas
- scikit-learn
- HTML
- CSS
- JavaScript
- Gunicorn
- WhiteNoise
- PostgreSQL (via psycopg2)

## Dependências

O projeto utiliza as seguintes dependências Python:

```txt
asgiref==3.8.1
deap==1.4.1
dj-database-url==2.2.0
Django==4.2.14
djangorestframework==3.15.2
filelock==3.15.4
fsspec==2024.6.1
gunicorn==23.0.0
Jinja2==3.1.4
MarkupSafe==2.1.5
mpmath==1.3.0
networkx==3.2.1
numpy==1.26.4
packaging==24.1
pillow==10.4.0
psycopg2==2.9.9
sqlparse==0.5.1
sympy==1.13.2
torch==2.4.0
torchaudio==2.4.0
torchvision==0.19.0
typing_extensions==4.12.2
tzdata==2024.1
whitenoise==6.7.0
```

## Instalação

### 1. Clonar o repositório

```bash
git clone https://github.com/nickmaia/MACES.git
cd MACES
```

### 2. Criar e ativar ambiente virtual

#### Linux / macOS
```bash
python -m venv .venv
source .venv/bin/activate
```

#### Windows
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente

Se o projeto utilizar Django com banco de dados e configurações de produção, crie um arquivo `.env` ou configure as variáveis de ambiente necessárias, por exemplo:

```env
DEBUG=True
SECRET_KEY=sua_chave_secreta
DATABASE_URL=sqlite:///db.sqlite3
```

> Ajuste as variáveis conforme a implementação real do projeto.

### 5. Executar migrações

```bash
python manage.py migrate
```

### 6. Iniciar o servidor local

```bash
python manage.py runserver
```

A aplicação estará disponível em:

```txt
http://127.0.0.1:8000/
```

## Exemplo de uso

O fluxo de uso do MACES pode ser resumido em:

1. Inserir os dados espectrais de entrada.
2. Informar os valores de razão massa/carga (`m/z`) e intensidade.
3. Definir a massa-alvo, quando disponível.
4. Executar a predição com os modelos MLP.
5. Refinar a saída com o algoritmo genético.
6. Visualizar a composição molecular sugerida.

No estudo, foi utilizado o espectro de massas da **dopamina** como exemplo de demonstração da interface. A molécula **C8H11NO2** foi identificada na simulação com **50% de chance de acerto**.

## Estrutura sugerida do projeto

```txt
MACES/
├── GA/
├── accounts
├── backend/
├── home/
├── simulation/
├── static/
├── templates/
├── .gitignore
├── JS_auto_file.txt
├── LICENCE
├── README.md
├── laricitrin_C16_H12_O8_332_05.csv
├── manage.py
└── requirements.txt
```

> A estrutura real pode variar conforme a organização atual do repositório.

## Limitações

Apesar dos resultados promissores, algumas limitações foram observadas:

- Desempenho inferior quando a massa molecular não é previamente informada.
- Potencial viés da base de dados devido à predominância de compostos orgânicos.
- Necessidade de ampliar a diversidade química dos espectros analisados para melhorar a generalização.

## Repositório

Código-fonte disponível em:

[https://github.com/nickmaia/MACES.git](https://github.com/nickmaia/MACES.git)

## Autores

- **Isaac Miranda Camargos**
- **Nicole Maia Argondizzi**
- **Ana Claudia Granato Malpass**

## Citação sugerida

Se este software ou metodologia for utilizado em trabalhos acadêmicos, cite:

```txt
CAMARGOS, Isaac Miranda; ARGONDIZZI, Nicole Maia; MALPASS, Ana Claudia Granato.
Desenvolvimento do software MACES para análise estrutural de moléculas orgânicas
a partir da espectrometria de massas.
```

## Licença

```txt
MIT License
```
