from django import template

register = template.Library()

@register.filter(name='GetDisplayName')
def GetDisplayName(CurrentStatus):
    if CurrentStatus == 'success':
        return 'Green'
    elif CurrentStatus == 'rejected':
        return 'Red'
    elif CurrentStatus == 'submitted':
        return 'Gray'
    elif CurrentStatus == 'inprogress':
        return 'Gray'
    else:
        return 'Gray'

@register.filter(name='GetDisplayStyle')
def GetDisplayStyle(CurrentStatus):
    if CurrentStatus == 'success':
        return 'Green'
    elif CurrentStatus == 'rejected':
        return 'Red'
    elif CurrentStatus == 'submitted':
        return 'Gray'
    elif CurrentStatus == 'inprogress':
        return 'Orange'
    else:
        return 'Gray'

@register.filter(name='GetDisplayNameDashboard')
def GetDisplayNameDashboard(CurrentStatus):
    if CurrentStatus == 'success':
        return 'Success'
    elif CurrentStatus == 'rejected':
        return 'Rejected'
    elif CurrentStatus == 'submitted':
        return 'Submitted'
    elif CurrentStatus == 'inprogress':
        return 'In Progress'
    else:
        return 'Submitted'