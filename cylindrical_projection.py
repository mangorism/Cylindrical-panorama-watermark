from PIL import Image
import numpy as np
import math


view_point_angle = 0
HFOV_angle = 30
f_length = 1000
# f_length = focal length
'''
view_point : Where to see 0 ~ 360
HFOV : Horizontal Field of View
'''
HFOV = math.pi*HFOV_angle/180
view_point = math.pi*view_point_angle/180

cdc_image = Image.open('cylindrical.jpg')
cdc_image_array = np.array(cdc_image)
cdc_height, cdc_width, cdc_channel = np.shape(cdc_image_array)

radius = cdc_width/(2*math.pi)

prj_width = 2 * (math.tan(HFOV/2) * f_length)
prj_height = cdc_height * math.sqrt(math.pow(f_length,2) + math.pow((prj_width/2),2)) / radius

prj_width = int(prj_width)
prj_height = int(prj_height)

if prj_width % 2 == 0:
    prj_width = prj_width - 1
if prj_height % 2 == 0:
    prj_height = prj_height - 1
# projection image width & height become odd number

prj_channel = 3

prj_index_map = np.zeros(shape = [prj_height,prj_width,2])
# 1 = theta
# 0 = h



x_c = int((prj_width-1)/2)
y_c = int((prj_height-1)/2)

for x_i in range(prj_width):
    for y_i in range(prj_height):
        prj_index_map[y_i, x_i, 1] = math.atan((x_i-x_c)/f_length)
        prj_index_map[y_i, x_i, 0] = radius *(y_i-y_c) / math.sqrt(math.pow(x_i-x_c,2)+math.pow(f_length,2))

prj_image_array = np.zeros(shape=[prj_height, prj_width, prj_channel], dtype=np.uint8)

prj_view_point_map = np.zeros(shape = [prj_height,prj_width,2])

prj_view_point_map[:, :, 1] = (((view_point + prj_index_map[:, :, 1]) + (2* math.pi)) % (2* math.pi)) * cdc_width / (2 * math.pi)
prj_view_point_map[:, :, 0] = prj_index_map[:,:,0] + cdc_height/2

for x_i in range(prj_width):
    for y_i in range(prj_height):
        y = int(prj_view_point_map[y_i, x_i, 0])
        x = int(prj_view_point_map[y_i,x_i,1])
        flag = True
        if y < 0 or y >= cdc_height:
            flag = False
            prj_image_array[y_i, x_i, :] = [0,0,0]
        if x < 0 or x >= cdc_width:
            prj_image_array[y_i, x_i, :] = [0,0,0]
            flag = False
        if flag == True:
            prj_image_array[y_i, x_i, :] = cdc_image_array[y,x,:]

img = Image.fromarray(prj_image_array)
img.show()



'''
for i in range(15):
    view_point_angle = i*10
    view_point = math.pi*view_point_angle/180
    prj_view_point_map[:, :, 1] = (((view_point + prj_index_map[:, :, 1]) + (2* math.pi)) % (2* math.pi)) * cdc_width / (2 * math.pi)
    for x_i in range(prj_width):
        for y_i in range(prj_height):
            y = int(prj_view_point_map[y_i, x_i, 0])
            x = int(prj_view_point_map[y_i,x_i,1])
            flag = True
            if y < 0 or y >= cdc_height:
                flag = False
                prj_image_array[y_i, x_i, :] = [0,0,0]
            if x < 0 or x >= cdc_width:
                prj_image_array[y_i, x_i, :] = [0,0,0]
                flag = False
            if flag == True:
                prj_image_array[y_i, x_i, :] = cdc_image_array[y,x,:]

    img = Image.fromarray(prj_image_array)
    img.show()
'''