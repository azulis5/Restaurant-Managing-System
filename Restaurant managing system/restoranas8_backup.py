# =============================================================================
# Standartinės bibliotekos importai
# =============================================================================
from datetime import datetime
import json
import os
import tkinter as tk
from tkinter import messagebox

# =============================================================================
# Konstantos
# =============================================================================
FONT_HEADER = ("Arial", 14, "bold")
FONT_NORMAL = ("Arial", 12)
FONT_SMALL = ("Arial", 11)

# =============================================================================
# Klasės
# =============================================================================

class MenuItem:
    """Bazinė klasė visiems meniu elementams."""
    
    def __init__(self, name: str, price: float) -> None:
        self.name = name
        self.price = price
    
    def get_price(self) -> float:
        """Grąžina elemento kainą."""
        return self.price
    
    def get_name(self) -> str:
        """Grąžina elemento pavadinimą."""
        return self.name
    
    def get_display_info(self) -> str:
        """Grąžina elemento informaciją atvaizdavimui."""
        return f"{self.name} - {self.price}€"

class Pizza(MenuItem):
    """Picos klasė."""
    
    def __init__(self, name: str, base_price: float) -> None:
        super().__init__(name, base_price)
        self.base_price = base_price
        self.size = "medium"  # Numatytasis dydis
        
    def set_size(self, size: str) -> None:
        """Nustatyti picos dydį ir atnaujinti kainą."""
        self.size = size
        if size == "large":
            self.price = self.base_price + 2
        else:
            self.price = self.base_price
    
    def get_display_info(self) -> str:
        """Grąžina picos informaciją atvaizdavimui."""
        return f"{self.name} ({self.size}) - {self.price}€"

class Snack(MenuItem):
    """Užkandžių klasė."""
    pass

class Drink(MenuItem):
    """Gėrimų klasė."""
    pass

class Employee:
    """Darbuotojo klasė."""
    
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password
        self.is_logged_in = False

    def login(self, username: str, password: str) -> bool:
        """Darbuotojo prisijungimo patikrinimas."""
        if self.username == username and self.password == password:
            self.is_logged_in = True
            return True
        return False

    def logout(self) -> None:
        """Darbuotojo atsijungimas."""
        self.is_logged_in = False

# =============================================================================
# MENIU DUOMENYS
# =============================================================================
# Konvertuojame esamus meniu elementus į naujus objektus
pizzas = [Pizza(name, price) for name, price in [
    ("Margherita", 8.0), ("Capricciosa", 8.0), ("Atlantis", 9.0),
    ("Italian", 8.0), ("Serrano", 8.0), ("Pepperoni", 8.0),
    ("Cheese", 8.0), ("Mushrooms", 8.0), ("Student's", 7.0),
    ("Farmer's", 10.0), ("BBQ", 8.0), ("Chick", 8.0),
    ("Calzone", 8.0), ("Pesto Lover", 10.0), ("Veronica", 9.0)
]]

snacks = [Snack(name, price) for name, price in [
    ("Čeburekas su mėsa (mažas)", 2.0),
    ("Čeburekas su mėsa (didelis)", 4.5),
    ("Kibinas su mėsa", 1.2),
    ("Gruzdinti koldūnai 'Chinkali' su mėsa (8 vnt.)", 4.0),
    ("Gruzdinti koldūnai 'Chinkali' su mėsa (14 vnt.)", 5.5),
    ("Gruzdintos bulvytės su padažu (mažas)", 3.0),
    ("Gruzdintos bulvytės su padažu (didelis)", 4.0),
    ("Gruzdintos bulvytės su padažu ir daržovėmis (mažas)", 3.5),
    ("Gruzdintos bulvytės su padažu ir daržovėmis (didelis)", 4.5),
    ("Traški naminė vištiena su gruzdintomis bulvytėmis ir salotomis", 5.5),
    ("'Vakarėlio' užkandžių rinkinys", 10.5),
    ("Spring roll's", 5.0),
    ("Sūrio spurgytės", 6.0)
]]

