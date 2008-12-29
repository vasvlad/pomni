#!/usr/bin/python -tt
# vim: sw=4 ts=4 expandtab ai
#
# SM2Gen.py SM2 engine based on generators
#
# Author: Ed Bartosh <bartosh@gmail.com>
#
# Sun Dec 28 09:25:54 UTC 2008

import random
import copy
import itertools

from mnemosyne.libmnemosyne.schedulers.SM2_mnemosyne import SM2Mnemosyne
from mnemosyne.libmnemosyne.component_manager import database, config, log

class CardQueue(object):
    """Card generator. See __call__ method for further explanations."""

    def __init__(self, limit=1, allow_dup=False):
        self.data = {}
        self.groups = []
        self.current_group = None
        self.limit = limit
        self.grade_limits = {}
        self.allow_dup = allow_dup

    def mkgroup(self, name, limit=None, allow_dup=False, randomise=True):
        """Make iterators group."""

        if name not in self.groups:
            self.groups.append(name)
            # data is a list of list of iterators, limit, limits for grades,
            # allow_duplicates flag, cache and randomise flag for cache
            if limit:
                cache = [None] * limit
            else:
                cache = []

            self.data[name] = [[], limit, {}, allow_dup, cache, randomise]

        self.current_group = name

    def add(self, iterable, group=None):
        """Add iterable to group."""

        if group == None:
            group = self.current_group
        self.data[group][0].append(iterable)

    def setlimit(self, limit, group=None, grade=None):
        """Set limits (global, group, global grade, group grade)."""

        if group:
            # Group limits
            if grade == None:
                self.data[group][2] = limit
            else:
                self.data[group][2][grade] = limit
        else:
            # Global limits
            if grade == None:
                self.limit = limit
            else:
                self.grade_limits[grade] = limit


    def __call__(self):
        """ Generate cards from the groups of card iterators.
            Check limits(global, group, grade), randomise group caches if
            needed
        """

        cached_ids = []
        grade_counters = {}
        j = 0 # global card counter
        for group in self.groups:
            iterators, limit, grade_limits, allow_dup, \
                cache, randomise = self.data[group]

            # fill group's cache
            cached_ids_group = []
            grade_counters_group = {}
            
            i = 0
            for iterator in iterators:
                for card in iterator:
                    # check if cache is full
                    if i == len(cache):
                        break

                    # skip duplicates in this group
                    if not allow_dup and card.id in cached_ids_group:
                        continue

                    # skip duplicates globally
                    if not self.allow_dup and card.id in cached_ids:
                        continue

                    # append id to group and global lists
                    cached_ids_group.append(card.id)
                    cached_ids.append(card.id)

                    # put card in cache
                    cache[i] = card
                    i += 1
               
                # No cards found in iterator
                if not cached_ids_group:
                    continue

                cached_ids.extend(cached_ids_group)

                if randomise and cached_ids_group:
                    # shuffle list of group ids
                    random.shuffle(cached_ids_group)
                    # reorganize cache accordingly
                    new_cache = cached_ids_group[:]
                    for card in cache:
                        if not card:
                            break
                        new_cache[cached_ids_group.index(card.id)] = card
                    cache = new_cache

                # yield cards
                i = 0 # group card counter
                for card in cache:
                    if not card:
                        break

                    yield card
                    i += 1
                    j += 1

                    # Check group limit
                    if limit and i == limit:
                        break
    
                    # Check grade limits for the group
                    if card.grade in grade_limits:
                        if card.grade not in grade_counters_group:
                            grade_counters_group[card.grade] = 0
                        
                        grade_counters_group[card.grade] += 1

                        if grade_counters_group[card.grade] >= \
                            grade_limits[card.grade]:
                            break

                    # Check global limit
                    if self.limit and j == self.limit:
                        return

                    # Check global grade limits
                    if card.grade in self.grade_limits:
                        if card.grade not in grade_counters:
                            grade_counters[card.grade] = 0
                        grade_counters[card.grade] += 1
                        if grade_counters[card.grade] >= \
                            self.grade_limits[card.grade]:
                            return


class SM2Gen(SM2Mnemosyne):
    """SM2 scheduler based on generators."""

    def __init__(self):
        SM2Mnemosyne.__init__(self)
        
        self.name = "SM2 generator edition"
        self.description = "SM2 scheduler based on generators"

    def rebuild_queue(self, learn_ahead=False):
        
        self.queue = []
        datab = database()
        if not datab.is_loaded():
            return

        queue = CardQueue(limit=20)
        
        if learn_ahead:
            queue.mkgroup("learn ahead", limit=5)
            queue.add(datab.cards_learn_ahead(sort_key="next_rep"))

        else:
            queue.mkgroup("scheduled", limit=10, allow_dup=None)

            # limit amount of grade0 cards for the current group
            queue.setlimit(limit=config()["grade_0_items_at_once"], group="scheduled",
                    grade=0)

            # add due_for_ret_rep generator
            queue.add(datab.cards_due_for_ret_rep(sort_key="interval"))
                
            # add final review generator, grade0
            queue.add(datab.cards_due_for_final_review(grade=0))

            # add final review generator, grade1
            queue.add(datab.cards_due_for_final_review(grade=1))

            # add new_memorizing generator, grade0
            new_mem = datab.cards_new_memorising(grade=0)
            queue.add(new_mem)

            # FIXME: HOW?
            #queue.add(iter(2*grade_0_selected))
            #queue.add(new_mem)
            #queue.add(new_mem)

            # The same for grade1
            new_mem = datab.cards_new_memorising(grade=1)
            queue.add(new_mem)

            # add cards_unseen generator
            queue.add(datab.cards_unseen(randomise=config()["randomise_new_cards"]))

            # FIXME: HOW???
            #grade_0_in_queue = sum(1 for i in self.queue if i.grade == 0)/2

        self.queue = [card for card in queue()]

# Local Variables:
# mode: python
# py-indent-offset: 4
# indent-tabs-mode nil
# tab-width 4
# End:
