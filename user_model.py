from typing import List

#--- PROJECT 1: OBJECT-ORIENTED PROGRAMMING BASICS ---

# OBJECTIVE: Define a class to represent a user in my future system.
# This establsihes the foundational data structure for Flask backend.

class User:
    """
    Represents a user in the application with basic account details.

    """

    def __init__(self, id, username: str, email: str, level: str = "Junior"):
        self.id = id
        self.username = username
        self.email = email
        self.level = level

    def to_dict(self):
        return {
            "username": self.username,
            "email": self.email,
            "level": self.level
        }
    
@classmethod
def from_dict(cls, source, id):
    return cls(
        id = id,
        username = source.get('username'),
        email = source.get('email'),
        level = source.get('level','Junior')
    )

def __repr__(self):
    return(
        f"User(id={self.id!r}, username={self.username!r},"
        f"email={self.email!r}, level={self.level!r}"
    )