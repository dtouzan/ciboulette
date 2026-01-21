"""
class mast widgets
"""

__authors__ = ("Dominique Touzan","ciboulette module")
__contact__ = ("dtouzan@gmail.com","https://github.com/dtouzan/ciboulette")
__copyright__ = "MIT"
__date__ = "2026-01-20"
__version__= "1.0.0"

# Globals mods
import ipywidgets as widgets
import os
import matplotlib.pyplot as plt
# Astropy mods
from astropy.io import fits

# User mods
from ciboulette.indiclient.imx477 import imx477Cam

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
    tooltip='Disconnect he driver',
)

# CCD name/IP 
ccd_ip = ['192.168.1.10',]
widget_ccd_ip = widgets.Dropdown(options=[(value, i+1) for i, value in enumerate(ccd_ip)], value=1, description='CCD IP:')
imx477 = imx477Cam(host=widget_ccd_ip.label, port=7624)

def connect_func(b):
    with output_ctrl:
        output_ctrl.clear_output()
        imx477.CONFIG_LOAD
        imx477.getprop
        
def disconnect_func(b):
    with output_ctrl:
        output_ctrl.clear_output()
        imx477.disconnect()


widget_connect.on_click(connect_func)
widget_disconnect.on_click(disconnect_func)

#####################################################################################
#
# CONFIGURATION
#
#####################################################################################    
# Properties button
widget_properties = widgets.Button(
    description='Properties',
    disabled=False,
    button_style='', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Properties indi_getprop',
)

def properties_func(b):
    with output_configuration:
        output_configuration.clear_output()
        imx477.getprop

# Format option
widget_CCD_CAPTURE_FORMAT = widgets.Dropdown(options=['Raw', 'Raw mono'], value='Raw mono', description='Format:')

def CCD_CAPTURE_FORMAT_change(change):
    with output_configuration:
        output_configuration.clear_output()
        if (change.new == 'Raw'):
            imx477.RAW
        if (change.new == 'Raw mono'):
            imx477.RAW_MONO

# Binning option
widget_CCD_BINNING = widgets.Dropdown(options=['1', '2'], value='1', description='Binning:')

def CCD_BINNING_change(change):
    with output_configuration:
        output_configuration.clear_output()
        if (change.new == '1'):
            imx477.BINNING1
        if (change.new == '2'):
            imx477.BINNING2

# Type option
widget_CCD_FRAME_TYPE = widgets.Dropdown(options=['Light', 'Bias', 'Dark', 'Flat'], value='Light', description='Type:')

def CCD_FRAME_TYPE_change(change):
    with output_configuration:
        output_configuration.clear_output()
        if (change.new == 'Light'):
            imx477.FRAME_LIGHT
        if (change.new == 'Bias'):
            imx477.FRAME_BIAS
        if (change.new == 'Dark'):
            imx477.FRAME_DARK
        if (change.new == 'Flat'):
            imx477.FRAME_FLAT

widget_properties.on_click(properties_func)
widget_CCD_CAPTURE_FORMAT.observe(CCD_CAPTURE_FORMAT_change, names='value')
widget_CCD_BINNING.observe(CCD_BINNING_change, names='value')
widget_CCD_FRAME_TYPE.observe(CCD_FRAME_TYPE_change, names='value')

#####################################################################################
#
# IDE
#
#####################################################################################             
# Mast VBox
box_connect = widgets.VBox([widget_ccd_ip,
                            HR3D,
                            widgets.HBox([widget_connect, widget_disconnect]), 
                            output_ctrl])
box_configuration = widgets.VBox([widgets.HBox([widget_CCD_CAPTURE_FORMAT,
                                                widget_CCD_BINNING,
                                                widget_CCD_FRAME_TYPE]),
                                  HR3D,
                                  widget_properties,
                                  output_configuration, ])
box_visu = widgets.VBox([output_visualisation, ])

# Mast Tab
tab_contents = ['Connect/Disconnect', 'Configuration', 'Visualisation']
imx477_tabs = widgets.Tab()
imx477_tabs.children = [box_connect, box_configuration, box_visu]
imx477_tabs.titles = [tab_contents[0],tab_contents[1],tab_contents[2], ]

