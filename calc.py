import math  
import numpy as np  
  
# start = [400, 2000, 60]  
# end = [-300, -500, 120]  
  
  
def convert(radians):  
    return math.degrees(radians)  
  
  
def get_distance(cor_set1, cor_set2):  
    l_return = math.sqrt(  
        math.pow(cor_set2[0] - cor_set1[0], 2) +  
        math.pow(cor_set2[1] - cor_set1[1], 2))  
    return l_return  
  
  
def get_vertical_distance(cor_set1, cor_set2):  
    return cor_set2[2] - cor_set1[2]  
  
  
def get_yaw(cor_set1, cor_set2, ):  
    dx = cor_set2[0] - cor_set1[0]  
    dy = cor_set2[1] - cor_set1[1]  
  
    if dx == 0 and dy == 0:  
        raise ValueError("Cannon and target are at the same point")  
    l_angle = math.degrees(math.atan2(dy, dx)) % 360  # 0-360°, counterclockwise from +X  
  
    if l_angle > 180:  
        l_angle = 360 - l_angle  
        l_retrun = [l_angle, "Clockwise"]  
  
    else:  
        l_retrun = [l_angle, "Anti-Clockwise"]  
  
    return l_retrun  
  
  
def get_pitch(l_horizontal_distance, l_vertical_distance, launch_speed, gravity=9.81, prefer_high_arc=True):  
    # Step 1 - shared term  
  
    l_gravity_term = (gravity * math.pow(l_horizontal_distance, 2)) / (2 * math.pow(launch_speed, 2))  
  
    # Step 2 quadratuic coefficients  
    l_horizontal_term = -l_horizontal_distance  
    l_height_adjusted_gravity_term = l_vertical_distance + l_gravity_term  
  
    # Step 3 Discriminant  
    l_disriminant = math.pow(l_horizontal_term, 2) - 4 * l_gravity_term * l_height_adjusted_gravity_term  
  
    # Step 4 unreachble check  
    if l_disriminant < 0:  
        return None  # target unreachable at this launch_speed  
  
    # Step 5 two tangent solutions    l_tan_angle_option_a = (-l_horizontal_term + math.sqrt(l_disriminant)) / (2 * l_gravity_term)  
    l_tan_angle_option_b = (-l_horizontal_term - math.sqrt(l_disriminant)) / (2 * l_gravity_term)  
  
    # Step 6 — convert to angles:  
    l_angle_option_a_rad = math.atan(l_tan_angle_option_a)  
    l_angle_option_b_rad = math.atan(l_tan_angle_option_b)  
  
    # Step 8 pick flat vs loafted  
    l_flat_angle_rad = min(l_angle_option_a_rad, l_angle_option_b_rad)  
    l_lofted_angle_rad = max(l_angle_option_a_rad, l_angle_option_b_rad)  
  
    # Step 9 decide path  
  
    if prefer_high_arc == True:  
        return l_lofted_angle_rad  
    elif prefer_high_arc == False:  
        return l_flat_angle_rad  
  
        # print("Angle betwean two points is", get_yaw(start, end), "°")  
  
  
def get_x_series(l_x_max, points):  
    step = l_x_max / points  
    return np.arange(0, l_x_max, step)  
  
  
def get_y_series(l_x_array, l_launch_speed, angle, gravity):  
    y_array = []  
    angle = math.radians(angle)  
    for x in l_x_array:  
        # Step 1: x * tan(angle)  
        step1 = x * math.tan(angle)  
  
        # Step 2: gravity * x squared  
        step2 = gravity * math.pow(x, 2)  
  
        # Step 3: 2 * velocity squared * cos^2(angle)  
        step3 = 2 * math.pow(l_launch_speed, 2) * math.cos(angle) ** 2  
  
        y_array.append(float(step1 - step2 / step3))  
    return y_array  
  
  
# print("Distance betwean two points is", math.ceil(get_distance(start, end)), "m")  
#  
# h = get_distance(start, end)  
# v = get_vertical_distance(start, end)  
#  
# print(get_pitch(h, v, 2000, gravity=9.81, prefer_high_arc=True))  
  
# x_array = get_x_series(4179.77013, 200)  
# print(x_array)  
# y_array=get_y_series(x_array, 240, 66.867, 9.82)  
#  
# print(y_array)