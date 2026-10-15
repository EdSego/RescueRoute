# Greedy Rule:
# Prioritize donations with the least amount of time remaining until expiration.
# Tie-breaker: prioritize the donation with the earlier ready time.

from collections import deque
from scheduler import assign_donations

# Precondition: donation is a prepared donation dictionary
# containing expiration_minutes and ready_minutes
# Postcondition: return the number of minutes until expiration.
def expiration_time_remaining(donation):
    return donation['expiration_minutes'] - donation['ready_minutes']

# Precondition: donations is a list of prepared donation dictionaries
# Post condition: returns a deque ordered by expiration time remaining
# If tied, donations with an earlier ready time are placed first.
def put_into_deque(donations):
    sorted_donations = sorted(
        donations,
        key= lambda donation: (
            expiration_time_remaining(donation),
            donation['ready_minutes']
        )
    )
    queue = deque(sorted_donations)
    return queue

# Precondition: donations, recipients, volunteers are validated/prepared lists.
# Postcondition: donations are processed by greedy urgency priority.
# Donations with the least remaining shelf life are processed first.
# If tied, donations with earlier ready times are processed first.
# Returns the assignment history, one record per donation.
# Input lists are not modified.
def greedy_schedule(donations,recipients, volunteers):
    # Get donations sorted by greedy priority
    queue = put_into_deque(donations)

    # Process donations from most urgert to least urgent
    def greedy_order():
        while queue:
            yield queue.popleft()

    return assign_donations(greedy_order(),recipients,volunteers)