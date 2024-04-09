import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

name_cage = 'EFAU003'
date = '31032021'
connection = sqlite3.connect(f"X:\Data_LMT_3_mice\Expe1_Single_lever_food_{name_cage}/Expe1_Single_lever_food_{date}/Expe1_Single_lever_food_{date}.sqlite")
c = connection.cursor()

day = 2592000
hour= day / 24

# For EFAU-006 Day 20210508, experiment stopped at 20:30 so we have to re-calculate the two next days (add the 2nd day of 20210507 to the first day of 20210508 recalculated with the new "day" value)
#day = 2181800

# To sort the ID of the animals and to class in ascending order
req = 'select RFID from Animal'
c.execute(req)
ID_animal = c.fetchall()
ID_animal = pd.DataFrame(ID_animal)
ID_animal = pd.DataFrame.sort_values(ID_animal, by=0, ascending=True)

#ID Animals
animal_1 = ID_animal.iloc[0, 0]
animal_2 = ID_animal.iloc[1, 0]
animal_3 = ID_animal.iloc[2, 0]

for i in range(0,25):
    for j in range (1,4):
        globals()[f'lever{j}_beam_not{j}_hour{i}'] = 0
        globals()[f'number_leverpress_{j}_hour{i}']=0
        globals()[f'number_beam_{j}_hour{i}'] = 0
        globals()[f'frame_beam{j}_hour{i}']=[]
        globals()[f'frame_lever{j}_hour{i}']=[]
        globals()[f'sequence_complete_animal{j}_hour{i}']=[]
        globals()[f'sequence_non_complete_animal{j}_hour{i}']=[]


latency=0

time=200


# Coordinates for lever_press zone: x = 250 and y = 350
list_frames_leverpress = pd.read_pickle(f"X:\Data_LMT_3_mice\Expe1_Single_lever_food_{name_cage}/Reward_lever/Expe1_Single_lever_food_{date}Reward_lever.pkl")
list_frames_beam = pd.read_pickle(f"X:\Data_LMT_3_mice\Expe1_Single_lever_food_{name_cage}/Beam_feeder/Expe1_Single_lever_food_{date}Beam_feeder.pkl")


# Coordinates for lever_press zone: x = 250 and y = 350
x_min_lever = 215
x_max_lever = 310
y_min_lever = 320
y_max_lever = 385

# Coordinates for Dispenser zone: x = 250 and y = 350
x_min_beam = 240
x_max_beam = 275
y_min_beam = 45
y_max_beam = 85

# Leverpress###############################################################################

for frame in (list_frames_leverpress):
    frame_number = 0
    query = f'select d.FRAMENUMBER, a.RFID, d.MASS_X, d.MASS_Y from animal a, detection d where a.ID = d.ANIMALID ' \
            f'and d.FRAMENUMBER = {frame}'

    c.execute(query)
    all_rows = c.fetchall()

    if len(all_rows) == 0:
        continue

    df_all = pd.DataFrame(all_rows)

    df_animal1 = df_all[df_all[1] == animal_1]
    df_animal2 = df_all[df_all[1] == animal_2]
    df_animal3 = df_all[df_all[1] == animal_3]

    if len(df_animal1) != 0:
        if x_min_lever <= df_animal1[2].iloc[frame_number] <= x_max_lever and y_min_lever <= df_animal1[3].iloc[frame_number] <= y_max_lever:
            for i in range(0, 25):
                lower_bound = i * hour
                upper_bound = (i + 1) * hour
                if lower_bound <= frame < upper_bound:
                    globals()[f'number_leverpress_1_hour{i}'] += 1
                    globals()[f'frame_lever1_hour{i}'].append(frame)
            total_leverpress_1 = sum(globals()[f"number_leverpress_1_hour{i}"] for i in range(0, 25))


    if len(df_animal2) != 0:
        if x_min_lever <= df_animal2[2].iloc[frame_number] <= x_max_lever and y_min_lever <= df_animal2[3].iloc[frame_number] <= y_max_lever:
            for i in range(0, 25):
                lower_bound = i * hour
                upper_bound = (i + 1) * hour
                if lower_bound <= frame < upper_bound:
                    globals()[f'number_leverpress_2_hour{i}'] += 1
                    globals()[f'frame_lever2_hour{i}'].append(frame)
            total_leverpress_2 = sum(globals()[f"number_leverpress_2_hour{i}"] for i in range(0, 25))


    if len(df_animal3) != 0:
        if x_min_lever <= df_animal3[2].iloc[frame_number] <= x_max_lever and y_min_lever <= df_animal3[3].iloc[frame_number] <= y_max_lever:
            for i in range(0, 25):
                lower_bound = i * hour
                upper_bound = (i + 1) * hour
                if lower_bound <= frame < upper_bound:
                    globals()[f'number_leverpress_3_hour{i}'] += 1
                    globals()[f'frame_lever3_hour{i}'].append(frame)
            total_leverpress_3 = sum(globals()[f"number_leverpress_3_hour{i}"] for i in range(0, 25))

frame_lever_1=[]
frame_lever_2=[]
frame_lever_3=[]

for i in range(0, 25):
    frame_lever_1.append(globals()[f'frame_lever1_hour{i}'])
#print(frame_beam_1)
for i in range(0, 25):
    frame_lever_2.append(globals()[f'frame_lever2_hour{i}'])
#print(frame_beam_2)
for i in range(0, 25):
    frame_lever_3.append(globals()[f'frame_lever3_hour{i}'])
#print(frame_beam_3)

