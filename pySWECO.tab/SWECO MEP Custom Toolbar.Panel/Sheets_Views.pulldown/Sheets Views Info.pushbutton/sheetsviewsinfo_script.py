# IMPORTS
# import Revit & pyrevit libraries
from Autodesk.Revit.DB import (
	FilteredElementCollector, 
	View, 
	BuiltInParameter
	)

from pyrevit import script

import os

# get current Revit document
doc = __revit__.ActiveUIDocument.Document

# get current working directory where current Python script is located
# specify the relative path to the file image
# join the current directory with the relative path to create the full path
current_dir      = os.path.dirname(os.path.realpath(__file__))
relative_path    = 'pySWECOLogo.png'
sweco_image_path = os.path.join(current_dir, relative_path)

# DATA COLLECTION
# get all view types in the model
all_views = FilteredElementCollector(doc).\
			OfClass(View).\
			WhereElementIsNotElementType().\
			ToElements()

# create a list of most used views
view_list = [
			"3D Views",
			"Area Plans",
			"Ceiling Plans",
			"Drafting Views",
			"Elevations",
			"Floor Plans", 
			"Legends",
			"Renderings",
			"Sections",
			"Schedules",
			"Sheets", 
			"Structural Plans",
			"Walkthroughs"
			]

# filter views / remove view templates
all_views_types = [av for av in all_views if not av.IsTemplate and av.get_Parameter(BuiltInParameter.VIEW_FAMILY).AsString() in view_list]

# FUNCTION
# create a function to count views
def views_count(view_name):
	try:
		if view_name in ["Legends", "Sheets"]:
			l_s	 	 	= len([ls for ls in all_views_types if ls.get_Parameter(BuiltInParameter.VIEW_FAMILY).AsString() == view_name])
			result_1 	= ['<b>{}</b>'.format(view_name), l_s, "N/A", "N/A"]
			return result_1
		elif view_name  == "Schedules":
			schedule	= len([sc for sc in all_views_types if sc.get_Parameter(BuiltInParameter.VIEW_FAMILY).AsString() == view_name and not "Revision Schedule" in sc.get_Parameter(BuiltInParameter.VIEW_NAME).AsString()])
			result_2 	= ['<b>{}</b>'.format(view_name), schedule, "N/A", "N/A"]
			return result_2
		else:
			view		= [v for v in all_views_types if v.get_Parameter(BuiltInParameter.VIEW_FAMILY).AsString() == view_name]
			v_sh		= len([vs for vs in view if vs.get_Parameter(BuiltInParameter.VIEWER_SHEET_NUMBER).AsString() != "---"])
			v_not_sh	= len([vns for vns in view if vns.get_Parameter(BuiltInParameter.VIEWER_SHEET_NUMBER).AsString() == "---"])
			result_3 	= ['<b>{}</b>'.format(view_name), len(view), v_sh, v_not_sh]
			return result_3
	except:
		pass

# OUTPUT FOR USER
# table data
data = [
		[""],
		views_count("3D Views"),
		[""],
		views_count("Ceiling Plans"),
		[""],
		views_count("Elevations"),
		[""],
		views_count("Floor Plans"),
		[""],
		views_count("Legends"),
		[""],
		views_count("Sections"),
		[""],
		views_count("Schedules"),
		[""],
		views_count("Sheets"),
		[""],
		[""],
		[""],
		views_count("Area Plans"),
		[""],
		views_count("Drafting Views"),
		[""],
		views_count("Renderings"),
		[""],
		views_count("Structural Plans"),
		[""],
		views_count("Walkthroughs")
		]

# import output module
output = script.get_output()

# set output style and window height
output.add_style('body { color: black; background-color: white; font-size: 14px; font-family: Arial }')
output.set_height(700)

# import SWECO logo
output.print_image(sweco_image_path)

output.print_table(
					data, 
					title = "TABLE OF SHEETS & VIEWS COUNT",
					columns = ["VIEW TYPE", "Total Number of Views", "Views on Sheets", "Views not on Sheets"]
					)
script.exit()