# FIFO Rule:
# Process donations in the order they were submitted (first in, first out).
# Donations are not reordered by urgency or expiration time.

from collections import deque
from scheduler import assign_donations

# Precondition: donations, recipients, volunteers are validated/prepared lists.
# Postcondition: donations are processed First In First Out.
# Donations submitted earliest are processed first.
# Each donation goes to the first compatible recipient and the first compatible volunteer.
# Returns the assignment history, one record per donation.
# Input lists are not modified.
def fifo_schedule(donations, recipients, volunteers):
    # Keep donations in their original submission order
    queue = deque(donations)

    # Process donations from first submitted to last submitted
    def arrival_order():
        while queue:
            yield queue.popleft()

    return assign_donations(arrival_order(), recipients, volunteers)