drinks = [Drink(name, price) for name, price in [
    ("Pepsi/Mirinda/7up 0.33l", 1.3), ("Pepsi/Mirinda/7up 0.5l", 1.6),
    ("Gira 0.5l", 1.6), ("Sultys 0.25l", 2.0), ("Nealkoholinis sidras 0.5l", 2.5),
    ("Vanduo 0.5l", 1.1), ("Acala 0.75l", 15.0), ("Juoda kava", 1.5),
    ("Latte", 2.0), ("Cappuccino", 2.0)
]]

# =============================================================================
# KLASĖS
# =============================================================================

class Dish:
    """Patiekalo klasė, sauganti patiekalo pavadinimą ir kainą"""
    def __init__(self, name, price):
        self.name = name
        self.price = price

class RestaurantSystem:
    """Pagrindinė restorano sistemos klasė.
    
    Attributes:
        current_order (list[MenuItem]): Dabartinio užsakymo patiekalų sąrašas
        total (float): Dabartinio užsakymo suma
        employees (list[Employee]): Darbuotojų sąrašas
        employee_orders (dict[str, int]): Darbuotojų užsakymų statistika
        employee_turnover (dict[str, float]): Darbuotojų apyvarta
        all_orders (list[dict]): Visų užsakymų sąrašas
        orders_file (str): Užsakymų failo pavadinimas
        stats_file (str): Statistikos failo pavadinimas
    """
    current_order: list[MenuItem]
    total: float
    employees: list[Employee]
    employee_orders: dict[str, int]
    employee_turnover: dict[str, float]
    all_orders: list[dict]
    orders_file: str
    stats_file: str
    
    def __init__(self, orders_file: str = 'orders.json', stats_file: str = 'stats.json') -> None:
        self.current_order = []
        self.total = 0.0
        self.employees = []
        self.employee_orders = {}
        self.employee_turnover = {}
        self.all_orders = []
        self.orders_file = orders_file
        self.stats_file = stats_file
        self.load_data()

    def add_employee(self, employee: Employee) -> None:
        """Naujo darbuotojo pridėjimas į sistemą.
        
        Args:
            employee (Employee): Darbuotojo objektas
            
        Raises:
            ValueError: Jei darbuotojas jau egzistuoja sistemoje
            TypeError: Jei perduotas netinkamo tipo objektas
        """
        if not isinstance(employee, Employee):
            raise TypeError("Darbuotojo objektas turi būti Employee klasės")
        if any(e.username == employee.username for e in self.employees):
            raise ValueError(f"Darbuotojas '{employee.username}' jau egzistuoja")
        self.employees.append(employee)
        self.employee_orders[employee.username] = 0
        self.employee_turnover[employee.username] = 0.0

    def login_employee(self, username: str, password: str) -> bool:
        """Darbuotojo prisijungimo patikrinimas.
        
        Args:
            username (str): Įvestas vartotojo vardas
            password (str): Įvestas slaptažodis
            
        Returns:
            bool: True jei prisijungimas sėkmingas, False kitu atveju
        """
        for employee in self.employees:
            if employee.login(username, password):
                return True
        return False

    def is_admin(self, username: str) -> bool:
        """Patikrina ar vartotojas yra administratorius.
        
        Args:
            username (str): Vartotojo vardas
            
        Returns:
            bool: True jei vartotojas yra administratorius, False kitu atveju
        """
        return username == "admin"

    def add_dish_to_order(self, item: MenuItem) -> None:
        """Patiekalo pridėjimas į užsakymą.
        
        Args:
            item (MenuItem): Patiekalas, kurį norime pridėti
            
        Raises:
            TypeError: Jei perduotas netinkamo tipo objektas
        """
        if not isinstance(item, MenuItem):
            raise TypeError("Patiekalas turi būti MenuItem klasės")
        self.current_order.append(item)
        self.total += item.get_price()

    def remove_dish_from_order(self, item: MenuItem) -> None:
        """Patiekalo pašalinimas iš užsakymo.
        
        Args:
            item (MenuItem): Patiekalas, kurį norime pašalinti
            
        Raises:
            ValueError: Jei patiekalas nerastas užsakyme
            TypeError: Jei perduotas netinkamo tipo objektas
        """
        if not isinstance(item, MenuItem):
            raise TypeError("Patiekalas turi būti MenuItem klasės")
        if item not in self.current_order:
            raise ValueError("Patiekalas nerastas užsakyme")
        self.current_order.remove(item)
        self.total -= item.get_price()

    def get_order_total(self) -> float:
        """Gauti dabartinio užsakymo sumą.
        
        Returns:
            float: Dabartinio užsakymo suma
        """
        return self.total

    def get_order_items(self) -> list:
        """Gauti dabartinio užsakymo patiekalus.
        
        Returns:
            list: Dabartinio užsakymo patiekalų sąrašas
        """
        return self.current_order

    def save_data(self) -> bool:
        """Išsaugoti visus duomenis į failus.
        
        Returns:
            bool: True jei išsaugojimas sėkmingas, False kitu atveju
        
        Raises:
            IOError: Jei nepavyksta įrašyti į failą
            JSONDecodeError: Jei nepavyksta konvertuoti duomenų į JSON
        """
        try:
            # Išsaugome užsakymus
            orders_data = {
                'orders': [
                    {
                        'number': order['number'],
                        'items': [
                            (item[0], item[1]) 
                            for item in order['items']
                        ],
                        'total': order['total'],
                        'timestamp': order['timestamp'],
                        'employee': order['employee']
                    }
                    for order in self.all_orders
                ]
            }
            
            # Išsaugome statistiką
            stats_data = {
                'employee_orders': self.employee_orders,
                'employee_turnover': self.employee_turnover
            }
            
            # Įrašome į failus
            with open(self.orders_file, 'w', encoding='utf-8') as f:
                json.dump(orders_data, f, ensure_ascii=False, indent=4)
            
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(stats_data, f, ensure_ascii=False, indent=4)
                
            return True
        except (IOError, json.JSONDecodeError) as e:
            error_msg = f"Klaida išsaugant duomenis: {str(e)}"
            print(error_msg)
            messagebox.showerror("Klaida", error_msg)
            return False

    def load_data(self) -> None:
        """Užkrauti duomenis iš failų."""
        try:
            # Užkrauname užsakymus
            if os.path.exists(self.orders_file):
                with open(self.orders_file, 'r', encoding='utf-8') as f:
                    orders_data = json.load(f)
                    self.all_orders = orders_data.get('orders', [])
                    
                    # Perskaičiuojame statistiką iš užsakymų
                    self.employee_orders = {}
                    self.employee_turnover = {}
                    
                    # Einame per visus užsakymus ir skaičiuojame statistiką
                    for order in self.all_orders:
                        employee = order.get('employee')
                        if employee:
                            if employee not in self.employee_orders:
                                self.employee_orders[employee] = 0
                            if employee not in self.employee_turnover:
                                self.employee_turnover[employee] = 0.0
                            
                            self.employee_orders[employee] += 1
                            self.employee_turnover[employee] += float(order.get('total', 0))
            
            # Užtikriname, kad visi darbuotojai turėtų įrašus statistikoje
            for employee in self.employees:
                if employee.username not in self.employee_orders:
                    self.employee_orders[employee.username] = 0
                if employee.username not in self.employee_turnover:
                    self.employee_turnover[employee.username] = 0.0
                    
            # Išsaugome atnaujintą statistiką
            self.save_data()
                    
        except Exception as e:
            print(f"Klaida kraunant duomenis: {str(e)}")
            messagebox.showerror("Klaida", f"Nepavyko užkrauti duomenų: {str(e)}")
            # Klaidos atveju inicializuojame tuščius žodynus
            self.employee_orders = {}
            self.employee_turnover = {}
            for employee in self.employees:
                self.employee_orders[employee.username] = 0
                self.employee_turnover[employee.username] = 0.0

    def finish_order(self, employee_username: str) -> bool:
        """Užsakymo užbaigimas ir išsaugojimas.
        
        Args:
            employee_username (str): Darbuotojo, kuris užbaigia užsakymą, vardas
            
        Returns:
            bool: True jei užsakymas sėkmingai užbaigtas, False kitu atveju
            
        Raises:
            ValueError: Jei darbuotojas nerastas
            TypeError: Jei perduotas netinkamo tipo argumentas
        """
        if not isinstance(employee_username, str):
            raise TypeError("Darbuotojo vardas turi būti tekstinė eilutė")
        if not any(e.username == employee_username for e in self.employees):
            raise ValueError(f"Darbuotojas '{employee_username}' nerastas")
        
        if not self.current_order:
            return False
            
        try:
            order_number = len(self.all_orders) + 1
            items = [(item.get_name(), item.get_price()) for item in self.current_order]
            total = float(self.total)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Pridedame užsakymą į bendrą sąrašą
            self.all_orders.append({
                'number': order_number,
                'items': items,
                'total': total,
                'timestamp': timestamp,
                'employee': employee_username
            })
            
            # Atnaujiname darbuotojo statistiką
            if employee_username not in self.employee_orders:
                self.employee_orders[employee_username] = 0
            if employee_username not in self.employee_turnover:
                self.employee_turnover[employee_username] = 0.0
            
            self.employee_orders[employee_username] += 1
            self.employee_turnover[employee_username] = float(
                self.employee_turnover[employee_username]) + total
            
            # Išsaugome duomenis į failus
            success = self.save_data()
            if not success:
                messagebox.showerror("Klaida", "Nepavyko išsaugoti statistikos!")
                return False
            
            # Išvalome dabartinį užsakymą
            self.current_order = []
            self.total = 0
            return True
        except Exception as e:
            messagebox.showerror("Klaida", f"Klaida užbaigiant užsakymą: {str(e)}")
            return False

    def get_employee_stats(self) -> list:
        """Gauti darbuotojų statistiką.
        
        Returns:
            list: Darbuotojų statistikos sąrašas su žodynais
        """
        stats = []
        for username in self.employee_orders.keys():
            if username != "admin":  # Neįtraukiame admin į statistiką
                stats.append({
                    'username': username,
                    'orders': self.employee_orders.get(username, 0),
                    'turnover': self.employee_turnover.get(username, 0.0)
                })
        return stats

    def get_all_orders(self) -> list:
        """Gauti visų užsakymų sąrašą.
        
        Returns:
            list: Visų užsakymų sąrašas
        """
        return self.all_orders

