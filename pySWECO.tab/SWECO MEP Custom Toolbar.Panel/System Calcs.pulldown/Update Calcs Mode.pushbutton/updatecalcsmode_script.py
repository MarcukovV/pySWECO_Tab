# IMPORTS
# import Revit & pyrevit libraries
from Autodesk.Revit.DB import (
	 FilteredElementCollector, 
	 BuiltInParameter, 
	 WorksharingUtils,
	 CheckoutStatus,
	 ModelUpdatesStatus,
	 Transaction,
	 TransactionStatus
	 )

from Autodesk.Revit.DB.Mechanical import MechanicalSystemType
from Autodesk.Revit.DB.Plumbing import PipingSystemType

from pyrevit import forms, script

# get current Revit document
doc = __revit__.ActiveUIDocument.Document

# DATA COLLECTION
# collect all duct system types in current model
duct_system_type = FilteredElementCollector(doc).\
				OfClass(MechanicalSystemType).\
				WhereElementIsElementType().\
				ToElements()

# collect all pipe system types in current model
pipe_system_type = FilteredElementCollector(doc).\
				OfClass(PipingSystemType).\
				WhereElementIsElementType().\
				ToElements()

# combined the above lists into one
combined_system_type = list(duct_system_type) + list(pipe_system_type)

# FUNCTIONS
# 1) create a function that takes a list and splits it into 2 lists: duct/pipe with not None mode and duct/pipe with not Performance mode
def check_system_types(combined_list):
	# 1.1) create 2 lists to separate duct and pipe system types which calculation parameter modes are either not none or not performance
	not_none_list, not_perf_list = [], []
	for e in combined_list:
		system_name = e.get_Parameter(BuiltInParameter.SYMBOL_FAMILY_NAME_PARAM)
		if system_name and system_name.AsString() == "Duct System":
			duct_param_mode = e.get_Parameter(BuiltInParameter.RBS_DUCT_SYSTEM_CALCULATION_PARAM).AsInteger()
			if duct_param_mode != 0:
				not_none_list.append(e)
			if duct_param_mode != 4:
				not_perf_list.append(e)
		elif system_name and system_name.AsString() == "Piping System":
			pipe_param_mode = e.get_Parameter(BuiltInParameter.RBS_PIPE_SYSTEM_CALCULATION_PARAM).AsInteger()
			if pipe_param_mode != 0:
				not_none_list.append(e)
			if pipe_param_mode != 4:
				not_perf_list.append(e)

	# 1.2) count number of system types in not none list and not performance list
	not_none_list_count = len(not_none_list)
	not_perf_list_count = len(not_perf_list)
	# prepare the result
	result = [
			  not_none_list_count,	# @ index 0
			  not_perf_list_count,	# @ index 1
			  not_none_list,		# @ index 2
			  not_perf_list			# @ index 3
			  ]
	return result

# 2) create a function that updates mode to either None or Performance
def update_system_types(list_to_update, set_to_none = False, set_to_performance = False):
	# if user decides to set everything to None
	if set_to_none == True:
		for m in list_to_update:
			family_name = m.get_Parameter(BuiltInParameter.SYMBOL_FAMILY_NAME_PARAM)
			if family_name and family_name.AsString() == "Duct System":
				m.get_Parameter(BuiltInParameter.RBS_DUCT_SYSTEM_CALCULATION_PARAM).Set(0)
			elif family_name and family_name.AsString() == "Piping System":
				m.get_Parameter(BuiltInParameter.RBS_PIPE_SYSTEM_CALCULATION_PARAM).Set(0)
	# if user decides to set everything to Performance
	if set_to_performance == True:
		for m in list_to_update:
			family_name = m.get_Parameter(BuiltInParameter.SYMBOL_FAMILY_NAME_PARAM)
			if family_name and family_name.AsString() == "Duct System":
				m.get_Parameter(BuiltInParameter.RBS_DUCT_SYSTEM_CALCULATION_PARAM).Set(4)
			elif family_name and family_name.AsString() == "Piping System":
				m.get_Parameter(BuiltInParameter.RBS_PIPE_SYSTEM_CALCULATION_PARAM).Set(4)

# 3) create a function that checks status and ownership of elements
def ownership_status(d, system_list):
	ownership_status_list = [
					[WorksharingUtils.GetCheckoutStatus(d, system.Id)	   != CheckoutStatus.OwnedByOtherUser,
					 WorksharingUtils.GetModelUpdatesStatus(d, system.Id)  != ModelUpdatesStatus.DeletedInCentral,
					 WorksharingUtils.GetModelUpdatesStatus(d, system.Id)  != ModelUpdatesStatus.UpdatedInCentral]
					 for system in system_list
					 ]
	bool_val = any(False in row for row in ownership_status_list)
	return bool_val

# 4) create a function to display alert form
def sweco_alert(message):
	forms.alert(
	message, 
	title = "Script is cancelled",
	ok = False
	)
	script.exit()

# messages for 4) function
msg_1 = "No calculation parameter mode selected."
msg_2 = "Some calculation parameter modes cannot be updated. They are either owned by other user or they have been deleted / updated in the central model."
msg_3 = 'All duct and piping systems calculation parameters are already set to "None" mode.'
msg_4 = 'All duct and piping systems calculation parameters are already set to "Performance" mode.'

