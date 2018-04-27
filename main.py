from cylindrical_projection import cylindrical_projection
from inverse_cylindrical_projection import inverse_cylindrical_projection


f_length = 300
HFOV_angle = 120
view_point_angle = 90

cylindrical_image_name = "cylindrical.jpg"

prj_image_name = "cylindrical_projected_image.jpg"
# prj = projected

cylindrical_projected_image = cylindrical_projection(cylindrical_image_name, view_point_angle, HFOV_angle, f_length)
cylindrical_projected_image.save('cylindrical_projected_image.jpg')
#cylinder image to projected image and save the image

inversed_image = inverse_cylindrical_projection(prj_image_name, f_length, HFOV_angle)
inversed_image.save('inversed_image.jpg')
#Recover projected image and save the image