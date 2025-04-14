import os
import joblib
import re
import json
import numpy as np

def fun_2_json(input_dir, output_dir):
    for WSI_name in sorted(os.listdir(input_dir)):

        patient_path = os.path.join(input_dir, WSI_name)

        cell_num = 0

        data = {
            'mag': 40,
            'nuc': {}
        }

        for tile in sorted(os.listdir(patient_path)):
            # print('111')
            tile_path = os.path.join(patient_path, tile)
            # 使用正则表达式提取 x 和 y 的值
            pattern = r'x-(\d+)_y-(\d+)'
            match = re.search(pattern, tile)
            if match:
                x = int(match.group(1))  # 获取 x 后面的坐标值
                y = int(match.group(2))  # 获取 y 后面的坐标值

            tile_preds = joblib.load(os.path.join(tile_path, '0.dat'))

            for key, value in tile_preds.items():

                cell_num = cell_num + 1
                data['nuc'][str(cell_num)] = {
                    'bbox': None,
                    'centroid': None,
                    'contour': None,
                    'type_prob': None,
                    'type': None
                }

                # # 向每个小字典中添加元素（可以根据实际需要调整数据）
                # data['nuc'][str(cell_num)]['bbox'] = [[value['box'][0] + x, value['box'][1] + y], [value['box'][2] + x, value['box'][3] + y]]
                # data['nuc'][str(cell_num)]['centroid'] = value['centroid'].tolist()
                # data['nuc'][str(cell_num)]['contour'] = value['contour'].tolist()
                # data['nuc'][str(cell_num)]['type_prob'] = value['prob']
                # data['nuc'][str(cell_num)]['type'] = value['type']

                # 向每个小字典中添加元素（可以根据实际需要调整数据）
                data['nuc'][str(cell_num)]['bbox'] = [[value['box'][0] + x, value['box'][1] + y], [value['box'][2] + x, value['box'][3] + y]]
                data['nuc'][str(cell_num)]['centroid'] = [value['centroid'][0] + x, value['centroid'][1] + y]
                data['nuc'][str(cell_num)]['contour'] = [[point[0] + x, point[1] + y] for point in value['contour'].tolist()]
                data['nuc'][str(cell_num)]['type_prob'] = value['prob']
                data['nuc'][str(cell_num)]['type'] = value['type']

        """ 这一步需要将int64转换为int类型，才可以使用 """
        def convert_numpy(data):
            if isinstance(data, dict):
                return {key: convert_numpy(value) for key, value in data.items()}
            elif isinstance(data, list):
                return [convert_numpy(item) for item in data]
            elif isinstance(data, np.integer):
                return int(data)
            elif isinstance(data, np.floating):
                return float(data)
            else:
                return data

        # 假设你的数据保存在变量 data 中
        data = convert_numpy(data)
        save_path = os.path.join(output_dir, WSI_name + '.json')
        # 将字典保存为 JSON 文件
        with open(save_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)  # 使用 indent=4 格式化输出
        print('已保存')