#mettre tout sous forme de liste
liste_frame_lever_1 = []
liste_frame_lever_2 = []
liste_frame_lever_3 = []

for sous_liste in frame_lever_1:
    liste_frame_lever_1.extend(sous_liste)
print(f'frames lever 1:{liste_frame_lever_1}')


for sous_liste in frame_lever_2:
    liste_frame_lever_2.extend(sous_liste)
print(f'frames lever 2:{liste_frame_lever_2}')


for sous_liste in frame_lever_3:
    liste_frame_lever_3.extend(sous_liste)
print(f'frames lever 3:{liste_frame_lever_3}')




# Print the counts for each hour
# for i in range(0, 25):
#     print(f'Number of leverpress 1 in hour {i}: {globals()[f"number_leverpress_1_hour{i}"]}')
#
# for i in range(0, 25):
#     print(f'Number of leverpress 2 in hour {i}: {globals()[f"number_leverpress_2_hour{i}"]}')
#
#
# for i in range(0, 25):
#     print(f'Number of leverpress 3 in hour {i}: {globals()[f"number_leverpress_3_hour{i}"]}')


print(f'Total number of leverpress 1: {total_leverpress_1}')
y1_values_lever = [globals()[f'number_leverpress_1_hour{i}'] for i in range(0, 25)]
print(f'Total number of leverpress 2: {total_leverpress_2}')
y2_values_lever = [globals()[f'number_leverpress_2_hour{i}'] for i in range(0, 25)]
print(f'Total number of leverpress 3: {total_leverpress_3}')
y3_values_lever = [globals()[f'number_leverpress_3_hour{i}'] for i in range(0, 25)]

    # print the total
for i in range(0, 25):
    number_leverpress_total_i = globals()[f"number_leverpress_1_hour{i}"] + globals()[f"number_leverpress_2_hour{i}"] + globals()[f"number_leverpress_3_hour{i}"]
    #print(f'Number of leverpress total in hour {i}: {number_leverpress_total_i}')
number_leverpress_total = total_leverpress_1 + total_leverpress_2 + total_leverpress_3
#print(f'number_leverpress_total:{number_leverpress_total}')

#number of Beam#################################################################################################################################################################

for frame in list_frames_beam:
    frame_number = 0
    query = f'select d.FRAMENUMBER, a.RFID, d.MASS_X, d.MASS_Y from animal a, detection d where a.ID = d.ANIMALID ' \
            f'and d.FRAMENUMBER = {frame}'

    c.execute(query)
    all_rows = c.fetchall()

    if len(all_rows) == 0:
        continue

    df_all = pd.DataFrame(all_rows)

    df_animal1 = df_all[df_all[1] == animal_1]
    df_animal2 = df_all[df_all[1] == animal_2]
    df_animal3 = df_all[df_all[1] == animal_3]

    if len(df_animal1) != 0:
        if x_min_beam <= df_animal1[2].iloc[frame_number] <= x_max_beam and y_min_beam <= df_animal1[3].iloc[frame_number] <= y_max_beam:
            for i in range(0, 25):
                lower_bound = i * hour
                upper_bound = (i + 1) * hour
                if lower_bound <= frame < upper_bound:
                    globals()[f'number_beam_1_hour{i}'] += 1
                    globals()[f'frame_beam1_hour{i}'].append(frame)
            total_beam_1 = sum(globals()[f"number_beam_1_hour{i}"] for i in range(0, 25))



    if len(df_animal2) != 0:
        if x_min_beam <= df_animal2[2].iloc[frame_number] <= x_max_beam and y_min_beam <= df_animal2[3].iloc[frame_number] <= y_max_beam:
            for i in range(0, 25):
                lower_bound = i * hour
                upper_bound = (i + 1) * hour
                if lower_bound <= frame < upper_bound:
                    globals()[f'number_beam_2_hour{i}'] += 1
                    globals()[f'frame_beam2_hour{i}'].append(frame)
            total_beam_2 = sum(globals()[f"number_beam_2_hour{i}"] for i in range(0, 25))


    if len(df_animal3) != 0:
        if x_min_beam <= df_animal3[2].iloc[frame_number] <= x_max_beam and y_min_beam <= df_animal3[3].iloc[frame_number] <= y_max_beam:
            for i in range(0, 25):
                lower_bound = i * hour
                upper_bound = (i + 1) * hour
                if lower_bound <= frame < upper_bound:
                    globals()[f'number_beam_3_hour{i}'] += 1
                    globals()[f'frame_beam3_hour{i}'].append(frame)
            total_beam_3 = sum(globals()[f"number_beam_3_hour{i}"] for i in range(0, 25))



##liste de frames des beams pour chaque sous liste

frame_beam_1=[]
frame_beam_2=[]
frame_beam_3=[]

for i in range(0, 25):
    frame_beam_1.append(globals()[f'frame_beam1_hour{i}'])
#print(frame_beam_1)
for i in range(0, 25):
    frame_beam_2.append(globals()[f'frame_beam2_hour{i}'])
#print(frame_beam_2)
for i in range(0, 25):
    frame_beam_3.append(globals()[f'frame_beam3_hour{i}'])
#print(frame_beam_3)

#mettre tout sous forme de liste
liste_frame_beam_1 = []
liste_frame_beam_2 = []
liste_frame_beam_3 = []

for sous_liste in frame_beam_1:
    liste_frame_beam_1.extend(sous_liste)
print(f'frames beam 1:{liste_frame_beam_1}')

for sous_liste in frame_beam_2:
    liste_frame_beam_2.extend(sous_liste)
