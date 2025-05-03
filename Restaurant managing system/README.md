# Restaurant-Managing-System
Restaurant order management system with GUI interface

## Introduction

### What is Restaurant Management System?

The **Restaurant Management System** is a GUI-based application for managing restaurant operations. The system handles order processing, employee management, and statistical analysis. Written in Python using tkinter, it demonstrates Object-Oriented Programming (OOP) principles and design patterns to create a robust and maintainable solution.

### How to run the program?
1. Ensure Python 3 is installed.
2. Save the program as `restoranas8.py`.
3. Open a terminal and run: `python restoranas8.py`.

### How to use?

Upon launch, users interact with a graphical interface to:
1. Login as employee/admin (username: tomas, password: tomas123; username: monika, password: monika123; username: admin, password: admin123)
2. Create orders
3. Manage menu items
4. View statistics
5. Track employee activity
6. Save/load data
0. Exit

### Program Design

#### GUI Architecture
The system features a modern, user-friendly interface built with tkinter:

1. **Window Sizes**
   ```python
   WINDOW_SIZE_LOGIN = "400x300"
   WINDOW_SIZE_MENU = "900x400"
   WINDOW_SIZE_ORDER = "400x600"
   WINDOW_SIZE_ADMIN = "600x400"
   ```

2. **Visual Elements**
   ```python
   # Professional color scheme
   COLOR_ERROR = "red"
   COLOR_TEXT_LIGHT = "white"

   # Typography
   FONT_HEADER = ("Arial", 14, "bold")
   FONT_NORMAL = ("Arial", 12)
   FONT_SMALL = ("Arial", 11)
   ```

3. **Interface Components**
   - Login window with secure authentication
   - Menu management interface with categories
   - Order processing window with real-time updates
   - Administrative panel for statistics
   - Order history viewer

## Analysis

### OOP Implementation

#### 1. Inheritance
Clear class hierarchy for menu items:
```python
class MenuItem:
    def __init__(self, name: str, price: float) -> None:
        self.name = name
        self.price = price

class Pizza(MenuItem):
    def set_size(self, size: str) -> None:
        self.size = size
        if size == "large":
            self.price = self.base_price + 2

class Snack(MenuItem):
    pass

class Drink(MenuItem):
    pass
```

#### 2. Encapsulation
Data protection through private attributes and methods:
```python
class RestaurantSystem:
    def __init__(self):
        self._orders = []
        self._employees = []
        self._employee_orders = {}
        self._employee_turnover = {}
```

#### 3. Polymorphism
Method overriding in menu items:
```python
class MenuItem:
    def get_display_info(self):
        return f"{self.name} - {self.price}€"

class Pizza(MenuItem):
    def get_display_info(self):
        return f"{self.name} ({self.size}) - {self.price}€"
```

#### 4. Abstraction
Base class defining common interface:
```python
class MenuItem:
    def get_price(self) -> float:
        return self.price
    
    def get_name(self) -> str:
        return self.name
```

### Design Patterns

#### 1. Template Method Pattern
Implemented in the `MenuItem` class hierarchy, providing a template for item creation and display:
```python
class MenuItem:
    def get_display_info(self):
        return f"{self.name} - {self.price}€"
    
    def get_price(self):
        return self.price
```

#### 2. Factory Method Pattern
Used for creating menu items:
```python
pizzas = [Pizza(name, price) for name, price in [
    ("Margherita", 8.0),
    ("Capricciosa", 8.0),
    # ...
]]

snacks = [Snack(name, price) for name, price in [
    ("Čeburekas su mėsa (mažas)", 2.0),
    # ...
]]
```

### Exception Handling

Custom exception hierarchy for better error management:
```python
class RestaurantError(Exception):
    """Base restaurant system exception."""
    pass

class OrderError(RestaurantError):
    pass

class EmployeeError(RestaurantError):
    pass

class DataError(RestaurantError):
    pass
```

### Data Persistence

The system implements JSON-based data persistence for orders and statistics:
```python
def save_data(self) -> bool:
    try:
        with open(self.orders_file, 'w', encoding='utf-8') as f:
            json.dump(orders_data, f, ensure_ascii=False, indent=4)
        return True
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error saving data: {str(e)}")
        return False
```

## Testing
The system includes unit tests in `test_restoranas.py` to ensure reliability and correct functionality. Tests cover:

1. Menu Item Operations
   - Item creation
   - Price calculations
   - Display information formatting

2. Order Management
   - Adding items to order
   - Removing items from order
   - Order total calculation
   - Order completion

3. Employee Management
   - Login functionality
   - Access control
   - Statistics tracking

4. Data Persistence
   - Data saving
   - Data loading
   - Error handling

## Features

### 1. User Management
- Secure login system
- Role-based access (admin/employee)
- Activity tracking
- Employee statistics

### 2. Order Processing
- Dynamic menu management
- Real-time price calculation
- Order history tracking
- Multiple item categories (Pizza, Snacks, Drinks)

### 3. Menu Management
- Pizza size customization
- Price adjustments
- Category organization
- Item information display

### 4. Data Management
- JSON-based persistence
- Automatic data loading/saving
- Error handling
- Statistics tracking

## Results and Future Development

### Current Achievements
1. Fully functional GUI interface
2. Robust order management system
3. Secure employee authentication
4. Comprehensive statistics tracking
5. Reliable data persistence
6. Error handling system

### Future Prospects
1. Database integration
2. Advanced reporting features
3. Kitchen management system
4. Online ordering integration
5. Payment system integration
6. Multi-language support
