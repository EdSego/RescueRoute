from data_loader import load_file

def main():
    print("Welcome to RescureRoute")

    donations = load_file("data/donations.json")
    print(donations)
    print("\n-- Test print donation id with pick up area --")
    for donation in donations:
        print(donation["donation_id"],donation["pickup_area"])

if __name__ == "__main__":
    main()