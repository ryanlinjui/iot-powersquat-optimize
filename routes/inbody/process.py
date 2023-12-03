# -*- coding: utf-8 -*-

from PIL import Image
from shapely.geometry import Point, Polygon, LineString
import json
import re

from .gcloud import image_detection_api

def preprocess(img):
    resized_img = img.resize((2100, 2970)) # A4 size * 10
    return resized_img
    
def calculate_area(poly_bound):
    x1 = poly_bound[0].x
    x2 = poly_bound[1].x
    x3 = poly_bound[2].x
    x4 = poly_bound[3].x

    y1 = poly_bound[0].y
    y2 = poly_bound[1].y
    y3 = poly_bound[2].y
    y4 = poly_bound[3].y

    area = 0.5 * abs(x1 * y2 + x2 * y3 + x3 * y4 + x4 * y1 - y1 * x2 - y2 * x3 - y3 * x4 - y4 * x1)
    return area

def bounding_filter(text_data, start_text:str, direction:int, search_rate:float, key_text=None):

    key_data = None
    for data in text_data:
        if data.description == start_text:
            key_data = data
            break

    if key_data == None: return []
    filter_result = []
    start_point = Point(key_data.bounding_poly.vertices[0].x, key_data.bounding_poly.vertices[0].y)
    
    if direction==1: end_point = Point(key_data.bounding_poly.vertices[0].x + 1e4, key_data.bounding_poly.vertices[0].y)
    elif direction==2: end_point = Point(key_data.bounding_poly.vertices[0].x, key_data.bounding_poly.vertices[0].y + 1e4)
    elif direction==3: end_point = Point(key_data.bounding_poly.vertices[0].x - 1e4, key_data.bounding_poly.vertices[0].y)
    else: end_point = Point(key_data.bounding_poly.vertices[0].x, key_data.bounding_poly.vertices[0].y - 1e4)

    line_segment = LineString([start_point, end_point]).buffer(search_rate * abs(data.bounding_poly.vertices[0].y - data.bounding_poly.vertices[3].y), cap_style=2)
    for data in text_data:
        polygon = Polygon([
            (data.bounding_poly.vertices[0].x, data.bounding_poly.vertices[0].y),
            (data.bounding_poly.vertices[3].x, data.bounding_poly.vertices[3].y),
            (data.bounding_poly.vertices[2].x, data.bounding_poly.vertices[2].y),
            (data.bounding_poly.vertices[1].x, data.bounding_poly.vertices[1].y)
        ])
        if polygon.intersects(line_segment):
            if key_text == data.description or key_text == None:
                filter_result.append(data)
    
    return filter_result

def data_extraction(text_data):
    result_data = []
    for data in text_data:
        if re.match(r'^[0-9]+\.[0-9]+$', data.description):
            result_data.append(data.description)
    
    if len(result_data) != 5: 
        result_data = ["NaN"] * 5

    return result_data

def get_inbody_data(img):
    width, height = img.size
    new_height = height // 5
    data = []

    for i in range(5):
        top = i * new_height
        bottom = (i + 1) * new_height
        cropped_image = img.crop((0, top, width, bottom))
        data.append(data_extraction(google_vision(cropped_image)))

    inbody_data = {
        "right_arm": {
            "mass": [data[0][0], data[0][1], data[0][2]],
            "ECF": data[0][3],
            "ECW": data[0][4]
        },
        "left_arm": {
            "mass": [data[1][0], data[1][1], data[1][2]],
            "ECF": data[1][3],
            "ECW": data[1][4]
        },
        "trunk": {
            "mass": [data[2][0], data[2][1], data[2][2]],
            "ECF": data[2][3],
            "ECW": data[2][4]
        },
        "right_leg": {
            "mass": [data[3][0], data[3][1], data[3][2]],
            "ECF": data[3][3],
            "ECW": data[3][4]
        },
        "left_leg": {
            "mass": [data[4][0], data[4][1], data[4][2]],
            "ECF": data[4][3],
            "ECW": data[4][4]
        }
    }
    
    with open("output.json", "w") as json_file:
        json_file.write(json.dumps(inbody_data))

def segmental_lean_analysis(img):
    text_data = image_detection_api.run(img)
    text_data = bounding_filter(text_data, "InBody", 2, 1.0)
    text_data =  bounding_filter(text_data, "平衡", 3, 1.0, "肌肉")[0]
    # text_data =  bounding_filter(text_data, "Segmental", 3, 1.0, "Segmental")[0]
    img = img.crop(
        (text_data.bounding_poly.vertices[3].x, text_data.bounding_poly.vertices[3].y + 55, 
        text_data.bounding_poly.vertices[3].x + 1150, text_data.bounding_poly.vertices[3].y + 675)
    )
    
    # img.save("test.jpg")
    return get_inbody_data(img)

def inbody_recognition(img_path:str):
    img = preprocess(Image.open(img_path))
    return segmental_lean_analysis(img)

    