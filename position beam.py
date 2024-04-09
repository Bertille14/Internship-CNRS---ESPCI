import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

name_cage = 'EFAU0139_1'
date = '20230810'
connection = sqlite3.connect(f"X:\Data_LMT_1_mouse_females\Expe1_Single_lever_food_Alone_females_{name_cage}/Expe1_Single_lever_food_Alone_females_{date}/Expe1_Single_lever_food_Alone_females_{date}.sqlite")
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

for i in range(0,73):
    for j in range (1,4):
        globals()[f'lever{j}_beam_not{j}_hour{i}'] = 0
        globals()[f'number_leverpress_{j}_hour{i}']=0
        globals()[f'number_beam_{j}_hour{i}'] = 0
        globals()[f'frame_beam{j}_hour{i}']=[]
        globals()[f'frame_lever{j}_hour{i}']=[]
        globals()[f'sequence_complete_animal{j}_hour{i}']=[]
        globals()[f'sequence_non_complete_animal{j}_hour{i}']=[]
        globals()[f'position_beam{j}_hour{i}'] = 0
        globals()[f'frame_position_beam{j}_hour{i}']=[]
        globals()[f'position_lever{j}_hour{i}'] = 0
        globals()[f'frame_position_lever{j}_hour{i}'] = []
        globals()[f'position_nest{j}_hour{i}'] = 0
        globals()[f'frame_position_nest{j}_hour{i}'] = []
        globals()[f'position_beam{j}_3s_hour{i}'] = 0
        globals()[f'frame_position_beam{j}_3s_hour{i}'] = []
        globals()[f'position_lever{j}_3s_hour{i}'] = 0
        globals()[f'frame_position_lever{j}_3s_hour{i}'] = []
        globals()[f'position_nest{j}_3s_hour{i}'] = 0
        globals()[f'frame_position_nest{j}_3s_hour{i}'] = []
        globals()[f'after_lever{j}_nest1_hour{i}']=0
        globals()[f'after_lever{j}_nest2_hour{i}']=0
        globals()[f'after_lever{j}_nest3_hour{i}']=0
        globals()[f'after_lever{j}_beam1_hour{i}']=0
        globals()[f'after_lever{j}_beam2_hour{i}']=0
        globals()[f'after_lever{j}_beam3_hour{i}']=0
        globals()[f'after_lever{j}_lever1_hour{i}']=0
        globals()[f'after_lever{j}_lever2_hour{i}']=0
        globals()[f'after_lever{j}_lever3_hour{i}']=0



latency=0

time=200


# Coordinates for lever_press zone: x = 250 and y = 350
list_frames_leverpress = pd.read_pickle(f"X:\Data_LMT_1_mouse_females\Expe1_Single_lever_food_Alone_females_{name_cage}/Reward_lever/Expe1_Single_lever_food_Alone_females_{date}Reward_lever.pkl")
list_frames_beam = pd.read_pickle(f"X:\Data_LMT_1_mouse_females\Expe1_Single_lever_food_Alone_females_{name_cage}/Beam_feeder/Expe1_Single_lever_food_Alone_females_{date}Beam_feeder.pkl")
print(list_frames_leverpress)

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

# Coordinates for Nest zone: x = 250 and y = 350
x_min_nest = 191
x_max_nest = 297
y_min_nest = 192
y_max_nest = 255

#attribution levers
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
            for i in range(0, 73):
                lower_bound = i * hour
                upper_bound = (i + 1) * hour
                if lower_bound <= frame < upper_bound:
                    globals()[f'number_leverpress_1_hour{i}'] += 1
                    globals()[f'frame_lever1_hour{i}'].append(frame)
            total_leverpress_1 = sum(globals()[f"number_leverpress_1_hour{i}"] for i in range(0, 73))


    if len(df_animal2) != 0:
        if x_min_lever <= df_animal2[2].iloc[frame_number] <= x_max_lever and y_min_lever <= df_animal2[3].iloc[frame_number] <= y_max_lever:
            for i in range(0, 73):
                lower_bound = i * hour
                upper_bound = (i + 1) * hour
                if lower_bound <= frame < upper_bound:
                    globals()[f'number_leverpress_2_hour{i}'] += 1
                    globals()[f'frame_lever2_hour{i}'].append(frame)
            total_leverpress_2 = sum(globals()[f"number_leverpress_2_hour{i}"] for i in range(0, 73))


    if len(df_animal3) != 0:
        if x_min_lever <= df_animal3[2].iloc[frame_number] <= x_max_lever and y_min_lever <= df_animal3[3].iloc[frame_number] <= y_max_lever:
            for i in range(0, 73):
                lower_bound = i * hour
                upper_bound = (i + 1) * hour
                if lower_bound <= frame < upper_bound:
                    globals()[f'number_leverpress_3_hour{i}'] += 1
                    globals()[f'frame_lever3_hour{i}'].append(frame)
            total_leverpress_3 = sum(globals()[f"number_leverpress_3_hour{i}"] for i in range(0, 73))



frame_lever_1=[]
frame_lever_2=[]
frame_lever_3=[]

for i in range(0, 73):
    frame_lever_1.append(globals()[f'frame_lever1_hour{i}'])
#print(frame_beam_1)
for i in range(0, 73):
    frame_lever_2.append(globals()[f'frame_lever2_hour{i}'])
