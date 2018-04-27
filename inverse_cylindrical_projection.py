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


def inverse_cylindrical_projection(prj_image_name, f_length, HFOV_angle):

    HFOV = math.pi * HFOV_angle / 180
    # Horizontal FOV degree value to radian value

    prj_image = Image.open(prj_image_name)
    prj_image_array = np.array(prj_image)
    prj_height, prj_width, prj_channel = np.shape(prj_image_array)
    # get projected image and image information

    prj_x_c = int((prj_width-1)/2)
    prj_y_c = int((prj_height-1)/2)
    # get center coordinate
    # Image width and height should be odd number

    radius = f_length
    # Suppose radius of cylinder and focal length have same value

    recv_cdc_width = HFOV * radius
    # recv_cdc = recovered cylindrical
    # 2*pi*r : width = 2*pi : HFOV


    zero_counter = 0
    # zero counter는 이미지 가로의 중앙 픽셀들에서 이미지가 없는 부분의 길이를 의미함
    for i in range(prj_height):
        if(prj_image_array[i,prj_x_c, :].all() == 0):
            zero_counter = zero_counter + 1
    recv_cdc_height = prj_height - zero_counter

    recv_cdc_width = int(recv_cdc_width)
    recv_cdc_height = int(recv_cdc_height)

    if recv_cdc_width % 2 == 0:
        recv_cdc_width = recv_cdc_width - 1
    if recv_cdc_height % 2 == 0:
        recv_cdc_height = recv_cdc_height - 1

    #set length of width and height as odd number

    recv_cdc_image_array = np.zeros([recv_cdc_height, recv_cdc_width, prj_channel], dtype= np.uint8)

    x_c = int((recv_cdc_width - 1) / 2)
    y_c = int((recv_cdc_height - 1) / 2)

    interp_x = np.arange(0, prj_width - 0.5, 1)
    interp_y = np.arange(0, prj_height - 0.5, 1)
    interp_r = interpolate.interp2d(interp_x, interp_y, prj_image_array[:, :, 0], kind='cubic')
    interp_g = interpolate.interp2d(interp_x, interp_y, prj_image_array[:, :, 1], kind='cubic')
    interp_b = interpolate.interp2d(interp_x, interp_y, prj_image_array[:, :, 2], kind='cubic')

    #cubic interpolation for each R G B.
    # 한번에 할 수도 있을 것 같긴한데 아직 잘 모르겠음

    for y_i in range(recv_cdc_height):
        for x_i in range(recv_cdc_width):
            theta = (x_i - x_c)/radius
            x_index = prj_x_c + f_length * math.tan(theta)
            y_index = prj_y_c + ((y_i-y_c)* math.sqrt(math.pow(x_index-prj_x_c, 2)+math.pow(f_length, 2)) / radius)
            # x_index, y_index = projected image에서 coordinate 를 의미

            flag = True
            if y_index < 0 or y_index >= prj_height:
                flag = False
                recv_cdc_image_array[y_i, x_i, :] =[0, 0, 0]
            if x_index < 0 or x_index >= prj_width:
                recv_cdc_image_array[y_i, x_i, :] = [0, 0, 0]
                flag = False
            # image의 범위를 넘어가면 zero padding
            if flag == True:
                recv_cdc_image_array[y_i, x_i, 0] = cut_limit(interp_r(x_index, y_index))
                recv_cdc_image_array[y_i, x_i, 1] = cut_limit(interp_g(x_index, y_index))
                recv_cdc_image_array[y_i, x_i, 2] = cut_limit(interp_b(x_index, y_index))
            # cubic interpolation 으로 값을 가져옴
    img = Image.fromarray(recv_cdc_image_array)
    return img