# =============================================================================
# SISTEMOS INICIJAVIMAS
# =============================================================================
# Sukuriame restorano sistemą
system = RestaurantSystem()

# Įkeliame duomenis prieš pridedant darbuotojus
system.load_data()

# Pridedame darbuotojus
employee1 = Employee("tomas", "tomas123")
employee2 = Employee("monika", "monika123")
admin = Employee("admin", "admin123")

# Pridedame darbuotojus į sistemą ir išsaugome jų statistiką
system.add_employee(employee1)
system.add_employee(employee2)
system.add_employee(admin)

# Išsaugome pradinius duomenis
system.save_data()

# Globalūs kintamieji
current_user = None
order_window = None
all_orders_window = None
root = None
menu_window = None
username_entry = None
password_entry = None

# =============================================================================
# LANGŲ FUNKCIJOS
# =============================================================================

def open_menu() -> None:
    """Meniu lango atidarymas ir konfigūracija.
    
    Sukuria langą su trimis sekcijomis:
    - Picos
    - Užkandžiai
    - Gėrimai
    
    Raises:
        tk.TclError: Jei nepavyksta sukurti lango ar valdiklių
    """
    try:
        global menu_window
        menu_window = tk.Toplevel(root)
        menu_window.title("Meniu")
        menu_window.geometry("900x400")

        # Sukuriame 3 stulpelius
        frames = {
            'pizza': tk.Frame(menu_window),
            'snack': tk.Frame(menu_window),
            'drink': tk.Frame(menu_window)
        }
        
        for frame in frames.values():
            frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Picos sekcija
        pizza_label = tk.Label(
            frames['pizza'],
            text="Picos:",
            font=FONT_HEADER
        )
        pizza_label.pack()
        
        # Picos dydžio pasirinkimas
        size_var = tk.StringVar(value="medium")
        size_frame = tk.Frame(frames['pizza'])
        size_frame.pack(pady=5)
        
        size_options = [
            ("Vidutinė", "medium"),
            ("Didelė (+2€)", "large")
        ]
        
        for text, value in size_options:
            tk.Radiobutton(
                size_frame,
                text=text,
                variable=size_var,
                value=value
            ).pack(side=tk.LEFT)
        
        pizza_listbox = tk.Listbox(
            frames['pizza'],
            selectmode=tk.MULTIPLE,
            width=45,
            height=15
        )
        pizza_listbox.pack()
        
        def update_pizza_prices(*args: tuple) -> None:
            """Atnaujina picų kainas pagal pasirinktą dydį."""
            pizza_listbox.delete(0, tk.END)
            for pizza in pizzas:
                pizza.set_size(size_var.get())
                pizza_listbox.insert(tk.END, pizza.get_display_info())
        
        size_var.trace('w', update_pizza_prices)
        update_pizza_prices()

        # Užkandžių sekcija
        snack_label = tk.Label(
            frames['snack'],
            text="Užkandžiai:",
            font=FONT_HEADER
        )
        snack_label.pack()
        
        snack_frame = tk.Frame(frames['snack'])
        snack_frame.pack(fill=tk.BOTH, expand=True)
        
        snack_scroll_x = tk.Scrollbar(
            snack_frame,
            orient=tk.HORIZONTAL
        )
        snack_scroll_y = tk.Scrollbar(
            snack_frame,
            orient=tk.VERTICAL
        )
        
        snack_listbox = tk.Listbox(
            snack_frame,
            selectmode=tk.MULTIPLE,
            width=45,
            height=15,
            xscrollcommand=snack_scroll_x.set,
            yscrollcommand=snack_scroll_y.set
        )
        
        snack_scroll_x.config(command=snack_listbox.xview)
        snack_scroll_y.config(command=snack_listbox.yview)
        
        snack_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        snack_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        snack_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        for snack in snacks:
            snack_listbox.insert(tk.END, snack.get_display_info())

        # Gėrimų sekcija
        drink_label = tk.Label(
            frames['drink'],
            text="Gėrimai:",
            font=FONT_HEADER
        )
        drink_label.pack()
        
        drink_listbox = tk.Listbox(
            frames['drink'],
            selectmode=tk.MULTIPLE,
            width=45,
            height=15
        )
        drink_listbox.pack()
        
        for drink in drinks:
            drink_listbox.insert(tk.END, drink.get_display_info())

        def add_to_order() -> None:
            """Prideda pasirinktus produktus į užsakymą."""
            try:
                # Picos
                for i in pizza_listbox.curselection():
                    selected_pizza = pizzas[i]
                    new_pizza = Pizza(
                        selected_pizza.name,
                        selected_pizza.base_price
                    )
                    new_pizza.set_size(size_var.get())
                    system.add_dish_to_order(new_pizza)
                
                # Užkandžiai
                for i in snack_listbox.curselection():
                    system.add_dish_to_order(snacks[i])
                
                # Gėrimai
                for i in drink_listbox.curselection():
                    system.add_dish_to_order(drinks[i])
                
                if 'order_listbox' in globals():
                    update_order_display()
                
                messagebox.showinfo(
                    "Pridėta",
                    "Produktai pridėti į užsakymą!"
                )
                
                # Nužymėti pasirinkimus
                for listbox in [pizza_listbox, snack_listbox, drink_listbox]:
                    listbox.selection_clear(0, tk.END)
                    
            except Exception as e:
                messagebox.showerror(
                    "Klaida",
                    f"Nepavyko pridėti produktų: {str(e)}"
                )

        add_button = tk.Button(
            frames['snack'],
            text="Pridėti į užsakymą",
            command=add_to_order
        )
        add_button.pack(pady=10)
        
    except tk.TclError as e:
        messagebox.showerror(
            "Klaida",
            f"Nepavyko atidaryti meniu lango: {str(e)}"
        )

