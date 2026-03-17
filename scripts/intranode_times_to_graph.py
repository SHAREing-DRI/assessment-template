#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import argparse as ap
import sys
import os


def intranode_times_crit_80_60(times: list[tuple[int, float]]) -> (float, float):
    """ 
    Calculate the 80% and 60% critical proportions

    :param times: list of (core count, time taken in seconds)
    :return: 80% proportion, 60% proportion
    """
    # Extract core count and times from the list as separate arrays
    times = np.transpose(np.array(times))
    core_counts = times[0]
    parallel_times = times[1]
    serial_time = times[1][0]

    # Calculate efficiency and 80%/60% critical core points
    speed_up = serial_time / parallel_times
    efficiency = speed_up / core_counts

    p_crit_80 = core_counts[(efficiency < 0.8) & (efficiency >= 0.6)][-1]
    p_crit_60 = core_counts[(efficiency < 0.6) & (core_counts > p_crit_80)][0]

    intra_node_prop_80 = p_crit_80 / max(core_counts)
    intra_node_prop_60 = p_crit_60 / max(core_counts)

    return intra_node_prop_80, intra_node_prop_60

def intranode_times_to_graph(times: list[tuple[int, float]]) -> plt.Figure:
    """ 
    Create matplotlib graph

    :param times: list of (core count, time taken in seconds)
    :return: matplotlib figure
    """

    # Extract core count and times from the list as separate arrays
    times = np.transpose(np.array(times))
    core_counts = times[0]
    parallel_times = times[1]
    serial_time = times[1][0]

    # Calculate efficiency and 80%/60% critical core counts
    speed_up = serial_time / parallel_times
    efficiency = speed_up / core_counts
    p_crit_80 = core_counts[(efficiency < 0.8) & (efficiency >= 0.6)][-1]
    p_crit_60 = core_counts[(efficiency < 0.6) & (core_counts > p_crit_80)][0]

    fig, ax = plt.subplots()
    ax.set_xlabel(r'$p$')
    ax.set_ylabel(r'$E(p)$')

    ax.axvline(x=p_crit_80, color="#ffc844", linestyle="--")
    ax.axvline(x=p_crit_60, color="#e35555", linestyle="--")
    ax.plot(core_counts, efficiency, '.-', color="black", linewidth=2)

    return fig

def intranode_times_to_markdown(times: list[tuple[int, float]]) -> str:
    """
    Generate markdown table with 
    """

    times = np.transpose(np.array(times))
    core_counts = times[0]
    parallel_times = times[1]
    serial_time = times[1][0]

    # Calculate efficiency and 80%/60% critical core counts
    speed_up = serial_time / parallel_times
    efficiency = speed_up / core_counts

    header = "| Thread count | Time (s) | Parallel efficiency |\n| --- | ------- | ----- |"
    lines = [header]

    # If we assert that these are equal, we can use one length in the for loop.
    assert(len(core_counts) == len(parallel_times))
    for i in range(len(core_counts)):
        line = f"| {int(core_counts[i]):3d} | {parallel_times[i]:7.03f} | {efficiency[i]:5.03f} |"
        lines.append(line)
    
    return "\n".join(lines)

