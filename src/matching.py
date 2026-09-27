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
    if ['ready_minutes'] >= reciptient['closing_minutes']:
        return False, "Recipient closes before the donation is ready."
    return True, "Recipient is compatible"