#print(frame_beam_2)
for i in range(0, 73):
    frame_lever_3.append(globals()[f'frame_lever3_hour{i}'])
#print(frame_beam_3)


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


print(f'Total number of leverpress 1: {total_leverpress_1}')
y1_values_lever = [globals()[f'number_leverpress_1_hour{i}'] for i in range(0, 73)]
print(f'Total number of leverpress 2: {total_leverpress_2}')
y2_values_lever = [globals()[f'number_leverpress_2_hour{i}'] for i in range(0, 73)]
print(f'Total number of leverpress 3: {total_leverpress_3}')
y3_values_lever = [globals()[f'number_leverpress_3_hour{i}'] for i in range(0, 73)]

#attribution beams
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
            for i in range(0, 73):
                lower_bound = i * hour
                upper_bound = (i + 1) * hour
                if lower_bound <= frame < upper_bound:
                    globals()[f'number_beam_1_hour{i}'] += 1
                    globals()[f'frame_beam1_hour{i}'].append(frame)
            total_beam_1 = sum(globals()[f"number_beam_1_hour{i}"] for i in range(0, 73))



    if len(df_animal2) != 0:
        if x_min_beam <= df_animal2[2].iloc[frame_number] <= x_max_beam and y_min_beam <= df_animal2[3].iloc[frame_number] <= y_max_beam:
            for i in range(0, 73):
                lower_bound = i * hour
                upper_bound = (i + 1) * hour
                if lower_bound <= frame < upper_bound:
                    globals()[f'number_beam_2_hour{i}'] += 1
                    globals()[f'frame_beam2_hour{i}'].append(frame)
            total_beam_2 = sum(globals()[f"number_beam_2_hour{i}"] for i in range(0, 73))


    if len(df_animal3) != 0:
        if x_min_beam <= df_animal3[2].iloc[frame_number] <= x_max_beam and y_min_beam <= df_animal3[3].iloc[frame_number] <= y_max_beam:
            for i in range(0, 73):
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

for i in range(0, 73):
    frame_beam_1.append(globals()[f'frame_beam1_hour{i}'])
#print(frame_beam_1)
for i in range(0, 73):
    frame_beam_2.append(globals()[f'frame_beam2_hour{i}'])
#print(frame_beam_2)
for i in range(0, 73):
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


### position 6 secondes before beam ##################################################################################################################################

#mouse1
liste_before_beam1=[]
for frame in liste_frame_beam_1:
    liste_before_beam1.append(frame-6*30)
print(liste_before_beam1)

for frame in liste_before_beam1:
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
            for i in range(0, 73):
                lower_bound = i * hour
                upper_bound = (i + 1) * hour
                if lower_bound <= frame < upper_bound:
                    globals()[f'position_beam1_hour{i}'] += 1
                    globals()[f'frame_position_beam1_hour{i}'].append(frame)
        if x_min_lever <= df_animal1[2].iloc[frame_number] <= x_max_lever and y_min_lever <= df_animal1[3].iloc[frame_number] <= y_max_lever:
            for i in range(0, 73):
                lower_bound = i * hour
                upper_bound = (i + 1) * hour
                if lower_bound <= frame < upper_bound:
                    globals()[f'position_lever1_hour{i}'] += 1
                    globals()[f'frame_position_lever1_hour{i}'].append(frame)
        if x_min_nest <= df_animal1[2].iloc[frame_number] <= x_max_nest and y_min_nest <= df_animal1[3].iloc[frame_number] <= y_max_nest:
            for i in range(0, 73):
                lower_bound = i * hour
                upper_bound = (i + 1) * hour
                if lower_bound <= frame < upper_bound:
                    globals()[f'position_nest1_hour{i}'] += 1
                    globals()[f'frame_position_nest1_hour{i}'].append(frame)

y1_position_beam = [globals()[f'position_beam1_hour{i}'] for i in range(0, 73)]
print(f'position of beam 6 secondes before mouse 1: {y1_position_beam}')
y1_position_lever = [globals()[f'position_lever1_hour{i}'] for i in range(0, 73)]
print(f'position of lever 6 secondes before mouse 1: {y1_position_lever}')
y1_position_nest = [globals()[f'position_nest1_hour{i}'] for i in range(0, 73)]
print(f'position of nest 6 secondes before mouse 1: {y1_position_nest}')



## mouse 2
liste_before_beam2=[]
for frame in liste_frame_beam_2:
    liste_before_beam2.append(frame-6*30)
print(liste_before_beam2)

for frame in liste_before_beam2:
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

    if len(df_animal2) != 0:
        if x_min_beam <= df_animal2[2].iloc[frame_number] <= x_max_beam and y_min_beam <= df_animal2[3].iloc[frame_number] <= y_max_beam:
            for i in range(0, 73):
                lower_bound = i * hour
                upper_bound = (i + 1) * hour
                if lower_bound <= frame < upper_bound:
                    globals()[f'position_beam2_hour{i}'] += 1
                    globals()[f'frame_position_beam2_hour{i}'].append(frame)
        if x_min_lever <= df_animal2[2].iloc[frame_number] <= x_max_lever and y_min_lever <= df_animal2[3].iloc[frame_number] <= y_max_lever:
            for i in range(0, 73):
                lower_bound = i * hour
                upper_bound = (i + 1) * hour
                if lower_bound <= frame < upper_bound:
                    globals()[f'position_lever2_hour{i}'] += 1
                    globals()[f'frame_position_lever2_hour{i}'].append(frame)
        if x_min_nest <= df_animal2[2].iloc[frame_number] <= x_max_nest and y_min_nest <= df_animal2[3].iloc[frame_number] <= y_max_nest:
            for i in range(0, 73):
                lower_bound = i * hour
                upper_bound = (i + 1) * hour
                if lower_bound <= frame < upper_bound:
                    globals()[f'position_nest2_hour{i}'] += 1
                    globals()[f'frame_position_nest2_hour{i}'].append(frame)

