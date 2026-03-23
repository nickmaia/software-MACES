from deap import creator, base, tools, algorithms
import random
import numpy as np
from .utils.fitness_function import *
import concurrent
from concurrent.futures import ThreadPoolExecutor
from .utils.elitms import *
from pprint import pprint
import torch
from .utils.mlp import MLP
import json


def gene(lower: float, upper: float):
    return random.uniform(lower, upper)


def init_toolbox(
    components: dict, mass: int, mlp_solution, MASS_WEIGTH=1000, MLP_WEIGHT=0
):
    # register components, mass, mlpsolution
    toolbox = base.Toolbox()
    toolbox.components = components
    toolbox.mass = mass
    toolbox.mlp_solution = mlp_solution
    toolbox.MASS_WEIGTH = MASS_WEIGTH

    # PARAMETERS
    element_list = list(components.keys())
    lower_boundaries_list = [0 for element in element_list]  # fmt: skip
    upper_boundaries_list = [mass // components[element]["mass"] for element in element_list]  # fmt: skip
    ETA = 10

    # STRUCTURE
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("ChromosomeStruct", list, fitness=creator.FitnessMin)

    # GENES
    gene_functions = ()
    for element, lower, upper in zip(
        element_list, lower_boundaries_list, upper_boundaries_list
    ):
        toolbox.register(f"Gene_{element}", gene, lower=lower, upper=upper)  # fmt: skip
        gene_functions += (toolbox.__getattribute__(f"Gene_{element}"),)
    toolbox.register("individual", tools.initCycle, creator.ChromosomeStruct, gene_functions, n=1)  # fmt: skip
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # OPERATORS
    toolbox.register("evaluate", fitness_function, componentes=components, MASS_WEIGTH=MASS_WEIGTH, MLP_WEIGHT=MLP_WEIGHT, ESPECTOMETER_MASS=mass, mlp_solution=mlp_solution)  # fmt: skip
    toolbox.register("select", tools.selTournament, tournsize=5)
    toolbox.register("mate", tools.cxSimulatedBinaryBounded, low=lower_boundaries_list, up=upper_boundaries_list, eta=ETA)  # fmt: skip
    toolbox.register("mutate", tools.mutPolynomialBounded, low=lower_boundaries_list, up=upper_boundaries_list, eta=ETA, indpb= 1 / len(element_list))  # fmt: skip

    return toolbox


def init_stats_hof(hof_size=10):
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)
    hof = tools.HallOfFame(hof_size)
    return stats, hof


def run_evolution(toolbox, stats, hof, population_size, ngen, cxpb, mutpb, verbose=True):  # fmt: skip
    population = toolbox.population(n=population_size)
    population, log = eaSimpleWithElitism(
        population,
        toolbox,
        cxpb=cxpb,
        mutpb=mutpb,
        ngen=ngen,
        stats=stats,
        halloffame=hof,
        verbose=verbose,
    )
    return population, log, hof


def serie_niching(
    toolbox, stats, hof, population_size, ngen, cxpb, mutpb, verbose=True, run_number=4
):

    def run_single_evolution(run_code):
        stats, hof = init_stats_hof(round(population_size * 0.1))
        population, log, hof = run_evolution(toolbox, stats, hof, population_size, ngen, cxpb, mutpb, verbose)  # fmt: skip
        return hof[0:10], run_code

    best_list = []
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(run_single_evolution, run_code) for run_code in range(run_number)]  # fmt: skip
        for future in concurrent.futures.as_completed(futures):
            hof, run_code = future.result()
            fitness = fitness_function(
                hof[0],
                toolbox.components,
                2,
                toolbox.mass,
                toolbox.MASS_WEIGTH,
                toolbox.mlp_solution,
            )
            best_list.append((fitness, hof[0], run_code))

    best_list.sort(key=lambda x: x[0])

    return best_list


def load_model(input_dim=21, hidden_dim=526, output_dim=21, mode="with_mass"):
    assert mode in [
        "with_mass",
        "without_mass",
    ], "Mode need to be 'with_mass' or 'without_mass'"
    if mode == "with_mass":
        weigths = torch.load(
            f"GA/checkpoints/model_with_mass_700_checkpoint.pth",
            weights_only=True,
            map_location=torch.device("cpu"),
        )
        model = MLP(input_dim, hidden_dim, output_dim).to("cpu")
        model.load_state_dict(weigths)
        return model
    elif mode == "without_mass":
        weigths = torch.load(
            f"GA/checkpoints/model_without_mass_120_checkpoint.pth",
            weights_only=True,
            map_location=torch.device("cpu"),
        )
        model_mass = MLP(20, hidden_dim, 1).to("cpu")
        model_mass.load_state_dict(weigths)
        weigths = torch.load(
            f"GA/checkpoints/model_with_mass_700_checkpoint.pth",
            weights_only=True,
            map_location=torch.device("cpu"),
        )
        model = MLP(input_dim, hidden_dim, output_dim).to("cpu")
        model.load_state_dict(weigths)
        return model_mass, model