print(f'frames beam 2:{liste_frame_beam_2}')

for sous_liste in frame_beam_3:
    liste_frame_beam_3.extend(sous_liste)
print(f'frames beam 3:{liste_frame_beam_3}')


# for i in range(0, 25):
#     print(f'Number of beam 1 in hour {i}: {globals()[f"number_beam_1_hour{i}"]}')
#
#     # Print the counts for each hour 2
# for i in range(0, 25):
#     print(f'Number of beam 2 in hour {i}: {globals()[f"number_beam_2_hour{i}"]}')
#
#     # Print the counts for each hour 3
# for i in range(0, 25):
#     print(f'Number of beam 3 in hour {i}: {globals()[f"number_beam_3_hour{i}"]}')


print(f'Total number of beam 1: {total_beam_1}')
y1_values_beam = [globals()[f'number_beam_1_hour{i}'] for i in range(0, 25)]
print(f'Total number of beam 2: {total_beam_2}')
y2_values_beam = [globals()[f'number_beam_2_hour{i}'] for i in range(0, 25)]
print(f'Total number of beam 3: {total_beam_3}')
y3_values_beam = [globals()[f'number_beam_3_hour{i}'] for i in range(0, 25)]

    # print the total
for i in range(0, 25):
    number_beam_total_i = globals()[f"number_beam_1_hour{i}"] + globals()[f"number_beam_2_hour{i}"] + globals()[f"number_beam_3_hour{i}"]
    #print(f'Number of beam total in hour {i}: {number_beam_total_i}')
number_beam_total = total_beam_1 + total_beam_2 + total_beam_3
#print(f'number_beam_total:{number_beam_total}')





#Ratio Lever/Beam###############################################################################################################################################################

# print(f'liste beam souris 1:{y1_values_beam}')
print(f'liste lever souris 1:{y1_values_lever}')
# print(f'liste beam souris 2:{y2_values_beam}')
print(f'liste lever souris 2:{y2_values_lever}')
# print(f'liste beam souris 3:{y3_values_beam}')
print(f'liste lever souris 3:{y3_values_lever}')

y1_ratio=[]
y2_ratio=[]
y3_ratio=[]
for i in range (len(y1_values_lever)):
    if y1_values_beam[i]== 0:
        y1_ratio.append(0)
    else:
        y1_ratio.append(y1_values_lever[i]/y1_values_beam[i])
    if y2_values_beam[i] == 0:
        y2_ratio.append(0)
    else:
        y2_ratio.append(y2_values_lever[i] / y2_values_beam[i])
    if y3_values_beam[i]== 0:
        y3_ratio.append(0)
    else:
        y3_ratio.append(y3_values_lever[i] / y3_values_beam[i])
# print(f'ratio1:{y1_ratio}')
# print(f'ratio2:{y2_ratio}')
# print(f'ratio3:{y3_ratio}')


#Nombre de séquences complètes ################################################################################################################################################

for frame_lever in list_frames_leverpress:
    for j in range(0, len(list_frames_beam)):
        if frame_lever - list_frames_beam[j] < 0:  # CHOOSE THE NEGATIVE SUBTRACTION
            latency = [abs(frame_lever - list_frames_beam[j])]
            break  # To stop at the first negative value
    if abs(pd.DataFrame(latency).iloc[0, 0]) > 1000:  # Because above 1000 frame it does not mean anything
        continue



    query_lever = f'select d.FRAMENUMBER, a.RFID, d.MASS_X, d.MASS_Y from animal a, detection d where a.ID = d.ANIMALID ' \
            f'and d.FRAMENUMBER = {frame_lever}'

    query_beam = f'select d.FRAMENUMBER, a.RFID, d.MASS_X, d.MASS_Y from animal a, detection d where a.ID = d.ANIMALID ' \
             f'and d.FRAMENUMBER == {list_frames_beam[j]}'


    c.execute(query_lever)
    all_rows_lever = c.fetchall()

    c.execute(query_beam)
    all_rows_beam = c.fetchall()


    if len(all_rows_lever) == 0:
        continue

    df_all_lever = pd.DataFrame(all_rows_lever)

    if len(all_rows_beam) == 0:
        continue

    df_all_beam = pd.DataFrame(all_rows_beam)


    df_animal1_lever = df_all_lever[df_all_lever[1] == animal_1]
    df_animal2_lever = df_all_lever[df_all_lever[1] == animal_2]
    df_animal3_lever = df_all_lever[df_all_lever[1] == animal_3]

    df_animal1_beam = df_all_beam[df_all_beam[1] == animal_1]
    df_animal2_beam = df_all_beam[df_all_beam[1] == animal_2]
    df_animal3_beam = df_all_beam[df_all_beam[1] == animal_3]

    # To get the numbers of complete sequence for animal 1
    if len(df_animal1_lever) != 0 and len(df_animal1_beam) != 0:
        if x_min_lever <= df_animal1_lever.iloc[0, 2] <= x_max_lever and y_min_lever <= df_animal1_lever.iloc[0, 3] <= y_max_lever:
            if x_min_beam <= df_animal1_beam.iloc[0, 2] <= x_max_beam and y_min_beam <= df_animal1_beam.iloc[0, 3] <= y_max_beam:
                if abs(pd.DataFrame(latency).iloc[0, 0]) < time:
                    for i in range(0, 25):
                        lower_bound = i * hour
                        upper_bound = (i + 1) * hour
                        if lower_bound <= frame_lever < upper_bound:
                            globals()[f'sequence_complete_animal1_hour{i}'].append(frame_lever)


                    #list_beam_animal1_complete.append(list_frames_beam[j])

    # To get the numbers of complete sequence for animal 2
    if len(df_animal2_lever) != 0 and len(df_animal2_beam) != 0:
        if x_min_lever <= df_animal2_lever.iloc[0, 2] <= x_max_lever and y_min_lever <= df_animal2_lever.iloc[0, 3] <= y_max_lever:
            if x_min_beam <= df_animal2_beam.iloc[0, 2] <= x_max_beam and y_min_beam <= df_animal2_beam.iloc[0, 3] <= y_max_beam:
                if abs(pd.DataFrame(latency).iloc[0, 0]) < time:
                    for i in range(0, 25):
                        lower_bound = i * hour
                        upper_bound = (i + 1) * hour
                        if lower_bound<= frame_lever <upper_bound:
                            globals()[f'sequence_complete_animal2_hour{i}'].append(frame_lever)


    # To get the numbers of complete sequence for animal 3
    if len(df_animal3_lever) != 0 and len(df_animal3_beam) != 0:
        if x_min_lever <= df_animal3_lever.iloc[0, 2] <= x_max_lever and y_min_lever <= df_animal3_lever.iloc[0, 3] <= y_max_lever:
            if x_min_beam <= df_animal3_beam.iloc[0, 2] <= x_max_beam and y_min_beam <= df_animal3_beam.iloc[0, 3] <= y_max_beam:
                if abs(pd.DataFrame(latency).iloc[0, 0]) < time:
                    for i in range(0, 25):
                        lower_bound = i * hour
                        upper_bound = (i + 1) * hour
                        if lower_bound<= frame_lever <upper_bound:
                            globals()[f'sequence_complete_animal3_hour{i}'].append(frame_lever)