def parse_args():
    parser = ap.ArgumentParser(
        prog="intranode_times_to_graph.py",
        description="Tools to generate a strong scaling efficiency graph and table from intra-node runtimes. "+_main.__doc__,
        epilog="Unless an output flag is specified, a requested output will be echoed to the standard console output."
    )

    #parser.add_argument("-h", "--help", action="help", help="Show this help message and exit")
    parser.add_argument("--version", action="version", version="%(prog)s 1.1", help="Show program version number and exit")

    parser.add_argument("-g", "--graph", action="store_true", help="Generate graph")
    parser.add_argument("-m", "--markdown", action="store_true", help="Generate markdown table")
    parser.add_argument("-c", "--critical-points", action="store_true", help="Calculate 80 and 60 percent critical values")
    parser.add_argument("-a", "--output-all", action="store_true", help="Output all output types")
    parser.add_argument("-d", "--default", action="store_true", help="Output any requested outputs with unspecified file to their default file.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print extra debug outputs")
    parser.add_argument("-s", "--stdout-graph", action="store_true", help="Output image data to stdout")

    parser.add_argument("-o", "--output", help="Specify an output file. This can only be used if exactly one output type is requested")
    parser.add_argument("--graph-file", help="Specify an output file for the graph. Default: 'images/intranode.png'")
    parser.add_argument("--markdown-file", help="Specify an output file for the markdown table. Default: 'intranode_table.md'")
    parser.add_argument("--critical-points-file", help="Specify an output file for the calculated critical values. Default: 'intranode_critical_proportions.txt'")

    args = parser.parse_args()

    if args.verbose:
        print(f"args: {args}")

    if args.output_all:
        args.graph = True
        args.markdown = True
        args.critical_points = True
    
    if args.default:
        if args.verbose:
            print(f"Setting default files")
        if not args.graph_file:
            args.graph_file = 'images/intranode.png'
        if not args.markdown_file:
            args.markdown_file = 'intranode_table.md'
        if not args.critical_points_file:
            args.critical_points_file = 'intranode_critical_proportions.txt'

    if args.graph + args.markdown + args.critical_points >= 2 and args.output:
        print("ERROR: single specified output file is not valid when multiple outputs are requested at once.")
        exit()
    elif args.output != "stdout":
        if not args.graph_file:
            args.graph_file = args.output
        if not args.markdown_file:
            args.markdown_file = args.output
        if not args.critical_points_file:
            args.critical_points_file = args.output
    
    if args.graph_file == "stdout":
        args.graph_file = None
        args.stdout_graph = True
    if args.markdown_file == "stdout":
        args.markdown_file = None
    if args.critical_points_file == "stdout":
        args.critical_points_file = None

    if not args.graph and not args.markdown and not args.critical_points:
        print("WARNING: No output specified, defaulting to graph only")
        args.graph = True

    return args

def _main():
    '''
    This script may be passed either a markdown table containing thread count, time, and (optional) parallel efficiency,
    or by passing CSV thread count, time.

    It can output a matplotlib graph and a markdown formatted table with all three columns filled in.
    '''

    args = parse_args()

    is_pipe = not os.isatty(sys.stdin.fileno())

    if not is_pipe:
        print(f"Please paste the graph below, ending with an empty line:")

    lines = []

    for line in sys.stdin:
        if line.strip() == '':
            break
        lines.append(line)
        
    if args.verbose:
            print("STATUS: processing input")

    if is_pipe and args.verbose:
        print("Inputted table:")
        print("".join(lines))

    if lines[0][0] == '|':
        lines = lines[2:]
        lines = map(lambda l: list(map(lambda s: s.strip(), l.split('|')))[1:-2], lines)
    else:
        split_commas = lambda l: l.split(',')
        lines = map(split_commas, lines)
    
    lines = list(lines)
    if args.verbose:
        print(f"lines: {lines}")

    strings_to_numbers = lambda l: (int(l[0]), float(l[1]))
    times = list(map(strings_to_numbers, lines))
    if args.verbose:
        print(f"times: {times}")
    
    if args.graph:    
        if args.verbose:
            print("STATUS: generating graph")
        fig = intranode_times_to_graph(times)
        if args.graph_file:
            # Ensure output directory exists
            if '/' in args.graph_file:
                os.makedirs(os.path.dirname(args.graph_file), exist_ok=True)
            # Save figure to file
            fig.savefig(args.graph_file)
        if not args.stdout_graph and not args.graph_file:
            plt.show()
        if args.stdout_graph:
            fig.savefig(sys.stdout)
    
    if args.markdown:
        if args.verbose:
            print("STATUS: generating markdown")
        table = intranode_times_to_markdown(times)
        if args.markdown_file:
            # Ensure output directory exists
            if '/' in args.markdown_file:
                os.makedirs(os.path.dirname(args.markdown_file), exist_ok=True)
            # Write to file
            with open(args.markdown_file, "w") as file:
                file.write(f"{table}")
        else:
            print(f"{table}\0")
    
    if args.critical_points:
        if args.verbose:
            print("STATUS: calculating critical points")
        points = intranode_times_crit_80_60(times)
        if args.critical_points_file:
            # Ensure output directory exists
            if '/' in args.critical_points_file:
                os.makedirs(os.path.dirname(args.critical_points_file), exist_ok=True)
            # Write to file
            with open(args.critical_points_file, "w") as file:
                file.write(f"{points}")
        else:
            print(f"The 80% critical point is {points[0]*100}% of the total core count\n" +
                  f"The 60% critical point is {points[1]*100}% of the total core count\0", file=sys.stdout)

if __name__ == "__main__":
    _main()