def open_order_window() -> None:
    """Užsakymų lango atidarymas ir konfigūracija."""
    global order_window, order_listbox, current_user
    if order_window is None or not order_window.winfo_exists():
        order_window = tk.Toplevel(root)
        order_window.title("Užsakymas")
        order_window.geometry("400x600")

        # Prisijungęs darbuotojas
        user_label = tk.Label(
            order_window, 
            text=f"Darbuotojas: {current_user.capitalize()}", 
            font=FONT_NORMAL
        )
        user_label.pack(pady=(5, 0))

        # Data ir laikas
        datetime_label = tk.Label(order_window, font=FONT_NORMAL)
        datetime_label.pack(pady=5)

        def update_datetime():
            """Atnaujina datos ir laiko rodymą."""
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            datetime_label.config(text=now)
            datetime_label.after(1000, update_datetime)
        update_datetime()

        # Užsakymo sąrašas
        order_frame = tk.Frame(order_window)
        order_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Slinkjuostės
        scrollbar_y = tk.Scrollbar(order_frame)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        scrollbar_x = tk.Scrollbar(order_frame, orient=tk.HORIZONTAL)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        # Užsakymo sąrašo langas
        order_listbox = tk.Listbox(
            order_frame,
            width=45,
            height=15,
            xscrollcommand=scrollbar_x.set,
            yscrollcommand=scrollbar_y.set
        )
        order_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Susiejame slinkjuostes su sąrašu
        scrollbar_y.config(command=order_listbox.yview)
        scrollbar_x.config(command=order_listbox.xview)

        # Bendra suma
        total_label = tk.Label(
            order_window,
            text="Bendra suma: 0€",
            font=FONT_HEADER
        )
        total_label.pack(pady=10)

        # Mygtukų rėmelis
        buttons_frame = tk.Frame(order_window)
        buttons_frame.pack(pady=5)

        # Mygtukai
        remove_button = tk.Button(
            buttons_frame,
            text="Pašalinti iš užsakymo",
            command=remove_from_order
        )
        remove_button.pack(pady=5)

        calculate_button = tk.Button(
            buttons_frame,
            text="Rodyti sumą",
            command=lambda: total_label.config(
                text=f"Bendra suma: {system.get_order_total()}€"
            )
        )
        calculate_button.pack(pady=5)

        finish_button = tk.Button(
            buttons_frame,
            text="Užsakymas baigtas",
            command=finish_order
        )
        finish_button.pack(pady=5)

        end_shift_button = tk.Button(
            buttons_frame,
            text="Baigti pamainą",
            command=lambda: end_shift(order_window),
            bg="red",
            fg="white"
        )
        end_shift_button.pack(pady=10)

        # Atnaujinti užsakymo rodinį
        update_order_display()