y1_values_sequence=[]
y2_values_sequence=[]
y3_values_sequence=[]


frame_sequence_1=[]
frame_sequence_2=[]
frame_sequence_3=[]

for i in range (0,25):
    globals()[f'nb_sequence_animal1_hour{i}']=len(globals()[f'sequence_complete_animal1_hour{i}'])
    frame_sequence_1.append(globals()[f'sequence_complete_animal1_hour{i}'])
#print(f'frames des séquences souris 1:{frame_sequence_1}')
#print(f'number of sequence 1 hour {i} : {globals()[f"nb_sequence_animal1_hour{i}"]}')
for i in range(0, 25):
    globals()[f'nb_sequence_animal2_hour{i}'] = len(globals()[f'sequence_complete_animal2_hour{i}'])
    frame_sequence_2.append(globals()[f'sequence_complete_animal2_hour{i}'])
#print(f'frames des séquences souris 2:{frame_sequence_2}')
#print(f'number of sequence 2 hour {i} : {globals()[f"nb_sequence_animal2_hour{i}"]}')
for i in range(0, 25):
    globals()[f'nb_sequence_animal3_hour{i}'] = len(globals()[f'sequence_complete_animal3_hour{i}'])
    frame_sequence_3.append(globals()[f'sequence_complete_animal3_hour{i}'])
#print(f'frames des séquences souris 3:{frame_sequence_3}')
#print(f'number of sequence 3 hour {i} : {globals()[f"nb_sequence_animal3_hour{i}"]}')


y1_values_sequence=[globals()[f'nb_sequence_animal1_hour{i}'] for i in range(0,25)]
y2_values_sequence=[globals()[f'nb_sequence_animal2_hour{i}'] for i in range(0,25)]
y3_values_sequence=[globals()[f'nb_sequence_animal3_hour{i}'] for i in range(0,25)]
# print(f'sequence 1: {y1_values_sequence}')
# print(f'sequence 2: {y2_values_sequence}')
# print(f'sequence 3: {y3_values_sequence}')

total_sequence_1 = sum(globals()[f"nb_sequence_animal1_hour{i}"] for i in range(0, 25))
print(f'total sequence animal 1: {total_sequence_1}')
total_sequence_2 = sum(globals()[f"nb_sequence_animal2_hour{i}"] for i in range(0, 25))
print(f'total sequence animal 2: {total_sequence_2}')
total_sequence_3 = sum(globals()[f"nb_sequence_animal3_hour{i}"] for i in range(0, 25))
print(f'total sequence animal 3: {total_sequence_3}')

#frames des levers correspondant aux sequences complètes
liste_frame_sequence_1 = []
liste_frame_sequence_2 = []
liste_frame_sequence_3 = []

for sous_liste in frame_sequence_1:
    liste_frame_sequence_1.extend(sous_liste)
print(f'frames sequence 1:{liste_frame_sequence_1}')

for sous_liste in frame_sequence_2:
    liste_frame_sequence_2.extend(sous_liste)
print(f'frames sequence 2:{liste_frame_sequence_2}')

for sous_liste in frame_sequence_3:
    liste_frame_sequence_3.extend(sous_liste)
print(f'frames sequence 3:{liste_frame_sequence_3}')


#number of lever followed by a beam from a different mouse############################################################################################################

not_sequence_1=[]
not_sequence_2=[]
not_sequence_3=[]
y_values_lever_not_beam_1=[]
y_values_lever_not_beam_2=[]
y_values_lever_not_beam_3=[]

for frame_lever in liste_frame_lever_1:
    frame_beam_proche = None
    distance_min = float('inf')
    for frame_beam in list_frames_beam:
        if frame_beam > frame_lever:
            distance_actuelle = frame_beam - frame_lever
            if distance_actuelle < distance_min:
                distance_min = distance_actuelle
                frame_beam_proche = frame_beam
    if frame_beam_proche is not None and frame_beam_proche not in liste_frame_beam_1:
        not_sequence_1.append(frame_beam_proche)
