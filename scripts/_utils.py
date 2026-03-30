import argparse as ap
import os
import sys

def read_data(args, prompt: str) -> [str]:
    lines = []
    is_pipe = not os.isatty(sys.stdin.fileno())

    if not args.file:
        if not is_pipe:
            print(f"{prompt}")

        for line in sys.stdin:
            if line.strip() == '':
                break
            lines.append(line.strip())
    else:
        if is_pipe:
            print("WARNING: receiving piped data and file input requested. Prioritising file input; if you intended to pipe in data, remove the file input flag.")
        with open(args.file, "r") as file:
            lines = list(filter(lambda l: l != '', map(lambda l: l.strip(), file.readlines())))
    
    if args.verbose and (is_pipe or args.file):
        print("Inputted table:")
        if len(lines) > 12:
            print("\n".join(lines[:5]))
            print(f"... Skipped {len(lines) - 7} lines")
            print("\n".join(lines[-2:]))
        else:
            print("\n".join(lines))

    return lines