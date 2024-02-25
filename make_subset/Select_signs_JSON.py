import json

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



json_file_path = '../WLASL/code/I3D/preprocess/nslt_100.json'
output_path = 'nslt_selected.json'
signs = ["0","1","2"]

out = read_and_show_json(json_file_path,signs,output_path)