y2_position_beam = [globals()[f'position_beam2_hour{i}'] for i in range(0, 73)]
print(f'position of beam 6 secondes before mouse 2: {y2_position_beam}')
y2_position_lever = [globals()[f'position_lever2_hour{i}'] for i in range(0, 73)]
print(f'position of lever 6 secondes before mouse 2: {y2_position_lever}')
y2_position_nest = [globals()[f'position_nest2_hour{i}'] for i in range(0, 73)]
print(f'position of nest 6 secondes before mouse 2: {y2_position_nest}')


## mouse 3

liste_before_beam3=[]
for frame in liste_frame_beam_3:
    liste_before_beam3.append(frame-6*30)
print(liste_before_beam3)

for frame in liste_before_beam3:
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

    if len(df_animal3) != 0:
        if x_min_beam <= df_animal3[2].iloc[frame_number] <= x_max_beam and y_min_beam <= df_animal3[3].iloc[frame_number] <= y_max_beam:
            for i in range(0,73):
                lower_bound = i * hour
                upper_bound = (i + 1) * hour
                if lower_bound <= frame < upper_bound:
                    globals()[f'position_beam3_hour{i}'] += 1
                    globals()[f'frame_position_beam3_hour{i}'].append(frame)
        if x_min_lever <= df_animal3[2].iloc[frame_number] <= x_max_lever and y_min_lever <= df_animal3[3].iloc[frame_number] <= y_max_lever:
            for i in range(0, 73):
                lower_bound = i * hour
                upper_bound = (i + 1) * hour
                if lower_bound <= frame < upper_bound:
                    globals()[f'position_lever3_hour{i}'] += 1
                    globals()[f'frame_position_lever3_hour{i}'].append(frame)
        if x_min_nest <= df_animal3[2].iloc[frame_number] <= x_max_nest and y_min_nest <= df_animal3[3].iloc[frame_number] <= y_max_nest:
            for i in range(0, 73):
                lower_bound = i * hour
                upper_bound = (i + 1) * hour
                if lower_bound <= frame < upper_bound:
                    globals()[f'position_nest3_hour{i}'] += 1
                    globals()[f'frame_position_nest3_hour{i}'].append(frame)

y3_position_beam = [globals()[f'position_beam3_hour{i}'] for i in range(0, 73)]
print(f'position of beam 6 secondes before mouse 3: {y3_position_beam}')
y3_position_lever = [globals()[f'position_lever3_hour{i}'] for i in range(0, 73)]
print(f'position of lever 6 secondes before mouse 3: {y3_position_lever}')
y3_position_nest = [globals()[f'position_nest3_hour{i}'] for i in range(0, 73)]
print(f'position of nest 6 secondes before mouse 3: {y3_position_nest}')




# position 3 seconds before beam ##################################################################################################
# mouse 1
liste_before_beam1_3s=[]
for frame in liste_frame_beam_1:
    liste_before_beam1_3s.append(frame-3*30)
print(liste_before_beam1_3s)

for frame in liste_before_beam1_3s:
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
                    globals()[f'position_beam1_3s_hour{i}'] += 1
                    globals()[f'frame_position_beam1_3s_hour{i}'].append(frame)
        if x_min_lever <= df_animal1[2].iloc[frame_number] <= x_max_lever and y_min_lever <= df_animal1[3].iloc[frame_number] <= y_max_lever:
            for i in range(0, 25):
                lower_bound = i * hour
                upper_bound = (i + 1) * hour
                if lower_bound <= frame < upper_bound:
                    globals()[f'position_lever1_3s_hour{i}'] += 1
                    globals()[f'frame_position_lever1_3s_hour{i}'].append(frame)
        if x_min_nest <= df_animal1[2].iloc[frame_number] <= x_max_nest and y_min_nest <= df_animal1[3].iloc[frame_number] <= y_max_nest:
            for i in range(0, 25):
                lower_bound = i * hour
                upper_bound = (i + 1) * hour
                if lower_bound <= frame < upper_bound:
                    globals()[f'position_nest1_3s_hour{i}'] += 1
                    globals()[f'frame_position_nest1_3s_hour{i}'].append(frame)

y1_position_beam_3s = [globals()[f'position_beam1_3s_hour{i}'] for i in range(0, 25)]
print(f'position of beam 3 secondes before mouse 1: {y1_position_beam_3s}')
y1_position_lever_3s = [globals()[f'position_lever1_3s_hour{i}'] for i in range(0, 25)]
print(f'position of lever 3 secondes before mouse 1: {y1_position_lever_3s}')
y1_position_nest_3s = [globals()[f'position_nest1_3s_hour{i}'] for i in range(0, 25)]
print(f'position of nest 3 secondes before mouse 1: {y1_position_nest_3s}')

