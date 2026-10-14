import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import validations
from test_helper import make_donation, make_recipient, make_volunteer
from fifo import fifo_schedule


def run_fifo(donations, recipients, volunteers):
    validations.prepare_data(donations, recipients, volunteers)
    return fifo_schedule(donations, recipients, volunteers)


class TestFifoSchedule(unittest.TestCase):

    def test_normal_match(self):
        history = run_fifo([make_donation("D-1")], [make_recipient("R-1")],
                           [make_volunteer("V-1")])
        self.assertEqual(len(history), 1)
        record = history[0]
        self.assertEqual(record["status"], "assigned")
        self.assertEqual(record["recipient_id"], "R-1")
        self.assertEqual(record["volunteer_id"], "V-1")
        self.assertEqual(record["scheduled_time"], "14:00")
        self.assertIn("was assigned to", record["reason"])

    def test_insufficient_recipient_capacity(self):
        history = run_fifo([make_donation("D-1", quantity=30)],
                           [make_recipient("R-1", capacity=20)],
                           [make_volunteer("V-1")])
        self.assertEqual(history[0]["status"], "unassigned")
        self.assertIn("Not enough recipient capacity", history[0]["reason"])

    def test_no_volunteer_with_enough_vehicle_capacity(self):
        history = run_fifo([make_donation("D-1", quantity=30)],
                           [make_recipient("R-1")],
                           [make_volunteer("V-1", vehicle_capacity=10)])
        self.assertEqual(history[0]["status"], "unassigned")
        self.assertIn("Not enough vehicle capacity", history[0]["reason"])

    def test_donation_expires_before_volunteer_is_available(self):
        history = run_fifo([make_donation("D-1", ready="14:00", expires="14:30")],
                           [make_recipient("R-1")],
                           [make_volunteer("V-1", available_from="15:00")])
        self.assertEqual(history[0]["status"], "unassigned")
        self.assertIn("Donation expires before volunteer is available", history[0]["reason"])

    def test_competing_donations_first_in_wins(self):
        # Both need the same recipient; only enough capacity for one
        history = run_fifo([make_donation("D-1", quantity=20), make_donation("D-2", quantity=20)],
                           [make_recipient("R-1", capacity=30)],
                           [make_volunteer("V-1")])
        self.assertEqual([r["donation_id"] for r in history], ["D-1", "D-2"])
        self.assertEqual(history[0]["status"], "assigned")
        self.assertEqual(history[1]["status"], "unassigned")

    def test_first_feasible_recipient_is_chosen(self):
        history = run_fifo([make_donation("D-1")],
                           [make_recipient("R-1", food_types=("baked_goods",)),
                            make_recipient("R-2"), make_recipient("R-3")],
                           [make_volunteer("V-1")])
        self.assertEqual(history[0]["recipient_id"], "R-2")

    def test_empty_lists(self):
        self.assertEqual(run_fifo([], [], []), [])
        history = run_fifo([make_donation("D-1")], [], [])
        self.assertEqual(history[0]["status"], "unassigned")

    def test_inputs_are_not_modified(self):
        recipients = [make_recipient("R-1", capacity=50)]
        volunteers = [make_volunteer("V-1")]
        run_fifo([make_donation("D-1", quantity=20)], recipients, volunteers)
        self.assertEqual(recipients[0]["remaining_capacity"], 50)
        self.assertEqual(volunteers[0]["completed_pickups"], 0)


if __name__ == "__main__":
    unittest.main()
