from fractions import Fraction
import re
import numpy as np

# Read the content of a text file
def read_txt_file(filename):
    with open(filename, 'r') as f:
        return f.read()

# Get rhythm durations from a file
def get_durations(filename):
    return read_txt_file(filename)

def om_to_python(om_list_str):
    # Initialize an empty list to store the parsed elements
    python_list = []

    # Define a regular expression to match digits and fractions in the input string
    pattern = r"(\d+/\d+|\d+)"

    # Find all matches of the pattern in the input string
    matches = re.findall(pattern, om_list_str)

    for match in matches:
        # If the match is a fraction (e.g., '1/2'), convert it to a Python Fraction
        if '/' in match:
            numerator, denominator = map(int, match.split('/'))
            element = Fraction(numerator, denominator)
        else:
            # If the match is an integer, convert it to an integer
            element = int(match)

        # Append the parsed element to the Python list
        python_list.append(element)

    return python_list

def convert_to_om(data):
    if isinstance(data, list):
        return list_to_om(data)
    elif isinstance(data, tuple):
        return tuple_to_om(data)
    elif isinstance(data, Fraction):
        return fraction_to_om(data)
    elif isinstance(data, int):
        # Handle integer data by converting it to a string representation
        return str(data)
    elif isinstance(data, float):
        # Handle float data by converting it to a string representation
        return str(data)
    else:
        # For unsupported data types, convert to a string representation
        return str(data)

def list_to_om(lst):
    # Helper function to convert elements of the list recursively
    def convert_element(element):
        if isinstance(element, list):
            # If the element is a nested list, recursively convert it
            return list_to_om(element)
        elif isinstance(element, tuple):
            # If the element is a tuple, recursively convert it
            return tuple_to_om(element)
        elif isinstance(element, Fraction):
            # If the element is a Fraction, convert it to the OpenMusic format
            return fraction_to_om(element)
        else:
            # For other data types (int, float), convert to a string representation
            return str(element)

    # Use the helper function to convert each element of the list
    om_elements = [convert_element(element) for element in lst]
    # Join the converted elements and format the list as OpenMusic text format
    return "(" + " ".join(om_elements) + ")"

def tuple_to_om(tpl):
    # Helper function to convert elements of the tuple recursively
    def convert_element(element):
        if isinstance(element, list):
            # If the element is a nested list, recursively convert it
            return list_to_om(element)
        elif isinstance(element, tuple):
            # If the element is a nested tuple, recursively convert it
            return tuple_to_om(element)
        elif isinstance(element, Fraction):
            # If the element is a Fraction, convert it to the OpenMusic format
            return fraction_to_om(element)
        else:
            # For other data types (int, float), convert to a string representation
            return str(element)

    # Use the helper function to convert each element of the tuple
    om_elements = [convert_element(element) for element in tpl]
    # Join the converted elements and format the tuple as OpenMusic text format
    return "(" + " ".join(om_elements) + ")"

def fraction_to_om(fraction):
    return f"{fraction.numerator}/{fraction.denominator}"


def calculate_error(original_durations, quantized_durations):
    if len(original_durations) != len(quantized_durations):
        raise ValueError("The lengths of original_durations and quantized_durations must be the same.")
    
    errors = np.sum(np.array(original_durations) - np.array(quantized_durations))
    errors_abs = np.abs(errors)
    return errors


def x_2_dx(lox):
    lodx = []
    for i in range(len(lox)-1):
        lodx.append(lox[i+1]-lox[i])
    return lodx


def get_tempo(result):
    return result[0]

def get_standard_duration(result):
    return result[1]

def get_number_of_beat(result):
    return result[2]

def get_note_value(result):
    return result[3]

def make_time_signature(l_n_b, l_n_v):
    l_t_s = []
    for i in range(len(l_n_b)):
        l_t_s.append(l_n_b[i] * l_n_v[i])
    return l_t_s
