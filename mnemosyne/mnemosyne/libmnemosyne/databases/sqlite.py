#!/usr/bin/python -tt
# vim: sw=4 ts=4 expandtab ai
#
# sqlite.py 
# Author: Ed Bartosh <bartosh@gmail.com>
#

from sqlite3 import connect

from mnemosyne.libmnemosyne.database import Database

class Sqlite(Database):

    """ Sqllite backend """

    # Creating, loading and saving the entire database.

    def __init__(self):
        self.connection = None
        self.cursor = None

    def new(self, path):
        connection = connect(path)
        cursor = connection.cursor()
        
        cursor.execute('''create table facts
        (id integer primary key, guid int, facttype_id int, 
        ctime timestamp, mtime timestamp)''')

        cursor.execute('''create table factdata
        (id integer primary key, fact_id int, key text, value text)''')

        cursor.execute('''create table facttypes
        (id integer primary key, name varchar(20), enabled boolean)''')

        cursor.execute('''create table views
        (id integer primary key, facttype_id int, name varchar(20),
        enabled boolean)''')

        cursor.execute('''create table reviewstats
        (id integer primary key, fact_id int, view_id int, grade int,
        easiness int, next_rep timestamp)''')
        
        cursor.execute('''create table categories
        (id integer primary key, parent_id int, name varchar(20), 
        enabled boolean)''')

        cursor.execute('''create table fact_categories
        (id integer primary key, category_id int, fact_id int)''')

        cursor.execute('''create table reviews
        (card_id int, time timestamp, number int, prev int, 
        client_guid int)''')

        cursor.execute('''create table meta
        (row_id int, key text, value text)''')

        self.cursor = cursor
        self.connection = connection

    def save(self):
        raise NotImplementedError

    def backup(self):
        raise NotImplementedError

    def load(self):
        raise NotImplementedError

    def unload(self):
        raise NotImplementedError

    def is_loaded():
        raise NotImplementedError

    # Start date.

    def set_start_date(self, start_date_obj):
        raise NotImplementedError

    def days_since_start(self):
        raise NotImplementedError

    # Adding, modifying and deleting categories, facts and cards.

    def add_category(self, category):
        raise NotImplementedError

    def modify_category(self, modified_category):
        raise NotImplementedError

    def delete_category(self, category):
        raise NotImplementedError

    def get_or_create_category_with_name(self, name):
        raise NotImplementedError

    def remove_category_if_unused(self, cat):
        raise NotImplementedError

    def add_fact(self, fact):
        raise NotImplementedError

    def update_fact(self, fact):
        raise NotImplementedError
        
    def add_fact_view(self, fact_view):
        raise NotImplementedError

    def update_fact_view(self, fact_view):
        raise NotImplementedError

    def add_card(self, card):
        raise NotImplementedError

    def update_card(self, card):
        raise NotImplementedError
        
    def cards_from_fact(self, fact):
        return NotImplementedError
        
    def delete_fact_and_related_cards(self, fact):
        raise NotImplementedError
        
    # Queries.

    def has_fact_with_data(self, fact_data):
        raise NotImplementedError

    def duplicates_for_fact(self, fact):

        """Returns list of facts which have the same unique key."""

        raise NotImplementedError

    def fact_count(self):
        raise NotImplementedError

    def card_count(self):
        raise NotImplementedError

    def non_memorised_count(self):
        raise NotImplementedError

    def scheduled_count(self):
        raise NotImplementedError

    def active_count(self):
        raise NotImplementedError

    def average_easiness(self):
        raise NotImplementedError

    # Filter is a SQL filter, used e.g. to filter out inactive categories.

    def set_filter(self, filter):
        raise NotImplementedError

    # The following functions should return an iterator, in order to 
    # save memory. sort_key is an attribute of card to be used for sorting.
    # (Note that this is different from the sort key used to sort lists in
    # the Python itself, in order to allow easier interfacing with SQL.)

    def cards_due_for_ret_rep(self, sort_key=""):
        raise NotImplementedError

    def cards_due_for_final_review(self, grade, sort_key=""):
        raise NotImplementedError

    def cards_new_memorising(self, grade, sort_key=""):
        raise NotImplementedError

    def cards_unseen(self, sort_key=""):
        raise NotImplementedError
    
    def cards_learn_ahead(self, sort_key=""):
        raise NotImplementedError

# Local Variables:
# mode: python
# py-indent-offset: 4
# indent-tabs-mode nil
# tab-width 4
# End:
