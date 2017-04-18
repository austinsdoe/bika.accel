import logging


def PatientAddedEventHandler(instance, event):
    """ Event fired when Patient object gets modified.
        We have to redirect the user to the Patient's Analysis Requests view.
    """
    if instance.aq_parent.portal_type == "TempFolder":
        # It hasn't been created yet. Archetypes creates and adds the object
        # into the TempFolder before adding it to the defined parent
        return
