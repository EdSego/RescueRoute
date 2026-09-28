import copy
import matching
from validations import minutes_to_time


# Precondition: ordered_donations is an iterable of prepared donations in the order
# they should be processed; recipients and volunteers are prepared lists
# Postcondition: returns an assignment history (list) with one record per donation.
# The input recipients and volunteers are NOT modified, so FIFO and greedy can be
# run on the same data and compared.
def assign_donations(ordered_donations, recipients, volunteers):
    recipients = copy.deepcopy(recipients)
    volunteers = copy.deepcopy(volunteers)
    history = []

    for donation in ordered_donations:
        # Step 1: first compatible recipient
        recipient = None
        recipient_failures = []
        for candidate in recipients:
            result, reason = matching.recipient_is_compatible(donation, candidate)
            if result:
                recipient = candidate
                break
            recipient_failures.append(f"{candidate['recipient_id']}: {reason}")

        if recipient is None:
            history.append(unassigned_record(
                donation,
                "no compatible recipient was found",
                recipient_failures))
            continue

        # Step 2: first compatible volunteer who can also deliver before the recipient closes
        volunteer = None
        volunteer_failures = []
        for candidate in volunteers:
            result, reason = matching.volunteer_is_compatible(donation, candidate)
            if result and matching.pickup_time(donation, candidate) >= recipient['closing_minutes']:
                result, reason = False, "Recipient closes before volunteer can pick up"
            if result:
                volunteer = candidate
                break
            volunteer_failures.append(f"{candidate['volunteer_id']}: {reason}")

        if volunteer is None:
            history.append(unassigned_record(
                donation,
                f"{recipient['organization_name']} ({recipient['recipient_id']}) could take it, "
                f"but no volunteer could pick it up",
                volunteer_failures))
            continue

        # Step 3: reserve capacity only once both a recipient and a volunteer are found
        history.append(assigned_record(donation, recipient, volunteer))
        recipient['remaining_capacity'] -= donation['quantity']
        volunteer['remaining_vehicle_capacity'] -= donation['quantity']
        volunteer['completed_pickups'] += 1

    return history


# Build the record and human-readable explanation for an assigned donation
# (called before capacity is reserved, so remaining values are the ones that were checked)
def assigned_record(donation, recipient, volunteer):
    pickup_minutes = matching.pickup_time(donation, volunteer)
    minutes_left = donation['expiration_minutes'] - pickup_minutes
    reason = (
        f"Donation {donation['donation_id']} ({donation['quantity']} {donation['food_type']} "
        f"from {donation['donor_name']}) was assigned to {recipient['organization_name']} "
        f"({recipient['recipient_id']}) with volunteer {volunteer['volunteer_id']} at "
        f"{minutes_to_time(pickup_minutes)} because it expires {minutes_left} minutes after pickup, "
        f"the recipient accepts {donation['food_type']} and has {recipient['remaining_capacity']} "
        f"capacity left, and the volunteer can carry {donation['quantity']} "
        f"({volunteer['remaining_vehicle_capacity']} space left)."
    )
    return {
        "donation_id": donation['donation_id'],
        "recipient_id": recipient['recipient_id'],
        "volunteer_id": volunteer['volunteer_id'],
        "quantity": donation['quantity'],
        "scheduled_time": minutes_to_time(pickup_minutes),
        "status": "assigned",
        "reason": reason
    }


# Build the record and human-readable explanation for an unassigned donation,
# listing why every candidate was rejected
def unassigned_record(donation, summary, failures):
    details = "; ".join(failures) if failures else "none available"
    reason = (
        f"Donation {donation['donation_id']} ({donation['quantity']} {donation['food_type']} "
        f"from {donation['donor_name']}) could not be assigned because {summary}. "
        f"Checked: {details}."
    )
    return {
        "donation_id": donation['donation_id'],
        "recipient_id": None,
        "volunteer_id": None,
        "quantity": donation['quantity'],
        "scheduled_time": None,
        "status": "unassigned",
        "reason": reason
    }
