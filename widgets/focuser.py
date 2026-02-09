"""
class mast widgets
"""

__authors__ = ("Dominique Touzan","ciboulette module")
__contact__ = ("dtouzan@gmail.com","https://github.com/dtouzan/ciboulette")
__copyright__ = "MIT"
__date__ = "2026-02-09"
__version__= "1.0.0"

# Globals mods
import ipywidgets as widgets
import os

# User mods
from ciboulette.indiclient.indiEAFpy import EAFpy

# Output
output_ctrl = widgets.Output()
output_configuration = widgets.Output()
output_visualisation = widgets.Output()

# 3D line
HR3D = widgets.HTML(value='<P><HR SIZE="2"></P>', placeholder='', description='')

#####################################################################################
#
# CONNECT/DISCONNECT
#
#####################################################################################    
# Connect button
widget_connect = widgets.Button(
    description='Connect',
    disabled=False,
    button_style='', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Connect the driver',
)

# Disconnect button
widget_disconnect = widgets.Button(
    description='Disconnect',
    disabled=False,
    button_style='', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Disconnect the driver',
)

# CCD name/IP 
EAF_ip = ['192.168.1.141',]
widget_EAF_ip = widgets.Dropdown(options=[(value, i+1) for i, value in enumerate(EAF_ip)], value=1, description='EAF IP:')
EAF_focuser = EAFpy(host=widget_EAF_ip.label, port=7624)

def connect_func(b):
    with output_ctrl:
        output_ctrl.clear_output()
        EAF_focuser.CONFIG_LOAD
        EAF_focuser.getprop
        
def disconnect_func(b):
    with output_ctrl:
        output_ctrl.clear_output()
        EAF_focuser.disconnect()

widget_connect.on_click(connect_func)
widget_disconnect.on_click(disconnect_func)

#####################################################################################
#
# CONTROL
#
#####################################################################################    
# Focuser increment
focuser_values = ['2', '5', '10', '20', '50', '200', '500', '1000']
widget_focuser_inc = widgets.Dropdown(options=[(value, i+1) for i, value in enumerate(focuser_values)], value=4, description='Step:')

# Up button
widget_up = widgets.Button(
description='<',
disabled=False,
button_style='', # 'success', 'info', 'warning', 'danger' or ''
tooltip='Up turn',)

# Down button
widget_down = widgets.Button(
description='>',
disabled=False,
button_style='', # 'success', 'info', 'warning', 'danger' or ''
tooltip='Down turn',)

#####################################################################################
#
# IDE
#
#####################################################################################             
# Focuser VBox
box_connect = widgets.VBox([widget_EAF_ip,
                            HR3D,
                            widgets.HBox([widget_connect, widget_disconnect]), 
                            output_ctrl])
box_control = widgets.VBox([widgets.HBox([widget_focuser_inc, widget_up, widget_down]), ])

# Mast Tab
tab_contents = ['Connect/Disconnect', 'EAF', ]
EAFpy_tabs = widgets.Tab()
EAFpy_tabs.children = [box_connect, box_control]
EAFpy_tabs.titles = [tab_contents[0], tab_contents[1]]