def end_shift(order_window: tk.Toplevel) -> None:
    """Baigia darbuotojo pamainą."""
    global current_user, menu_window
    # Uždarome visus langus
    if order_window and order_window.winfo_exists():
        order_window.destroy()
    if menu_window and menu_window.winfo_exists():
        menu_window.destroy()
    if 'all_orders_window' in globals() and all_orders_window and all_orders_window.winfo_exists():
        all_orders_window.destroy()
    
    # Išsaugome duomenis
    system.save_data()
    
    # Atsijungiame
    current_user = None
    root.deiconify()
    
    # Išvalome prisijungimo laukus
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    messagebox.showinfo("Atsijungimas", "Pamaina baigta. Viso gero!")

def update_order_display() -> None:
    """Atnaujina užsakymo rodinį."""
    if 'order_listbox' in globals():
        order_listbox.delete(0, tk.END)
        for item in system.get_order_items():
            order_listbox.insert(tk.END, item.get_display_info())

def remove_from_order() -> None:
    """Pašalina pasirinktą patiekalą iš užsakymo."""
    if order_listbox.curselection():
        selected_index = order_listbox.curselection()[0]
        item_to_remove = system.current_order[selected_index]
        system.remove_dish_from_order(item_to_remove)
        update_order_display()

def finish_order() -> None:
    """Užbaigia dabartinį užsakymą."""
    if system.finish_order(current_user):
        messagebox.showinfo("Užsakymas", "Užsakymas sėkmingai užbaigtas!")
        update_order_display()
        open_all_orders_window()
    else:
        messagebox.showwarning("Klaida", "Nėra ką užbaigti!")