print(f'lever not beam 1 frames:{not_sequence_1}')
print(f'lever not beam 1 total:{len(not_sequence_1)}')

for i in range(0, 25):
    lower_bound = i * hour
    upper_bound = (i + 1) * hour
    for frame in not_sequence_1:
        if lower_bound < frame <upper_bound:
            globals()[f'lever1_beam_not1_hour{i}']+=1

y_values_lever_not_beam_1=[globals()[f'lever1_beam_not1_hour{i}'] for i in range(0,25)]
print(f'liste_lever_not_beam_1:{y_values_lever_not_beam_1}')



for frame_lever in liste_frame_lever_2:
    frame_beam_proche = None
    distance_min = float('inf')
    for frame_beam in list_frames_beam:
        if frame_beam > frame_lever:
            distance_actuelle2 = frame_beam - frame_lever
            if distance_actuelle2 < distance_min:
                distance_min = distance_actuelle2
                frame_beam_proche = frame_beam
    if frame_beam_proche is not None and frame_beam_proche not in liste_frame_beam_2:
        not_sequence_2.append(frame_beam_proche)
print(f'lever not beam 2 frames:{not_sequence_2}')
print(f'lever not beam 2 total:{len(not_sequence_2)}')

for i in range(0, 25):
    lower_bound = i * hour
    upper_bound = (i + 1) * hour
    for frame in not_sequence_2:
        if lower_bound < frame <upper_bound:
            globals()[f'lever2_beam_not2_hour{i}']+=1

y_values_lever_not_beam_2=[globals()[f'lever2_beam_not2_hour{i}'] for i in range(0,25)]
print(f'liste_lever_not_beam_2:{y_values_lever_not_beam_2}')


for frame_lever in liste_frame_lever_3:
    frame_beam_proche = None
    distance_min = float('inf')
    for frame_beam in list_frames_beam:
        if frame_beam > frame_lever:
            distance_actuelle = frame_beam - frame_lever
            if distance_actuelle <= distance_min:
                distance_min = distance_actuelle
                frame_beam_proche = frame_beam
    if frame_beam_proche is not None and frame_beam_proche not in liste_frame_beam_3:
        not_sequence_3.append(frame_beam_proche)
print(f'lever not beam 3 frames:{not_sequence_3}')
print(f'lever not beam 3 total:{len(not_sequence_3)}')

for i in range(0, 25):
    lower_bound = i * hour
    upper_bound = (i + 1) * hour
    for frame in not_sequence_3:
        if frame is not None and lower_bound < frame <upper_bound:
            globals()[f'lever3_beam_not3_hour{i}']+=1

y_values_lever_not_beam_3=[globals()[f'lever3_beam_not3_hour{i}'] for i in range(0,25)]
print(f'liste_lever_not_beam_3:{y_values_lever_not_beam_3}')

#Ratio lever not followed by a beam of the same mouse / total of lever####################################################################################
y_ratio_lever_not_beam_1=[]
y_ratio_lever_not_beam_2=[]
y_ratio_lever_not_beam_3=[]
for i in range (len(y1_values_lever)):
    if y1_values_lever[i]== 0:
        y_ratio_lever_not_beam_1.append(0)
    else:
        y_ratio_lever_not_beam_1.append(y_values_lever_not_beam_1[i]/y1_values_lever[i])
    if y2_values_lever[i]== 0:
        y_ratio_lever_not_beam_2.append(0)
    else:
        y_ratio_lever_not_beam_2.append(y_values_lever_not_beam_2[i]/y2_values_lever[i])
    if y3_values_lever[i]== 0:
        y_ratio_lever_not_beam_3.append(0)
    else:
        y_ratio_lever_not_beam_3.append(y_values_lever_not_beam_3[i]/y3_values_lever[i])
print(f'list ratio lever no beam 1:{y_ratio_lever_not_beam_1}')
print(f'list ratio lever no beam 2:{y_ratio_lever_not_beam_2}')
print(f'list ratio lever no beam 3:{y_ratio_lever_not_beam_3}')



#Percentage complete sequences ###################################################################################################################################################

y1_sq_ratio=[]
y2_sq_ratio=[]
y3_sq_ratio=[]
for i in range (len(y1_values_sequence)):
    if y1_values_lever[i]== 0:
        y1_sq_ratio.append(0)
    else:
        y1_sq_ratio.append(y1_values_sequence[i]/y1_values_lever[i])
    if y2_values_lever[i] == 0:
        y2_sq_ratio.append(0)
    else:
        y2_sq_ratio.append(y2_values_sequence[i] / y2_values_lever[i])
    if y3_values_lever[i]== 0:
        y3_sq_ratio.append(0)
    else:
        y3_sq_ratio.append(y3_values_sequence[i] / y3_values_lever[i])
print(f'percentage complete sequences 1:{y1_sq_ratio}')
print(f'percentage complete sequences 2:{y2_sq_ratio}')
print(f'percentage complete sequences 3:{y3_sq_ratio}')


#Time between lever and beam before the first complete sequence#####################################################################################

data_time_before_sequence= []
data_mean_before_sequence = []
data_time_between_sequence = []
data_mean_between_sequence = []

time_before_sequence_1=[]
time_before_sequence_2=[]
time_before_sequence_3=[]

