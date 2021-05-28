import json
import glob
import os
import numpy as np
import json
class_name = ["short sleeve top",
                "long sleeve top",
                "short sleeve outwear",
                "long sleeve outwear",
                "vest",
                "sling",
                "shorts",
                "trousers",
                "skirt",
                "short sleeve dress",
                "long sleeve dress",
                "vest dress",
                "sling dress"]
label_polygon_dict = {}

for file_path in glob.glob('*.json'):
    json_data = open(file_path)
    json_data = json.load(json_data)
    regions = []
    for name, json_item in json_data.items():
        if 'item' not in name:
            continue
        segmentation = np.array(json_item['segmentation']).reshape(-1,2).astype(int)
        all_points_x = segmentation[:,0].tolist()
        all_points_y = segmentation[:,1].tolist()
        category_name = class_name[json_item['category_id']-1]

        regions.append({'shape_attributes':{'name':'polygon', 'all_points_x':all_points_x, 'all_points_y':all_points_y},
                            'region_attributes':{'type':{category_name:True}}})


    file_name = os.path.basename(file_path)[:-4]
    image_size = os.stat(file_name+'jpg').st_size

    label_polygon_dict[file_name + 'jpg' + str(image_size)] = {'filename':file_name + 'jpg', 'size': image_size, 'regions':regions, "file_attributes": {}}

file_path = 'box/image_small_box/via_project_17May2021_10h50m_json.json'

output_file = open('new.json', 'w')
# output_file.write(json_data)
json.dump(label_polygon_dict, output_file)
output_file.close()