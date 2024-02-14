# IMPORTS
# import Revit & pyrevit libraries 
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInParameter
from Autodesk.Revit.DB.Mechanical import MechanicalSystemType
from Autodesk.Revit.DB.Plumbing import PipingSystemType
from pyrevit import script
import os

# get current Revit document
doc = __revit__.ActiveUIDocument.Document

# DATA COLLECTION
# collect duct system types in current model / returns a list
mep_duct_sys = FilteredElementCollector(doc).\
				OfClass(MechanicalSystemType).\
				WhereElementIsElementType().\
				ToElements()

# collect pipe system types in current model / returns a list
mep_pipe_sys = FilteredElementCollector(doc).\
				OfClass(PipingSystemType).\
				WhereElementIsElementType().\
				ToElements()

# create lists of system type names and their calcs modes
duct_calcs_sys, pipe_calcs_sys = [], []

# append duct system types and calculation parameter modes to a list
for dc in mep_duct_sys:
	duct_sys	= dc.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
	duct_calcs	= dc.get_Parameter(BuiltInParameter.RBS_DUCT_SYSTEM_CALCULATION_PARAM).AsValueString()
	duct_calcs_sys.append((duct_sys, duct_calcs))

# append pipe system types and calculation parameter modes to a list
for pp in mep_pipe_sys:
	pipe_sys	= pp.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
	pipe_calcs	= pp.get_Parameter(BuiltInParameter.RBS_PIPE_SYSTEM_CALCULATION_PARAM).AsValueString()
	pipe_calcs_sys.append((pipe_sys, pipe_calcs))

# sort duct list in alphabetical order and count total number of duct system types
duct_calcs_sys = sorted(duct_calcs_sys)

# sort pipe list in alphabetical order and count total number of pipe system types
pipe_calcs_sys = sorted(pipe_calcs_sys)

table_separator_1 = [("<b>1. DUCT SYSTEM TYPE ({})</b>".format(len(mep_duct_sys)), "")]
table_separator_2 = [("<b>2. PIPE SYSTEM TYPE ({})</b>".format(len(mep_pipe_sys)), "")]
combined_data = table_separator_1 + duct_calcs_sys + table_separator_2 + pipe_calcs_sys

# OUTPUT FOR USER
# get current working directory where current Python script is located
# specify the relative path to the file image
# join the current directory with the relative path to create the full path
current_dir      = os.path.dirname(os.path.realpath(__file__))
relative_path    = 'pySWECOLogo.png'
sweco_image_path = os.path.join(current_dir, relative_path)

# output module / set output window style
output = script.get_output()
output.add_style('body { color: black; background-color: white; font-size: 14px; font-family: Arial }')

# import SWECO logo
output.print_image(sweco_image_path)

output.print_table(combined_data, 
					columns = ["SYSTEM TYPE", "CALCULATION MODE"]
					)

script.exit()