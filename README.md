# Rhythm Quantization Project

This repository contains a Python project for rhythm quantization, a process that involves converting musical onsets (from audio analysis) into a regular rhythmic grid using highly-readable and playable conventional notation. Rhythm quantization plays a crucial role in ensuring precise and synchronized performances of complex musical compositions. Thus, this project is created as an assistive tool for my doctoral dissertation, a large-scale orchestral piece scheduled to be completed in 2023.

## Project Overview

The project consists of several utility functions and algorithms to perform rhythm quantization and related tasks. The main components of the project are as follows:

- `pre_clustering`: This module implements pre-clustering of musical onsets using K-means clustering. Onsets are grouped into clusters to facilitate subsequent quantization. The current implementation requires the input sequence of onsets to be in the OpenMusic format (LISP).

- `rhythm_quantization`: This module performs rhythm quantization on the grouped onsets/durations using an optimization approach. It finds the optimal tempo for quantization and identifies the closest standard durations for each actual duration.

- `OM_PY_utilities`: This module provides utility functions to convert data between Python data structures and OpenMusic format (LISP), allowing seamless integration with OpenMusic.

- `main.py`: This module is the main body that you can run to get the quantization information. When you run 'main.py', it reads the onset data from 'input.txt', performs pre-clustering using the 'pre_clustering' module, and then applies rhythm quantization using the 'rhythm_quantization' module. The quantization results, including the optimized tempo, time signatures, standard durations, and other relevant information for each group of onsets, will be saved in the 'output.txt' file.

## How to Use

1. Clone the repository to your local machine using the following command: `git clone <https://github.com/lang216/Not-Too-Crazy-Rhythm-Quantization.git>`.

2. Install the required dependencies, such as numpy and scikit-learn. The list of required packages will be provided in the 'requirements.txt' file (to be released).

3. Prepare your rhythm data: Open or create a text file (rename it to 'input.txt') containing a sequence of onsets in the OpenMusic format (LISP). You can use the 'convert_to_om' function from 'OM_PY_utilities' to convert a Python list to an OpenMusic (LISP) list. The time unit used thoroughly is ms.

6. Apply rhythm quantization:
- Simply run 'main.py' to execute the quantization process.
- The script will generate a text file named 'output.txt' that contains all the information needed for further use in OpenMusic. All the numeric outputs are provided in the OpenMusic (LISP) format.
- You can set the maximum number of sections the original onset sequence is broken into. The default value is 10. Additionally, you can customize the divisions by modifying the 'divisions' list in the 'rhythm_quantization' module. The default divisions are [1/32, 1/24, 1/20, 1/28, 1/18].

8. Customize the quantization parameters: Adjust the 'tempo_range' and 'divisions' in the 'rhythm_quantization' module to meet your specific musical requirements.

9. View the results: The 'output.txt' file will contain the optimized tempo, time signatures, standard durations, and other relevant information for each group of onsets after quantization.

## Note

This project is intended for educational and experimental purposes. Feel free to use and modify the code to suit your needs. If you find this project helpful or have suggestions for improvements, we welcome contributions and feedback.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
