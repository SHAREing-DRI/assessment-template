#!/usr/bin/env python3

import argparse as ap
import numpy as np
import re
import io
import pandas

import _utils


def process_nvidia_csv(args, data):
    dataframe = pandas.read_csv(io.StringIO(data))
    
    if args.verbose:
        print(dataframe)
    
    num_kernels = max(dataframe["ID"]) + 1
    metrics = dataframe["Metric Name"].unique()

    if args.verbose:
        print(f"{num_kernels} kernels by metrics: {metrics}")


    nice_frame = {metric: [None for _ in range(num_kernels)] for metric in metrics}
    nice_frame["kernel_name"] = [None for _ in range(num_kernels)]

    kernel_name_regex = re.compile("^(void )?(.*?)\\(")

    for i in dataframe.index:
        kernel_index = dataframe["ID"][i]
        if i % len(metrics) == 0:
            nice_frame["kernel_name"][kernel_index] = kernel_name_regex.match(dataframe["Kernel Name"][i])[2]
        nice_frame[dataframe["Metric Name"][i]][kernel_index] = dataframe["Metric Value"][i]
    
    nice_frame = pandas.DataFrame(nice_frame)
    
    metric_name_regex = re.compile(r"(.*)__(sass_thread_inst_executed_)?([^\.\n]*?)(_pred_on)?\.([^\.\n]*)(\.(.*))?")
    match = lambda metric: metric_name_regex.match(metric)
    nice_metric_name = lambda metric: match(metric)[1] + "/" + match(metric)[3] + "/" + match(metric)[5] + (("/" + match(metric)[7]) if match(metric)[6] else "")
    rename_dict = { metric: nice_metric_name(metric) for metric in metrics }
    
    if args.verbose:
        print(f"Renaming columns by {rename_dict}")
    nice_frame = nice_frame.rename(rename_dict, axis=1)
    
    if args.output:
        nice_frame.to_csv(args.output)
    
    return nice_frame

def parse_args():
    parser = ap.ArgumentParser(
        prog="summary.py",
        description="Tools to process GPU metrics. "+_main.__doc__,
    )

    #parser.add_argument("-h", "--help", action="help", help="Show this help message and exit")
    parser.add_argument("--version", action="version", version="%(prog)s dev", help="Show program version number and exit")
    parser.add_argument("-f", "--file", help="Input file")
    parser.add_argument("-e", "--echo-input", help="Echo input data to a file")

    parser.add_argument("-v", "--verbose", action="store_true", help="Print extra debug outputs")
    parser.add_argument("-o", "--output", help="Specify an output file to output a reformatted CSV to")

    parser.add_argument("-t", "--program-time", type=float, help="Specify the total program execution time to calculate inferred average FLOPS/s")
    parser.add_argument("--gpu-max-tflops", type=float, help="Specify the maximum TFLOPS/s of the GPU to calculate peak performance percentage")

    vendor_group = parser.add_argument_group("CSV Input Format")
    vendor_group = vendor_group.add_mutually_exclusive_group(required=True)
    vendor_group.add_argument("-n", "--nvidia", action="store_true", help="CSV from nsight-compute")
    vendor_group.add_argument("-a", "--amd", action="store_true", help="CSV from rocprofiler")
    vendor_group.add_argument("-i", "--intel", action="store_true", help="CSV from intel vtune")
    vendor_group.add_argument("-c", "--nice-csv", action="store_true", help="CSV from this script")

    args = parser.parse_args()

    if args.verbose:
        print(f"args: {args}")
    
    return args

def _main():
    '''
    This script may be given a CSV file output by NSight Compute, ROCProfiler, or Intel VTune, or alternatively in the normalised format output by this script.

    It can then calculate the FLOPS/s over the runtime of a program.
    '''

    args = parse_args()

    lines = _utils.read_data(args, prompt="Please paste the data below, ending with an empty line:")
    if args.echo_input:
        with open(args.echo_input, "w") as echo_file:
            echo_file.write("\n".join(lines))

    if args.nvidia:
        dataframe = process_nvidia_csv(args, "\n".join(filter(lambda l: not l.startswith('='), lines)))
    elif args.amd:
        print("AMD data processing is not implemented yet.")
        exit(1)
    elif args.intel:
        print("Intel data processing is not implemented yet.")
        exit(1)
    elif args.nice_csv:
        dataframe = pandas.read_csv(io.StringIO("\n".join(lines)), index_col=0)
    
    if args.verbose:
        print(dataframe)
    
    # Fused multiply-add instructions count as 2 floating point operations in one
    dataframe["sm/op_ffma/sum"] *= 2
    dataframe["sm/op_dfma/sum"] *= 2
    
    # If we double the double-precision op counts we can sum them all as equal
    dataframe["sm/op_dadd/sum"] *= 2
    dataframe["sm/op_dmul/sum"] *= 2
    dataframe["sm/op_dfma/sum"] *= 2

    # dataframe["sm/op_dadd/sum"] *= dataframe["cycles_elapsed"]
    # dataframe["sm/op_dmul/sum"] *= dataframe["cycles_elapsed"]
    # dataframe["sm/op_dfma/sum"] *= dataframe["cycles_elapsed"]
    # dataframe["sm/op_fadd/sum"] *= dataframe["cycles_elapsed"]
    # dataframe["sm/op_fmul/sum"] *= dataframe["cycles_elapsed"]
    # dataframe["sm/op_ffma/sum"] *= dataframe["cycles_elapsed"]

    flops = (sum(sum(dataframe[op]) for op in ("sm/op_fadd/sum", "sm/op_fmul/sum", "sm/op_ffma/sum", "sm/op_dadd/sum", "sm/op_dmul/sum", "sm/op_dfma/sum"))) #("op_dadd", "op_dmul", "op_dfma")))
    print(f"Total number of floating point operations executed (inferred): {flops}")

    if "gpu/time_duration/sum" in dataframe.columns:
        print(f"WARNING: take these during GPU execution metrics with a grain of salt, as the gpu time duration measured by nsight compute includes some profiling overhead.")
        print(f"Total GPU time elapsed: {sum(dataframe["gpu/time_duration/sum"]) * 1e-9}s")
        flops_broadcast_per_second = (sum(sum(dataframe[op] / (dataframe["gpu/time_duration/sum"] * 1e-9)) for op in ("sm/op_fadd/sum", "sm/op_fmul/sum", "sm/op_ffma/sum", "sm/op_dadd/sum", "sm/op_dmul/sum", "sm/op_dfma/sum"))) #("op_dadd", "op_dmul", "op_dfma")))
        print(f"Final average FLOPS/s during GPU execution: {flops_broadcast_per_second * 1e-12 / dataframe.shape[0]} TFLOPS/s")
        print(f"Final average FLOPS/s during GPU execution: {flops * 1e-12 / sum(dataframe["gpu/time_duration/sum"] * 1e-9)} TFLOPS/s")
        print(f"END WARNING")
    
    if args.program_time:
        print(f"Final average overall FLOPS/s based on an execution time of {args.program_time}s: {flops * 1e-12 / args.program_time} TFLOPS/s")
        if args.gpu_max_tflops:
            print(f"Final peak performance percentage based on a maximum of {args.gpu_max_tflops} TFLOPS/s: {flops * 1e-12 / args.program_time / args.gpu_max_tflops * 100:.2f}%")

if __name__ == '__main__': 
    _main()