if len(liste_frame_sequence_1)!=0:
    for frame_lever in liste_frame_lever_1:
        frame_beam_proche = None
        distance_min = float('inf')
        time=0
        if frame_lever == liste_frame_sequence_1[0]:
            break
        for frame_beam in liste_frame_beam_1:
            if frame_beam > frame_lever:
                distance_actuelle = frame_beam - frame_lever
                if distance_actuelle < distance_min:
                    distance_min = distance_actuelle
                    frame_beam_proche = frame_beam
                    time=(frame_beam-frame_lever)/30
                    time_before_sequence_1.append(time)

print(f'times between lever and beam before the first complete sequence mouse 1: {time_before_sequence_1}')
print(f'number of leverpress before the first complete sequence mouse 1:{len(time_before_sequence_1)}')
if len(liste_frame_sequence_1)!=0 and len(time_before_sequence_1)!=0:
    print(f'time mean of leverpress before the first complete sequence mouse 1:{sum(time_before_sequence_1)/len(time_before_sequence_1)}')


if len(liste_frame_sequence_2)!=0:
    for frame_lever in liste_frame_lever_2:
        frame_beam_proche = None
        distance_min = float('inf')
        time=0
        if frame_lever == liste_frame_sequence_2[0]:
            break
        for frame_beam in liste_frame_beam_2:
            if frame_beam > frame_lever:
                distance_actuelle = frame_beam - frame_lever
                if distance_actuelle < distance_min:
                    distance_min = distance_actuelle
                    frame_beam_proche = frame_beam
                    time=(frame_beam-frame_lever)/30
                    time_before_sequence_2.append(time)

print(f'times between lever and beam before the first complete sequence mouse 2: {time_before_sequence_2}')
print(f'number of leverpress before the first complete sequence mouse 2:{len(time_before_sequence_2)}')
if len(liste_frame_sequence_2)!=0 and len(time_before_sequence_2)!=0:
    print(f'time mean of leverpress before the first complete sequence mouse 2:{sum(time_before_sequence_2)/len(time_before_sequence_2)}')


if len(liste_frame_sequence_3)!=0:
    for frame_lever in liste_frame_lever_3:
        frame_beam_proche = None
        distance_min = float('inf')
        time=0
        if frame_lever == liste_frame_sequence_3[0]:
            break
        for frame_beam in liste_frame_beam_3:
            if frame_beam > frame_lever:
                distance_actuelle = frame_beam - frame_lever
                if distance_actuelle < distance_min:
                    distance_min = distance_actuelle
                    frame_beam_proche = frame_beam
                    time=(frame_beam-frame_lever)/30
                    time_before_sequence_3.append(time)

print(f'times between lever and beam before the first complete sequence mouse 3: {time_before_sequence_3}')
print(f'number of leverpress before the first complete sequence mouse 3:{len(time_before_sequence_3)}')
if len(liste_frame_sequence_3)!=0 and len(time_before_sequence_3)!=0:
    print(f'time mean of leverpress before the first complete sequence mouse 3:{sum(time_before_sequence_3)/len(time_before_sequence_3)}')


# time between the 2 first complete sequences##########

time_between_sequence_1=[]
time_between_sequence_2=[]
time_between_sequence_3=[]

if len(liste_frame_sequence_1)>1:
    for frame_lever in liste_frame_lever_1:
        if liste_frame_sequence_1[0] <= frame_lever <= liste_frame_sequence_1[1]:
            frame_beam_proche = None
            distance_min = float('inf')
            time=0
            for frame_beam in liste_frame_beam_1:
                if frame_beam > frame_lever:
                    distance_actuelle = frame_beam - frame_lever
                    if distance_actuelle < distance_min:
                        distance_min = distance_actuelle
                        frame_beam_proche = frame_beam
                        time=(frame_beam-frame_lever)/30
                        time_between_sequence_1.append(time)

print(f'times between lever and beam before the first two complete sequences mouse 1: {time_between_sequence_1}')
print(f'number of leverpress between the first two complete sequences mouse 1:{len(time_between_sequence_1)}')
if len(liste_frame_sequence_1)!=0 and len(time_between_sequence_1)!=0:
    print(f'time mean of leverpress between the first two complete sequences mouse 1:{sum(time_between_sequence_1)/len(time_between_sequence_1)}')


if len(liste_frame_sequence_2)>1:
    for frame_lever in liste_frame_lever_2:
        if liste_frame_sequence_2[0] <= frame_lever <= liste_frame_sequence_2[1]:
            frame_beam_proche = None
            distance_min = float('inf')
            time=0
            for frame_beam in liste_frame_beam_2:
                if frame_beam > frame_lever:
                    distance_actuelle = frame_beam - frame_lever
                    if distance_actuelle < distance_min:
                        distance_min = distance_actuelle
                        frame_beam_proche = frame_beam
                        time=(frame_beam-frame_lever)/30
                        time_between_sequence_2.append(time)

print(f'times between lever and beam before the first two complete sequences mouse 2: {time_between_sequence_2}')
print(f'number of leverpress between the first two complete sequences mouse 2:{len(time_between_sequence_2)}')
if len(liste_frame_sequence_2)!=0 and len(time_between_sequence_2)!=0:
    print(f'time mean of leverpress between the first two complete sequences mouse 2:{sum(time_between_sequence_2)/len(time_between_sequence_2)}')