#mouse 2

liste_before_beam2_3s=[]
for frame in liste_frame_beam_2:
    liste_before_beam2_3s.append(frame-3*30)
print(liste_before_beam2_3s)

for frame in liste_before_beam2_3s:
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

    if len(df_animal2) != 0:
        if x_min_beam <= df_animal2[2].iloc[frame_number] <= x_max_beam and y_min_beam <= df_animal2[3].iloc[frame_number] <= y_max_beam:
            for i in range(0, 25):
                lower_bound = i * hour
                upper_bound = (i + 1) * hour
                if lower_bound <= frame < upper_bound:
                    globals()[f'position_beam2_3s_hour{i}'] += 1
                    globals()[f'frame_position_beam2_3s_hour{i}'].append(frame)
        if x_min_lever <= df_animal2[2].iloc[frame_number] <= x_max_lever and y_min_lever <= df_animal2[3].iloc[frame_number] <= y_max_lever:
            for i in range(0, 25):
                lower_bound = i * hour
                upper_bound = (i + 1) * hour
                if lower_bound <= frame < upper_bound:
                    globals()[f'position_lever2_3s_hour{i}'] += 1
                    globals()[f'frame_position_lever2_3s_hour{i}'].append(frame)
        if x_min_nest <= df_animal2[2].iloc[frame_number] <= x_max_nest and y_min_nest <= df_animal2[3].iloc[frame_number] <= y_max_nest:
            for i in range(0, 25):
                lower_bound = i * hour
                upper_bound = (i + 1) * hour
                if lower_bound <= frame < upper_bound:
                    globals()[f'position_nest2_3s_hour{i}'] += 1
                    globals()[f'frame_position_nest2_3s_hour{i}'].append(frame)

y2_position_beam_3s = [globals()[f'position_beam2_3s_hour{i}'] for i in range(0, 25)]
print(f'position of beam 3 secondes before mouse 2: {y2_position_beam_3s}')
y2_position_lever_3s = [globals()[f'position_lever2_3s_hour{i}'] for i in range(0, 25)]
print(f'position of lever 3 secondes before mouse 2: {y2_position_lever_3s}')
y2_position_nest_3s = [globals()[f'position_nest2_3s_hour{i}'] for i in range(0, 25)]
print(f'position of nest 3 secondes before mouse 2: {y2_position_nest_3s}')

## mouse 3

liste_before_beam3_3s=[]
for frame in liste_frame_beam_3:
    liste_before_beam3_3s.append(frame-3*30)
print(liste_before_beam3_3s)

for frame in liste_before_beam3_3s:
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

    if len(df_animal3) != 0:
        if x_min_beam <= df_animal3[2].iloc[frame_number] <= x_max_beam and y_min_beam <= df_animal3[3].iloc[frame_number] <= y_max_beam:
            for i in range(0, 25):
                lower_bound = i * hour
                upper_bound = (i + 1) * hour
                if lower_bound <= frame < upper_bound:
                    globals()[f'position_beam3_3s_hour{i}'] += 1
                    globals()[f'frame_position_beam3_3s_hour{i}'].append(frame)
        if x_min_lever <= df_animal3[2].iloc[frame_number] <= x_max_lever and y_min_lever <= df_animal3[3].iloc[frame_number] <= y_max_lever:
            for i in range(0, 25):
                lower_bound = i * hour
                upper_bound = (i + 1) * hour
                if lower_bound <= frame < upper_bound:
                    globals()[f'position_lever3_3s_hour{i}'] += 1
                    globals()[f'frame_position_lever3_3s_hour{i}'].append(frame)
        if x_min_nest <= df_animal3[2].iloc[frame_number] <= x_max_nest and y_min_nest <= df_animal3[3].iloc[frame_number] <= y_max_nest:
            for i in range(0, 25):
                lower_bound = i * hour
                upper_bound = (i + 1) * hour
                if lower_bound <= frame < upper_bound:
                    globals()[f'position_nest3_3s_hour{i}'] += 1
                    globals()[f'frame_position_nest3_3s_hour{i}'].append(frame)

y3_position_beam_3s = [globals()[f'position_beam3_3s_hour{i}'] for i in range(0, 25)]
print(f'position of beam 3 secondes before mouse 3: {y3_position_beam_3s}')
y3_position_lever_3s = [globals()[f'position_lever3_3s_hour{i}'] for i in range(0, 25)]
print(f'position of lever 3 secondes before mouse 3: {y3_position_lever_3s}')
y3_position_nest_3s = [globals()[f'position_nest3_3s_hour{i}'] for i in range(0, 25)]
print(f'position of nest 3 secondes before mouse 3: {y3_position_nest_3s}')


# excel 6 seconds before beam

excel_file_path_position_beam = "C:/Users/LMT3-B7bis/Desktop/bm stage/position_6secondes_beam_end.xlsx"
df_file_position_beam = pd.read_excel(excel_file_path_position_beam)
excel_file_path_position_lever = "C:/Users/LMT3-B7bis/Desktop/bm stage/position_6secondes_lever_end.xlsx"
df_file_position_lever = pd.read_excel(excel_file_path_position_lever)
excel_file_path_position_nest = "C:/Users/LMT3-B7bis/Desktop/bm stage/position_6secondes_nest_end.xlsx"
df_file_position_nest = pd.read_excel(excel_file_path_position_nest)

