from scipy.optimize import minimize_scalar
from fractions import Fraction

# User-defined parameters
initial_tempo = 40
tempo_range = (40, 144)
#divisions = [1, 1/2, 1/4, 1/8, 1/16, 1/32, 1/3, 1/6, 1/12, 1/24, 1/5, 1/10, 1/20, 1/7, 1/14, 1/28, 1/9, 1/18]
divisions = [1/32, 1/24, 1/20, 1/28, 1/18]
#divisions = [1, 1/2, 1/4, 1/8, 1/16, 1/3, 1/6, 1/12, 1/5, 1/10, 1/7, 1/14, 1/9]
#actual_durations = [211, 213, 12639, 701, 234, 12180, 811, 1029, 8137, 1606, 104, 2210, 2194, 3074, 3797, 168, 1991]

def calculate_standard_durations(tempo, divisions):
    standard_durations = [(4 * 60 / tempo) * 1000 * division for division in divisions]
    return standard_durations

def find_closest_standard_duration(actual_duration, standard_durations, divisions):
    closest_duration = min(standard_durations, key=lambda x: abs(x - actual_duration))
    multiplier = max(round(actual_duration / closest_duration), 1)  # Ensure the multiplier is at least 1
    closest_index = standard_durations.index(closest_duration)
    closest_division = divisions[closest_index]
    closest_division_fraction = Fraction.from_float(closest_division).limit_denominator()  # Convert division to fraction
    return closest_duration * multiplier, multiplier, closest_division_fraction


def calculate_difference(actual_duration, closest_duration):
    return actual_duration - closest_duration


def objective_function(tempo, actual_durations, divisions):
    standard_durations = calculate_standard_durations(tempo, divisions)
    total_differences = sum(calculate_difference(actual_duration, find_closest_standard_duration(actual_duration, standard_durations, divisions)[0]) for actual_duration in actual_durations)
    return total_differences

def get_optimized_tempo(actual_durations, divisions):

    # Iterative optimization
    result = minimize_scalar(objective_function, bounds=tempo_range, args=(actual_durations, divisions), method='bounded')
    optimized_tempo = result.x

    # Calculate standard durations for the optimized tempo
    standard_durations = calculate_standard_durations(optimized_tempo, divisions)

    # Find closest standard durations, multipliers, and corresponding divisions for each actual duration
    closest_standard_durations, multipliers, corresponding_divisions = zip(*(find_closest_standard_duration(actual_duration, standard_durations, divisions) for actual_duration in actual_durations))

    return optimized_tempo, closest_standard_durations, multipliers, corresponding_divisions