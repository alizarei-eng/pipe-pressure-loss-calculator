import math
import unittest

from core.headloss import calculate_head_loss
from core.friction import darcy_friction_factor
from core.pipe_database import load_pipe_database, available_grades, available_sdrs


class TestFrictionFactor(unittest.TestCase):
    def test_laminar_flow(self):
        factor, warning = darcy_friction_factor(1000, 0.0001)
        self.assertAlmostEqual(factor, 0.064, places=12)
        self.assertIsNone(warning)

    def test_transition_warning(self):
        _, warning = darcy_friction_factor(3000, 0.0001)
        self.assertIsNotNone(warning)


class TestHeadLoss(unittest.TestCase):
    def test_zero_length_and_no_fittings(self):
        result = calculate_head_loss(20, 0, 0.1, 0.0015, 0)
        self.assertAlmostEqual(result["total_head_loss_m"], 0.0)

    def test_total_is_sum_of_major_and_minor(self):
        result = calculate_head_loss(50, 100, 0.1, 0.0015, 2.0)
        self.assertAlmostEqual(
            result["total_head_loss_m"],
            result["major_head_loss_m"] + result["minor_head_loss_m"],
        )
        self.assertGreater(result["velocity_m_s"], 0)
        self.assertGreater(result["reynolds"], 0)

    def test_invalid_diameter(self):
        with self.assertRaises(ValueError):
            calculate_head_loss(10, 100, 0, 0.0015)


class TestPipeDatabase(unittest.TestCase):
    def test_grade_and_sdr_menus_are_read_from_database(self):
        database = load_pipe_database()
        self.assertEqual(available_grades(database), ["PE100", "PE80"])
        self.assertIn(11, available_sdrs(database, "PE100"))
        self.assertNotIn(6, available_sdrs(database, "PE100"))


if __name__ == "__main__":
    unittest.main()
