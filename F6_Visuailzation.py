import os
import matplotlib.pyplot as plt
import csv
import numpy as np
import xml.etree.ElementTree as ET
import pandas as pd

from tiatoolbox.wsicore.wsireader import WSIReader
from tiatoolbox.models.engine.semantic_segmentor import (
    IOSegmentorConfig,
)

bcc_wsi_ioconfig = IOSegmentorConfig(
    input_resolutions=[{"units": "mpp", "resolution": 0.25}],
    output_resolutions=[{"units": "mpp", "resolution": 0.25}],
    patch_input_shape=[1024, 1024],
    patch_output_shape=[512, 512],
    stride_shape=[512, 512],
    save_resolution={"units": "mpp", "resolution": 2},
)

def get_windows(xml_path):
    window_bbox = []
    assert os.path.exists(xml_path), f"Can't find {xml_path}"
    tree = ET.parse(xml_path)
    root = tree.getroot()
    # 初始化最小和最大值
    x_min, y_min = float('inf'), float('inf')
    x_max, y_max = float('-inf'), float('-inf')

    # 遍历所有的 Vertex 节点，找到最大的和最小的 x 和 y
    for vertex in root.findall('.//Vertex'):
        x = float(vertex.get('X'))
        y = float(vertex.get('Y'))

        # 更新最大和最小值
        x_min = min(x_min, x)
        x_max = max(x_max, x)
        y_min = min(y_min, y)
        y_max = max(y_max, y)

    window_bbox.append([[x_min, y_min],
                        [x_max, y_max]])
    return window_bbox

wsi_file_path = ""
# xml_file_path = '.xml'
feature_path = ''


for WSI in os.listdir(wsi_file_path):
    wsi_file = os.path.join(wsi_file_path, WSI)

    wsi = WSIReader.open(wsi_file)
    # using the prediction save_resolution to create the wsi overview at the same resolution
    overview_info = bcc_wsi_ioconfig.save_resolution
    # extracting slide overview using `slide_thumbnail` method
    wsi_overview = wsi.slide_thumbnail(
        resolution=overview_info["resolution"],
        units=overview_info["units"],
    )

    print('WSI Done!')

    # sample_name = os.path.split(WSI)[0]
    sample_name = 'TCGA-4Z-AA7Q-01Z-00-DX1'

    # window_bbox = np.array(get_windows(xml_file_path))

    csv_file = ['T', 'I', 'S']
    csv_data = None
    n_data = 0
    for c in csv_file:
        if csv_data is None:
            csv_data = pd.read_csv(os.path.join(feature_path, sample_name + '_Feats_' + c + '.csv'))
        else:
            temp = pd.read_csv(os.path.join(feature_path, sample_name + '_Feats_' + c + '.csv'))
            csv_data = pd.concat([csv_data, temp])
    inbox_name = np.empty((0), dtype=np.int64)
    inbox_centroid = np.empty((0, 2), dtype=np.float32)
    centroid = np.array(list(map(lambda x: eval(x), csv_data.Centroid)))
    # name = csv_data.name.values

    # centroid[:, 0] = centroid[:, 0] + window_bbox[0][0][0]
    # centroid[:, 1] = centroid[:, 1] + window_bbox[0][0][1]

    centroid = centroid * 0.13

    print(centroid)

    # 分离 X 和 Y 坐标
    x_coords = centroid[:, 0]
    y_coords = centroid[:, 1]

    plt.figure(figsize=(20,20))
    plt.imshow(wsi_overview)
    plt.axis("off")

    # 在背景图像上绘制这些坐标点
    plt.scatter(x_coords, y_coords, c='red', s=1, marker='.', label='Centroids')
    plt.savefig('/mnt/data/a.tif',dpi=300)
    print('Done!')

    plt.show()




