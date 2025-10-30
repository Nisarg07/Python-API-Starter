from typing import List

#--- PROJECT 1: OBJECT-ORIENTED PROGRAMMING BASICS ---

# OBJECTIVE: Define a class to represent a user in my future system.
# This establsihes the foundational data structure for Flask backend.

class User:
    """
    Represents a user in the application with basic account details.
    
    TODO:
    1. Complete the __init__ method to set all attributes.
    2. Implement the get_initials method.
    3. Instantiate at least two User objects outside of the class.
    4. Call the get_initials method on both objects and print the result.
    """

    def __init__(self, first_name: str, last_name: str, email: str, is_admin: bool = False):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

    def get_initials(self) -> str:

        return f"{self.first_name[0].upper()}.{self.last_name[0].upper()}."
    

jane_doe = User("Jane", "Doe", "jane@example.com")
john_smith = User("John", "Smith", "john@admin.com", True)

print("---User Object Testing ---")
print(f"User 1 Name: {jane_doe.first_name} {jane_doe.last_name}")
print(f"User 1 initials: {jane_doe.get_initials()}")

print(f"User 2 Name: {john_smith.first_name} {john_smith.last_name}")
print(f"User 2 is admin: {john_smith.is_admin}")
print(f"User 2 initials: {john_smith.get_initials()}")