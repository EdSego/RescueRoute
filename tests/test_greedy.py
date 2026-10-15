import os
import queue
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import validations
from test_helper import make_donation, make_recipient, make_volunteer
from fifo import fifo_schedule
from greedy import greedy_schedule, put_into_deque

def run_fifo(donations, recipients, volunteers):
    validations.prepare_data(donations, recipients, volunteers)
    return(fifo_schedule(donations,recipients,volunteers))

def run_greedy(donations, recipients, volunteers):
    validations.prepare_data(donations,recipients,volunteers)
    return(greedy_schedule(donations,recipients,volunteers))


class TestGreedySchedule(unittest.TestCase):

    def test_greedy_processes_shortest_shelf_life_first(self):
        donations = [
            make_donation("D-Late", ready="12:00", expires="16:00"),
            make_donation("D-Urgent", ready="12:30", expires="13:00")
        ]
        recipients = [
            make_recipient("R-1",capacity=50)
        ]
        volunteers = [
            make_volunteer("V-1", vehicle_capacity=50,available_from="10:00")
        ]
        validations.prepare_data(donations, recipients, volunteers)
        queue = put_into_deque(donations)
        order = []
        for donation in queue:
            order.append(donation["donation_id"])

        self.assertEqual(order, ["D-Urgent","D-Late"])

    def test_greedy_uses_earlier_ready_time_as_tie_breaker(self):
        donations = [
            make_donation("D-2", ready="12:00", expires="13:00"),
            make_donation("D-1", ready="11:00", expires="12:00")
        ]
        recipients = [make_recipient("R-1")]
        volunteers = [make_volunteer("V-1")]
        validations.prepare_data(donations,recipients,volunteers)
        queue = put_into_deque(donations)
        order = []
        for donation in queue:
            order.append(donation["donation_id"])
                
        self.assertEqual(order, ["D-1","D-2"])
        
    def test_fifo_and_greedy_choose_different_donations(self):
        # Fifo chooses D-nonurgent  
        # Greedy chooses D-urgent
        donations = [
            make_donation("D-Nonurgent",quantity=10,ready="12:00",expires="18:00"),
            make_donation("D-Urgent",quantity=10,ready="12:30",expires="14:00")
        ]
        recipients = [make_recipient("R-1",capacity=10)]
        volunteers = [make_volunteer("V-1",vehicle_capacity=20,available_from="12:00")]

        validations.prepare_data(donations,recipients,volunteers)
        
        fifo_assigned_ids = []
        fifo_history = fifo_schedule(donations,recipients,volunteers)
        for record in fifo_history:
            if record["status"] == "assigned":
                fifo_assigned_ids.append(record["donation_id"])

        greedy_assigned_ids = []
        greedy_history = greedy_schedule(donations,recipients,volunteers)
        for record in greedy_history:
            if record["status"] == "assigned":
                greedy_assigned_ids.append(record["donation_id"])

        self.assertEqual(fifo_assigned_ids,["D-Nonurgent"])
        self.assertEqual(greedy_assigned_ids,["D-Urgent"])

    def test_less_urgent_donation_loses_to_urgent_donation(self):
        # Less Urgent Donation loses remaining capcity by Urgent Donation
        # Leaving Less Urgent Donation unassigned
        donations = [
            make_donation("D-LESS-URGENT",quantity=10,ready="12:00",expires="18:00"),
            make_donation("D-URGENT",quantity=10,ready="12:05",expires="12:30")
        ]
        history = run_greedy(
            donations,
            [make_recipient("R-1", capacity=10)],
            [make_volunteer("V-1", vehicle_capacity=20,available_from="12:00")]
        )

        records_by_id = {}

        for record in history:
            records_by_id[record["donation_id"]] = record

        self.assertEqual(records_by_id["D-URGENT"]["status"],"assigned")
        self.assertEqual(records_by_id["D-LESS-URGENT"]["status"],"unassigned")




if __name__ == "__main__":
    unittest.main()