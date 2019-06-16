import os
import numpy as np
import sys
data_input=sys.argv[1]
#Open .out file and read lines
data_file=os.path.join('Ag', 'DFT', data_input)
data=open(data_file)
data=data.readlines()
#Go through lines of the full file and obtain line number
#Use unique keywords written in the code to isolate relevant data
for linenum, line in enumerate(data):
    if 'from one for' in line:
        CT_start=linenum+5
    if 'The bond energy is' in line:
        CT_end=linenum-10
CT_data=data[CT_start:CT_end]
CT_length=len(CT_data)
#Set empty arrays for iterative data
#Looking to compare energy level with total contribution from silver and benzenthiol fragment contribution
Ag_con=[]
Mol_con=[]
sum_index=[]
energy=[]
contributions=[]
twenty_cent=[]
energy_level=[]
level_array_20=[]
level_array_80=[]
eighty_cent=[]
bandgap=[]
ind=1
#loop through data lines, split each character
#For each character search for only 'A' as it indicates the line with the energy level and start of contribution data
#Record line number in iterative array to index the start of the data sum
#Make iterative array of the energy value of each level
#Make iterative array of the orbital occupation
for num in range(0,CT_length):
    line = CT_data[num].split()
    for i in line:
        if 'A' in i and 'Ag' not in i:
            sum_index.append(num)
            energy.append(line[0])
            bandgap.append(float(line[1]))
#Find HOMO/LUMO gap with index to get energy
bandgap_length=len(bandgap)
for val in range(0,bandgap_length-1):
    if bandgap[val+1]-bandgap[val]==-2:
        HOMO_ind=sum_index[val]
        LUMO_ind=sum_index[val+1]
        HOMO=float(energy[val])
        LUMO=float(energy[val+1])
bandgap_energy=LUMO-HOMO
#Print HOMO, LUMO, bandgap energy, and title for CT States list
print(F'HOMO = {HOMO}')
print(F'LUMO = {LUMO}')
print(F'Bandgap Energy = {bandgap_energy:.3f}')
print("CT States")
#Loop through data again to search for percentage contribution and turn percents into floats
for num in range(0,CT_length):
    line = CT_data[num].split()
    for i in line:
        if '%' in i:
            per_con=float(i[:-1])
            per_con=abs(per_con)
#Record last item in array, which gives the atom fragment for each contribution
    atom=line[-1]
#If atom is silver, create interative array of that contribution
    if atom=='Ag':
        Ag=per_con
        Ag_con.append(Ag)
#If atom is not silver, create iterative array of those contributions
    else:
        Mol=per_con
        Mol_con.append(Mol)
#If the line of data matches the line corresponding to the start of the contributions for each energy level
    if num==sum_index[ind]-1:
#Sum each contribution with however many floats are in the array for the current iteration of the for loop
#Create array with each sum at the corresponding energy level
        Ag_sum=sum(Ag_con)
        Mol_sum=sum(Mol_con)
        cons=F'{energy[ind-1]} | {Mol_sum:.3f} | {Ag_sum:.3f}'
        contributions.append(cons)
#Clear the array after summing it to start data for next energy level
        Ag_con=[]
        Mol_con=[]
#Increases the index for the array containing the line for energy levels
#Only execute if it not the last energy level to avoid over indexing
        if num!=sum_index[-1]-1:
            ind=ind+1
#Isolate molecular contributions and associated energy level
for level, lin in enumerate(contributions):
    lin_split=lin.split()
    percent=float(lin_split[2])
    e_lev=float(lin_split[0])
#Find starting and ending energy levels for 20% to 80% limit
    if percent>=20 and e_lev>=-7:
        twenty_cent.append(percent)
        energy_level.append(e_lev)
        level_array_20.append(level)
    if percent>=80 and e_lev>=-7:
        eighty_cent.append(percent)
        level_array_80.append(level)
#Impose limit on contribution array
contribution_start=level_array_20[0]
contribution_end=level_array_80[0]
#Remove any energies where the molecule does not contribute
for n in range(contribution_start,contribution_end+1):
    lin_split=contributions[n].split()
    for k in lin_split:
        percent=float(lin_split[2])
    if percent!=0:
        print(contributions[n])