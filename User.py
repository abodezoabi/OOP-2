import importlib

from Post import PostFactory
from Post import Post
from Post import TextPost
from Post import ImagePost
from Post import SalePost


class User:

    def __init__(self, username, password, is_online, networkname):
        """
        Initialize a User object.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.
            is_online (bool): Indicates if the user is currently online.
            networkname (str): The name of the social network the user belongs to.
        """
        self.username = username
        self.password = password
        self.followers = set()
        self.posts = []
        self.notifications = []
        self.is_online = is_online
        self.networkname = networkname

    def name(self):
        """
        Return the username of the user.
        """
        return self.username

    def get_user_fromname(self, username):
        """
        Get a user object by username.

        Args:
            username (str): The username of the user to retrieve.

        Returns:
            User: The User object with the specified username.
        """
        if self.username == username:
            return self
        return None

    def on_same_network2(self, u1, u2):
        """
        Check if two users are on the same network.

        Args:
            u1 (User): The first user.
            u2 (User): The second user.

        Returns:
            bool: True if both users are on the same network, False otherwise.
        """
        if u1.networkname == u2.networkname:
            return True
        return False

    def notify_observers(self):
        """
        Notify all followers when a new post is published by this user (Observer Design Pattern).
        """
        for follower in self.followers:
            notification = f"{self.username} has a new post"
            follower.notifications.append(notification)

    def follow(self, other_user):
        """
        Follow another user.

        Args:
            other_user (User): The user to follow.
        """
        if self in other_user.followers:
            print(f"{self.username} is already following {other_user.username}")
            return None

        if self.is_online:  # no need to check authentication(username & password) because already online
            if self.name() != other_user.name():  # user cannot follow himself
                other_user.followers.add(
                    self)  # this line helps when using the observer design pattern by adding observers
                print(self.username + " started following " + other_user.username)

    def unfollow(self, other_user):
        """
        Unfollow another user.

        Args:
            other_user (User): The user to unfollow.
        """
        if self.is_online:  # no need to check authentication(username & password) because already online
            if self in other_user.followers:
                other_user.followers.remove(self)
                print(f"{self.username} unfollowed {other_user.username}")
            else:
                print(f"{self.username} is not following {other_user.username}")

    def publish_post(self, post_type, content=None, price=None, location=None):
        """
        Publish a post.

        Args:
            post_type (str): The type of the post (e.g., "Text", "Image", "Sale").
            content (str, optional): The content of the post. Defaults to None.
            price (float, optional): The price of the post (for Sale posts). Defaults to None.
            location (str, optional): The location of the post (for Sale posts). Defaults to None.

        Returns:
            Post: The published post.
        """
        if not self.is_online:
            print("Error: User is not logged in.")
            return None

        post = PostFactory.createpost(self, post_type, content, price, location)

        if post:
            self.posts.append(post)  # Add the post to the user's list of posts
            # notify observers
            self.notify_observers()  # Notify observers

            print(post)
            return post
        else:
            print("Error: Failed to create post.")
            return None

    def print_notifications(self):
        """
        Print notifications for the user.
        """
        print(f"{self.username}'s notifications:")
        for notification in self.notifications:
            print(notification)

    def __str__(self):
        """
        Return a string representation of the user.
        """
        return (f"User name: {self.username}, Number of posts: {len(self.posts)},"
                f" Number of followers: {len(self.followers)}")
