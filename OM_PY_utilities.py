from fractions import Fraction
import re
import numpy as np
from math import gcd

# Read the content of a text file
def read_txt_file(filename):
    with open(filename, 'r') as f:
        return f.read()

# Get rhythm durations from a file
def get_durations(filename):
    return read_txt_file(filename)

from fractions import Fraction
import re

def om_to_python(om_list_str):
    # Define a regular expression to match elements in the OpenMusic list
    pattern = r"\(([^()]+)\)"

    # Find all matches of the pattern in the input string
    matches = re.findall(pattern, om_list_str)

    def convert_element(element):
        # If the element contains parentheses, it is a nested list or tuple
        if '(' in element and ')' in element:
            return om_to_python(element)
        else:
            # Split the element by spaces and convert each part individually
            elements = element.split()
            return [int(e) if e.isdigit() else float(e) for e in elements]

    # Use the helper function to convert each element of the list
    python_list = [convert_element(match) for match in matches]

    # If there is only one element in the python_list, return it as the final result
    if len(python_list) == 1:
        return python_list[0]

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
    
    simple_errors = np.array(original_durations) - np.array(quantized_durations)
    literal_errors = np.sum(np.abs(simple_errors))
    overall_errors = np.sum(simple_errors)
    overall_errors_abs = np.abs(overall_errors)
    return overall_errors, overall_errors_abs, literal_errors


def x_2_dx(lox):

    # Function to preprocess the input list and convert non-list elements into single-element lists
    def preprocess_input_list(input_list):
        processed_list = []
        sublist = []
        for element in input_list:
            if isinstance(element, list):
                if sublist:
                    processed_list.append(sublist)
                    sublist = []
                processed_list.append(element)
            else:
                sublist.append(element)
        if sublist:
            processed_list.append(sublist)
        return processed_list
    # Preprocess the input list to convert non-list elements into single-element lists
    lox = preprocess_input_list(lox)

    # Step 1: Append the first element of the next internal list to the end of each internal list
    def append_next_element_to_end(list_of_lists):
        result = []
        for i in range(len(list_of_lists)):
            sublist = list_of_lists[i]
            if i < len(list_of_lists) - 1:
                next_sublist = list_of_lists[i + 1]
                sublist = sublist + [next_sublist[0]]
            result.append(sublist)
        return result

    # Step 2: Append the first element of the next internal list to the end of each internal list
    lox = append_next_element_to_end(lox)

    # Step 3: Calculate the durations between adjacent onsets within each sublist using list comprehension
    lodx = [[sublist[i + 1] - sublist[i] for i in range(len(sublist) - 1)] for sublist in lox]
   
    # Step 4: Remove the empty list at the end, if present
    if lodx and not lodx[-1]:
        lodx.pop()
    
    # Step 5: Return the list of lists containing the durations between adjacent onsets
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
