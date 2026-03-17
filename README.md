# <img src='./images/logo.svg' width=90 style="vertical-align:middle" /> SHAREing: High-level performance assessment notebook

**This repository is in a very early stage of development**

This repository is part of the [SHAREing](https://shareing-dri.github.io/) project and is focused on conducting high-level performance assessments of research software.
We use a markdown document and set of associated scripts to generate graphs during the high-level assessment.

## Setup



Very few Python dependencies are required and can be installed locally, or in a virtual
environment, by running the command 
```bash
pip install -r requirements.txt
```
Otherwise, the notebook relies on just a few scripts located in the `scripts` directory.

## Structure of high-level performance assessment

Performance is broken down into 5 main topics
1. Core
2. Intra-node
3. Inter-node
4. GPU
5. I/O

Further details of how to conduct each performance measurement are given in the notebook.
Below we list the usage of each script for the high-level assessment.

### `intranode_times_to_graph.py`

Intra-node performance analysis is located in the `intranode_times_to_graph.py` script.

When called as a script, it takes data input from the standard input or a unix pipe.
For demonstration purposes, suppose we have the data
```csv
1, 29.995
2, 18.23
4, 10.74
8, 10.33
16, 9.1307
32, 8.5401
64, 7.4589
```
in a csv file `times.csv`, where the first column is core count and the second is time in seconds.
If we want to check the graph looks reasonable, we can run wih
```
$ ./scripts/intranode_times_to_graph.py --graph
Please paste the graph below, ending with an empty line:
```
and paste the data below.
Now we've checked the graph, we want a markdown table to copy-paste to the report and a graph image output to the default directory.
```
$ cat times.csv | ./scripts/intranode_times_to_graph.py -gmd --markdown-file=stdout
```

There are a variety of other usage flags, details of which can be found with
```shell
$ ./scripts/intranode_times_to_graph.py --help
```

Internally, this script contains three useful functions which could be used from other code:
1. `intranode_times_crit_80_60(times: list[tuple[int, float]]) -> (float, float)` - this calculates the 80% and 60% efficiency points and returns them as a tuple
2. `intranode_times_to_graph(times: list[tuple[int, float]]) -> plt.Figure`
3. `intranode_times_to_markdown(times: list[tuple[int, float]]) -> str` - this renders the core counts and times as a three-column markdown table with core count, time, and parallel efficiency

Each function is passed the times as a list of tuples of core count and time taken.

### `internode_times_to_graph.py`

This script is `TODO`

### `summary.py`

This script is `TODO`

## Contributions

This performance assessment is intentionally limited as we want to simply
capture the performance of software at a *high level*. However, if you have
ideas of performance metrics which are necessary but missing, or if you find
any faults with the notebook, please raise an issue.

## Acknowledgements
The initial development of this notebook was implemented by Ben Clark.  This
project has received funding through the UKRI Digital Research Infrastructure
Programme under grant UKRI1801 (SHAREing). 

<img src='./images/ukri.png' width=200 style="vertical-align:middle" /> 
