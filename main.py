import pre_clustering
import rhythm_quantization
from OM_PY_utilities import *
import numpy as np

def main(onsets, max_num_clusters=10, divisions=[1/32, 1/24, 1/20, 1/28]):
    tmp = {}
    best_grouped_onsets_final = []
    best_grouped_durations = []
    best_result = []
    best_total_error = float('inf')

    for n_c in range(1, max_num_clusters + 1):
        grouped_onsets = pre_clustering.group_onsets(onsets, n_c)
        grouped_onsets_final = [grouped_onsets[e] for e in grouped_onsets.keys()]
        grouped_durations = [x_2_dx(lod) for lod in grouped_onsets_final]
        result = [rhythm_quantization.get_optimized_tempo(durations, divisions) for durations in grouped_durations]
        #result = [optimized_tempo, closest_standard_durations, multipliers, corresponding_divisions]

        total_error = sum([calculate_error(actual_dur, standard_dur[1])
                           for actual_dur, standard_dur in zip(grouped_durations, result)])

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
    
    onsets = om_to_python('(0 211 424 13063 13764 13998 26178 26989 28018 36155 37761 37865 40075 42269 45343 49140 49308 51299 55907 55924 60595 61504 63032 63835 64477 64582 70749 70794 74458 74537 74856 78589 79936 83015 88332 90504 92155 92357 93444 94096 94363 94774 96154 97374 98048 98684 101300 106131 110020 111171 113288 113515 114762 114939 115914 117752 119281 120624 122360 122491 122800 123346 123416 123862 124902 125611 128319 128940 129070 130265 130889 132606 133492 135340 135816 136549 138231 139060 139193 139639 139738 142181 145167 145213 146054 146354 147779 148669 152339 153049 153583 153669 154125 154522 154842 155167 156138 156526 156893 157732 157891 157930 158688 158952 159030 159506 160210 160692 161303 161313 162268 164620 164780 165759 165906 166903 167434 167597 167970 168276 168348 169202 169736 171429 171492 171709 172980 173142 174931 175224 176398 176730 177397 177455 179050 179172 179410 180380 181072 181689 182378 182792 183756 185286 186386 186574 186912 186957 188427 189224 189412 189701 191333 192812 193005 193456 193681 194728 195983 196569 196607 197315 198461 199544 202134 202308 202518 202908 203977 204357 206634 206957 207232 207610 207699 207957 209314 209693 210500 211519 211673 211675 213490 214661 214729 214967 214967 215078 215698 215847 216468 217084 217091 217231 218092 218294 218468 219033 219215 219668 219821 220104 220257 221384 221501 223598 224407 225008 225894 226636 228384 229813 229828 230152 231068 231105 231118 233943 236176 236456 236511 237513 237760 239783 239889 239975 240308 241791 242231 242389 243758 245035 245626 246177 248974 249108 249235 250022 250493 250838 252057 252932 253574 254104 254865 255708 255894 256810 256826 257613 259371 268845 272385 272385)')
    divisions=[1/32, 1/24, 1/20, 1/28]

    optimized_n_c, best_grouped_onsets_final, best_grouped_durations, best_result, best_total_error= main(onsets)

    list_of_tempo = [get_tempo(e) for e in best_result]
    list_of_standard_duartions = [get_standard_duration(e) for e in best_result]
    list_of_durations_of_each_section = [sum(s_d) for s_d in list_of_standard_duartions]
    list_of_number_of_beats = [get_number_of_beat(e) for e in best_result]
    list_of_note_values = [get_note_value(e) for e in best_result]
    list_of_time_signature = [make_time_signature(l_n_b, l_n_v) for l_n_b, l_n_v in zip(list_of_number_of_beats, list_of_note_values)]

    with open('output.txt', 'w') as f:
            f.write('Optimized Number of Sections: '+str(optimized_n_c) + '\n'+'\n')
            f.write('Best Total Error: '+str(best_total_error) + '\n'+'\n')
            f.write('Duration Of Each Section: '+convert_to_om(list_of_durations_of_each_section) + '\n'+'\n')
            f.write('Time Signatures: '+convert_to_om(list_of_time_signature) + '\n'+'\n')
            f.write('Tempi: '+convert_to_om(list_of_tempo) + '\n'+'\n')
            f.write('Durations Of Each Note: '+convert_to_om(list_of_standard_duartions) + '\n'+'\n')
            f.write('Details for Each Section: '+convert_to_om(best_result))

