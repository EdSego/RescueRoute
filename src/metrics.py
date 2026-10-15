
import greedy

# Need to add this to README. Urgent donations are considered
# 60 mins or less
URGENT_THRESHOLD = 60

# Precondition: history contains assignment records.
# donations, recipients, and volunteers contain prepared data.
# Postcondition: returns a dictionary containing donation counts,
# food quantities, urgent rescue rate, and capacity utilization
# percentages for recipients and volunteers.
# Does not modify the input data.
def calculate_metrics(history, donations, recipients,volunteers):
    total_received = len(history)
    total_assigned = 0
    total_unassigned = 0
    assigned_ids = set()
    food_rescue = 0
    food_at_risk = 0

    urgent_total = 0
    urgent_assigned = 0

    total_recipient_capacity = 0
    total_volunteer_capacity = 0

    for record in history:
        if record['status'] == 'assigned':
            total_assigned += 1
            food_rescue += record['quantity']
            assigned_ids.add(record['donation_id'])
        elif record['status'] == 'unassigned':
            total_unassigned += 1
            food_at_risk += record['quantity']

    for donation in donations:
        if greedy.expiration_time_remaining(donation) <= URGENT_THRESHOLD:
            urgent_total += 1
            if donation['donation_id'] in assigned_ids:
                urgent_assigned += 1    
    if urgent_total > 0: 
        urgent_rescue_rate = (urgent_assigned/urgent_total) * 100
    else:
        urgent_rescue_rate = 0   

    for recipient in recipients:
        total_recipient_capacity += recipient['capacity']

    if total_recipient_capacity > 0:
        recipient_utilization = (food_rescue/total_recipient_capacity) * 100
    else:
        recipient_utilization = 0

    for volunteer in volunteers:
        total_volunteer_capacity += volunteer['vehicle_capacity']
    if total_volunteer_capacity > 0:
        volunteer_utilization = (food_rescue/total_volunteer_capacity) * 100
    else: 
        volunteer_utilization = 0
    return{
        'donations_received':total_received,
        'donations_assigned':total_assigned,
        'donations_unassigned':total_unassigned,
        'food_rescued':food_rescue,
        'food_at_risk':food_at_risk,
        'urgent_rescue_rate': urgent_rescue_rate,
        'recipient_utilization':recipient_utilization,
        'volunteer_utilization':volunteer_utilization
    }