from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import reduce


def mass_balance(solution: list, componentes: dict):
    elements_list = componentes.keys()
    mass_sum = 0
    for element, coef in zip(elements_list, solution):
        mass_sum += componentes[element]["mass"] * round(coef)
    return mass_sum


def fitness_function(solution: list, componentes: dict, MASS_WEIGTH, MLP_WEIGHT, ESPECTOMETER_MASS, mlp_solution=None):  # fmt: skip
    mass = mass_balance(solution, componentes)  # fmt: skip
    distance = (
        [abs(x1 - x2) for x1, x2 in zip(solution, mlp_solution)] if mlp_solution else 0
    )
    distance_limit = (
        [d / mlp for d, mlp in zip(distance, mlp_solution)] if mlp_solution else [0]
    )

    multiplayer = 1
    for d in distance_limit:
        if d >= 1:
            multiplayer += d**d + MLP_WEIGHT
        elif d >= 0.5:
            multiplayer += d - 0.5 + MLP_WEIGHT

    score = abs(mass - ESPECTOMETER_MASS) * MASS_WEIGTH * multiplayer
    return (score,)


def preprocess_componentes(componentes, ESPECTOMETER_MASS):
    componentes_temp = componentes.copy()
    for element in componentes.keys():
        max_element = ESPECTOMETER_MASS // componentes[element]["mass"]
        if max_element == 0:
            del componentes_temp[element]
            continue
        componentes_temp[element]["upper_boundary"] = max_element  # fmt: skip
    return componentes_temp


if __name__ == "__main__":
    componentes = {
        "H": {"mass": 1},
        "C": {"mass": 12},
        "O": {"mass": 16},
        "N": {"mass": 15},
        "Br^79": {"mass": 79},
        "Br^81": {"mass": 81},
    }

    molecule = [7, 3, 0, 0, 1, 0]
    mass_sum = mass_balance(molecule, componentes)
    print(mass_sum)
    score = fitness_function(molecule, componentes, 1, 122, mlp_solution=None)
    print(score)