# create a simple class with name and description to feed pyrevit forms's info panel
class Mode:
	def __init__(self, name, description):
		self.name = name
		self.description = description
# name and description of None mode
none = Mode("None Mode", "***Prior updating, read the description below which is taken from the official Autodesk website.*** \n\n\
System calculation is off. \n\n\
1. Duct System Type: \n\
None -> the Flow parameter is not computed. Revit still maintains \
the logical sections in the duct system.\n\n\
2. Pipe System Type: \n\
None -> the Volume parameter is not computed. Revit still maintains \
the logical sections in the pipe system.")
# name and description of Performance mode
perf = Mode("Performance Mode", "***Prior updating, read the description below which is taken from the official Autodesk website.*** \n\n\
1. Duct System Type:\n\
Performance -> the Flow parameter and system-level calculations are not computed. \n\
Use the Performance mode to improve Revit's performance when editing large MEP duct \
system networks. System propagation is disabled on every system in the project that uses the selected system type.\n\
***Note: The Duct Sizing tools are not available for systems where the Calculations parameter is set to Performance. \n\n\
2. Pipe System Type:\n\
Performance -> the Volume parameter and system-level calculations are not computed. \n\
Use the Performance mode to improve Revit's performance when editing large MEP pipe system networks. \
System propagation is disabled on every system in the project that uses the selected system type. \n\
***Note: The Pipe Sizing tools are not available for systems where the Calculations parameter is set to Performance.")

# USER INTERACTION
# create a dialog window with 2 choices: None and Performance
context 	= [none, perf]
select_mode = forms.SelectFromList.show(
			context,
			title  = "Update Calculation Parameter Mode",
			width  = 500,
			height = 350,
			button_name = "Update",
			info_panel  = True
			)

# scenario if Revit user chooses zero options
if not select_mode:
	sweco_alert(msg_1)

# 1 scenario where Revit user decides to set everything to None mode
if select_mode.name == "None Mode":
	result = check_system_types(combined_system_type)
	# scenario where all system types have already mode None
	if result[0] == 0:
		sweco_alert(msg_3)
	# scenario where elements are owned by other user or have been deleted / updated in the central model
	elif doc.IsWorkshared and ownership_status(doc, result[2]):
		sweco_alert(msg_2)
	# throw another user form to double check and if yes, then proceed to action
	else:
		none_outcome = forms.alert(
		msg = 'All duct and piping systems calculation parameters will be set to \
		"None" mode. Would you like to proceed?\n\nClick "Yes" to proceed or "No" to cancel',
		sub_msg = 'Please note: BIM Managers only can perform this action',
		ok = False,
		yes = True,
		no = True,
		warn_icon = False,
		exitscript = True
		)
		if none_outcome == True:
			none_check_at_start = result[0]
			t = Transaction(doc, 'None Mode')
			try:
				t.Start()
				update_system_types(result[2], set_to_none = True)
				t.Commit()
				none_check_at_commit = check_system_types(combined_system_type)[0]
				# final user message (None)
				if t.GetStatus() == TransactionStatus.Committed and none_check_at_commit == 0:
					msg_none = "Calculation parameter of {} system types has been successfully set to None mode.\n\n\
					Transaction status: {}".format(none_check_at_start, t.GetStatus())
					forms.alert(
								msg_none, 
								title = "Script is successfully completed", 
								ok = False, 
								warn_icon = False
								)
			except Exception as e:
				t.RollBack()
				forms.alert(
							'Transaction status is: {}. Some modes could not be updated due to: {}'.format(t.GetStatus(), e),
							title = "Error", 
							ok = False
							)

# 2 scenario where Revit user decides to set everything to Performance mode
if select_mode.name == "Performance Mode":
	result = check_system_types(combined_system_type)
	# scenario where all system types have already mode Performance
	if result[1] == 0:
		sweco_alert(msg_4)
	# scenario where elements are owned by other user or have been deleted / updated in the central model
	elif doc.IsWorkshared and ownership_status(doc, result[3]):
		sweco_alert(msg_2)
	# throw another user form to double check and if yes, then proceed to action
	else:
		performance_outcome = forms.alert(
		msg = 'All duct and piping systems calculation parameters will be set to\
		"Performance" mode. Would you like to proceed?\n\nClick "Yes" to proceed or "No" to cancel',
		sub_msg = 'Please note: BIM Managers only can perform this action',
		ok = False,
		yes = True,
		no = True,
		warn_icon = False,
		exitscript = True
		)
		if performance_outcome == True:
			perf_check_at_start = result[1]
			t = Transaction(doc, 'Performance Mode')
			try:
				t.Start()
				update_system_types(result[3], set_to_performance = True)
				t.Commit()
				perf_check_at_commit = check_system_types(combined_system_type)[1]
				# final user message (Performance)
				if t.GetStatus() == TransactionStatus.Committed and perf_check_at_commit == 0:
					msg_perf = "Calculation parameter of {} system types has been successfully set to Performance mode.\n\n\
					Transaction status: {}".format(perf_check_at_start, t.GetStatus())
					forms.alert(
								msg_perf, 
								title = "Script is successfully completed", 
								ok = False, 
								warn_icon = False
								)
			except Exception as e:
				t.RollBack()
				forms.alert(
							'Transaction status is: {}. Some modes could not be updated due to: {}'.format(t.GetStatus(), e),
							title = "Error", 
							ok = False
							)