def get_molecule_with_mass(
    spectrum_weigth, spectrum_intensity, mass, verbose=False, run_number=8
):

    # assert 0 <= mass <= 2681, "Element mass need to be between 0 and 2681"
    # assert len(spectrum_weigth) == 10, "Spectrum need to have 10 mass peaks"
    # assert len(spectrum_intensity) == 10, "Spectrum need to have 10 intensity peaks"

    spectrum = []
    for weigth, intensity in zip(spectrum_weigth, spectrum_intensity):
        spectrum.append(weigth)
        spectrum.append(intensity)

    with open("GA/checkpoints/all_elements.json") as f:
        componentes = json.load(f)

    # SELECTING ELEMENTS
    model = load_model()
    prediction = model(torch.tensor(spectrum + [mass]).float())
    prediction = prediction.round_().tolist()
    columns = [
        "C",
        "H",
        "N",
        "O",
        "Br",
        "S",
        "F",
        "Cl",
        "P",
        "As",
        "I",
        "Na",
        "Si",
        "Al",
        "B",
        "Co",
        "Cr",
        "Se",
        "Fe",
        "K",
        "Au",
    ]
    element_index = [i for i in range(len(prediction)) if prediction[i] > 0]

    # GENETIC ALGORITHM
    population_size = 1000
    ngen = 125
    cxpb = 1
    mutpb = 0.25
    mlp_solution = [prediction[i] for i in element_index]
    columns = [columns[i] for i in element_index]
    componentes = {key: componentes[key] for key in columns}
    toolbox = init_toolbox(componentes, mass, mlp_solution)
    stats, hof = init_stats_hof(round(population_size * 0.1))

    # pack, time = run_evolution(toolbox, stats, hof, population_size, ngen, cxpb, mutpb, verbose=False)
    # population, log, hof = pack

    best_list = serie_niching(
        toolbox,
        stats,
        hof,
        population_size,
        ngen,
        cxpb,
        mutpb,
        False,
        run_number=run_number,
    )
    best = best_list[0][1]

    response = {}
    for i, item in enumerate(best_list):
        molecule = list(map(round, item[1]))
        mass = mass_balance(molecule, componentes)
        molecule_string = ""
        for element in range(len(molecule)):
            molecule_string += f"{columns[element]}{molecule[element]}"

        if molecule_string not in response:
            response[molecule_string] = {"mass": mass, "chance": 1}
        else:
            response[molecule_string]["chance"] += 1

    if verbose:
        pprint(response)

    return response


def get_molecule_without_mass(
    spectrum_weigth, spectrum_intensity, verbose=False, run_number=4
):
    # assert len(spectrum_weigth) == 10, "Spectrum need to have 10 mass peaks"
    # assert len(spectrum_intensity) == 10, "Spectrum need to have 10 intensity peaks"

    spectrum = []
    for weigth, intensity in zip(spectrum_weigth, spectrum_intensity):
        spectrum.append(weigth)
        spectrum.append(intensity)

    with open("GA/checkpoints/all_elements.json") as f:
        componentes = json.load(f)

    # SELECTING ELEMENTS
    model_mass, model = load_model(mode="without_mass")
    mass = model_mass(torch.tensor(spectrum).float()).tolist()[0]
    prediction = model(torch.tensor(spectrum + [mass]).float())
    prediction = prediction.round_().tolist()
    columns = [
        "C",
        "H",
        "N",
        "O",
        "Br",
        "S",
        "F",
        "Cl",
        "P",
        "As",
        "I",
        "Na",
        "Si",
        "Al",
        "B",
        "Co",
        "Cr",
        "Se",
        "Fe",
        "K",
        "Au",
    ]
    element_index = [i for i in range(len(prediction)) if prediction[i] > 0]

    # GENETIC ALGORITHM
    population_size = 500
    ngen = 150
    cxpb = 1
    mutpb = 0.25
    mlp_solution = [prediction[i] for i in element_index]
    columns = [columns[i] for i in element_index]
    componentes = {key: componentes[key] for key in columns}
    toolbox = init_toolbox(
        componentes, mass, mlp_solution, MASS_WEIGTH=2, MLP_WEIGHT=0.25
    )
    stats, hof = init_stats_hof(round(population_size * 0.1))

    # pack, time = run_evolution(toolbox, stats, hof, population_size, ngen, cxpb, mutpb, verbose=False)
    # population, log, hof = pack

    best_list = serie_niching(
        toolbox,
        stats,
        hof,
        population_size,
        ngen,
        cxpb,
        mutpb,
        False,
        run_number=run_number,
    )
    best = best_list[0][1]

    response = {}
    for i, item in enumerate(best_list):
        molecule = list(map(round, item[1]))
        mass = mass_balance(molecule, componentes)
        molecule_string = ""
        for element in range(len(molecule)):
            molecule_string += f"{columns[element]}{molecule[element]}"

        if molecule_string not in response:
            response[molecule_string] = {"mass": mass, "chance": 1}
        else:
            response[molecule_string]["chance"] += 1

    if verbose:
        pprint(response)

    return response


# fmt: off
if __name__ == "__main__":
    answer = [10., 15.,  1.,  2.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0., 0.,  0.,  0.,  0.,  0.,  0.,  0.]
    spectrum_weigth = [165.0000, 123.0000, 150.0000, 95.0000, 137.0000, 166.0000, 135.0000, 105.0000, 183.0000, 182.0000]
    spectrum_intensity = [9.0909, 4.6523, 3.9698, 1.3464, 1.0428, 0.7415, 0.6274, 0.5478, 0.5225, 0.5087]
    mass = 181.2350

    best = get_molecule_with_mass(spectrum_weigth, spectrum_intensity, mass)
    print(best)

    best_without_mass = get_molecule_without_mass(spectrum_weigth, spectrum_intensity)
    print(best_without_mass)


# fmt: on

# model = MLP(input_dim, hidden_dim, output_dim).to(device)
# model.load_state_dict(torch.load('model_1000_checkpoint.pth'))
# history = train_model(model, X_train, X_test, y_train, y_test, 20000, 100, 1)
