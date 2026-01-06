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
import os
import py7zr

# User mods
from ciboulette.sql import interface, mastUT, observingconditions, observinglog
from ciboulette.mastdb import mast

# Interfaces init
data_interface = interface.interfaces()

# 3D line
HR3D = widgets.HTML(value='<P><HR SIZE="2"></P>', placeholder='', description='')

#####################################################################################
#
# Export function and IDE
#
#####################################################################################
# Export directory
widget_catalog = widgets.Text(description='Catalog:', disabled=False)
widget_catalog.value = 'UT1_MAST_CATALOG.csv'


widget_mast_directory = widgets.Text(description='Directory:', disabled=False)
widget_mast_directory.value = '../archive'

# Export button
widget_export = widgets.Button(
    description='Export',
    disabled=False,
    button_style='', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Export',
)

# Export Output
output_export = widgets.Output()

def export_func(b):
    with output_export:
        output_export.clear_output()
        data = mast.Mast()
        data.read(widget_catalog.value)
        data.get_number(widget_catalog.value)
        data.create(widget_mast_directory.value)
                
widget_export.on_click(export_func)

#####################################################################################
#
# Import function and IDE
#
#####################################################################################
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
        data_interface.mast_in(widget_science_program.label)

widget_import.on_click(import_func)

#####################################################################################
#
# Update function and IDE
#
#####################################################################################
# Telescope Unit
units = ['UT1', 'UT2', 'UT3', 'UT4']
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

        match widget_unit.label:
            case "UT1": ut = mastUT.mast_UT1()
            case "UT2": ut = mastUT.mast_UT2()
            case "UT3": ut = mastUT.mast_UT3()
            case "UT4": ut = mastUT.mast_UT4()
        
        ut.connect
        print(ut.database)
        ut.close
        # Instrument Type 
        ut.default(widget_id.value)
        # ID, Title observation, Collection, target notes
        ut.mast_update(widget_id.value, widget_title.value, widget_collection.label, widget_target_note.label)
        obs_log = observinglog.log()
        obs_log.default(widget_id.value)
        obs_conditons = observingconditions.conditions()
        obs_conditons.medium(widget_id.value)

widget_valid.on_click(valid_func)

#####################################################################################
#
# Compress function and IDE
#
#####################################################################################
# Compress directory
widget_directory = widgets.Text(description='Directory:', disabled=False)
widget_directory.value = '../archive'

# Compress button
widget_compress = widgets.Button(
    description='Compress',
    disabled=False,
    button_style='', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Compress',
)

# Compress Output
output_compress = widgets.Output()

def compress_func(b):
    with output_compress:
        output_compress.clear_output()
        os.chdir(widget_directory.value)
        files = os.listdir()
        for file in files:
            print(file+'.7z')
            with py7zr.SevenZipFile(file+'.7z', 'w') as archive:
                archive.write(file)
                
widget_compress.on_click(compress_func)

#####################################################################################
#
# IDE
#
#####################################################################################             
# Mast VBox
box_export = widgets.VBox([widget_mast_directory, HR3D, widget_export, output_export])
box_import = widgets.VBox([widget_science_program, HR3D, widget_import, output_import])
box_update = widgets.VBox([widget_unit, widget_id, widget_title , widget_collection, widget_target_note, widget_observing_condition, HR3D, widget_valid, output_valid]) 
box_compress = widgets.VBox([widget_directory, HR3D, widget_compress, output_compress])

# Mast Tab
tab_contents = ['Export', 'Import', 'Update', 'Compress']
mast_tabs = widgets.Tab()
mast_tabs.children = [box_export, box_import, box_update, box_compress]
mast_tabs.titles = [tab_contents[0],tab_contents[1],tab_contents[2],tab_contents[3]]
mast_tabs