def open_all_orders_window() -> None:
    """Visų užsakymų lango atidarymas ir konfigūracija.
    
    Raises:
        tk.TclError: Jei nepavyksta sukurti lango ar valdiklių
    """
    try:
        global all_orders_window, orders_listbox
        if all_orders_window is None or not all_orders_window.winfo_exists():
            all_orders_window = tk.Toplevel(root)
            all_orders_window.title("Visi užsakymai")
            orders_text = tk.Text(
                all_orders_window, 
                width=60, 
                height=20, 
                wrap='word'
            )
            orders_text.pack(pady=10)
            orders_listbox = orders_text
        else:
            orders_listbox.delete('1.0', tk.END)
            
        # Užpildome visus užsakymus
        for order in system.get_all_orders():
            items_str = ', '.join(
                [f"{name} ({price}€)" for name, price in order['items']]
            )
            order_text = (
                f"Užsakymas #{order['number']} "
                f"({order['timestamp']}): "
                f"{items_str} | "
                f"Suma: {order['total']}€\n"
            )
            orders_listbox.insert(tk.END, order_text)
    except tk.TclError as e:
        error_msg = f"Nepavyko atidaryti užsakymų lango: {str(e)}"
        items_str = ', '.join([f"{name} ({price}€)" for name, price in order['items']])
        orders_listbox.insert(tk.END, 
            f"Užsakymas #{order['number']} ({order['timestamp']}): "
            f"{items_str} | Suma: {order['total']}€\n")
    except tk.TclError as e:
        messagebox.showerror("Klaida", f"Nepavyko atidaryti užsakymų lango: {str(e)}")

