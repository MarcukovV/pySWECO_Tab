# import pyrevit libraries
from pyrevit import revit, DB, forms, script

# import module to get directory path
import os 

# import Counter class to count occurances
from collections import Counter

# get current Revit document
doc = __revit__.ActiveUIDocument.Document

# import output module
output = script.get_output()

# collect all user worksets in current Revit model
user_workset_list	  = DB.FilteredWorksetCollector(doc).\
						OfKind(DB.WorksetKind.\
						UserWorkset).\
						ToWorksets()
# create a dictionary with workset names and ids
user_workset_dict 	  = {workset.Name: workset.Id for workset in user_workset_list}

# sort worksets keys in alphabetical order and select worksets for inspection by using pyrevit form
sorted_user_workset   = sorted(user_workset_dict.keys())
workset_inspect       = forms.SelectFromList.show(
						sorted_user_workset,
						title="Workset(s) Inspection",
						width = 450,
						height = 750,
						button_name="Inspect Workset(s)",
						multiselect=True
						)
# create a scenario where Revit user does not select anything and cancels
if not workset_inspect:
	forms.alert(
	"No workset(s) selected for inspection",
	title = "Script is cancelled",
	ok = False
	)
	script.exit()
else:
	# get current working directory where your Python script is located
	current_dir = os.path.dirname(os.path.realpath(__file__))
	# specify the relative path to your file image
	relative_path = 'pySWECOLogo.png'
	# join the current file directory with the relative path to create the full path
	sweco_image_path = os.path.join(current_dir, relative_path)
	# add SWECO logo to the output to create SWECO style
	output.print_image(sweco_image_path)

	# set general output style
	output.add_style('body { color: black; background-color: white; font-size: 14px; font-family: Arial }')
	# create a table that shows total number of user worksets and worksets selected for inspection
	table_data = [
				 [str(len(user_workset_list)), 
				 str(len(workset_inspect))]
				 ]
	output.print_table(
						table_data,
						columns = ["Total Number of User Worksets in the Revit Model", "User Worksets Selected for Inspection"]
						)
	# Iterate through selected worksets
	for idx, workset_name in enumerate(workset_inspect, 1):
		workset_id = user_workset_dict.get(workset_name)
		if workset_id:
			output.print_md("<span style='color: black; font-weight: bold; font-size: 15px; font-family: Arial'>{}. {} Workset:</span>".format(idx, workset_name))
			element_workset_filter = DB.ElementWorksetFilter(workset_id, False)
			user_workset_elements  = DB.FilteredElementCollector(doc).\
									 WherePasses(element_workset_filter).\
									 ToElements()
			# find elements that have supercomponent properties and remove elements with supercomponent properties 
			workset_elements = [el for el in user_workset_elements if not (isinstance(el, DB.FamilyInstance) and el.SuperComponent is not None)]
			# create a set with mep model categories 
			set_0 = set([
					"Abutments",
					"Air Terminals",
					"Areas",
					"Audio Visual Devices",
					"Bearings",
					"Bridge Cables",
					"Bridge Decks",
					"Bridge Framing",
					"Cable Tray Fittings",
					"Cable Trays",
					"Casework",
					"Ceilings",
					"Columns",
					"Communication Devices",
					"Conduit Fittings",
					"Conduits",
					"Curtain Panels",
					"Curtain Systems",
					"Curtain Wall Mullions",
					"Data Devices",
					"Doors",
					"Duct Accessories",
					"Duct Fittings",
					"Duct Insulations",
					"Duct Linings",
					"Duct Placeholders",
					"Ducts",
					"Electrical Equipment",
					"Electrical Fixtures",
					"Entourage",
					"Expansion Joints",
					"Fire Alarm Devices",
					"Fire Protection", 
					"Flex Ducts",
					"Flex Pipes",
					"Floors",
					"Food Service Equipment",
					"Furniture",
					"Furniture Systems",
					"Generic Models",
					"Grids",
					"Hardscape", 
					"HVAC Zones",
					"Levels",
					"Lighting Devices",
					"Lighting Fixtures",
					"Lines",
					"Mass",
					"Matchline",
					"Mechanical Control Devices",
					"Mechanical Equipment",
					"Medical Equipment", 
					"MEP Ancillary Framing", 
					"MEP Fabrication Containment",
					"MEP Fabrication Ductwork",
					"MEP Fabrication Ductwork Stiffeners",
					"MEP Fabrication Hangers",
					"MEP Fabrication Pipework",
					"Nurse Call Devices",
					"Parking",
					"Parts",
					"Piers",
					"Pipe Accessories",
					"Pipe Fittings",
					"Pipe Insulations",
					"Pipe Placeholders",
					"Pipes",
					"Planting",
					"Plumbing Equipment",
					"Plumbing Fixtures",
					"Railings",
					"Ramps",
					"Reference Planes",
					"Roads",
					"Roofs",
					"Rooms",
					"Scope Boxes", 
					"Security Devices",
					"Shaft Openings",
					"Signage", 
					"Site",
					"Spaces",
					"Specialty Equipment",
					"Sprinklers",
					"Stairs",
					"Structural Area Reinforcement",
					"Structural Beam Systems",
					"Structural Columns",
					"Structural Connections",
					"Structural Fabric Areas",
					"Structural Fabric Reinforcement",
					"Structural Foundations",
					"Structural Framing",
					"Structural Path Reinforcement",
					"Structural Rebar",
					"Structural Rebar Couplers",
					"Structural Stiffeners",
					"Structural Tendons",
					"Structural Trusses",
					"Telephone Devices",
					"Temporary Structures",
					"Topography",
					"Toposolid",
					"Vertical Circulation",
					"Vibration Management",
					"Walls",
					"Windows"
					])
			# get elements category names and filter mep categories only
			desired_category = [element.Category.Name for element in workset_elements if element.Category and element.Category.Name in set_0]

			# create categories set that can have family names / types
			set_1 = set([
					"Abutments",
					"Air Terminals",
					"Areas",
					"Audio Visual Devices",
					"Bearings",
					"Bridge Cables",
					"Bridge Decks",
					"Bridge Framing",
					"Casework",
					"Ceilings",
					"Columns",
					"Communication Devices", 
					"Curtain Panels",
					"Curtain Systems",
					"Curtain Wall Mullions",
					"Data Devices", 
					"Doors",
					"Duct Accessories",
					"Electrical Equipment",
					"Electrical Fixtures", 
					"Entourage",
					"Expansion Joints",
					"Fire Alarm Devices", 
					"Fire Protection", 
					"Floors",
					"Food Service Equipment",
					"Furniture",
					"Furniture Systems",
					"Generic Models",
					"Grids",
					"Hardscape", 
					"HVAC Zones",
					"Levels",
					"Lighting Devices", 
					"Lighting Fixtures", 
					"Lines",
					"Mass",
					"Matchline",
					"Mechanical Control Devices",
					"Mechanical Equipment",
					"Medical Equipment", 
					"MEP Ancillary Framing", 
					"MEP Fabrication Ductwork Stiffeners",
					"Nurse Call Devices",
					"Parking",
					"Parts",
					"Piers",
					"Planting",
					"Plumbing Equipment",
					"Railings",
					"Ramps",
					"Reference Planes",
					"Roads",
					"Roofs",
					"Rooms",
					"Scope Boxes",
					"Security Devices", 
					"Shaft Openings",
					"Signage", 
					"Site",
					"Spaces",
					"Specialty Equipment",
					"Stairs",
					"Structural Area Reinforcement",
					"Structural Beam Systems",
					"Structural Columns",
					"Structural Connections",
					"Structural Fabric Areas",
					"Structural Fabric Reinforcement",
					"Structural Foundations",
					"Structural Framing",
					"Structural Path Reinforcement",
					"Structural Rebar",
					"Structural Rebar Couplers",
					"Structural Stiffeners",
					"Structural Tendons",
					"Structural Trusses",
					"Telephone Devices",
					"Temporary Structures",
					"Topography",
					"Toposolid",
					"Vertical Circulation",
					"Vibration Management",
					"Walls",
					"Windows"
					])

			# create categories set that can have system types
			set_2 = set([
					"Duct Fittings", 
					"Duct Insulations",
					"Duct Linings",
					"Duct Placeholders",
					"Ducts",
					"Flex Ducts",
					"Flex Pipes",
					"Pipe Accessories", 
					"Pipe Fittings", 
					"Pipe Insulations", 
					"Pipe Placeholders",
					"Plumbing Fixtures", 
					"Sprinklers"
					])

			# create categories set for MEP Fabrication Parts
			set_3 = set([
					"MEP Fabrication Containment",
					"MEP Fabrication Ductwork",
					"MEP Fabrication Hangers",
					"MEP Fabrication Pipework"
					])

			# count desired category unique names and overall counts with Counter
			category_counter = Counter(desired_category)

			if category_counter:
				output.print_md("<pre>  &#9654; <span style='color: black; font-size: 15px; font-family: Arial'>Model Categories (total elements count - {}):</span><pre>".format(len(desired_category)))
				for category_name, category_count in sorted(category_counter.items()):
					output.print_md("<pre>    &#9658; <span style='color: black; font-size: 14.5px; font-family: Arial'>{} Category ({})</span><pre>".format(category_name, category_count))

					# 1) filter through set_1 and collect family names and their counts
					filtered_elements_1  = [elem1 for elem1 in workset_elements if elem1.Category and elem1.Category.Name == category_name and elem1.Category.Name in set_1]
					family_types_counter = Counter()
					for elem1 in filtered_elements_1:
						try:
							if elem1.Category.Name not in ["Areas", "HVAC Zones", "Lines", "Matchline", "Parts", "Reference Planes", "Rooms", "Scope Boxes", "Shaft Openings", "Spaces"]:
								elem1_name_type = elem1.get_Parameter(DB.BuiltInParameter.ELEM_FAMILY_AND_TYPE_PARAM)
								family_types_counter[elem1_name_type.AsValueString()] += 1
							else: 
								elem1_cat_name  = elem1.get_Parameter(DB.BuiltInParameter.ELEM_CATEGORY_PARAM)
								family_types_counter[elem1_cat_name.AsValueString()] += 1
						except Exception as e:
							pass

					# 2) filter through set_2 and collect system types and their counts
					filtered_elements_2  = [elem2 for elem2 in workset_elements if elem2.Category and elem2.Category.Name == category_name and elem2.Category.Name in set_2]
					system_types_counter = Counter()
					for elem2 in filtered_elements_2:
						try:
							mep_sys_type = elem2.LookupParameter("System Type").AsValueString()
							system_types_counter[mep_sys_type] += 1
						except Exception as e:
							pass

					# 3) filter through trays/conduits and collect service types and family names and their counts
					filtered_elements_3  = [elem3 for elem3 in workset_elements if elem3.Category and elem3.Category.Name == category_name and elem3.Category.Name in ["Cable Tray Fittings", "Cable Trays", "Conduit Fittings", "Conduits"]]
					service_type_counter = Counter()
					for elem3 in filtered_elements_3:
						try:
							service_type = elem3.get_Parameter(DB.BuiltInParameter.RBS_CTC_SERVICE_TYPE).AsString()
							tc_name_type = elem3.get_Parameter(DB.BuiltInParameter.ELEM_FAMILY_AND_TYPE_PARAM).AsValueString()
							if service_type and service_type.strip():
								type_key = "Service Type: " + service_type
							else:
								type_key = "Family and Type: " + tc_name_type
							service_type_counter[type_key] += 1
						except Exception as e:
							pass

					# 4) filter through pipes and collect system types and family names and their counts
					filtered_elements_4 = [elem4 for elem4 in workset_elements if elem4.Category and elem4.Category.Name == category_name and elem4.Category.Name == "Pipes"]
					pipe_sys_counter    = Counter()
					pipe_type_counter   = {}
					for elem4 in filtered_elements_4:
						try:
							pipe_sys_type = elem4.LookupParameter("System Type").AsValueString()
							pipe_type     = elem4.get_Parameter(DB.BuiltInParameter.ELEM_FAMILY_AND_TYPE_PARAM).AsValueString()
							pipe_sys_counter[pipe_sys_type] += 1
							if pipe_type not in pipe_type_counter.setdefault(pipe_sys_type, Counter()):
								pipe_type_counter[pipe_sys_type][pipe_type] = 1
							else:
								pipe_type_counter[pipe_sys_type][pipe_type] += 1
						except Exception as e:
							pass

					# 5) filter through set_3 and collect fabrication service types and their counts
					filtered_elements_5 = [elem5 for elem5 in workset_elements if elem5.Category and elem5.Category.Name == category_name and elem5.Category.Name in set_3]
					fabrication_types_counter = Counter()
					for elem5 in filtered_elements_5:
						try:
							fab_ser_type = elem5.get_Parameter(DB.BuiltInParameter.FABRICATION_SERVICE_PARAM).AsValueString()
							fabrication_types_counter[fab_ser_type] += 1
						except Exception as e:
							pass

					# prepare the elements output
					for family_type, family_count in sorted(family_types_counter.items()):
						output.print_md("<pre>      &#9675; <span style='color: black; font-size: 13.5px; font-family: Arial;'> Family and Type: {} ({})</span><pre>".format(family_type, family_count))
					for sys_type, sys_count in sorted(system_types_counter.items()):
						output.print_md("<pre>      &#9675; <span style='color: black; font-size: 13.5px; font-family: Arial;'> System Type: {} ({})</span><pre>".format(sys_type, sys_count))
					for tc_type, tc_count in sorted(service_type_counter.items()):
						output.print_md("<pre>      &#9675; <span style='color: black; font-size: 13.5px; font-family: Arial;'> {} ({})</span><pre>".format(tc_type, tc_count))
					for system_type, system_count in sorted(pipe_sys_counter.items()):
						output.print_md("<pre>      &#9675; <span style='color: black; font-size: 13.5px; font-family: Arial;'> System Type: {} ({})</span><pre>".format(system_type, system_count))
						if system_type in pipe_type_counter:
							for pipe_type, pipe_count in sorted(pipe_type_counter[system_type].items()):
								output.print_md("<pre>        &#9679; <span style='color: black; font-size: 12.5px; font-family: Arial;'> {} ({})</span><pre>".format(pipe_type, pipe_count))
					for fab_type, fab_count in sorted(fabrication_types_counter.items()):
						output.print_md("<pre>      &#9675; <span style='color: black; font-size: 13.5px; font-family: Arial;'> Fabrication Service: {} ({})</span><pre>".format(fab_type, fab_count))
			else:
				output.print_md("<pre>   <span style='color: black; font-size: 14px; font-family: Arial;'> No model categories found on this workset</span><pre>")
			output.print_md("-" * 50)