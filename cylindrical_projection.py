from PIL import Image
import numpy as np
import math
from scipy import interpolate

def cut_limit(value):
    if value > 255:
        return np.uint8(255)
    elif value < 0:
        return np.uint8(0)
    else:
        return np.uint8(value)
# RGB value should be 0 <= x <= 255

def cylindrical_projection(image_name, view_point_angle = 0, HFOV_angle = 120, f_length = 300):

    HFOV = math.pi*HFOV_angle/180
    view_point = math.pi*view_point_angle/180
    # convert angles to radians

    cdc_image = Image.open(image_name)
    cdc_image_array = np.array(cdc_image)
    cdc_height, cdc_width, cdc_channel = np.shape(cdc_image_array)
    # get cylindrical image and information

    radius = cdc_width/(2*math.pi)
    # radius of cylinder

    prj_width = 2 * (math.tan(HFOV/2) * f_length)
    prj_height = cdc_height * math.sqrt(math.pow(f_length,2) + math.pow((prj_width/2),2)) / radius
    # calculate projected image's width length and height length

    prj_width = int(prj_width)
    prj_height = int(prj_height)

    if prj_width % 2 == 0:
        prj_width = prj_width - 1
    if prj_height % 2 == 0:
        prj_height = prj_height - 1
    # projected image width & height become odd number

    prj_channel = 3
    # for color image

    prj_index_map = np.zeros(shape = [prj_height,prj_width,2])
    # prj_index_map[height, width, mode]
    # mode = 1  => theta
    # mode = 0 => height of cylinder from center height   (-1*half of cylinder height <=  h <= half of cylinder height)

    interp_x = np.arange(0, cdc_width-0.5, 1)
    interp_y = np.arange(0, cdc_height-0.5, 1)
    interp_r = interpolate.interp2d(interp_x, interp_y, cdc_image_array[:, :, 0], kind = 'cubic')
    interp_g = interpolate.interp2d(interp_x, interp_y, cdc_image_array[:, :, 1], kind = 'cubic')
    interp_b = interpolate.interp2d(interp_x, interp_y, cdc_image_array[:, :, 2], kind = 'cubic')
    # cubic interpolation for each R, G, B

    x_c = (prj_width-1)/2
    y_c = (prj_height-1)/2

    # center point coordinates of projected image

    for y_i in range(prj_height):
        for x_i in range(prj_width):
            prj_index_map[y_i, x_i, 1] = math.atan((x_i-x_c)/f_length)
            prj_index_map[y_i, x_i, 0] = radius *(y_i-y_c) / math.sqrt(math.pow(x_i-x_c,2)+math.pow(f_length,2))
    # get theta and h for each coordinate in projected image

    prj_image_array = np.zeros(shape=[prj_height, prj_width, prj_channel], dtype=np.uint8)
    prj_view_point_map = np.zeros(shape = [prj_height,prj_width,2])

    prj_view_point_map[:, :, 1] = (((view_point + prj_index_map[:, :, 1]) + (2* math.pi)) % (2* math.pi)) * cdc_width / (2 * math.pi)
    prj_view_point_map[:, :, 0] = prj_index_map[:,:,0] + cdc_height/2
    # calculated coordinates using view point information

    for y_i in range(prj_height):
        for x_i in range(prj_width):
            y = prj_view_point_map[y_i, x_i, 0]
            x = prj_view_point_map[y_i,x_i,1]
            flag = True
            if y < 0 or y >= cdc_height:
                flag = False
                prj_image_array[y_i, x_i, :] = [0,0,0]
            if x < 0 or x >= cdc_width:
                prj_image_array[y_i, x_i, :] = [0,0,0]
                flag = False
            # zero padding for
            if flag == True:
                prj_image_array[y_i, x_i, 0] = cut_limit(interp_r(x, y))
                prj_image_array[y_i, x_i, 1] = cut_limit(interp_g(x, y))
                prj_image_array[y_i, x_i, 2] = cut_limit(interp_b(x, y))
            #  채우기 using interpolation
    img = Image.fromarray(prj_image_array)
    return img
