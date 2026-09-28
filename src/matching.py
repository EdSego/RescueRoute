# Precondition: donation and recipient are validated/prepared dictionaries
# Postcondition: returns True if recipient is compatible, otherwise False,
# along with a reason
def recipient_is_compatible(donation, reciptient):
    #Check 1: Food type
    if donation['food_type'] not in reciptient['accepted_food_types']:
        return False, "Food Type not accepted"
    #Check 2 Capacity: 
    if donation['quantity'] > reciptient['remaining_capacity']:
        return False, "Not enough recipient capacity"
    #Check 3 Area:
    if donation['pickup_area'] != reciptient['area']:
        return False, "Recipient is not in the area"
    #Check 4 Closing Time:
    if donation['ready_minutes'] >= reciptient['closing_minutes']:
        return False, "Recipient closes before the donation is ready."
    return True, "Recipient is compatible"

# Precondition: donation and volunteer are validated/prepared dictionaries
# Postcondition: returns True if volunteer can pick up the donation, otherwise False,
# along with a reason
def volunteer_is_compatible(donation, volunteer):
    #Check 1: Area
    if donation['pickup_area'] != volunteer['area']:
        return False, "Volunteer is not in the area"
    #Check 2: Pickup limit
    if volunteer['completed_pickups'] >= volunteer['maximum_pickups']:
        return False, "Volunteer reached maximum pickups"
    #Check 3: Vehicle capacity
    if donation['quantity'] > volunteer['remaining_vehicle_capacity']:
        return False, "Not enough vehicle capacity"
    #Check 4: Availability window overlaps with donation window
    pickup_minutes = pickup_time(donation, volunteer)
    if pickup_minutes > volunteer['available_until_minutes']:
        return False, "Volunteer is not available when the donation is ready"
    if pickup_minutes >= donation['expiration_minutes']:
        return False, "Donation expires before volunteer is available"
    return True, "Volunteer is compatible"

# Earliest time the volunteer can pick up the donation (in minutes)
def pickup_time(donation, volunteer):
    return max(donation['ready_minutes'], volunteer['available_from_minutes'])
