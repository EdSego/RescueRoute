
#Convert time to minutes and validate 
def time_to_minutes(time):
    if not isinstance(time,str):
        raise ValueError("Time must be a string in HH:MM format")

    split_time = time.split(":")

    if len(split_time) != 2:
        raise ValueError("Time must be in HH:MM format")

    time_hour = split_time[0]
    time_minutes = split_time[1]

    if not time_hour.isdigit() or not time_minutes.isdigit():
        raise ValueError("Time must be in numeric values")

    hour = int(time_hour)
    minute = int(time_minutes)

    if hour < 0 or hour > 23:
        raise ValueError("Hour must be between 0 and 23")

    if minute < 0 or minute > 59:
        raise ValueError("Minutes must be between 0 and 59")
    return hour * 60 + minute

#Convert minutes to HH:MM format
def minutes_to_time(total_minutes):
    hour = total_minutes // 60
    minute = total_minutes % 60
    return f"{hour:02d}:{minute:02d}"


# Validate information for a donation
def validate_donations(donation):
    required_details = [
        "donation_id",
        "donor_name",
        "food_type",
        "quantity",
        "expiration_time",
        "pickup_area",
        "ready_time"
    ]
    # Raise error if required information is missing
    for detail in required_details:
        if detail not in donation:
            raise ValueError(f"Missing {detail} for Donation: {donation["donation_id"]}")

    # Raise error if quantity is invalid
    if donation["quantity"] <= 0:
        raise ValueError(
            f"Donation quantity of {donation["quantity"]} for {donation["donation_id"]} is invalid."
            )

    # Convert time to minutes for ready time and expiration time
    ready_minutes = time_to_minutes(donation['ready_time'])
    expiration_minutes = time_to_minutes(donation['expiration_time'])

    # Check if expiration time is before or on ready time
    if expiration_minutes <= ready_minutes:
        raise ValueError(
            f"Donation {donation['donation_id']} expires before or when it's ready."
        )

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

    # Raise error if accepted food types is not a list
    if not isinstance(recipient['accepted_food_types'], list):
        raise ValueError(
            f"Recipient {recipient['recipient_id']} must use a list for accepted food types")

    # Raise error if there are no accepted food types
    if len(recipient['accepted_food_types']) == 0:
        raise ValueError(
            f"Recipient {recipient['recipient_id']} must have at least one accepted food type"
        )

    # Convert closing time
    time_to_minutes(recipient['closing_time'])

    

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

    # Raise error if vehicle capacity is invalid
    if volunteer['vehicle_capacity'] < 0:
        raise ValueError(
            f"Volunteer {volunteer['volunteer_id']} must have positive vehicle capacity.")

    # Raise error if maximum pickups is invalid
    if volunteer['maximum_pickups'] < 0:
        raise ValueError(
            f"Volunteer {volunteer['volunteer_id']} must have positive maximum pickups.")

    

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


# Validate and prepare all data for assignment and comparisons
def prepare_data(donations, recipients, volunteers):
    #validate ids
    validate_unique_ids(donations, "donation_id", "donation")
    validate_unique_ids(recipients, "recipient_id", "recipient")
    validate_unique_ids(volunteers, "volunteer_id", "volunteer")


    for donation in donations:
        validate_donations(donation)
        donation['food_type'] = donation['food_type'].lower().strip()
        donation['pickup_area'] = donation['pickup_area'].lower().strip()
        donation['ready_minutes'] = time_to_minutes(donation['ready_time'])
        donation['expiration_minutes'] = time_to_minutes(donation['expiration_time'])

    for recipient in recipients:
        validate_recipient(recipient)
        recipient['area'] = recipient['area'].lower().strip()
        recipient['accepted_food_types'] = {
            food_type.lower().strip()
            for food_type in recipient['accepted_food_types']}
        recipient['closing_minutes'] = time_to_minutes(recipient['closing_time'])
        recipient['remaining_capacity'] = recipient['capacity']

    for volunteer in volunteers:
        validate_volunteer(volunteer)
        volunteer['area'] = volunteer['area'].lower().strip()
        volunteer['available_from_minutes'] = time_to_minutes(volunteer['available_from'])
        volunteer['available_until_minutes'] = time_to_minutes(volunteer['available_until'])
        volunteer['remaining_vehicle_capacity'] = volunteer['vehicle_capacity']
        volunteer['completed_pickups'] = 0
