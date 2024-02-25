from User import User


def legal_password(pswrd):
    """Check if the password meets the criteria.

    Args:
        pswrd (str): The password to be checked.

    Returns:
        bool: True if the password meets the criteria, False otherwise.
    """
    return 4 <= len(pswrd) <= 8


class SocialNetwork:
    """Class representing a social network."""

    _single = None  # instance flag

    """Create a new instance of the SocialNetwork class if one doesn't exist.

        This method ensures that only one instance of the SocialNetwork class exists
        by maintaining a single instance flag (_single). If an instance already exists,
        it returns the existing instance. If not, it creates a new instance with the
        provided name and initializes the necessary attributes.

        Args:
            cls (type): The class object.
            name (str): The name of the social network.

        Returns:
            SocialNetwork: The single instance of the SocialNetwork class.
        """

    def __new__(cls, name):
        if not cls._single:
            cls._single = super(SocialNetwork, cls).__new__(cls)
            cls._single.name = name
            cls._single.users = []
            cls._single.online_users = []
            print("The social network " + name + " was created!")
        return cls._single

    def __init__(self, name):
        """Initialize a new instance of the SocialNetwork class.

        Args:
            name (str): The name of the social network.
        """
        self.name = name
        self.users = []
        self.online_users = []
        self.created = True  # Set created flag to True to indicate instance been initialized

    def print_users(self):
        """Print the usernames of all users in the social network."""
        for user in self.users:
            print(user.username + ": " + user.networkname)

    def on_same_network(self, other):
        """Check if two users are on the same network.

        Args:
            other (User): The other user to compare with.

        Returns:
            bool: True if both users are on the same network, False otherwise.
        """
        if self.users is None:
            return True
        for user in self.users:
            if user.networkname != other.networkname:
                return False
        return True

    def user_exists(self, username):
        """Check if a user exists in the social network.

        Args:
            username (str): The username to check.

        Returns:
            bool: True if the user exists, False otherwise.
        """
        for user in self.users:
            if user.username == username:
                return True
        return False

    def get_user(self, username):
        """Get a user object based on the username.

        Args:
            username (str): The username of the user to retrieve.

        Returns:
            User: The user object if found, None otherwise.
        """
        for user in self.users:
            if user.username == username:
                return user
        return None

    def sign_up(self, username, pswrd):
        """Sign up a new user to the social network.

        Args:
            username (str): The username of the new user.
            pswrd (str): The password of the new user.

        Returns:
            User: The newly signed-up user object, or None if sign-up fails.
        """
        if self.user_exists(username) or not legal_password(pswrd):
            print("Invalid username or password")
            return
        new_user = User(username, pswrd, True, self.name)
        self.users.append(new_user)
        self.online_users.append(new_user)
        return new_user

    def log_in(self, username, password):
        """Log in an existing user to the social network.

        Args:
            username (str): The username of the user to log in.
            password (str): The password of the user.

        Returns:
            None
        """
        for user in self.users:
            if username == user.username and password == user.password:
                if user.is_online:
                    print(user.username + " already logged in")
                    return
                else:
                    user.is_online = True
                    self.online_users.append(user)
                    print(username + " connected")
                    return
        print("Incorrect username or password")

    def log_out(self, username):
        """Log out a user from the social network.

        Args:
            username (str): The username of the user to log out.

        Returns:
            None
        """
        for logged_in_user in self.online_users:
            if logged_in_user.username == username:
                print(username + " disconnected")
                logged_in_user.is_online = False
                self.online_users.remove(logged_in_user)
                return
        print("User not found or not logged in")

    def __str__(self):
        """String representation of the SocialNetwork object.

        Returns:
            str: The string representation of the SocialNetwork object.
        """
        result = f"{self.name} social network:\n"
        for user in self.users:
            result += f"User name: {user.username}, Number of posts: {len(user.posts)}, Number of followers: {len(user.followers)}\n"
        return result
