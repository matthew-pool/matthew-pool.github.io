""" Data Access Layer (DAL) class interacts with Data Store/Source (MongoDB) database """
from pymongo import MongoClient  # MongoDB driver
from pymongo.errors import DuplicateKeyError
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
logging.info("Program Executing...")


class MongoCrud:
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self, username, password, host, port, db, coll):
        """ MongoClient initialization """
        # TODO: remove hard-wired account info

        # Connection variables
        USER = username
        PASS = password
        HOST = host
        PORT = port
        DB = db
        COLL = coll

        # 'mongodb://aacuser:M22@nv-desktop-services.apporto.com:32474'
        self.client = MongoClient('mongodb://%s:%s@%s:%d' % (USER, PASS, HOST, PORT))
        self.database = self.client['%s' % DB]  # uses 'AAC' database
        self.collection = self.database['%s' % COLL]  # uses 'animals' collection

    # =============================================================================

    # CRUD methods
    def create(self, doc: dict) -> bool:
        """ Create (insert) a new animal document """

        if not doc or not isinstance(doc, dict):  # if empty {}
            raise ValueError("Document must be non-empty dict!")

        try:
            self.database.animals.insert_one(doc)  # Creates a new document
            return True  # Successful

        except DuplicateKeyError as e:  # if '_id' value already exists
            logger.error(f"Error updating {e}")
            # raise
            return False  # Unsuccessful

    def read(self, query_filter: dict) -> list:
        """ Read (query) documents based on query filter """

        if not query_filter or not isinstance(query_filter, dict):  # if empty {}
            raise ValueError("Query filter must be non-empty dict!")

        try:
            # Assigned iterable Cursor object
            cursor = self.database.animals.find(query_filter)
            # list comprehension: creates list of docs matching query filter
            doc_list = [doc for doc in cursor]  # Returns list of docs from cursor
            return doc_list  # Returns empty [] if no docs match query

        except TypeError as e:
            logger.error(f"Error reading {e}")
            raise
            # return []

    def update(self, query_filter: dict, update_dict: dict) -> int:
        """ Update documents based on query filter with update_dict key-value pairs """

        if not query_filter or not isinstance(query_filter, dict):
            raise ValueError("query_filter must be non-empty dict!")
        if not update_dict or not isinstance(update_dict, dict):
            raise ValueError("update_dict must be non-empty dict!")

        try:
            result = self.database.animals.update_many(query_filter, {'$set': update_dict})
            return result.modified_count  # returns update_many() 'modified_count' value

        except Exception as e:
            logger.error(f"Error updating: {e}")
            raise

    def delete(self, query_filter: dict) -> int:
        """ Delete (remove) documents based on query filter """

        if not query_filter or not isinstance(query_filter, dict):
            raise ValueError("query_filter must be non-empty dict!")

        try:
            result = self.database.animals.delete_many(query_filter)
            return result.deleted_count  # returns delete_many() 'deleted_count' value

        except Exception as e:
            logger.error(f"Error deleting: {e}")
            raise
