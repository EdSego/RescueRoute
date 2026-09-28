from collections import deque
from scheduler import assign_donations


# Precondition: donations, recipients, volunteers are validated/prepared lists
# Postcondition: donations are processed First In First Out (the order they were
# submitted). Each donation goes to the first compatible recipient and the first
# compatible volunteer. Returns the assignment history, one record per donation.
# Input lists are not modified.
def fifo_schedule(donations, recipients, volunteers):
    queue = deque(donations)

    def arrival_order():
        while queue:
            yield queue.popleft()

    return assign_donations(arrival_order(), recipients, volunteers)
