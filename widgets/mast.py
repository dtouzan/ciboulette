"""
class mast widgets
"""

__authors__ = ("Dominique Touzan","ciboulette module")
__contact__ = ("dtouzan@gmail.com","https://github.com/dtouzan/ciboulette")
__copyright__ = "MIT"
__date__ = "2025-12-08"
__version__= "1.0.0"

# Globals mods
import ipywidgets as widgets

# User mods
from ciboulette.sql import interface

# Interfaces init
data_interface = interface.interfaces()

# 3D line
HR3D = widgets.HTML(value='<P><HR SIZE="2"></P>', placeholder='', description='')

# Science Programe available
science_programs = data_interface.scienceprogram_title
widget_science_program = widgets.Dropdown(options=[(value, i+1) for i, value in enumerate(science_programs)], value=3, description='Available:')

# Valid button
widget_import = widgets.Button(
    description='Import',
    disabled=False,
    button_style='', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Import',
)

# Import Output
output_import = widgets.Output()

def import_func(b):
    with output_import:
        output_import.clear_output()
        print(widget_science_program.label)

widget_import.on_click(import_func)

# Telescope Unit
units = ['UT1', 'UT2', 'UT3', 'UT4', 'UT5' , 'UT6', 'UT7', 'UT8']
widget_unit = widgets.Dropdown(options=[(value, i+1) for i, value in enumerate(units)], value=1, description='Unit:')

# Observation ID
widget_id = widgets.Text(description='ID:', disabled=False)

# Observation Title
widget_title = widgets.Text(description='Title:', disabled=False)

# Observation Collections
collections = data_interface.collection
widget_collection = widgets.Dropdown(options=[(value, i+1) for i, value in enumerate(collections)], value=1, description='Collection:')

# Target Notes
target_notes = ['Not specified', 'Nova report', 'Supernova report', 'Asteroid tracking', 'Comet tracking' , 'Observation tracking', 'Variable tracking', 'Region', 'HII region', 'Instrument control']
widget_target_note = widgets.Dropdown(options=[(value, i+1) for i, value in enumerate(target_notes)], value=1, description='Notes:')

# Observing Conditions 
observing_conditions = ['Default', 'Minimum', 'Medium']
widget_observing_condition = widgets.Dropdown(options=[(value, i+1) for i, value in enumerate(observing_conditions)], value=3, description='Conditions:')

# Valid button
widget_valid = widgets.Button(
    description='Valid',
    disabled=False,
    button_style='', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Valid',
)

# Valid Output
output_valid = widgets.Output()

def valid_func(b):
    with output_valid:
        output_valid.clear_output()
        print(widget_unit.label)
        print(widget_id.value)
        print(widget_title.value)
        print(widget_collection.label)
        print(widget_target_note.label)
        print(widget_observing_condition.label)

widget_valid.on_click(valid_func)

             
# Mast VBox
box_import= widgets.VBox([widget_science_program, HR3D, widget_import, output_import])
box_mast = widgets.VBox([widget_unit, widget_id, widget_title , widget_collection, widget_target_note, widget_observing_condition, HR3D, widget_valid, output_valid]) 