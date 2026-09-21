from data_loader import load_file
import validations

def main():
    print("Welcome to RescureRoute")

    donations = load_file("data/donations.json")
    print(donations)
    print("\n-- Test print and validate donations id with pick up area --")
    for donation in donations:
        validations.validate_donations(donation)
        validations.validate_unique_ids(donations, "donation_id","donation")
        print(donation["donation_id"],donation["pickup_area"])

    recipients = load_file("data/reciptients.json")
    print(recipients)
    print("\n-- Test print and validate recipients id and capacity")
    for recipient in recipients:
        validations.validate_recipient(recipient)
        validations.validate_unique_ids(recipients, "recipient_id", "recipient")
        print(f"Recipeint {recipient["recipient_id"]} has capacity of {recipient["capacity"]}")

    volunteers = load_file("data/volunteers.json")
    print("\n-- Test print and validate volenteers and availability")
    print(volunteers)
    for volunteer in volunteers:
        validations.validate_volunteer(volunteer) # validate information
        validations.validate_unique_ids(volunteers, "volunteer_id", "volunteer") # validate for unique ids
        print(f"Volunteer {volunteer["volunteer_id"]} is available from: {volunteer["available_from"]} to: {volunteer["available_until"]}")


if __name__ == "__main__":
    main()