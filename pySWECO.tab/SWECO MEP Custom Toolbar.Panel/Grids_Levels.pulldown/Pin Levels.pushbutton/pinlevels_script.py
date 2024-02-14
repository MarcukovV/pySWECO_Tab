# IMPORTS
# import specific Revit libraries which are needed for this script
from Autodesk.Revit.DB import (
	FilteredElementCollector,
	Level,
	WorksharingUtils,
	CheckoutStatus,
	ModelUpdatesStatus,
	Transaction, 
	TransactionStatus
	)

# import pyrevit libraries
from pyrevit import forms, script

# get current Revit document
doc = __revit__.ActiveUIDocument.Document

# DATA COLLECTION
# collect all levels in the model
levels_all = FilteredElementCollector(doc).\
			OfClass(Level).\
			WhereElementIsNotElementType().\
			ToElements()

# get a list of un-pinned levels
unpinned_levels = [lvl for lvl in levels_all if not lvl.Pinned]

# FUNCTIONS
# 1) create a function that sets Pinned property to True or in other words pins levels
def pin_level(l):
	l.Pinned = True

# 2) create a function that checks ownership and status of levels
def ownership_status(d, levels_list):
	boolean_list = [
				   [WorksharingUtils.GetCheckoutStatus(d, level.Id)		!= CheckoutStatus.OwnedByOtherUser,
					WorksharingUtils.GetModelUpdatesStatus(d, level.Id) != ModelUpdatesStatus.DeletedInCentral,
					WorksharingUtils.GetModelUpdatesStatus(d, level.Id) != ModelUpdatesStatus.UpdatedInCentral]
					for level in levels_list
					]
	bool_val = any(False in row for row in boolean_list)
	return bool_val

# 3) create a function to return pyrevit forms
def sweco_alert(message):
	forms.alert(
	message,
	title = "Script is cancelled",
	ok = False
	)
	script.exit()

# messages for 3) function
msg_1 = "Active Revit document does not contain un-pinned levels"
msg_2 = "Some levels cannot be pinned. They are either owned by other user or they have been deleted / updated in the central model."

# FORMS / USER INTERACTION
# create scenarios where levels are pinned and check for status
if not unpinned_levels:
	sweco_alert(msg_1)

elif doc.IsWorkshared and ownership_status(doc, unpinned_levels) == True:
	sweco_alert(msg_2)

# COMPLETE ACTION
else:
	yes_outcome = forms.alert(
	'All levels will be pinned. Would you like to proceed?\n\nClick "Yes" to proceed \
	or "No" to cancel',
	ok = False,
	yes = True,
	no = True,
	warn_icon = False,
	exitscript = True
	)
	if yes_outcome == True:
		pinned_levels_counter = 0
		t = Transaction(doc, "Pin All Levels")
		try:
			t.Start()
			for lv in unpinned_levels:
				pin_level(lv)
				pinned_levels_counter += 1
			t.Commit()
			# final user message
			if t.GetStatus() == TransactionStatus.Committed and len(unpinned_levels) == pinned_levels_counter:
				msg = "{} level(s) have been successfully pinned.\n\n\
				Transaction status: {}".format(pinned_levels_counter, t.GetStatus())
				forms.alert(
							msg,
							title = "Script is successfully completed", 
							ok = False, 
							warn_icon = False
							)
		except Exception as e:
			t.RollBack()
			forms.alert(
						'Transaction status is: {}. Some levels could not be pinned due to: {}'.format(t.GetStatus(), e),
						title = "Error", 
						ok = False
						)