data_position_beam = {
    f'Mouse_1_{name_cage}_{date}': y1_position_beam,
    f'Mouse_2_{name_cage}_{date}': y2_position_beam,
    f'Mouse_3_{name_cage}_{date}': y3_position_beam
}
df_position_beam = pd.DataFrame(data_position_beam)
df_combined_position_beam = pd.concat([df_file_position_beam, df_position_beam], axis=1)
df_combined_position_beam.to_excel(excel_file_path_position_beam, index=False)
#print(df_lever)
print(f'Data has been written to {excel_file_path_position_beam}')



data_position_lever = {
    f'Mouse_1_{name_cage}_{date}': y1_position_lever,
    f'Mouse_2_{name_cage}_{date}': y2_position_lever,
    f'Mouse_3_{name_cage}_{date}': y3_position_lever
}
df_position_lever = pd.DataFrame(data_position_lever)
df_combined_position_lever = pd.concat([df_file_position_lever, df_position_lever], axis=1)
df_combined_position_lever.to_excel(excel_file_path_position_lever, index=False)
print(f'Data has been written to {excel_file_path_position_lever}')

data_position_nest = {
    f'Mouse_1_{name_cage}_{date}': y1_position_nest,
    f'Mouse_2_{name_cage}_{date}': y2_position_nest,
    f'Mouse_3_{name_cage}_{date}': y3_position_nest
}
df_position_nest = pd.DataFrame(data_position_nest)
df_combined_position_nest = pd.concat([df_file_position_nest, df_position_nest], axis=1)
df_combined_position_nest.to_excel(excel_file_path_position_nest, index=False)
print(f'Data has been written to {excel_file_path_position_nest}')


#excel 3 seconds before beam
excel_file_path_position_beam_3s = "C:/Users/LMT3-B7bis/Desktop/bm stage/position_3secondes_beam.xlsx"
df_file_position_beam_3s = pd.read_excel(excel_file_path_position_beam_3s)
excel_file_path_position_lever_3s = "C:/Users/LMT3-B7bis/Desktop/bm stage/position_3secondes_lever.xlsx"
df_file_position_lever_3s = pd.read_excel(excel_file_path_position_lever_3s)
excel_file_path_position_nest_3s = "C:/Users/LMT3-B7bis/Desktop/bm stage/position_3secondes_nest.xlsx"
df_file_position_nest_3s = pd.read_excel(excel_file_path_position_nest_3s)


data_position_beam_3s = {
    f'Mouse_1_{name_cage}_{date}': y1_position_beam_3s,
    f'Mouse_2_{name_cage}_{date}': y2_position_beam_3s,
    f'Mouse_3_{name_cage}_{date}': y3_position_beam_3s
}
df_position_beam_3s = pd.DataFrame(data_position_beam_3s)
df_combined_position_beam_3s = pd.concat([df_file_position_beam_3s, df_position_beam_3s], axis=1)
df_combined_position_beam_3s.to_excel(excel_file_path_position_beam_3s, index=False)
print(f'Data has been written to {excel_file_path_position_beam_3s}')



data_position_lever_3s = {
    f'Mouse_1_{name_cage}_{date}': y1_position_lever_3s,
    f'Mouse_2_{name_cage}_{date}': y2_position_lever_3s,
    f'Mouse_3_{name_cage}_{date}': y3_position_lever_3s
}
df_position_lever_3s = pd.DataFrame(data_position_lever_3s)
df_combined_position_lever_3s = pd.concat([df_file_position_lever_3s, df_position_lever_3s], axis=1)
df_combined_position_lever_3s.to_excel(excel_file_path_position_lever_3s, index=False)
print(f'Data has been written to {excel_file_path_position_lever_3s}')

data_position_nest_3s = {
    f'Mouse_1_{name_cage}_{date}': y1_position_nest_3s,
    f'Mouse_2_{name_cage}_{date}': y2_position_nest_3s,
    f'Mouse_3_{name_cage}_{date}': y3_position_nest_3s
}
df_position_nest_3s = pd.DataFrame(data_position_nest_3s)
df_combined_position_nest_3s = pd.concat([df_file_position_nest_3s, df_position_nest_3s], axis=1)
df_combined_position_nest_3s.to_excel(excel_file_path_position_nest_3s, index=False)
print(f'Data has been written to {excel_file_path_position_nest_3s}')


#position when a lever is done############################################################################################################################


#when mouse 1 presses
for frame in liste_frame_lever_1:
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

    if len(df_animal2) != 0:
        if x_min_beam <= df_animal2[2].iloc[frame_number] <= x_max_beam and y_min_beam <= df_animal2[3].iloc[frame_number] <= y_max_beam:
            for i in range(0, 25):
                lower_bound = i * hour
                upper_bound = (i + 1) * hour
                if lower_bound <= frame < upper_bound:
                    globals()[f'after_lever1_beam2_hour{i}'] += 1
        if x_min_lever <= df_animal2[2].iloc[frame_number] <= x_max_lever and y_min_lever <= df_animal2[3].iloc[frame_number] <= y_max_lever:
            for i in range(0, 25):
                lower_bound = i * hour
                upper_bound = (i + 1) * hour
                if lower_bound <= frame < upper_bound:
                    globals()[f'after_lever1_lever2_hour{i}'] += 1
        if x_min_nest <= df_animal2[2].iloc[frame_number] <= x_max_nest and y_min_nest <= df_animal2[3].iloc[frame_number] <= y_max_nest:
            for i in range(0, 25):
                lower_bound = i * hour
                upper_bound = (i + 1) * hour
                if lower_bound <= frame < upper_bound:
                    globals()[f'after_lever1_nest2_hour{i}'] += 1