def open_admin_window() -> None:
    """Administratoriaus lango atidarymas ir konfigūracija.
    
    Sukuria langą su darbuotojų statistika, įskaitant:
    - Užsakymų kiekį
    - Apyvartą
    - Atnaujinimo ir atsijungimo mygtukus
    
    Raises:
        tk.TclError: Jei nepavyksta sukurti lango ar valdiklių
        Exception: Jei nepavyksta užkrauti statistikos
    """
    try:
        admin_window = tk.Toplevel(root)
        admin_window.title("Administratoriaus panelė")
        admin_window.geometry("600x400")

        # Antraštė
        header_label = tk.Label(admin_window, text="Darbuotojų statistika", font=FONT_HEADER)
        header_label.pack(pady=20)

        # Statistikos lentelė
        stats_frame = tk.Frame(admin_window)
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        def display_stats() -> None:
            """Atnaujina ir rodo darbuotojų statistiką.
            
            Raises:
                Exception: Jei nepavyksta užkrauti ar atvaizduoti statistikos
            """
            try:
                # Išvalome senus duomenis
                for widget in stats_frame.winfo_children():
                    widget.destroy()

                # Stulpelių antraštės
                headers = ["Darbuotojas", "Užsakymų kiekis", "Apyvarta (€)"]
                for i, header in enumerate(headers):
                    label = tk.Label(stats_frame, text=header, font=FONT_NORMAL)
                    label.grid(row=0, column=i, padx=10, pady=5, sticky="w")

                # Įkeliame naujausius duomenis
                system.load_data()
                
                # Darbuotojų statistika
                stats = system.get_employee_stats()
                for i, stat in enumerate(stats, start=1):
                    tk.Label(
                        stats_frame, 
                        text=stat['username'].capitalize(), 
                        font=FONT_SMALL
                    ).grid(row=i, column=0, padx=10, pady=5, sticky="w")
                    
                    tk.Label(
                        stats_frame, 
                        text=str(stat['orders']), 
                        font=FONT_SMALL
                    ).grid(row=i, column=1, padx=10, pady=5)
                    
                    tk.Label(
                        stats_frame, 
                        text=f"{stat['turnover']:.2f}", 
                        font=FONT_SMALL
                    ).grid(row=i, column=2, padx=10, pady=5)
            except Exception as e:
                messagebox.showerror("Klaida", f"Nepavyko atnaujinti statistikos: {str(e)}")

        # Iškart rodome statistiką
        display_stats()

        # Mygtukų frame'as
        buttons_frame = tk.Frame(admin_window)
        buttons_frame.pack(pady=10)

        # Atnaujinimo mygtukas
        refresh_button = tk.Button(
            buttons_frame, 
            text="Atnaujinti statistiką", 
            command=display_stats
        )
        refresh_button.pack(side=tk.LEFT, padx=10)

        def admin_logout() -> None:
            """Administratoriaus atsijungimo funkcija.
            
            Raises:
                tk.TclError: Jei nepavyksta manipuliuoti GUI elementais
            """
            try:
                global current_user
                # Uždarome administratoriaus langą
                admin_window.destroy()
                # Atsijungiame
                current_user = None
                # Rodome prisijungimo langą
                root.deiconify()
                # Išvalome prisijungimo laukus
                username_entry.delete(0, tk.END)
                password_entry.delete(0, tk.END)
                messagebox.showinfo("Atsijungimas", "Administratorius atsijungė sėkmingai!")
            except tk.TclError as e:
                messagebox.showerror("Klaida", f"Klaida atsijungiant: {str(e)}")

        # Atsijungimo mygtukas
        logout_button = tk.Button(
            buttons_frame, 
            text="Atsijungti", 
            command=admin_logout, 
            bg="red", 
            fg="white"
        )
        logout_button.pack(side=tk.LEFT, padx=10)
    except tk.TclError as e:
        messagebox.showerror(
            "Klaida", 
            f"Nepavyko atidaryti administratoriaus lango: {str(e)}"
        )

def login() -> None:
    """Prisijungimo funkcija."""
    global current_user
    username = username_entry.get()
    password = password_entry.get()
    
    if system.login_employee(username, password):
        current_user = username
        messagebox.showinfo("Prisijungimas", "Prisijungimas sėkmingas!")
        root.withdraw()
        
        if system.is_admin(username):
            open_admin_window()
        else:
            open_menu()
            open_order_window()
    else:
        messagebox.showerror("Klaida", "Neteisingi prisijungimo duomenys!")

def main() -> None:
    """Pagrindinė programos paleidimo funkcija."""
    global root, username_entry, password_entry
    
    root = tk.Tk()
    root.geometry("400x300")
    root.title("Prisijungimo sistema")

    username_label = tk.Label(root, text="Vartotojo vardas:")
    username_label.pack(pady=10)
    username_entry = tk.Entry(root)
    username_entry.pack(pady=5)

    password_label = tk.Label(root, text="Slaptažodis:")
    password_label.pack(pady=10)
    password_entry = tk.Entry(root, show="*")
    password_entry.pack(pady=5)

    login_button = tk.Button(root, text="Prisijungti", command=login)
    login_button.pack(pady=20)

    root.mainloop()

if __name__ == '__main__':
    main()
