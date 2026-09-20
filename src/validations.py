# Validate information for a donation
def validate_donations(donation):
    required_details = [
        "donation_id",
        "donor_name",
        "food_type",
        "quantity",
        "shelf_life_minutes",
        "pickup_area",
        "ready_time"
    ]
    # Raise error if required information is missing
    for detail in required_details:
        if detail not in donation:
            raise ValueError(f"Missing {detail} for Donation: {donation["donation_id"]}")

    # Raise error if quantity is invalid
    if donation["quantity"] <= 0:
        raise ValueError(f"Donation quantity of {donation["quantity"]} for {donation["donation_id"]} is invalid.")

# Validate information for a recipient
def validate_recipient(recipient):
    required_details = [
        "recipient_id",
        "organization_name",
        "accepted_food_types",
        "capacity",
        "area",
        "closing_time"
    ]
    # Raise error if required information is missing
    for detail in required_details:
        if detail not in recipient:
            raise ValueError(f"Missing {detail} for Recipient: {recipient["recipient_id"]}")

def validate_volunteer(volunteer):
    required_details = [
        "volunteer_id",
        "vehicle_capacity",
        "area",
        "available_from",
        "available_until",
        "maximum_pickups"
    ]
    # Raise error if required information is missing
    for detail in required_details:
        if detail not in volunteer:
            raise ValueError(f"Missing {detail} for Volunteer: {volunteer["volunteer_id"]}")

    

# Verify that there are no duplicate ids for any record
def validate_unique_ids(records, id, name):
    seen_id = set()

    for record in records:
        if id not in record:
            raise ValueError(f"{name} is missing {id}")

        record_id = record[id]

        if record_id in seen_id:
            raise ValueError(f"Duplicate {name} ID found {record_id}")
        seen_id.add(record_id)