after_lever_1_beam2 = [globals()[f'after_lever1_beam2_hour{i}'] for i in range(0, 25)]
print(f'after_lever1_beam2: {after_lever_1_beam2}')
after_lever_1_lever2 = [globals()[f'after_lever1_lever2_hour{i}'] for i in range(0, 25)]
print(f'after_lever_1_lever2: {after_lever_1_lever2}')
after_lever_1_nest2 = [globals()[f'after_lever1_nest2_hour{i}'] for i in range(0, 25)]
print(f'after_lever_1_nest2: {after_lever_1_nest2}')

for frame in liste_frame_lever_1:
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

    if len(df_animal3) != 0:
        if x_min_beam <= df_animal3[2].iloc[frame_number] <= x_max_beam and y_min_beam <= df_animal3[3].iloc[frame_number] <= y_max_beam:
            for i in range(0, 25):
                lower_bound = i * hour
                upper_bound = (i + 1) * hour
                if lower_bound <= frame < upper_bound:
                    globals()[f'after_lever1_beam3_hour{i}'] += 1
        if x_min_lever <= df_animal3[2].iloc[frame_number] <= x_max_lever and y_min_lever <= df_animal3[3].iloc[frame_number] <= y_max_lever:
            for i in range(0, 25):
                lower_bound = i * hour
                upper_bound = (i + 1) * hour
                if lower_bound <= frame < upper_bound:
                    globals()[f'after_lever1_lever3_hour{i}'] += 1
        if x_min_nest <= df_animal3[2].iloc[frame_number] <= x_max_nest and y_min_nest <= df_animal3[3].iloc[frame_number] <= y_max_nest:
            for i in range(0, 25):
                lower_bound = i * hour
                upper_bound = (i + 1) * hour
                if lower_bound <= frame < upper_bound:
                    globals()[f'after_lever1_nest3_hour{i}'] += 1

after_lever_1_beam3 = [globals()[f'after_lever1_beam3_hour{i}'] for i in range(0, 25)]
print(f'after_lever_1_beam3: {after_lever_1_beam3}')
after_lever_1_lever3 = [globals()[f'after_lever1_lever3_hour{i}'] for i in range(0, 25)]
print(f'after_lever_1_lever3: {after_lever_1_lever3}')
after_lever_1_nest3 = [globals()[f'after_lever1_nest3_hour{i}'] for i in range(0, 25)]
print(f'after_lever_1_nest3: {after_lever_1_nest3}')

#when mouse 2 presses
for frame in liste_frame_lever_2:
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
                    globals()[f'after_lever2_beam1_hour{i}'] += 1
        if x_min_lever <= df_animal1[2].iloc[frame_number] <= x_max_lever and y_min_lever <= df_animal1[3].iloc[frame_number] <= y_max_lever:
            for i in range(0, 25):
                lower_bound = i * hour
                upper_bound = (i + 1) * hour
                if lower_bound <= frame < upper_bound:
                    globals()[f'after_lever2_lever1_hour{i}'] += 1
        if x_min_nest <= df_animal1[2].iloc[frame_number] <= x_max_nest and y_min_nest <= df_animal1[3].iloc[frame_number] <= y_max_nest:
            for i in range(0, 25):
                lower_bound = i * hour
                upper_bound = (i + 1) * hour
                if lower_bound <= frame < upper_bound:
                    globals()[f'after_lever2_nest1_hour{i}'] += 1


    if len(df_animal3) != 0:
        if x_min_beam <= df_animal3[2].iloc[frame_number] <= x_max_beam and y_min_beam <= df_animal3[3].iloc[frame_number] <= y_max_beam:
            for i in range(0, 25):
                lower_bound = i * hour
                upper_bound = (i + 1) * hour
                if lower_bound <= frame < upper_bound:
                    globals()[f'after_lever2_beam3_hour{i}'] += 1
        if x_min_lever <= df_animal3[2].iloc[frame_number] <= x_max_lever and y_min_lever <= df_animal3[3].iloc[frame_number] <= y_max_lever:
            for i in range(0, 25):
                lower_bound = i * hour
                upper_bound = (i + 1) * hour
                if lower_bound <= frame < upper_bound:
                    globals()[f'after_lever2_lever3_hour{i}'] += 1
        if x_min_nest <= df_animal3[2].iloc[frame_number] <= x_max_nest and y_min_nest <= df_animal3[3].iloc[frame_number] <= y_max_nest:
            for i in range(0, 25):
                lower_bound = i * hour
                upper_bound = (i + 1) * hour
                if lower_bound <= frame < upper_bound:
                    globals()[f'after_lever2_nest3_hour{i}'] += 1

after_lever_2_beam1 = [globals()[f'after_lever2_beam1_hour{i}'] for i in range(0, 25)]
print(f'after_lever_2_beam1: {after_lever_2_beam1}')
after_lever_2_lever1 = [globals()[f'after_lever2_lever1_hour{i}'] for i in range(0, 25)]
print(f'after_lever_2_lever1: {after_lever_2_lever1}')
after_lever_2_nest1 = [globals()[f'after_lever2_nest1_hour{i}'] for i in range(0, 25)]
print(f'after_lever_2_nest1: {after_lever_2_nest1}')

