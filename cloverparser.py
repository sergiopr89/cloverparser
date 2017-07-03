#!/usr/bin/env python

import os
import sys
from bs4 import BeautifulSoup


DEFAULT_PARSER = 'lxml-xml'


def get_clover_from_args():
    """ Validate the system args and retrieves the clover file and minimal cover arguments """
    # Validate input
    if len(sys.argv) != 3:
        script_name = os.path.basename(__file__)
        error_message = 'Usage: {} <clover-report-file> <minimum_cover_percent>'.format(script_name)
        raise Exception(error_message)
    clover_report = sys.argv[1]
    # Validate coverage file
    if not os.path.isfile(clover_report):
        error_message = 'Cannot retrieve the colver file {}'.format(clover_report)
        raise Exception(error_message)
    # Validate minimal coverage
    minimal_coverage = int(sys.argv[2]) 
    if minimal_coverage > 100 or minimal_coverage < 0:
        error_message = 'Minimal coverage {} percent must be in [0,100]'.format(minimal_coverage)
        raise Exception(error_message)
    return clover_report, minimal_coverage


def get_clover_parser(clover_report):
    """ Gets the clover report filename and returns a BS parser """
    with open(clover_report) as raw_file:
        clover_parser = BeautifulSoup(raw_file, DEFAULT_PARSER)
    return clover_parser


def get_percent(dividend, divisor):
    """ Get the percent, if divisor equals to 0, then 0 is returned """
    result = 0
    if int(divisor) != 0:
        result = int(dividend) / int(divisor) * 100
    return str(result)


def get_metrics(clover_parser):
    """ Gets a clover parser and returns a metrics dict """
    metrics = {}
    total_metrics_tag = clover_parser.find_all('metrics')[-1]
    # Methods metrics
    metrics['methods'] = total_metrics_tag['methods']
    metrics['coveredmethods'] = total_metrics_tag['coveredmethods']
    metrics['coveredmethodspercent']  = get_percent(total_metrics_tag['coveredmethods'], total_metrics_tag['methods'])
    # Conditionals metrics
    metrics['conditionals'] = total_metrics_tag['conditionals']
    metrics['coveredconditionals'] = total_metrics_tag['coveredconditionals']
    metrics['coveredconditionalspercent'] = get_percent(total_metrics_tag['coveredconditionals'], total_metrics_tag['conditionals'])
    # Statements metrics
    metrics['statements'] = total_metrics_tag['statements']
    metrics['coveredstatements'] = total_metrics_tag['coveredstatements']
    metrics['coveredstatementspercent'] = get_percent(total_metrics_tag['coveredstatements'], total_metrics_tag['statements'])
    # Elements metrics (Statements + Conditionals + Methods)
    metrics['elements'] = total_metrics_tag['elements']
    metrics['coveredelements'] = total_metrics_tag['coveredelements']
    metrics['coveredelementspercent'] = get_percent(total_metrics_tag['coveredelements'], total_metrics_tag['elements'])
    return metrics


def show_metrics_info(metrics):
    """ Prints to the stdout the coverage info """
    message = 'The code coverage is {}%'.format(metrics['coveredelementspercent'])
    print(message)


def eval_and_exit(metrics, minimal_coverage):
    """ Evaluates the coverage and exits with a status code """
    error_code = 0
    if float(metrics['coveredelementspercent']) < minimal_coverage:
        error_code = 1
    exit(error_code)


def main():
    """ Main program """
    clover_report, minimal_coverage = get_clover_from_args()
    clover_parser = get_clover_parser(clover_report)
    metrics = get_metrics(clover_parser)
    show_metrics_info(metrics)
    eval_and_exit(metrics, minimal_coverage)


if __name__ == '__main__':
    main()
