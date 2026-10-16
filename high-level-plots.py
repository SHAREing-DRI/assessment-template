#!/usr/bin/env python

import argparse as ap
import os
import assessmenttemplate.scaling as scaling
import assessmenttemplate.summary as summary


def _main():
    """
    Processes commandline arguments and the input table containing intranode/internode runtimes per
    core/thread/node counts, or high-level metrics per rubric. Input can be either a Markdown table or a CSV.

    Produces the relevant graph (line, point or spiderweb plot) and a Markdown formatted version of the input
    table with further processed data added (like parallel efficiency) if applicable.
    """
    parser = ap.ArgumentParser(
        prog=os.path.basename(__file__),
        description="Tools to generate plots for the high-level assessment.",
        epilog=_main.__doc__ + "Unless an output flag is specified, a requested output will be echoed to the "
                               "standard console output."
    )

    # Source - https://stackoverflow.com/a/75100875
    # Posted by sinoroc, modified by community. See post 'Timeline' for change history
    # Retrieved 2026-09-07, License - CC BY-SA 4.0

    import importlib.metadata
    version = importlib.metadata.version('assessmenttemplate')

    parser.add_argument("--version",
                        action="version",
                        version=f"%(prog)s {version}",
                        help="Show program version number and exit.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print extra debug outputs.")
    parser.add_argument("-d", "--default", action="store_true",
                        help="Output any requested outputs with unspecified file to their default file.")
    parser.add_argument("--svg", action="store_true",
                        help="Output graph to default file will output SVG rather than PNG.")
    parser.add_argument("-i", "--input",
                        default=None,
                        required=False,
                        help="Specify an optional input file containing the table for the metric."
                             "requested. Will use stdin if none specified.")
    parser.add_argument("-o", "--output",
                        help="Specify an output file. This can only be used if exactly one output type is requested.")
    parser.add_argument("-s", "--stdout-graph", action="store_true",
                        help="Output image data to stdout (useful for piping)")
    parser.add_argument("--show", action="store_true",
                        help="Show graph in window at runtime.")

    sub_parsers = parser.add_subparsers(dest="mode", required=True, help="Mode pertaining to the high-level rubric for "
                                                                         "which the plots are to be generated.")
    # Add plots per rubric/mode
    scaling.scaling_add_args(sub_parsers)
    scaling.scaling_add_args(sub_parsers, scaling_rubric="internode")
    summary.summary_add_args(sub_parsers)

    args = parser.parse_args()

    if args.mode == "summary":
        summary.summary_main(args)
    else:
        scaling.scaling_main(args)


if __name__ == "__main__":
    _main()