after_lever_2_beam3 = [globals()[f'after_lever2_beam3_hour{i}'] for i in range(0, 25)]
print(f'after_lever_2_beam3: {after_lever_2_beam3}')
after_lever_2_lever3 = [globals()[f'after_lever2_lever3_hour{i}'] for i in range(0, 25)]
print(f'after_lever_2_lever3: {after_lever_2_lever3}')
after_lever_2_nest3 = [globals()[f'after_lever2_nest3_hour{i}'] for i in range(0, 25)]
print(f'after_lever_2_nest3: {after_lever_2_nest3}')

# when mouse 3 presses
for frame in liste_frame_lever_3:
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
        if x_min_beam <= df_animal1[2].iloc[frame_number] <= x_max_beam and y_min_beam <= df_animal1[3].iloc[
            frame_number] <= y_max_beam:
            for i in range(0, 25):
                lower_bound = i * hour
                upper_bound = (i + 1) * hour
                if lower_bound <= frame < upper_bound:
                    globals()[f'after_lever3_beam1_hour{i}'] += 1
        if x_min_lever <= df_animal1[2].iloc[frame_number] <= x_max_lever and y_min_lever <= df_animal1[3].iloc[
            frame_number] <= y_max_lever:
            for i in range(0, 25):
                lower_bound = i * hour
                upper_bound = (i + 1) * hour
                if lower_bound <= frame < upper_bound:
                    globals()[f'after_lever3_lever1_hour{i}'] += 1
        if x_min_nest <= df_animal1[2].iloc[frame_number] <= x_max_nest and y_min_nest <= df_animal1[3].iloc[
            frame_number] <= y_max_nest:
            for i in range(0, 25):
                lower_bound = i * hour
                upper_bound = (i + 1) * hour
                if lower_bound <= frame < upper_bound:
                    globals()[f'after_lever3_nest1_hour{i}'] += 1
    if len(df_animal2) != 0:
        if x_min_beam <= df_animal2[2].iloc[frame_number] <= x_max_beam and y_min_beam <= df_animal2[3].iloc[frame_number] <= y_max_beam:
            for i in range(0, 25):
                lower_bound = i * hour
                upper_bound = (i + 1) * hour
                if lower_bound <= frame < upper_bound:
                    globals()[f'after_lever3_beam2_hour{i}'] += 1
        if x_min_lever <= df_animal2[2].iloc[frame_number] <= x_max_lever and y_min_lever <= df_animal2[3].iloc[frame_number] <= y_max_lever:
            for i in range(0, 25):
                lower_bound = i * hour
                upper_bound = (i + 1) * hour
                if lower_bound <= frame < upper_bound:
                    globals()[f'after_lever3_lever2_hour{i}'] += 1
        if x_min_nest <= df_animal2[2].iloc[frame_number] <= x_max_nest and y_min_nest <= df_animal2[3].iloc[frame_number] <= y_max_nest:
            for i in range(0, 25):
                lower_bound = i * hour
                upper_bound = (i + 1) * hour
                if lower_bound <= frame < upper_bound:
                    globals()[f'after_lever3_nest2_hour{i}'] += 1

after_lever_3_beam2 = [globals()[f'after_lever3_beam2_hour{i}'] for i in range(0, 25)]
print(f'after_lever_3_beam2: {after_lever_3_beam2}')
after_lever_3_lever2 = [globals()[f'after_lever3_lever2_hour{i}'] for i in range(0, 25)]
print(f'after_lever_3_lever2: {after_lever_3_lever2}')
after_lever_3_nest2 = [globals()[f'after_lever3_nest2_hour{i}'] for i in range(0, 25)]
print(f'after_lever_3_nest2: {after_lever_3_nest2}')

after_lever_3_beam1 = [globals()[f'after_lever3_beam1_hour{i}'] for i in range(0, 25)]
print(f'after_lever_3_beam1: {after_lever_3_beam1}')
after_lever_3_lever1 = [globals()[f'after_lever3_lever1_hour{i}'] for i in range(0, 25)]
print(f'after_lever_3_lever1: {after_lever_3_lever1}')
after_lever_3_nest1 = [globals()[f'after_lever3_nest1_hour{i}'] for i in range(0, 25)]
print(f'after_lever_3_nest1: {after_lever_3_nest1}')

#### excel position when a mouse presses the lever
excel_file_path_apres_lever_beam = "C:/Users/LMT3-B7bis/Desktop/bm stage/position_apres_lever_beam.xlsx"
df_file_position_apres_lever_beam = pd.read_excel(excel_file_path_apres_lever_beam)


