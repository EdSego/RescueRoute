
def make_donation(donation_id, quantity=10, food_type="produce", area="Fullerton",
                  ready="14:00", expires="16:00"):
    return {
        "donation_id": donation_id,
        "donor_name": "Test Donor",
        "food_type": food_type,
        "quantity": quantity,
        "expiration_time": expires,
        "pickup_area": area,
        "ready_time": ready
    }


def make_recipient(recipient_id, capacity=50, food_types=("produce",), area="Fullerton",
                   closing="20:00"):
    return {
        "recipient_id": recipient_id,
        "organization_name": "Test Shelter",
        "accepted_food_types": list(food_types),
        "capacity": capacity,
        "area": area,
        "closing_time": closing
    }


def make_volunteer(volunteer_id, vehicle_capacity=50, area="Fullerton",
                   available_from="13:00", available_until="18:00", maximum_pickups=3):
    return {
        "volunteer_id": volunteer_id,
        "vehicle_capacity": vehicle_capacity,
        "area": area,
        "available_from": available_from,
        "available_until": available_until,
        "maximum_pickups": maximum_pickups
    }

