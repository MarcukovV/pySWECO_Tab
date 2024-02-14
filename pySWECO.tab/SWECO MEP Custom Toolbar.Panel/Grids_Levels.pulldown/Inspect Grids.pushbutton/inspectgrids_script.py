# import Revit & pyrevit libraries 
from Autodesk.Revit.DB import FilteredElementCollector, Grid
from pyrevit import forms, script
import os

# get current Revit document
doc = __revit__.ActiveUIDocument.Document

# collect all grids in the current project
grids_all = FilteredElementCollector(doc).\
			OfClass(Grid).\
			WhereElementIsNotElementType().\
			ToElements()

# create a scenario where there are no grids in the model
if not grids_all:
	forms.alert(
	'Active Revit document does not contain grids',
	title = "Script is cancelled",
	ok = False
	)
	script.exit()

# take grids names, check if pinned and check if is being monitored
grids_data = sorted([[g1.Name, g1.Pinned, g1.IsMonitoringLinkElement()] for g1 in grids_all])

# loop through all grids and count pinned, nonpinned, monitored and nonmonitored grids
count_pinned 	   = 0
count_unpinned 	   = 0
count_monitored    = 0
count_nonmonitored = 0

for grd in grids_all:
	if grd.Pinned:
		count_pinned += 1
	else:
		count_unpinned += 1

	if grd.IsMonitoringLinkElement():
		count_monitored += 1
	else:
		count_nonmonitored += 1

# create primary table data
count_data = [
			[len(grids_all),
			"{} / {}".format(count_pinned, count_unpinned),
			"{} / {}".format(count_monitored, count_nonmonitored)]
			]

# get current working directory where current Python script is located
# specify the relative path to the file image
# join the current directory with the relative path to create the full path
current_dir      = os.path.dirname(os.path.realpath(__file__))
relative_path    = 'pySWECOLogo.png'
sweco_image_path = os.path.join(current_dir, relative_path)

# output module 
output = script.get_output()

# set output window style
output.add_style('body { color: black; font-size: 14px; background-color: white; font-family: Arial }')

# import SWECO logo
output.print_image(sweco_image_path)

# primary table data
output.print_table(count_data, 
				columns = ["Total Count", "Pinned / Un-Pinned Count", "Monitored / Non-monitored Count"],
				title = "GRIDS INSPECTION RESULTS"
				)

# secondary table data
output.print_table(grids_data, 
				columns = ["Grid Name", "Pinned (True or False)", "Monitored (True or False)"]
				)
script.exit()