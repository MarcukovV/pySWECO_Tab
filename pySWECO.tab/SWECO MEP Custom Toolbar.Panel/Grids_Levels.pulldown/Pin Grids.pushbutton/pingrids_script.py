# IMPORTS
# import specific Revit libraries which are needed for this script
from Autodesk.Revit.DB import (
	FilteredElementCollector, 
	Grid, 
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
# collect all grids in the model
grids_all = FilteredElementCollector(doc).\
			OfClass(Grid).\
			WhereElementIsNotElementType().\
			ToElements()

# get a list of un-pinned grids
unpinned_grids = [grd for grd in grids_all if not grd.Pinned]

# FUNCTIONS
# 1) create a function that sets Pinned property to True or in other words pins grids
def pin_grid(g):
	g.Pinned = True

# 2) create a function that checks ownership and status of grids
def ownership_status(d, grids_list):
	boolean_list = [
				   [WorksharingUtils.GetCheckoutStatus(d, grid.Id)		!= CheckoutStatus.OwnedByOtherUser, 
					WorksharingUtils.GetModelUpdatesStatus(d, grid.Id)  != ModelUpdatesStatus.DeletedInCentral,
					WorksharingUtils.GetModelUpdatesStatus(d, grid.Id)  != ModelUpdatesStatus.UpdatedInCentral]
					for grid in grids_list
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
msg_1 = "Active Revit document does not contain grids"
msg_2 = "Active Revit document does not contain un-pinned grids"
msg_3 = "Some grids cannot be pinned. They are either owned by other user or they have been deleted / updated in the central model."

# FORMS / USER INTERACTION
# create scenarios where no grids in the model, grids are pinned and check for status
if not grids_all:
	sweco_alert(msg_1)

elif not unpinned_grids:
	sweco_alert(msg_2)

elif doc.IsWorkshared and ownership_status(doc, unpinned_grids) == True:
	sweco_alert(msg_3)

# COMPLETE ACTION
else:
	yes_outcome = forms.alert(
	'All grids will be pinned. Would you like to proceed?\n\nClick "Yes" to proceed \
	or "No" to cancel',
	ok = False,
	yes = True,
	no = True,
	warn_icon = False,
	exitscript = True
	)
	if yes_outcome == True:
		pinned_grids_count = 0
		t = Transaction(doc, "Pin All Grids")
		try:
			t.Start()
			for gr in unpinned_grids:
				pin_grid(gr)
				pinned_grids_count += 1
			t.Commit()
			# final user message
			if t.GetStatus() == TransactionStatus.Committed and len(unpinned_grids) == pinned_grids_count:
				msg = "{} grid(s) have been successfully pinned.\n\n\
				Transaction status is: {}".format(pinned_grids_count, t.GetStatus())
				forms.alert(
							msg,
							title = "Script is successfully completed", 
							ok = False, 
							warn_icon = False
							)
		except Exception as e:
			t.RollBack()
			forms.alert(
						'Transaction status is: {}. Some grids could not be pinned due to: {}'.format(t.GetStatus(), e),
						title = "Error", 
						ok = False
						)