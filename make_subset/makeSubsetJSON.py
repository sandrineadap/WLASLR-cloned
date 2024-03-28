#######################################################################
# A combination of Dr. Will's scripts: 
# Select_signs_JSON.ipynb
#   Selects by word ID any words from an existing dataset. (IDs: line 36. Dataset: line 34)
#   Creates a new subset from selected words. (nslt_selected.json)
# VideoDatasetJSON.ipynb (VideoDatasetJSON (2).ipynb)
#   renumbers word ID's based on the positions entered in the code.
#   resplits subset into train, test, and validation sets: 60/20/20. (nslt_adjusted.json)
#######################################################################

#################### Select_signs_JSON.ipynb
import json
import numpy as np

def read_and_show_json(file_path,signs,output_path):
    output="{"
    try:
        with open(file_path, 'r') as file:
            json_content = json.load(file)
            for key, value in json_content.items():
                if json.dumps(value["action"][0]) in signs:
                    output+= '"'+key+'": '+json.dumps(value)+', '
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        
    out = output[:-2]+"}"

    f = open(output_path, "w")
    f.write(out)
    f.close()

    return out

json_file_path = '../wlasl-complete/nslt_2000.json'
output_path = 'nslt_selected.json'
signs = ["566", "255", "164", "30", "86", "12", "234", "333", "327", "139"] # word id's to select

out = read_and_show_json(json_file_path,signs,output_path)

#################### VideoDatasetJSON (2).ipynb
def countPercent(file_path):
    sets = np.array(["train","test","val"])
    countSets = np.array([0,0,0])
    try:
        with open(file_path, 'r') as file:
            json_content = json.load(file)
            for key, value in json_content.items():
                sample = json.dumps(value["subset"])[1:-1]
                i = np.where(sets == sample)
                countSets[i]+=1
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    return countSets

def countVideos(file_path):
    count = 1
    try:
        with open(file_path, 'r') as file:
            json_content = json.load(file)
            for key, value in json_content.items():
                count+=1
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    return count

def randomArray(N, a, b, c): 
    total_elements = a + b + c
    if total_elements != 100:
        raise ValueError("Percentages should add up to 100.")
    # I changed the following line because sometimes it wouldn't add up to the required number of videos due to the flooring action.
    array = ["test"] * (int(round((N * b / 100), 0))) + ["val"] * (int(round((N * c // 100), 0))) + ["train"] * (N - ((N * b // 100) + (N * c // 100)))
    random.shuffle(array)
    return array

def printSets(file_path):
    sets = np.array(["train","test","val"])
    countSets = np.array([0,0,0])
    try:
        with open(file_path, 'r') as file:
            json_content = json.load(file)
            for key, value in json_content.items():
                sample = json.dumps(value["subset"])[1:-1]
                print(sample)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    return countSets

import random 

def redefineSets(test, val, file_path, output_path):
    # ids = getWordIDs(file_path)     # change here. comment out to keep the order from given id list (line 36).
    ids = list(map(int, signs))   # change here. use this to keep the order from given id list (line 36)
    train = 100 - (test+val)
    N = countVideos(file_path)
    randSets = randomArray(N, train, test, val)
    # print(N)
    # print(len(randSets))
    # print(randSets)
    count = 0
    output="{"
    try:
        with open(file_path, 'r') as file:
            json_content = json.load(file)
            for key, value in json_content.items():  
                #str(ids.index(value["action"][0]))
                newValue = '"'+key+'": {"subset": "'+ randSets[count] + '", "action": ['+str(ids.index(value["action"][0])) +', '+str(value["action"][1])+', '+str(value["action"][2])+']}, '
                count+=1
                output += newValue
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    # except IndexError:
    #     print(f"List index out of range: {count}")
    out = output[:-2]+"}"

    f = open(output_path, "w")
    f.write(out)
    f.close()
    return out

def getWordIDs(file_path):
    ids=[]
    try:
        with open(file_path, 'r') as file:
            json_content = json.load(file)
            for key, value in json_content.items():             
                if value["action"][0] not in ids:
                    ids.append(value["action"][0])
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        
    ids.sort() # change here. uncomment to keep the order from given id list (line 36).
    return ids

json_file_path = 'nslt_selected.json'
# ids = getWordIDs(json_file_path)    # change here. comment out to keep the order from given id list (line 36).
# print(ids)                          # change here. comment out to keep the order from given id list (line 36).
ids = list(map(int, signs))   # change here. use this to keep the order from given id list (line 36)
print(list(map(int, signs)))

json_file_path = 'nslt_selected.json'
json_output_path = 'nslt_ajusted.json'
test = 17
val = 17
# train will be 100 - (test + val)
out = redefineSets(test, val, json_file_path,json_output_path)
#print(out)

print(getWordIDs(json_output_path))

new_ids = getWordIDs(json_output_path) 

word_list = open("../wlasl-complete/wlasl_class_list.txt")
content = word_list.readlines()

f = open("class_list.txt", "w")
for id in new_ids: 
    # f.write(str(id) + "	" + str(content[int(ids[id])].split("	", 1)[1]))      # change here. comment out (the original ids)
    f.write(str(id) + "	" + str(content[int(signs[id])].split("	", 1)[1])) # change here. use this to keep the order from given id list (line 36)
f.close()

# checking the new set definitions
sets = countPercent(json_output_path)
print("count of sets [train, test, val]")
print(sets)
print("\nPercentages")
print("train: %.4f"%(sets[0]/sum(sets)*100))
print("test: %.4f"%(sets[1]/sum(sets)*100))
print("val: %.4f"%(sets[2]/sum(sets)*100))

print("\nTotal: %.2f"%((sets[0]/sum(sets)+sets[1]/sum(sets)+sets[2]/sum(sets))*100))
