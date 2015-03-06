#!/usr/bin/python
import os
import sys
import argparse

from log import Log
from chat import Trend
from chat import plot_trend as pl
from settings import *


def parse_args():
    """
    Parsing shell command arguments, and override appropriate params
    from setting module

    :return: None
    """
    parser = argparse.ArgumentParser(version=VERSION)
    parser.add_argument('-u', action='store', dest='url')
    parser.add_argument('-f', action='store', dest='url_file')
    parser.add_argument('-t', action='store', dest='target_log_file')
    parser.add_argument('-l', action='store', dest='log_file')
    parser.add_argument('-p', action='store_true', dest='plotting', default=True)
    parser.add_argument('-m', action='store', dest='max_allowed_concurrent', type=int)
    parser.add_argument('-b', action='store', dest='base_concurrent', type=int)
    parser.add_argument('-s', action='store', dest='step_concurrent', type=int)

    result = parser.parse_args()

    if result.url:
        global url
        url = result.url
    if result.url_file:
        global url_file
        url_file = result.url_file
    if result.target_log_file:
        global target_file
        target_file = result.target_log_file
    if result.log_file:
        global log_file
        log_file = result.log_file
    if result.plotting:
        global plotting
        plotting = result.plotting
    if result.max_allowed_concurrent:
        global max_concurrent
        max_concurrent = result.max_allowed_concurrent
    if result.base_concurrent:
        global base_concurrent
        base_concurrent = result.base_concurrent
    if result.step_concurrent:
        global step_concurrent
        step_concurrent = result.step_concurrent



def check_url_source():
    """
    Check out Obtaining url from commend line or urls file.

    :return: A flag that represent the source of urls. String'
    """
    global plotting
    if not url_file and not url:
        plotting = False
        sys.stderr.write('You should figure out the url source.')
    elif url_file and url:
        plotting = False
        sys.stderr.write('Url source come from either url address or url file')
    elif url_file:
        exist = os.path.exists(url_file)
        if exist:
            return 'file'
        else:
            plotting = False
            sys.stderr.write('No such urls file.')
    elif url:
        return 'address'


def test(base_concurrent):
    """
    Main method to do the Testing.
    Looping siege tool until some conditions satisfied,
    and generate a new log file from siege log file.

    :param base_concurrent: number concurrent
    :return: None
    """
    url_source = check_url_source()
    while True:
        for i in range(num_samples):
            if url_source == 'address':
                #os.system('siege -c {concurrent} -t {duration} -l {address}'\
                os.system('siege -c {concurrent} -r {repeat} -l {address}'\
                        .format(address=url,
                                concurrent=base_concurrent,
                                #duration=duration))
                                repeat=repeat))
            elif url_source == 'file':
                #os.system('siege -c {concurrent} -t {duration} -f {url_file} -l'\
                os.system('siege -c {concurrent} -r {repeat} -f {url_file} -l'\
                        .format(url_file=url_file,
                                concurrent=base_concurrent,
                                #duration=duration))
                                repeat=repeat))
            last = Log.get_last_logs(log_file, siege_log_line_length, 1,\
                    base_concurrent)
            Log.add_new_log(target_file, last)

        base_concurrent += step_concurrent

        log = Log(target_file)
        if log.get_last_arrive_rate(num_samples) < (1-fails_allowed) \
                or base_concurrent > max_concurrent:
            break

def plot():
    """
    Plotting chat using the data that analyzed from testing log.

    :return: None
    """
    log = Log(target_file)
    trans_rate_dict = log.get_steps_trans_rate()
    arrive_rate_dict = log.get_steps_arrive_rate()
    resp_time_dict = log.get_steps_resp_time()

    trans_trend = Trend('Transaction Rate',
                        'simulated users',
                        'trans rate (trans/sec)',
                        'g', 1, 'bar',
                        step_concurrent/2)
    trans_trend.get_points(trans_rate_dict)

    arrive_trend = Trend('Arrive Rate',
                         'simulated users',
                         'arrive rate',
                         'g', 2, 'line')
    arrive_trend.get_points(arrive_rate_dict)

    resp_trend = Trend('Resp Time',
                       'simulated users',
                       'time(sec)',
                       'r', 2, 'line')
    resp_trend.get_points(resp_time_dict)

    pl(trans_trend, resp_trend, arrive_trend)

if __name__ == '__main__':
    parse_args()
    test(base_concurrent)
    if plotting:
        plot()