if len(liste_frame_sequence_3)>1:
    for frame_lever in liste_frame_lever_3:
        if liste_frame_sequence_3[0] < frame_lever < liste_frame_sequence_3[1]:
            frame_beam_proche = None
            distance_min = float('inf')
            time=0
            for frame_beam in liste_frame_beam_3:
                if frame_beam > frame_lever:
                    distance_actuelle = frame_beam - frame_lever
                    if distance_actuelle < distance_min:
                        distance_min = distance_actuelle
                        frame_beam_proche = frame_beam
                        time=(frame_beam-frame_lever)/30
                        time_between_sequence_3.append(time)

print(f'times between lever and beam before the first two complete sequences mouse 3: {time_between_sequence_3}')
print(f'number of leverpress between the first two complete sequences mouse 3:{len(time_between_sequence_3)}')
if len(liste_frame_sequence_3)!=0 and len(time_between_sequence_3)!=0:
    print(f'time mean of leverpress between the first two complete sequences mouse 3:{sum(time_between_sequence_3)/len(time_between_sequence_3)}')

l=max(len(time_before_sequence_1),len(time_before_sequence_2),len(time_before_sequence_3))
print(l)
for i in range (len(time_before_sequence_1),l):
    time_before_sequence_1.append(0)
print(time_before_sequence_1)

for i in range (len(time_before_sequence_2),l):
    time_before_sequence_2.append(0)
print(time_before_sequence_2)

for i in range (len(time_before_sequence_3),l):
    time_before_sequence_3.append(0)
print(time_before_sequence_3)

h=max(len(time_between_sequence_1),len(time_between_sequence_2),len(time_between_sequence_3))
print(h)
for i in range (len(time_between_sequence_1),h):
    time_between_sequence_1.append(0)
print(time_between_sequence_1)

for i in range (len(time_between_sequence_2),h):
    time_between_sequence_2.append(0)
print(time_between_sequence_2)

for i in range (len(time_between_sequence_3),h):
    time_between_sequence_3.append(0)
print(time_between_sequence_3)




# excel ###########################################################################################################################################################################

excel_file_path_lever = "C:/Users/LMT3-B7bis/Desktop/bm stage/number_lever_first_day2.xlsx"
excel_file_path_beam = "C:/Users/LMT3-B7bis/Desktop/bm stage/number_beam_first_day2.xlsx"
excel_file_path_sequences = "C:/Users/LMT3-B7bis/Desktop/bm stage/number_sequences_first_day2.xlsx"
excel_file_path_unfollowed = "C:/Users/LMT3-B7bis/Desktop/bm stage/number_unfollowed_lever_first_day.xlsx"
excel_file_path_time_before_sequence1="C:/Users/LMT3-B7bis/Desktop/bm stage/time_before_sequence1.xlsx"
excel_file_path_time_between_sequence12="C:/Users/LMT3-B7bis/Desktop/bm stage/time_between_sequence12.xlsx"



df_file_lever = pd.read_excel(excel_file_path_lever)
df_file_beam = pd.read_excel(excel_file_path_beam)
df_file_sequences = pd.read_excel(excel_file_path_sequences)
df_file_unfollowed = pd.read_excel(excel_file_path_unfollowed)
df_file_before = pd.read_excel(excel_file_path_time_before_sequence1)
df_file_between = pd.read_excel(excel_file_path_time_between_sequence12)

data_lever = {
    f'Mouse_1_{name_cage}_{date}': y1_values_lever,
    f'Mouse_2_{name_cage}_{date}': y2_values_lever,
    f'Mouse_3_{name_cage}_{date}': y3_values_lever
}

df_lever = pd.DataFrame(data_lever)
df_combined_lever = pd.concat([df_file_lever, df_lever], axis=1)
df_combined_lever.to_excel(excel_file_path_lever, index=False)
#print(df_lever)
print(f'Data has been written to {excel_file_path_lever}')


data_beam = {
    f'Mouse_1_{name_cage}_{date}': y1_values_beam,
    f'Mouse_2_{name_cage}_{date}': y2_values_beam,
    f'Mouse_3_{name_cage}_{date}': y3_values_beam
}
df_beam = pd.DataFrame(data_beam)
df_combined_beam = pd.concat([df_file_beam, df_beam], axis=1)
df_combined_beam.to_excel(excel_file_path_beam, index=False)
#print(df_beam)
print(f'Data has been written to {excel_file_path_beam}')


data_sequences = {
    f'Mouse_1_{name_cage}_{date}': y1_values_sequence,
    f'Mouse_2_{name_cage}_{date}': y2_values_sequence,
    f'Mouse_3_{name_cage}_{date}': y3_values_sequence
}
df_sequences = pd.DataFrame(data_sequences)
df_combined_sequences = pd.concat([df_file_sequences, df_sequences], axis=1)
df_combined_sequences.to_excel(excel_file_path_sequences, index=False)
#print(df_sequences)
print(f'Data has been written to {excel_file_path_sequences}')



data_unfollowed = {
    f'Mouse_1_{name_cage}_{date}': y_values_lever_not_beam_1,
    f'Mouse_2_{name_cage}_{date}': y_values_lever_not_beam_2,
    f'Mouse_3_{name_cage}_{date}': y_values_lever_not_beam_3
}
df_unfollowed = pd.DataFrame(data_unfollowed)
df_combined_unfollowed = pd.concat([df_file_unfollowed, df_unfollowed], axis=1)
df_combined_unfollowed.to_excel(excel_file_path_unfollowed, index=False)
#print(df_unfollowed)
print(f'Data has been written to {excel_file_path_unfollowed}')

