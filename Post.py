import matplotlib.pyplot as plt
import matplotlib.image as mpimg


class Post:
    def __init__(self, owner, post_type):
        """
        Initialize a Post object.

        Args:
            owner (User): The user who owns the post.
            post_type (str): The type of the post.
        """
        self.owner = owner
        self.post_type = post_type

    def like(self, liker):
        """
        Add a like to the post and notify the owner.

        Args:
            liker (User): The user who liked the post.
        """
        if liker.is_online:
            if liker != self.owner and liker not in self.owner.notifications:
                notification = f"{liker.username} liked your post"
                self.owner.notifications.append(notification)
                print(f"notification to {self.owner.username}: {notification}")

    def comment(self, commenter, comment_content):
        """
        Add a comment to the post and notify the owner.

        Args:
            commenter (User): The user who commented on the post.
            comment_content (str): The content of the comment.
        """
        if commenter.is_online:
            notification = f"{commenter.username} commented on your post"
            if commenter != self.owner and commenter not in self.owner.notifications:
                self.owner.notifications.append(notification)
                print(f"notification to {self.owner.username}: {notification}: {comment_content}")
        else:
            print("Cannot comment: User is not online")


class TextPost(Post):

    def __init__(self, owner, post_type, text):
        """
        Initialize a TextPost object.

        Args:
            owner (User): The user who owns the post.
            post_type (str): The type of the post.
            text (str): The text content of the post.
        """
        self.text = text
        super().__init__(owner, post_type)

    def __str__(self):
        """
        Get a string representation of the TextPost object.

        Returns:
            str: The string representation.
        """
        return f"{self.owner.username} published a post:\n\"{self.text}\"\n"


class ImagePost(Post):
    def __init__(self, owner, post_type, image_url):
        """
        Initialize an ImagePost object.

        Args:
            owner (User): The user who owns the post.
            post_type (str): The type of the post.
            image_url (str): The URL of the image.
        """
        self.image_url = image_url
        super().__init__(owner, post_type)

    def display(self):
        """
        Display the image of the ImagePost.
        """
        try:
            image_data = mpimg.imread(self.image_url)
            plt.imshow(image_data)
            plt.axis('off')
            plt.show()
            print("Shows picture")
        except Exception as e:
            print("Error displaying image:", e)

    def __str__(self):
        """
        Get a string representation of the ImagePost object.

        Returns:
            str: The string representation.
        """
        return f"{self.owner.username} posted a picture\n"


class SalePost(Post):
    def __init__(self, user, post_type, product, price, location):
        """
        Initialize a SalePost object.

        Args:
            user (User): The user who owns the post.
            post_type (str): The type of the post.
            product (str): The product for sale.
            price (float): The price of the product.
            location (str): The location of the product.
        """
        super().__init__(user, post_type)
        self.product = product
        self.price = price
        self.location = location
        self.available = True

    def discount(self, discount, password):
        """
        Apply a discount to the price of the product.

        Args:
            discount (float): The discount percentage.
            password (str): The password of the owner.
        """
        if self.owner.password == password:
            self.price *= (100 - discount) / 100.0
            print(f"Discount on {self.owner.username} product! the new price is: {self.price}")

    def sold(self, password):
        """
        Mark the product as sold.

        Args:
            password (str): The password of the owner.
        """
        if self.owner.password == password and self.available:
            self.available = False
            print(f"{self.owner.username}'s product is sold")

    def __str__(self):
        """
        Get a string representation of the SalePost object.

        Returns:
            str: The string representation.
        """
        if self.available:
            return (f"{self.owner.username} posted a product for sale:\n"
                    f"For sale! {self.product}, price: {self.price}, pickup from: {self.location}\n")
        else:
            return (f"{self.owner.username} posted a product for sale:\n"
                    f"Sold! {self.product}, price: {self.price}, pickup from: {self.location}\n")


class PostFactory:

    def createpost(owner, post_type, content, price=None, location=None):
        """
        Create a post using the Factory design pattern.

        Args:
            owner (User): The user who owns the post.
            post_type (str): The type of the post.
            content (str): The content of the post.
            price (float, optional): The price of the post (for Sale posts). Defaults to None.
            location (str, optional): The location of the post (for Sale posts). Defaults to None.

        Returns:
            Post: The created post.
        
        Raises:
            ValueError: If an invalid post type is provided.
        """
        if post_type == "Text":
            return TextPost(owner, post_type, content)
        elif post_type == "Image":
            return ImagePost(owner, post_type, content)
        elif post_type == "Sale":
            return SalePost(owner, post_type, content, price, location)
        else:
            raise ValueError("Invalid post type")