"""
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
  This file is part of the Smart Developer Hub Project:
    http://www.smartdeveloperhub.org

  Center for Open Middleware
        http://www.centeropenmiddleware.com/
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
  Copyright (C) 2015 Center for Open Middleware.
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at 

            http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
"""

__author__ = 'Fernando Serena'

import calendar
from datetime import datetime, date, timedelta
from threading import Thread
from datetime import datetime, timedelta
import pytz
from rdflib import Literal

__calculus = set([])
__dates = set([])
__triggers = {}

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    if n:
        for i in xrange(0, len(l), n):
            yield l[i:i + n]

def add_calculus(func, triggers):
    __calculus.add(func)
    if triggers is not None:
        for trigger in triggers:
            if trigger not in __triggers.keys():
                __triggers[trigger] = set([])
            __triggers[trigger].add(func)

def make_calculus(calculus, t_begin, t_end):
    # pre = datetime.now()
    calculus(t_begin, t_end)
    # print calculus.func_name, t_begin, t_end, (datetime.now() - pre).microseconds

def reset_time_interval():
    return pytz.utc.localize(datetime.utcnow()), pytz.utc.localize(datetime.utcfromtimestamp(0))


def check_triggers(collector, (t, s, p, o), stop_event, app):
    # min_date, max_date = reset_time_interval()

    if collector in __triggers:
        if isinstance(o, Literal):
            obj = o.toPython()
            if isinstance(obj, datetime):
                __dates.add(date(obj.year, obj.month, obj.day))
                if len(__dates) > 100:
                    date_chunks = chunks(list(__dates), 10)
                    for chunk in date_chunks:
                        threads = []
                        for d in chunk:
                            thread = Thread(target=calculate_metrics, args=(d, d, stop_event, app, __triggers[collector]))
                            threads.append(thread)
                            thread.start()
                        [t.join() for t in threads]
                    __dates.clear()


def calculate_metrics(first_date, max_date, stop_event, app, calcs):
    app.store.execute_pending()

    next_date = date(first_date.year, first_date.month, first_date.day)
    max_date = date(max_date.year, max_date.month, max_date.day) + timedelta(days=1)
    print 'Making calculus for [{}, {}]...'.format(next_date, max_date),
    pre = datetime.now()
    while next_date <= max_date:
        t_begin = calendar.timegm(next_date.timetuple())
        end_date = datetime(next_date.year, next_date.month, next_date.day)
        end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)
        t_end = calendar.timegm(end_date.timetuple())

        # Run all registered calculus
        for c in calcs:
            make_calculus(c, t_begin, t_end)

        next_date = next_date + timedelta(days=1)
        if stop_event.isSet():
            return
    print 'it took {}ms'.format((datetime.now() - pre).microseconds / float(1000))
    # app.store.execute_pending()
