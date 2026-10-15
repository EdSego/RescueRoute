from data_loader import load_file, save_file
import validations
import matching
import fifo
import greedy
import metrics

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

    # FIFO Scheduling: donations handled in the order they were submitted
    fifo_history = fifo.fifo_schedule(donations, recipients, volunteers)

    print("\nFIFO Schedule")
    print("-"*20)
    for record in fifo_history:
        print(f"[{record['status'].upper()}] {record['reason']}\n")

    save_file("data/assignments.json", fifo_history)

    #Greedy Testing
    # test_greedy_donation = donations[0]
    # remaining = greedy.expiration_time_remaining(test_greedy_donation)
    # print(f"Donation ID: {donation['donation_id']}\nRemaining time: {remaining}") 

    # queue = greedy.put_into_deque(donations)

    # for queued_donation in queue:
    #     print(
    #     queued_donation["donation_id"],
    #     greedy.expiration_time_remaining(queued_donation)
    #     )


    greedy_history = greedy.greedy_schedule(donations,recipients,volunteers)
    print("\nGreedy Schedule")
    print("-"*20)
    for greedy_record in greedy_history:
        print(f"[{greedy_record['status'].upper()}] {greedy_record['reason']}\n")

    fifo_metrics = metrics.calculate_metrics(fifo_history,donations,recipients,volunteers)
    greedy_metrics = metrics.calculate_metrics(greedy_history,donations,recipients,volunteers)

    # print("-"*20)
    # print("\nFifo Metrics",fifo_metrics)
    # print("\nGreedy Metrics",greedy_metrics)

    print("\n" + "=" * 60)
    print("RESCUEROUTE - METRICS".center(60))
    print("=" * 60)

    print(f"{'Metric':<30}{'FIFO':>15}{'Greedy':>15}")
    print("-" * 60)

    for key in fifo_metrics:
        fifo_value = fifo_metrics[key]
        greedy_value = greedy_metrics[key]

        if key in (
            'urgent_rescue_rate',
            'recipient_utilization',
            'volunteer_utilization'
        ):
            fifo_value = f"{fifo_value:.2f}%"
            greedy_value = f"{greedy_value:.2f}%"
        label = key.replace("_"," ").title()
        print(f"{label:<30}{fifo_value:>15}{greedy_value:>15}")
    print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    main()