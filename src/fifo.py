from collections import deque
import matching
from validations import minutes_to_time


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
    pickup_minutes = max(donation['ready_minutes'], volunteer['available_from_minutes'])
    if pickup_minutes > volunteer['available_until_minutes']:
        return False, "Volunteer is not available when the donation is ready"
    if pickup_minutes >= donation['expiration_minutes']:
        return False, "Donation expires before volunteer is available"
    return True, "Volunteer is compatible"


# Precondition: donations, recipients, volunteers are validated/prepared lists
# Postcondition: donations are processed First In First Out (the order they were
# submitted). Each donation goes to the first compatible recipient and the first
# compatible volunteer. Returns (assignments, unassigned).
def fifo_schedule(donations, recipients, volunteers):
    queue = deque(donations)
    assignments = []
    unassigned = []

    while queue:
        donation = queue.popleft()

        recipient = None
        recipient_reason = "No recipients available"
        for candidate in recipients:
            result, recipient_reason = matching.recipient_is_compatible(donation, candidate)
            if result:
                recipient = candidate
                break

        if recipient is None:
            unassigned.append({
                "donation_id": donation['donation_id'],
                "reason": f"No compatible recipient (last check: {recipient_reason})"
            })
            continue

        # Pickup time also has to be before the recipient closes
        volunteer = None
        volunteer_reason = "No volunteers available"
        for candidate in volunteers:
            result, volunteer_reason = volunteer_is_compatible(donation, candidate)
            if not result:
                continue
            pickup_minutes = max(donation['ready_minutes'], candidate['available_from_minutes'])
            if pickup_minutes >= recipient['closing_minutes']:
                volunteer_reason = "Recipient closes before volunteer can pick up"
                continue
            volunteer = candidate
            break

        if volunteer is None:
            unassigned.append({
                "donation_id": donation['donation_id'],
                "reason": f"No compatible volunteer (last check: {volunteer_reason})"
            })
            continue

        # Reserve capacity only once both a recipient and a volunteer are found
        pickup_minutes = max(donation['ready_minutes'], volunteer['available_from_minutes'])
        recipient['remaining_capacity'] -= donation['quantity']
        volunteer['remaining_vehicle_capacity'] -= donation['quantity']
        volunteer['completed_pickups'] += 1

        assignments.append({
            "donation_id": donation['donation_id'],
            "recipient_id": recipient['recipient_id'],
            "volunteer_id": volunteer['volunteer_id'],
            "quantity": donation['quantity'],
            "pickup_time": minutes_to_time(pickup_minutes)
        })

    return assignments, unassigned
