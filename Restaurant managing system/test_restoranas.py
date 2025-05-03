import unittest
import json
import os
import sys
from restoranas8 import MenuItem, Pizza, Snack, Drink, RestaurantSystem, Employee

# Testinių failų pavadinimai
TEST_ORDERS_FILE = 'test_orders.json'
TEST_STATS_FILE = 'test_stats.json'

class TestMenuItem(unittest.TestCase):
    """Meniu elemento testų klasė"""
    def setUp(self):
        self.item = MenuItem("Testas", 10.0)
    
    def test_get_price(self):
        """Testuoja kainos gavimą"""
        self.assertEqual(self.item.get_price(), 10.0)
    
    def test_get_name(self):
        """Testuoja pavadinimo gavimą"""
        self.assertEqual(self.item.get_name(), "Testas")
    
    def test_get_display_info(self):
        """Testuoja informacijos atvaizdavimą"""
        self.assertEqual(self.item.get_display_info(), "Testas - 10.0€")

class TestPizza(unittest.TestCase):
    """Picos testų klasė"""
    def setUp(self):
        self.pizza = Pizza("Margherita", 8.0)
    
    def test_default_size(self):
        """Testuoja numatytąjį picos dydį"""
        self.assertEqual(self.pizza.size, "medium")
        self.assertEqual(self.pizza.get_price(), 8.0)
    
    def test_set_size_large(self):
        """Testuoja didelės picos kainą"""
        self.pizza.set_size("large")
        self.assertEqual(self.pizza.get_price(), 10.0)
        self.assertEqual(self.pizza.get_display_info(), "Margherita (large) - 10.0€")
    
    def test_set_size_medium(self):
        """Testuoja vidutinės picos kainą"""
        self.pizza.set_size("medium")
        self.assertEqual(self.pizza.get_price(), 8.0)
        self.assertEqual(self.pizza.get_display_info(), "Margherita (medium) - 8.0€")

class TestEmployee(unittest.TestCase):
    """Darbuotojo testų klasė"""
    def setUp(self):
        self.employee = Employee("testas", "testas123")
    
    def test_login_success(self):
        """Testuoja sėkmingą prisijungimą"""
        self.assertTrue(self.employee.login("testas", "testas123"))
        self.assertTrue(self.employee.is_logged_in)
    
    def test_login_failure(self):
        """Testuoja nesėkmingą prisijungimą"""
        self.assertFalse(self.employee.login("testas", "neteisingas"))
        self.assertFalse(self.employee.is_logged_in)
    
    def test_logout(self):
        """Testuoja atsijungimą"""
        self.employee.login("testas", "testas123")
        self.employee.logout()
        self.assertFalse(self.employee.is_logged_in)

class TestRestaurantSystem(unittest.TestCase):
    """Restorano sistemos testų klasė"""
    def setUp(self):
        self.system = RestaurantSystem(
            orders_file=TEST_ORDERS_FILE,
            stats_file=TEST_STATS_FILE
        )
        self.employee = Employee("testas", "testas123")
        self.system.add_employee(self.employee)
        
    def tearDown(self):
        """Išvalo testinius failus"""
        for file in [TEST_ORDERS_FILE, TEST_STATS_FILE]:
            if os.path.exists(file):
                os.remove(file)
    
    def test_add_and_remove_dish(self):
        """Testuoja patiekalo pridėjimą ir pašalinimą"""
        # Pridedame picą
        pizza = Pizza("Margherita", 8.0)
        self.system.add_dish_to_order(pizza)
        self.assertEqual(len(self.system.current_order), 1)
        self.assertEqual(self.system.total, 8.0)
        
        # Pašaliname picą
        self.system.remove_dish_from_order(pizza)
        self.assertEqual(len(self.system.current_order), 0)
        self.assertEqual(self.system.total, 0.0)
    
    def test_finish_order(self):
        """Testuoja užsakymo užbaigimą"""
        # Pridedame kelis patiekalus
        pizza = Pizza("Margherita", 8.0)
        snack = Snack("Bulvytės", 3.0)
        drink = Drink("Pepsi", 2.0)
        
        self.system.add_dish_to_order(pizza)
        self.system.add_dish_to_order(snack)
        self.system.add_dish_to_order(drink)
        
        # Užbaigiame užsakymą
        self.assertTrue(self.system.finish_order("testas"))
        
        # Tikriname ar užsakymas išsaugotas
        self.assertEqual(len(self.system.all_orders), 1)
        self.assertEqual(self.system.all_orders[0]['total'], 13.0)
        self.assertEqual(len(self.system.current_order), 0)
    
    def test_employee_stats(self):
        """Testuoja darbuotojų statistiką"""
        # Sukuriame ir užbaigiame užsakymą
        pizza = Pizza("Margherita", 8.0)
        self.system.add_dish_to_order(pizza)
        self.system.finish_order("testas")
        
        # Tikriname statistiką
        stats = self.system.get_employee_stats()
        employee_stat = next(stat for stat in stats if stat['username'] == "testas")
        
        self.assertEqual(employee_stat['orders'], 1)
        self.assertEqual(employee_stat['turnover'], 8.0)
    
    def test_data_persistence(self):
        """Testuoja duomenų išsaugojimą ir įkėlimą"""
        # Sukuriame užsakymą
        pizza = Pizza("Margherita", 8.0)
        self.system.add_dish_to_order(pizza)
        self.system.finish_order("testas")
        
        # Išsaugome duomenis
        self.system.save_data()
        
        # Sukuriame naują sistemos instanceą
        new_system = RestaurantSystem(
            orders_file=TEST_ORDERS_FILE,
            stats_file=TEST_STATS_FILE
        )
        new_system.add_employee(self.employee)
        new_system.load_data()
        
        # Tikriname ar duomenys išliko
        self.assertEqual(len(new_system.all_orders), 1)
        self.assertEqual(new_system.all_orders[0]['total'], 8.0)

def run_tests():
    """Paleidžia visus testus"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()

if __name__ == '__main__':
    try:
        success = run_tests()
        print("\nTestų vykdymas baigtas.")
        if success:
            print("✅ Visi testai praėjo sėkmingai!")
        else:
            print("❌ Kai kurie testai nepavyko.")
    except Exception as e:
        print(f"\n❌ Įvyko klaida vykdant testus: {str(e)}")
    
    # Laukiame vartotojo įvesties prieš uždarant langą
    print("\nPaspauskite ENTER kad uždarytumėte langą...")
    input() 