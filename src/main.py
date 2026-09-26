from data_loader import load_file
import validations

def main():
    print("Welcome to RescureRoute")

    donations = load_file("data/donations.json")
    recipients = load_file("data/reciptients.json")
    volunteers = load_file("data/volunteers.json")

    validations.prepare_data(donations, recipients, volunteers)
    print("\nDonation List")
    for donation in donations:
        print(f"ID: {donation["donation_id"]} | Food Type: {donation['food_type']}| Location: {donation["pickup_area"]}")

    print("\nRecipient List")
    for recipient in recipients:
        print(f"ID: {recipient["recipient_id"]} | Food Types: {recipient['accepted_food_types']} | Capacity: {recipient["capacity"]}")

    print("\nVolunteers List")
    for volunteer in volunteers:
        print(f"ID: {volunteer["volunteer_id"]} | Availability: {volunteer["available_from"]}-{volunteer["available_until"]}")


if __name__ == "__main__":
    main()