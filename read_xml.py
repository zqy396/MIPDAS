import json
import xml.etree.ElementTree as ET

def geojson_to_xml(geojson):
    def dict_to_xml(tag, d):
        """Convert a dictionary to XML"""
        elem = ET.Element(tag)
        for key, val in d.items():
            if isinstance(val, dict):
                child = dict_to_xml(key, val)
                elem.append(child)
            elif isinstance(val, list):
                for sub_val in val:
                    child = dict_to_xml(key, sub_val)
                    elem.append(child)
            else:
                child = ET.Element(key)
                child.text = str(val)
                elem.append(child)
        return elem

    with open(geojson, 'r') as f:
        geojson_data = json.load(f)
    root = dict_to_xml('GeoJSON', geojson_data)
    return ET.tostring(root, encoding='unicode')

geojson = 'TCGA-4Z-AA7Q-01Z-00-DX1.9C30EAED-8DE3-437C-8852-0C64B415AFA8.geojson'
xml_string = geojson_to_xml(geojson)

import json
import xml.etree.ElementTree as ET

# 解析GeoJSON
with open(geojson, 'r') as f:
    geojson_data = json.load(f)

# 创建XML根元素
root = ET.Element('feature')

# 添加geometry元素
geometry = ET.SubElement(root, 'geometry')
type_el = ET.SubElement(geometry, 'type')
type_el.text = geojson_data['features'][0]['geometry']['type']
coordinates = ET.SubElement(geometry, 'coordinates')
coordinates.text = ', '.join(map(str, geojson_data['features'][0]['geometry']['coordinates']))

# 添加properties元素
properties = ET.SubElement(root, 'properties')
for key, value in geojson_data['features'][0]['properties'].items():
    prop = ET.SubElement(properties, key)
    prop.text = str(value)

# 生成XML字符串
xml_str = ET.tostring(root, encoding='utf8', method='xml').decode('utf8')
file_path = 'output.xml'

with open(file_path, 'w', encoding='utf-8') as file:
    file.write(xml_str)

import openslide
img = openslide.OpenSlide('/TCGA-4Z-AA7Q-01Z-00-DX1.9C30EAED-8DE3-437C-8852-0C64B415AFA8.svs')