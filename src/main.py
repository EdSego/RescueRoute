from data_loader import load_file, save_file
import validations
import fifo
import greedy
import metrics

def main():
    print("\n" + "=" * 60)
    print("Welcome to RescueRoute!".center(60))
    print("=" * 60)
    # Load the data 
    donations = load_file("data/donations.json")
    recipients = load_file("data/recipients.json")
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
    # FIFO Scheduling: donations handled in the order they were submitted
    fifo_history = fifo.fifo_schedule(donations, recipients, volunteers)

    print("\nFIFO Schedule")
    print("-"*20)
    for record in fifo_history:
        print(f"[{record['status'].upper()}] {record['reason']}\n")


    greedy_history = greedy.greedy_schedule(donations,recipients,volunteers)
    print("\nGreedy Schedule")
    print("-"*20)
    for greedy_record in greedy_history:
        print(f"[{greedy_record['status'].upper()}] {greedy_record['reason']}\n")

    assignments = {
        'fifo':fifo_history,
        'greedy':greedy_history
    }
    save_file('data/assignments.json',assignments)

    fifo_metrics = metrics.calculate_metrics(fifo_history,donations,recipients,volunteers)
    greedy_metrics = metrics.calculate_metrics(greedy_history,donations,recipients,volunteers)

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

    comparison = metrics.compare_schedules(fifo_metrics, greedy_metrics,fifo_history,greedy_history)
    
    print("\n" + "=" * 60)
    print("FIFO vs Greedy Differences".center(60))
    print("=" * 60)

    for metric, difference in comparison['metric_differences'].items():
        label = metric.replace("_"," ").title()

        if metric in (
            "urgent_rescue_rate",
            "recipient_utilization",
            "volunteer_utilization"
        ):
            value = f"{difference:+.2f} pp"
        else:
            value = f"{difference:+.0f}"

        print(f"{label:<30}{value:15}")
    print("\n" + "=" * 60 + "\n")
    print("\n" + "=" * 60)
    print("Assignment Differences".center(60))
    print("=" * 60)
    print("FIFO Only: ",sorted(comparison["fifo_only"]))
    print("Greedy Only: ", sorted(comparison['greedy_only']))
    print("Assigned by Both: ",sorted(comparison["both"]))
    print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    main()