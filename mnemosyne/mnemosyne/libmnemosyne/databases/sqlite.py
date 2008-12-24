#!/usr/bin/python -tt
# vim: sw=4 ts=4 expandtab ai
#
# sqlite.py 
# Author: Ed Bartosh <bartosh@gmail.com>
#

from datetime import datetime
from sqlite3 import connect, OperationalError

from mnemosyne.libmnemosyne.start_date import StartDate
from mnemosyne.libmnemosyne.utils import expand_path, contract_path
from mnemosyne.libmnemosyne.component_manager import config, log
from mnemosyne.libmnemosyne.database import Database

class Sqlite(Database):

    """ Sqllite backend """

    # Creating, loading and saving the entire database.

    def __init__(self):
        self.connection = None
        self.path = None
        self.start_date = None
        self.load_failed = False
        self.start_date = None

    def new(self, path):
        """ Create new database """
        
        if self.is_loaded():
            self.unload()

        self.start_date=StartDate()
        config()["path"] = path
        log().new_database()

        connection = connect(path)
        
        connection.executescript('''
            create table facts(
                id integer primary key, 
                guid int, 
                facttype_id int, 
                ctime timestamp, 
                mtime timestamp
            );

            create table factdata(
                id integer primary key,
                fact_id int,
                key text,
                value text
            );

            create table facttypes(
                id integer primary key,
                name varchar(20) UNIQUE NOT NULL,
                enabled default TRUE
            );

            create table views(
                id integer primary key,
                facttype_id int,
                name varchar(20) UNIQUE NOT NULL,
                enabled boolean default TRUE
            );

            create table reviewstats(
                id integer primary key,
                fact_id int, 
                view_id int, 
                grade int,
                easiness int, 
                next_rep timestamp
            );

            create table categories(
                id integer primary key, 
                parent_id int default 0, 
                name varchar(20) UNIQUE NOT NULL, 
                enabled boolean default TRUE
            );

            create table fact_categories(
                id integer primary key,
                category_id int,
                fact_id int
            ); 
            
            create table reviews(
                card_id int, 
                time timestamp, 
                number int, 
                prev int, 
                client_guid int
            );

            create table meta(
                id integer primary key, 
                key, 
                value
            );
        ''')

        # save start_date as a string. Object StartDate can't be stored
        connection.execute("insert into meta(key, value) values(?,?)", 
        ('start_date', datetime.strftime(self.start_date.start, 
                                         '%Y-%m-%d %H:%M:%S')))

        self.connection = connection
        self.save()

    def save(self):
        """ Commit changes  """
        if self.connection:
            self.connection.commit()

    def backup(self):
        raise NotImplementedError

    def load(self, fname):
        """ Load database from file """
        
        # Unload opened database if exists
        self.unload()

        path = expand_path(fname, config().basedir)
        try:
            self.connection = connect(path)
            res = self.connection.execute('select value from meta where key=?',
                ('start_date',)).fetchone()
            self.load_failed = False
            self.path = path
            self.set_start_date(StartDate(datetime.strptime(res[0], 
                '%Y-%m-%d %H:%M:%S')))
            self.load_failed = False
            self.path = path
        except OperationalError, exobj:
            self.load_failed = True
 
    def unload(self):
        """ Unload/Close the database """

        self.save()
        if self.connection:
            self.connection.close()
            self.connection = None
            self.load_failed = False

    def is_loaded(self):
        """ Is it alive? """

        return self.connection != None

    # Start date.

    def set_start_date(self, start_date_obj):
        self.start_date = start_date_obj

    def days_since_start(self):
        return self.start_date.days_since_start()

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

    def category_names(self):
        return self.connection.execute("select name from categories")

    def has_fact_with_data(self, fact_data):
        return bool(self.connection.execute('''select count() from factdata
            where key=? and value=?;''', 
            (fact_data['q'], fact_data['a'])).fetchone()[0])

    def duplicates_for_fact(self, fact):

        """Returns list of facts which have the same unique key."""

        raise NotImplementedError

    def fact_count(self):
        raise NotImplementedError

    def card_count(self):
        return self.connection.execute("select count() from reviews").\
            fetchone()[0]

    def non_memorised_count(self):
        return self.connection.execute("""select count() from reviewstats
            where grade < 2""").fetchone()[0]

    def scheduled_count(self, days=0):
        """ Number of cards scheduled within 'days' days."""

        return self.connection.execute("""select count() from reviewstats
            where grade >=2 and ? >= next_rep - ?""", 
            (self.days_since_start(), days)).fetchone()[0]

    def active_count(self):
        """ Return number of cards in an active category """

        return self.connection.execute("""select count() from fact_categories,
                categories where category_id = categories.id and
                categories.enabled=1""").fetchone()[0]

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
