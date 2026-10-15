import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import validations
from test_helper import make_donation, make_recipient, make_volunteer


class TestValidations(unittest.TestCase):

    def test_duplicate_donation_ids_raise_error(self):
        donations = [
            make_donation("D-1"),
            make_donation("D-1")
        ]
        with self.assertRaises(ValueError):
            validations.prepare_data(
                [donations],
                [make_recipient("R-1")],
                [make_volunteer("V-1")]
            )

    def test_duplicate_recipient_ids_raise_error(self):
        recipients = [
            make_recipient("R-1"),
            make_recipient("R-1")
        ]
        with self.assertRaises(ValueError):
            validations.prepare_data(
                [make_donation("D-1")],
                [recipients],
                [make_volunteer("V-1")]
            )

    def test_duplicate_volunteer_ids_raise_error(self):
        volunteers = [
            make_volunteer("V-1"),
            make_volunteer("V-1")
        ]
        with self.assertRaises(ValueError):
            validations.prepare_data(
                [make_donation("D-1")],
                [make_recipient("R-1")],
                [volunteers]
            )

    def test_expired_donation_raise_error(self):
        expired_donation = make_donation(
            "D-1", ready="14:00", expires="14:00"
        )
        with self.assertRaises(ValueError):
            validations.prepare_data(
                [expired_donation],
                [make_recipient("R-1")],
                [make_volunteer("V-1")]
            )
    
    def test_donation_with_invalid_quantity_raise_error(self):
        donation = make_donation(
            "D-1", quantity=-10
        )
        with self.assertRaises(ValueError):
            validations.prepare_data(
                [donation],
                [make_recipient("R-1")],
                [make_volunteer("V-1")]
            )
    
    def test_invalid_time_format_raise_error(self):
        donation = make_donation(
            "D-1", ready="4 PM"
        )
        with self.assertRaises(ValueError):
            validations.prepare_data(
                [donation],
                [make_recipient("R-1")],
                [make_volunteer("V-1")]
            )

    def test_prepare_data_normalizes_data(self):
        donation = make_donation(
            "D-1",
            food_type="PRODUCE ",
            area="FULLerton"
        )
        recipient = make_recipient(
            "R-1",
            food_types=("Produce",),
            area="Fullerton"
        )
        volunteer = make_volunteer(
            "V-1",
            area="FUllerton"
        )
        validations.prepare_data([donation],[recipient],[volunteer])
        self.assertEqual(donation["food_type"], "produce")
        self.assertEqual(donation["pickup_area"],"fullerton")
        self.assertIn("produce", recipient["accepted_food_types"])
        self.assertEqual(volunteer["area"],"fullerton")
        


if __name__ == "__main__":
    unittest.main()