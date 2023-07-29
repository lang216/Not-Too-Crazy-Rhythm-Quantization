import pre_clustering
import rhythm_quantization
from OM_PY_utilities import *

# a = {7: [0], 19: [12322.217], 1: [24811.536, 31860.036], 21: [39328.81], 14: [47870.47], 20: [55266.125, 60201.1], 4: [67175.805, 74380.86], 10: [78470.836, 83391.766], 17: [89259.29, 95528.73], 2: [99839.86, 105037.985, 111063.56], 12: [114528.57, 117969.11, 122112.05], 5: [127287.266, 132293.75, 136244.77], 8: [140130.52, 144461.46, 147843.96], 13: [151340.92, 155392.27, 158417.57], 0: [162046.39, 166379.74, 170033.94], 16: [174426.4, 177024.58, 180506.96], 11: [184661.28, 189162.05], 6: [192452.8, 195574.96, 198110.17], 15: [201143.77, 204016.55, 207488.4], 3: [211472.66, 214603.35], 18: [217753.8, 220764.0], 9: [224482.97, 228154.63, 232000.07]}
# b = [a[e] for e in a.keys()]

# print(x_2_dx(b))

def main(onsets, max_num_clusters=10, divisions=[1/32, 1/24, 1/20, 1/28]):
    tmp = {}
    best_grouped_onsets_final = []
    best_grouped_durations = []
    best_result = []
    best_total_error = float('inf')

    for n_c in range(1, max_num_clusters+1):
        grouped_onsets = pre_clustering.group_onsets(onsets, n_c)
        grouped_onsets_final = [grouped_onsets[e] for e in grouped_onsets.keys()]
        grouped_durations = x_2_dx(grouped_onsets_final)
        result = [rhythm_quantization.get_optimized_tempo(durations, divisions) for durations in grouped_durations]
        #result = [optimized_tempo, closest_standard_durations, multipliers, corresponding_divisions]
        
        total_error = sum([calculate_error(actual_dur, res[1])[2]
                           for actual_dur, res in zip(grouped_durations, result)])

        tmp[total_error] = n_c

        # Update the best results if the current one is better
        if total_error < best_total_error:
            best_grouped_onsets_final = grouped_onsets_final
            best_grouped_durations = grouped_durations
            best_result = result
            best_total_error = total_error

    optimized_n_c = tmp[best_total_error]

    return optimized_n_c, best_grouped_onsets_final, best_grouped_durations, best_result, best_total_error
    
 
if __name__ == "__main__":

    txt_file = './input.txt'

    #please change the onsets according to your own need
    #onsets = om_to_python('(0 211 424 13063 13764 13998 26178 26989 28018 36155)')
    onsets = om_to_python(get_durations(txt_file))

    #please change the smallest note divisions you want to use
    divisions=[1/32, 1/24, 1/20, 1/28] 

    optimized_n_c, best_grouped_onsets_final, best_grouped_durations, best_result, best_total_error= main(onsets,max_num_clusters=len(onsets), divisions=divisions)

    list_of_tempo = [get_tempo(e) for e in best_result]
    list_of_standard_duartions = [get_standard_duration(e) for e in best_result]
    list_of_durations_of_each_section = [sum(s_d) for s_d in list_of_standard_duartions]
    list_of_number_of_beats = [get_number_of_beat(e) for e in best_result]
    list_of_note_values = [get_note_value(e) for e in best_result]
    list_of_time_signature = [make_time_signature(l_n_b, l_n_v) for l_n_b, l_n_v in zip(list_of_number_of_beats, list_of_note_values)] #not real time sigature, just for the purpose of output


    #output the information to output.txt - numeric data is organized in the format of OpenMusic
    with open('./output.txt', 'w') as f:
            f.write('Optimized Number of Sections: '+str(optimized_n_c) + '\n'+'\n')
            f.write('Best Total Error: '+str(best_total_error) + '\n'+'\n')
            f.write('Duration Of Each Section: '+convert_to_om(list_of_durations_of_each_section) + '\n'+'\n')
            f.write('Time Signatures: '+convert_to_om(list_of_time_signature) + '\n'+'\n')
            f.write('Tempi: '+convert_to_om(list_of_tempo) + '\n'+'\n')
            f.write('Durations Of Each Note: '+convert_to_om(list_of_standard_duartions) + '\n'+'\n')
            #f.write('Details for Each Section: '+convert_to_om(best_result))

