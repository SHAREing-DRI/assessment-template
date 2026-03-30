#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import argparse as ap
import sys
import os

import _utils

from enum import StrEnum, auto

DEFAULT_FILE = "images/summary.png"

class Rubric(StrEnum):
    CPU   = auto()
    GPU   = auto()
    IO    = auto()
    INTRA = auto()
    INTER = auto()
    UNKNOWN = auto()

    def from_string(from_str: str):
        match from_str.lower():
            case s if s.startswith(Rubric.CPU):
                return Rubric.CPU
            case s if s.startswith(Rubric.GPU):
                return Rubric.GPU
            case s if s.startswith(Rubric.IO):
                return Rubric.IO
            case s if s.startswith(Rubric.INTRA):
                return Rubric.INTRA
            case s if s.startswith(Rubric.INTER):
                return Rubric.INTER
            case _:
                return Rubric.UNKNOWN


def summary_to_spiderweb(rubrics: list[tuple[str, float]]) -> plt.Figure:
    """ 
    Create matplotlib spiderweb diagram

    :param rubrics: list of (rubric, 0-to-1-normalised score)
    :return: matplotlib figure
    """
    
    rubrics = np.array(rubrics).transpose()
    scores = rubrics[1].astype(float)
    names = rubrics[0]

    nvars = len(scores)
    angles = np.linspace(0, 2 * np.pi, nvars, endpoint=False).tolist()
    scores = np.append(scores, scores[0])
    angles = np.append(angles, angles[0])

    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    ax.fill(angles, scores, color='lightseagreen', alpha=0.4)  # Fill area
    ax.plot(angles, scores, color='teal', linewidth=2)  # Outline

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(names)
    
    ax.set_title("Rubric Scores", fontsize=14)

    return fig

def summary_to_bar_chart(rubrics: list[tuple[int, float]]) -> plt.Figure:
    """ 
    Create matplotlib bar chart

    :param rubrics: list of (core count, time taken in seconds)
    :return: matplotlib figure
    """
    rubrics = np.array(rubrics).transpose()
    scores = rubrics[1].astype(float)
    names = rubrics[0]

    fig, ax = plt.subplots()

    ax.bar(names, scores)
    ax.set_ylim([0., 1.])
    
    # Rotate labels so they don't overlap
    fig.autofmt_xdate()

    return fig

def parse_args():
    parser = ap.ArgumentParser(
        prog="summary.py",
        description="Tools to generate a spiderweb diagram or bar graph for the SHAREing high-level performance assessment. "+_main.__doc__,
    )

    #parser.add_argument("-h", "--help", action="help", help="Show this help message and exit")
    parser.add_argument("--version", action="version", version="%(prog)s 1.0", help="Show program version number and exit")
    
    parser.add_argument("-f", "--file", help="Input file")

    parser.add_argument("-b", "--bar", action="store_true", help="Output a bar chart instead of a spiderweb")
    parser.add_argument("-d", "--default", action="store_true", help=f"Output to the default file, '{DEFAULT_FILE}'")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print extra debug outputs")
    parser.add_argument("-s", "--stdout-graph", action="store_true", help="Output image data to stdout (useful for piping)")
    parser.add_argument("--svg", action="store_true", help="Output graph as SVG to default file rather than PNG")

    parser.add_argument("-o", "--output", help="Specify an output file")

    args = parser.parse_args()

    if args.verbose:
        print(f"args: {args}")
    
    if args.default and not args.output:
        if args.verbose:
            print(f"STATUS: Setting output to default filepath '{DEFAULT_FILE}'")
        if args.svg:
            args.output = DEFAULT_FILE[:-3] + "svg"
        else:
            args.output = DEFAULT_FILE
    elif args.default and args.output:
        print("WARNING: Specifying output file overrides request to output to default file.")

    if args.svg and not args.default:
        print("WARNING: svg flag only has an effect when outputting to the default file. Matplotlib will output to svg if you specify a filename with file ending '.svg'")

    return args

def _main():
    '''
    This script may be passed either a markdown table containing thread count, time, and (optional) parallel efficiency,
    or by passing CSV thread count, time.

    It can output a matplotlib graph and a markdown formatted table with all three columns filled in.
    '''

    args = parse_args()

    lines = _utils.read_data(args, prompt="Please paste the data below, ending with an empty line:")    
        
    ####################
    # INPUT PROCESSING #
    ####################

    if args.verbose:
        print("STATUS: processing input")

    if args.verbose:
        print(f"lines: {lines}")
    if lines[0][0] == '|':
        if args.verbose:
            print("Assuming Markdown table input, discarding two header rows")
        lines = lines[2:]
        lines = map(lambda l: list(map(lambda s: s.strip(), l.split('|')))[1:-2], lines)
    else:
        if args.verbose:
            print("Assuming CSV input")
        split_commas = lambda l: l.split(',')
        lines = map(split_commas, lines)

    lines = list(lines)
    if args.verbose:
        print(f"lines (after converting to list): {lines}")

    strings_to_numbers = lambda l: (l[0], float(l[1]))
    times = list(map(strings_to_numbers, lines))
    if args.verbose:
        print(f"times: {times}")

    #####################
    # OUTPUT GENERATION #
    #####################

    if args.verbose:
        print("STATUS: generating graph")
    fig = None
    if args.bar:
        fig = summary_to_bar_chart(times)
    else:
        fig = summary_to_spiderweb(times)
    if args.output:
        # Ensure output directory exists
        if '/' in args.output:
            os.makedirs(os.path.dirname(args.output), exist_ok=True)
        # Save figure to file
        fig.savefig(args.output)
    if args.stdout_graph:
        fig.savefig(sys.stdout)
    if not args.stdout_graph and not args.output: # Only view in window if we haven't already output somewhere else
        plt.show()
    
if __name__ == "__main__":
    _main()
