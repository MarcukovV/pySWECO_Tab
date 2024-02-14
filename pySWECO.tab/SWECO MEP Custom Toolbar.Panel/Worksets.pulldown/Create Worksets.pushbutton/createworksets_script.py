# IMPORTS
# import pyrevit libraries
from pyrevit import revit, DB, forms, script

# get active Revit document
doc = revit.doc

# DATA COLLECTION
# get all user worksets as elements in an active Revit document
existing_user_worksets = DB.FilteredWorksetCollector(doc).\
						 OfKind(DB.WorksetKind.UserWorkset).\
						 ToWorksets()

# get user worksets names
existing_user_worksets_names = [wn.Name for wn in existing_user_worksets]

# SWECO default list of worksets 
default_sweco_worksets = sorted([
						'SWE-A_Architectural Components',
						'SWE-E_BMS',
						'SWE-E_Containment',
						'SWE-E_Fire Alarm',
						'SWE-E_Lighting',
						'SWE-E_Plant',
						'SWE-E_Small Power',
						'SWE-M_Ducts',
						'SWE-M_Pipes',
						'SWE-M_Plant',
						'SWE-N_Fire',
						'SWE-P_Domestic',
						'SWE-P_Sanitation',
						'SWE-P_Plant',
						'SWE-SE_ICT',
						'SWE-SE_Security',
						'SWE-X_3D_Link_Architecture',
						'SWE-X_3D_Link_Infrastructure',
						'SWE-X_3D_Link_Structure',
						'SWE-X_2D_Link_CAD',
						'SWE-X_Scope Boxes & Reference Planes',
						'SWE-Z_BWH',
						'SWE-Z_Preliminary MEP Zones',
						'SWE-Z_Utilities Services'
						])
# SWECO optional list of worksets 
optional_sweco_worksets = sorted([
						 'SWE-E_Apartment_Lighting & Fire Alarm',
						 'SWE-E_Apartment_Small Power',
						 'SWE-M_Apartment_Ducts',
						 'SWE-M_Apartment_Pipes',
						 'SWE-P_Apartment_Domestic',
						 'SWE-P_Apartment_Sanitation',
						 'SWE-Z_Bathroom Pods',
						 'SWE-Z_Utility Cupboard',
						 'SWE-SE_AV',
						 'SWE-X_Cobie Separation Lines'
						 ])

# worksets to create
default_worksets_to_create  = [dw for dw in default_sweco_worksets if dw not in existing_user_worksets_names]
optional_worksets_to_create = [ow for ow in optional_sweco_worksets if ow not in existing_user_worksets_names]

# FUNCTIONS
# create a function to create worksets
def worksets_creation(d, workset_name):
	DB.Workset.Create(d, workset_name)

# create sweco alert function
def sweco_alert(message):
	forms.alert(
	message,
	title = "Script is cancelled",
	ok = False
	)
	script.exit()

msg_1 = "Active Revit document is not workshared. To create workset(s), worksharing must be enabled."
msg_2 = "No options have been selected."
msg_3 = "No worksets have been selected."
msg_4 = "Worksets you are trying to create already exist in an active Revit document."

# USER INTERACTION
# check if active Revit document is workshared
if not doc.IsWorkshared:
	sweco_alert(msg_1)

# throw user interaction form showing default and optional worksets options
items = ["Default Sweco Worksets", "Optional Sweco Worksets"]
options_to_select = forms.ask_for_one_item(
				 items,
				 prompt = "Select one option from the dropdown menu",
				 title = "Worksets Creation"
				 )
if not options_to_select:
	sweco_alert(msg_2)

if options_to_select == "Default Sweco Worksets":
	if not default_worksets_to_create:
		sweco_alert(msg_4)
	# throw user interaction form with a list of default sweco worksets
	default_selection = forms.SelectFromList.show(
					 default_worksets_to_create,
					 title = "Worksets Creation",
					 width = 450,
					 height = 700,
					 button_name = "Create",
					 multiselect = True
					 )
	# scenario if user does not select anything
	if not default_selection:
		sweco_alert(msg_3)

	# double check if user wishes to proceed and if yes, call a function to create new default worksets
	yes_outcome_d = forms.alert(
	'{} workset(s) will be created. Would you like to proceed? \n\n\
	Click "Yes" to proceed or "No" to cancel.'.format(len(default_selection)),
	ok = False,
	yes = True,
	no = True,
	warn_icon = False,
	exitscript = True
	)
	if yes_outcome_d == True:
		default_worksets_counter = 0
		with revit.Transaction("Default Sweco Worksets"):
			for default_wk in default_selection:
				worksets_creation(doc, default_wk)
				default_worksets_counter += 1
		if len(default_selection) == default_worksets_counter:
			m = "{} worksets(s) have been successfully created.".format(default_worksets_counter)
			forms.alert(
						m,
						title = "Script is successfully completed", 
						ok = False, 
						warn_icon = False
						)

if options_to_select == "Optional Sweco Worksets":
	if not optional_worksets_to_create:
		sweco_alert(msg_4)
	# throw user interaction form with a list of optional sweco worksets
	optional_selection = forms.SelectFromList.show(
					 optional_worksets_to_create,
					 title = "Worksets Creation",
					 width = 450,
					 height = 450,
					 button_name = "Create",
					 multiselect = True
					 )
	# scenario if user does not select anything
	if not optional_selection:
		sweco_alert(msg_3)

	# double check if user wishes to proceed and if yes, call a function to create new optional worksets
	yes_outcome_o = forms.alert(
	'{} workset(s) will be created. Would you like to proceed? \n\n\
	Click "Yes" to proceed or "No" to cancel.'.format(len(optional_selection)),
	ok = False,
	yes = True,
	no = True,
	warn_icon = False,
	exitscript = True
	)
	if yes_outcome_o == True:
		optional_worksets_counter = 0
		with revit.Transaction("Optional Sweco Worksets"):
			for optional_wk in optional_selection:
				worksets_creation(doc, optional_wk)
				optional_worksets_counter += 1
		if len(optional_selection) == optional_worksets_counter:
			m = "{} worksets(s) have been successfully created.".format(optional_worksets_counter)
			forms.alert(
						m,
						title = "Script is successfully completed", 
						ok = False, 
						warn_icon = False
						)