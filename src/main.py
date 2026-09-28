from data_loader import load_file
import validations
import matching

def main():
    print("Welcome to RescueRoute")

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

    #Testing matching change these values to test
    test_donation = donations[0]
    test_recipient = recipients[0]

    result, reason = matching.recipient_is_compatible(test_donation,test_recipient)

    print("\nManual Matching Test\n(Recipient for Donation)")
    print("-"*20)
    print(f"Donation: {test_donation['donation_id']}")
    print(f"Donation Food Type: {test_donation['food_type']}")
    print(f"Donation Quantity: {test_donation['quantity']}")
    print(f"Donation Pick Up Area: {test_donation['pickup_area']}")
    print(f"Donation Ready Time: {test_donation['ready_time']}\n")
    print(f"Recipient: {test_recipient['recipient_id']}")
    print(f"Recipient Accepted Food: {test_recipient['accepted_food_types']}")
    print(f"Recipient Capacity: {test_recipient['capacity']}")
    print(f"Recipient Area: {test_recipient['area']}")
    print(f"Recipient Remaining Capcity: {test_recipient['remaining_capacity']}")
    print("-"*20)
    print(f"\nIs the recipient compatible?: {result}")
    print(f"Reason: {reason}\n")

if __name__ == "__main__":
    main()