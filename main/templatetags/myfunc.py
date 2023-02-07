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
    if CurrentStatus == 'clear':
        return 'Green'
    elif CurrentStatus == 'majorDis':
        return 'Red'
    elif CurrentStatus == 'submitted':
        return 'Gray'
    elif CurrentStatus == 'inprogress':
        return 'Orange'
    elif CurrentStatus == 'minorDis':
        return 'Yellow'
    else:
        return 'Gray'

@register.filter(name='GetDisplayNameDashboard')
def GetDisplayNameDashboard(CurrentStatus):
    if CurrentStatus == 'clear':
        return 'Success'
    elif CurrentStatus == 'majorDis':
        return 'Rejected'
    elif CurrentStatus == 'inaccessible':
        return 'In Accessible'
    elif CurrentStatus == 'minorDis':
        return 'Minor Dispenses'
    elif CurrentStatus == 'inprogress':
        return 'In Progress'
    else:
        return 'Submitted'