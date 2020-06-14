import unittest
import string
import userExperience


class TestBikeMethods(unittest.TestCase):

    def test_unique_IDs(self):
        a = userExperience.BikeObject()
        b = userExperience.BikeObject()
        self.assertNotEqual(a.id, b.id)


class TestCustomerMethods(unittest.TestCase):

    def test_correct_name(self):
        a = userExperience.CustomerObject("test")
        self.assertEqual(a.name, "test")

    def test_wrong_name(self):
        with self.assertRaises(TypeError):
            a = userExperience.CustomerObject(69)


class TestStoreMethods(unittest.TestCase):

    def test_ID_generation(self):
        s = userExperience.CustomerManagementObject()
        self.assertEqual(s.get_free_ID(), "0001")
        self.assertEqual(s.get_free_ID(), "0002")

    def test_customer_registration_correct(self):
        c = userExperience.CustomerObject()
        s = userExperience.CustomerManagementObject()
        s.register_new_customer(c)
        self.assertEqual(c.customerID, "0001")

    def test_customer_registration_incorrect(self):
        c = userExperience.CustomerObject()
        s = userExperience.CustomerManagementObject()
        c.customerID = "0001"
        with self.assertRaises(ValueError):
            s.register_new_customer(c)

    def test_customer_get_correct_str(self):
        c = userExperience.CustomerObject()
        s = userExperience.CustomerManagementObject()
        s.register_new_customer(c)
        self.assertEqual(s.get_customer_by_ID("0001"), c)
        self.assertEqual(s.get_customer_by_ID("1"), c)

    def test_customer_get_correct_int(self):
        c = userExperience.CustomerObject()
        s = userExperience.CustomerManagementObject()
        s.register_new_customer(c)
        self.assertEqual(s.get_customer_by_ID(1), c)

    def test_customer_get_wrong_type(self):
        s = userExperience.CustomerManagementObject()
        with self.assertRaises(TypeError):
            s.get_customer_by_ID([1])

    def test_customer_get_wrong_ID(self):
        c = userExperience.CustomerObject()
        s = userExperience.CustomerManagementObject()
        s.register_new_customer(c)
        with self.assertRaises(ValueError):
            s.get_customer_by_ID(5)


if __name__ == '__main__':
    unittest.main()