data_times_before_sequence1 = {
    f'Mouse_1_{name_cage}_{date}': time_before_sequence_1,
    f'Mouse_2_{name_cage}_{date}': time_before_sequence_2,
    f'Mouse_3_{name_cage}_{date}': time_before_sequence_3
}
df_before = pd.DataFrame(data_times_before_sequence1)
df_combined_before = pd.concat([df_file_before, df_before], axis=1)
df_combined_before.to_excel(excel_file_path_time_before_sequence1, index=False)
#print(df_sequences)
print(f'Data has been written to {excel_file_path_time_before_sequence1}')


data_times_between_sequence12 = {
    f'Mouse_1_{name_cage}_{date}': time_between_sequence_1,
    f'Mouse_2_{name_cage}_{date}': time_between_sequence_2,
    f'Mouse_3_{name_cage}_{date}': time_between_sequence_3
}
df_between = pd.DataFrame(data_times_between_sequence12)
df_combined_between = pd.concat([df_file_between, df_between], axis=1)
df_combined_between.to_excel(excel_file_path_time_between_sequence12, index=False)
#print(df_sequences)
print(f'Data has been written to {excel_file_path_unfollowed}')

data_lever = {
    f'Mouse_1_{name_cage}_{date}': y1_values_lever,
    f'Mouse_2_{name_cage}_{date}': y2_values_lever,
    f'Mouse_3_{name_cage}_{date}': y3_values_lever
}

data_beam = {
    f'Mouse_1_{name_cage}_{date}': y1_values_beam,
    f'Mouse_2_{name_cage}_{date}': y2_values_beam,
    f'Mouse_3_{name_cage}_{date}': y3_values_beam
}

data_sequences = {
    f'Mouse_1_{name_cage}_{date}': y1_values_sequence,
    f'Mouse_2_{name_cage}_{date}': y2_values_sequence,
    f'Mouse_3_{name_cage}_{date}': y3_values_sequence
}

df_lever = pd.DataFrame(data_lever)
df_beam = pd.DataFrame(data_beam)
df_sequences = pd.DataFrame(data_sequences)





#Graphes###############################################################################################################################################


plt.figure(figsize=(15,10))
plt.subplot(2,3,1)
plt.plot(range(0, 25), y1_values_lever, label='Mouse1_lever', color='red', marker='+')
plt.plot(range(0, 25), y2_values_lever, label='Mouse2_lever', color='green', marker='+')
plt.plot(range(0, 25), y3_values_lever, label='Mouse3_lever', color='blue', marker='+')
plt.plot(range(0, 25), y1_values_beam, label='Mouse1_beam', color='red',linestyle='dashed')
plt.plot(range(0, 25), y2_values_beam, label='Mouse2_beam', color='green',linestyle='dashed')
plt.plot(range(0, 25), y3_values_beam, label='Mouse3_beam', color='blue',linestyle='dashed')
plt.title('Number of Leverpress and Beam per hour')
plt.xlabel('Hour')
plt.ylabel('Number of Leverpress and Beam')
plt.legend()
plt.grid(True)

plt.subplot(2,3,2)
plt.plot(range(0,25),y1_ratio,label='ratio_1_lever/beam',color='red')
plt.plot(range(0,25),y2_ratio,label='ratio_2_lever/beam',color='green')
plt.plot(range(0,25),y3_ratio,label='ratio_3_lever/beam',color='blue')
plt.title('Ratio Leverpress / Beam per hour')
plt.xlabel('Hour')
plt.ylabel('Ratio Leverpress / Beam')
plt.legend()
plt.grid(True)

plt.subplot(2,3,3)
plt.plot(range(0, 25), y1_values_lever, label='Mouse1_lever', color='red', marker='+')
plt.plot(range(0, 25), y2_values_lever, label='Mouse2_lever', color='green', marker='+')
plt.plot(range(0, 25), y3_values_lever, label='Mouse3_lever', color='blue', marker='+')
plt.title('Number of Leverpress per hour')
plt.xlabel('Hour')
plt.ylabel('Number of Leverpress')
plt.legend()
plt.grid(True)

plt.subplot(2,3,4)
plt.plot(range(0,25), y1_values_sequence, label='Mouse1_sequence', color='red', marker='o')
plt.plot(range(0,25), y2_values_sequence, label='Mouse2_sequence', color='green', marker='o')
plt.plot(range(0,25), y3_values_sequence, label='Mouse3_sequence', color='blue', marker='o')
plt.title('Number of Sequence per hour')
plt.xlabel('Hour')
plt.ylabel('Number of Sequence')
plt.legend()
plt.grid(True)

plt.subplot(2,3,5)
plt.plot(range(0,25), y1_sq_ratio, label='mouse1_%seq', color='red')
plt.plot(range(0,25), y2_sq_ratio, label='mouse2_%seq', color='green')
plt.plot(range(0,25), y3_sq_ratio, label='mouse3_%seq', color='blue')
plt.title('Percentage of complete sequence per hour')
plt.xlabel('Hour')
plt.ylabel('percentage of complete sequence')
plt.legend()
plt.grid(True)

plt.subplot(2,3,6)
plt.plot(range(0,25),y_ratio_lever_not_beam_1, label='not_following_1',color='red', linestyle='dashed')
plt.plot(range(0,25),y_ratio_lever_not_beam_2, label='not_following_2',color='green', linestyle='dashed')
plt.plot(range(0,25),y_ratio_lever_not_beam_3, label='not_following_3',color='blue', linestyle='dashed')
plt.title('Percentage of unfollowed levers per hour')
plt.xlabel('Hour')
plt.ylabel('percentage of unfollowed levers')
plt.legend()
plt.grid(True)

plt.tight_layout
plt.show()