data_position_apres_lever_beam = {
    f'Mouse_1_2_{name_cage}_{date}': after_lever_1_beam2,
    f'Mouse_1_3_{name_cage}_{date}': after_lever_1_beam3,
    f'Mouse_2_1_{name_cage}_{date}': after_lever_2_beam1,
    f'Mouse_2_3_{name_cage}_{date}': after_lever_2_beam3,
    f'Mouse_3_1_{name_cage}_{date}': after_lever_3_beam1,
    f'Mouse_3_2_{name_cage}_{date}': after_lever_3_beam2
}
df_position_apres_lever_beam = pd.DataFrame(data_position_apres_lever_beam)
df_combined_position_apres_lever_beam = pd.concat([df_file_position_apres_lever_beam, df_position_apres_lever_beam], axis=1)
df_combined_position_apres_lever_beam.to_excel(excel_file_path_apres_lever_beam, index=False)
#print(df_lever)
print(f'Data has been written to {excel_file_path_apres_lever_beam}')


excel_file_path_apres_lever_lever = "C:/Users/LMT3-B7bis/Desktop/bm stage/position_apres_lever_lever.xlsx"
df_file_position_apres_lever_lever = pd.read_excel(excel_file_path_apres_lever_lever)

data_position_apres_lever_lever = {
    f'Mouse_1_2_{name_cage}_{date}': after_lever_1_lever2,
    f'Mouse_1_3_{name_cage}_{date}': after_lever_1_lever3,
    f'Mouse_2_1_{name_cage}_{date}': after_lever_2_lever1,
    f'Mouse_2_3_{name_cage}_{date}': after_lever_2_lever3,
    f'Mouse_3_1_{name_cage}_{date}': after_lever_3_lever1,
    f'Mouse_3_2_{name_cage}_{date}': after_lever_3_lever2
}
df_position_apres_lever_lever = pd.DataFrame(data_position_apres_lever_lever)
df_combined_position_apres_lever_lever = pd.concat([df_file_position_apres_lever_lever, df_position_apres_lever_lever], axis=1)
df_combined_position_apres_lever_lever.to_excel(excel_file_path_apres_lever_lever, index=False)
#print(df_lever)
print(f'Data has been written to {excel_file_path_apres_lever_lever}')

excel_file_path_apres_lever_nest = "C:/Users/LMT3-B7bis/Desktop/bm stage/position_apres_lever_nest.xlsx"
df_file_position_apres_lever_nest = pd.read_excel(excel_file_path_apres_lever_nest)

data_position_apres_lever_nest = {
    f'Mouse_1_2_{name_cage}_{date}': after_lever_1_nest2,
    f'Mouse_1_3_{name_cage}_{date}': after_lever_1_nest3,
    f'Mouse_2_1_{name_cage}_{date}': after_lever_2_nest1,
    f'Mouse_2_3_{name_cage}_{date}': after_lever_2_nest3,
    f'Mouse_3_1_{name_cage}_{date}': after_lever_3_nest1,
    f'Mouse_3_2_{name_cage}_{date}': after_lever_3_nest2
}
df_position_apres_lever_nest = pd.DataFrame(data_position_apres_lever_nest)
df_combined_position_apres_lever_nest = pd.concat([df_file_position_apres_lever_nest, df_position_apres_lever_nest], axis=1)
df_combined_position_apres_lever_nest.to_excel(excel_file_path_apres_lever_nest, index=False)
#print
print(f'Data has been written to {excel_file_path_apres_lever_nest}')
print(name_cage)
print(date)

### accumulation

print(f'list_frames_leverpress:{list_frames_leverpress}')
print(f'list_frames_beam:{list_frames_beam}')

liste_frames=list(list_frames_beam)+list(list_frames_leverpress)
print(liste_frames)
liste_frames_sorted=sorted(liste_frames)
print(f'list_frames_sorted:{liste_frames_sorted}')

lever_press_indices = [i for i, frame in enumerate(liste_frames_sorted) if frame in list_frames_leverpress]
beam_indices = [i for i, frame in enumerate(liste_frames_sorted) if frame in list_frames_beam]



# number of frames between following leverpress
frames_between_levers = []
for i in range(1, len(lever_press_indices)):
    nb_frames_between_levers = lever_press_indices[i] - lever_press_indices[i-1] - 1
    frames_between_levers.append(nb_frames_between_levers)

print(frames_between_levers)

excel_file_path_between_levers = "C:/Users/LMT3-B7bis/Desktop/bm stage/accumulation_between_levers.xlsx"
df_file_between_levers = pd.read_excel(excel_file_path_between_levers)

data_between_levers = {
    f'{name_cage}_{date}': frames_between_levers
}
df_between_levers = pd.DataFrame(data_between_levers)
df_combined_between_levers = pd.concat([df_file_between_levers, df_between_levers], axis=1)
df_combined_between_levers.to_excel(excel_file_path_between_levers, index=False)

print(f'Data has been written to {excel_file_path_between_levers}')


# number of frames between following beams
frames_between_beams = []
for i in range(1, len(beam_indices)):
    nb_frames_between_beams = beam_indices[i] - beam_indices[i-1] - 1
    frames_between_beams.append(nb_frames_between_beams)

print(frames_between_beams)

excel_file_path_between_beams = "C:/Users/LMT3-B7bis/Desktop/bm stage/accumulation_between_beams.xlsx"
df_file_between_beams = pd.read_excel(excel_file_path_between_beams)

data_between_beams = {
    f'{name_cage}_{date}': frames_between_beams
}
df_between_beams = pd.DataFrame(data_between_beams)
df_combined_between_beams = pd.concat([df_file_between_beams, df_between_beams], axis=1)
df_combined_between_beams.to_excel(excel_file_path_between_beams, index=False)

print(f'Data has been written to {excel_file_path_between_beams}')