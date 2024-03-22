# redefining sets

import json
import numpy as np

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
    array = ["train"] * (N * a // 100) + ["test"] * (N * b // 100) + ["val"] * (N * c // 100)
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
    train = 100 - (test+val)
    N = countVideos(file_path)
    randSets = randomArray(N, train, test, val)
    count = 0
    output="{"
    try:
        with open(file_path, 'r') as file:
            json_content = json.load(file)
            for key, value in json_content.items():  
                newValue = '"'+str(count)+'": {"subset": "'+ randSets[count] + '", "action": ['+str(value["action"][0]) +', '+str(value["action"][1])+', '+str(value["action"][2])+']}, '
                count+=1
                output += newValue
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    out = output[:-2]+"}"

    f = open(output_path, "w")
    f.write(out)
    f.close()
    return out

json_file_path = '../wlasl-complete/nslt_100.json'
json_output_path = 'nslt_ajusted.json'
test = 20
val = 20
# train will be 100 - (test + val)
out = redefineSets(test,val, json_file_path,json_output_path)
#print(out)

# checking the new set definitions
sets = countPercent(json_output_path)
print("count of sets [train, test, val]")
print(sets)
print("\nPercentages")
print("train: %.4f"%(sets[0]/sum(sets)*100))
print("test: %.4f"%(sets[1]/sum(sets)*100))
print("val: %.4f"%(sets[2]/sum(sets)*100))

print("\nTotal: %.2f"%((sets[0]/sum(sets)+sets[1]/sum(sets)+sets[2]/sum(sets))*100))