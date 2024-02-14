# import Revit & pyrevit libraries 
from Autodesk.Revit.DB import FilteredElementCollector, Level
from pyrevit import script
import os

# get current Revit document
doc = __revit__.ActiveUIDocument.Document

# collect all levels in the current project
levels_all = FilteredElementCollector(doc).\
			OfClass(Level).\
			WhereElementIsNotElementType().\
			ToElements()

# take levels names, check if pinned and check if is being monitored
levels_data = sorted([[l1.Name, l1.Pinned, l1.IsMonitoringLinkElement()] for l1 in levels_all])

# loop through all levels and count pinned, unpinned, monitored and nonmonitored levels
count_pinned       = 0
count_unpinned     = 0
count_monitored    = 0
count_nonmonitored = 0

for lvl in levels_all:
	if lvl.Pinned:
		count_pinned += 1
	else:
		count_unpinned += 1 

	if lvl.IsMonitoringLinkElement():
		count_monitored += 1
	else:
		count_nonmonitored += 1

# create primary table data
count_data = [
			[len(levels_all),
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
				title = "LEVELS INSPECTION RESULTS"
				)

# secondary table data
output.print_table(levels_data, 
				columns = ["Level Name", "Pinned (True or False)", "Monitored (True or False)"]
				)
script.exit()