class Model():
    def select(self):
        """
        Gets all entries from the database
        :return: Tuple containing all rows of database
        """
        pass

    def insert(self, product, category, location, description, image):
        """
        Inserts entry into database
        :param product: String
        :param location: Int
        :param description: String
        :param image: String
        :return: True
        :raises: Database errors on connection and insertion
        """
        pass

    def delete(self, product):
        """
        Deletes entry from database
        :param product: String
        :return: True
        :raises: Database errors on connection and deletion
        """
        pass

    def update(self, product, category):
        """
        Updates product and/or category
        :param product: String
        :param category: String
        :return: True
        :raises: Database errors on connection and deletion
        """
        pass