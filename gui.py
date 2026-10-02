from calc import *  
import dearpygui.dearpygui as dpg  
  
x_array=[0,0]  
y_array=[0,0]  
result_color=(92, 155, 255)  
  
dpg.create_context()  
dpg.create_viewport(title='Balistica', width=500, height=800)  
  
with dpg.theme() as calc_button_theme:  
    with dpg.theme_component(dpg.mvButton):  
        dpg.add_theme_color(dpg.mvThemeCol_Button,        (33, 118, 255), category=dpg.mvThemeCat_Core)  
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (70, 140, 255), category=dpg.mvThemeCat_Core)  # lighter  
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive,  (20, 90, 210),  category=dpg.mvThemeCat_Core)  # darker when pressed  
  
  
def calc_callback(sender, data):  
    start_set = [int(dpg.get_value("start_X")), int(dpg.get_value("start_Y")), int(dpg.get_value("start_Z"))]  
  
    end_set = [int(dpg.get_value("end_X")), int(dpg.get_value("end_Y")), int(dpg.get_value("end_Z"))]  
  
    l_horizontal_distance = get_distance(start_set, end_set)  
  
    l_vertical_distance = get_vertical_distance(start_set, end_set)  
  
    l_lauch_speed = dpg.get_value("dpg_lauch_speed")  
    l_gravity_force = dpg.get_value("dpg_gravity_force")  
    l_prefer_high_arc = dpg.get_value("dpg_prefer_high_arc")  
  
    l_yaw = get_yaw(start_set, end_set)  
    l_yaw_string = "Yaw is : " + str(round(l_yaw[0], 3)) + "° " + str(l_yaw[1])  
    print(l_yaw_string)  
    dpg.set_value("dpg_yaw_string", l_yaw_string)  
  
    l_distance_string = "Distance betwean points is : " + str(round(l_horizontal_distance, 3)) + " m"  
    print(l_distance_string)  
    dpg.set_value("dpg_distance_string", l_distance_string)  
  
    l_pitch = get_pitch(l_horizontal_distance, l_vertical_distance, l_lauch_speed, l_gravity_force, l_prefer_high_arc)  
    if l_pitch is None:  
        dpg.set_value("dpg_pitch_string","No pitch available.")  
    l_pitch = convert(l_pitch)  
    l_pitch_string = "Pich is : " + str(round(l_pitch, 3)) + "° "  
    dpg.set_value("dpg_pitch_string", l_pitch_string)  
  
    x_data=get_x_series(l_horizontal_distance,200)  
    y_data=get_y_series(x_data,l_lauch_speed,l_pitch,l_gravity_force)  
  
    dpg.set_value("my_series", [x_data, y_data])  
    dpg.fit_axis_data("x_axis")  
    dpg.fit_axis_data("y_axis")  
  
  
  
  
with dpg.window(label="Test", tag="main"):  
    dpg.add_text("Coordinates")  
    dpg.add_separator()  
  
    with dpg.group(horizontal=True):  
        dpg.add_text("Start point: ")  
        for axis in ("X", "Y", "Z"):  
            dpg.add_input_text(  
                tag=f"start_{axis}",  
                hint=axis,  # placeholder, shown while the field is empty  
                width=80,  
                decimal=True,  # only allow digits, "." and "-"  
            )  
  
    with dpg.group(horizontal=True):  
        dpg.add_text("End point:   ")  
        for axis in ("X", "Y", "Z"):  
            dpg.add_input_text(  
                tag=f"end_{axis}",  
                hint=axis,  # placeholder, shown while the field is empty  
                width=80,  
                decimal=True,  # only allow digits, "." and "-"  
            )  
    dpg.add_separator()  
    dpg.add_text("Properties")  
  
    dpg.add_input_float(label="Launch speed m/s", tag="dpg_lauch_speed")  
    dpg.add_input_float(default_value=9.81, label="Gravity force m/s^2", tag="dpg_gravity_force")  
    dpg.add_checkbox(label="Prefer high arc", tag="dpg_prefer_high_arc", default_value=True)  
  
    dpg.add_separator()  
    dpg.add_text("Summit")  
    with dpg.group(horizontal=True):  
        # dpg.add_spacer(width=10)  
        btn=dpg.add_button(label="Calculate", width=470, callback=calc_callback)  
  
    with dpg.plot(label="Projectile", width=470, height=420):  
        dpg.add_plot_legend()  
        dpg.add_plot_axis(dpg.mvXAxis, label="x (m)", tag="x_axis")  
        with dpg.plot_axis(dpg.mvYAxis, label="y (m)", tag="y_axis"):  
            dpg.add_line_series(x_array, y_array, label="Projectile", tag="my_series")  
  
        dpg.fit_axis_data("x_axis")  
        dpg.fit_axis_data("y_axis")  
  
    dpg.add_separator()  
    dpg.add_text("Results")  
    dpg.add_text("", tag="dpg_yaw_string", color=result_color)  
    dpg.add_text("", tag="dpg_distance_string", color=result_color)  
    dpg.add_text("", tag="dpg_pitch_string", color=result_color)  
  
dpg.bind_item_theme(btn, calc_button_theme)  
  
dpg.setup_dearpygui()  
dpg.show_viewport()  
dpg.set_primary_window("main", True)  
dpg.start_dearpygui()  
dpg.setup_dearpygui()  
dpg.destroy_context()