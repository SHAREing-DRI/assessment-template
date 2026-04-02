---
License: Durham University, All rights reserved.
Creator: Andrew Naden
Contributors: Andrew Naden; Ananya Gangopadhyay
Summary: For assessors working on SHAREing and ARC-Durham.
---

# Pre-assessment template

> [!NOTE]
>
> 1. Guidance is throughout this template is provided using information boxes, along with example text and placeholders. Please remove the information boxes and replace the example text in your report.
>
> 2. The template is based on Section 3 of the [performance assessment guidebook](https://shareing-dri.github.io/performance-assessment/guidebook). However, the guidebook should not be necessary to perform the pre-assessment using this template.
>
> 3. This template is not exhaustive, but should provide the framework for completing a pre-assessment using the information submitted via the [assessment submission form](https://forms.office.com/Pages/ResponsePage.aspx?id=i9hQcmhLKUW-RNWaLYpvlIUXnqx3D81Bt-KemxGOyY5UOU9RQkFSOE5UU1Y1QVZNS0QyNlFYNjRNOS4u), by the submitter.

## Assessment objective

>[!IMPORTANT]
> Is this a test submission, internal review or external review? If part of a larger project or funding add that information here. You may also include the assessor's name, optionally with contact details.

A test submission of `<benchmark_name>`, available at `<repository/website>`. Version tested `<version_number>` performed by `<assessor_name>` of `<assessor_affiliation>` on `<assessment_date>`.

## Disclaimers

1. This is not a commentary on code quality, but an indicator of the quality of the current SHAREing testing methodology as of `<guidance_date>`.
2. This forms only a preliminary assessment of submission suitability and does not guarantee a full assessment. The pre-assessment will be provided to the submitter with information on how to continue to assessment or rejection.

## Table of contents

>[!TIP]
> Place `x` inside the box when complete to mark the checkbox

- [ ] [1: Benchmark setup](#1-benchmark-setup)
- [ ] [2: Description of working environment](#2-description-of-working-environment)
- [ ] [3: Compiler setup and optimisations](#3-compiler-setup-and-optimisations)
- [ ] [4: Computational complexity and scaling](#4-computational-complexity-and-scaling)
- [ ] [5: Memory, storage and I/O](#5-memory-storage-and-io)
- [ ] [6: Additional comments from submitter](#6-additional-comments-from-submitter)
- [ ] [7: Pre-assessment outcome](#7-pre-assessment-outcome)

## 1: Benchmark setup

>[!IMPORTANT]
> This section should be composed of information provided by the submitter, unless there is a specific issue with compatibility on the machine the assessor is testing on, in which case additional information should be noted. The [third subsection](#problem-size-scaling) should comment on the suitability of the benchmark in terms of expected capacity for weak/strong scaling testing.

### Fetch and build program

>[!IMPORTANT]
> Provide commands to fetch and build program. Include version numbers where possible for the main program.

The submitter has requested an assessment of `<repository/program_name>`, version `<version_number`>/branch `<branch_name>`. It can be fetched/installed as follows:

```bash
# Example 1: Install specific version with a package manager
spack install <program_name>@<version_number>

# Example 2: Clone a specific branch of a repository
git clone -p <branch_name> <repository> && make release
   
```

>[!IMPORTANT]
> Provide commands to fetch benchmark, unless provided directly by submitter, in which case attach with this document.

### Fetch and run benchmark

The benchmark can be obtained from:

```bash
git clone <benchmark_repository>
```

>[!IMPORTANT]
> Provide instructions on how to run the benchmark and the expected output. This output should be minimal in order to test the performance of the working performance of the program rather than I/O saturation.

To run the benchmark:

```bash
cd <benchmark_folder>
mpirun -np 24 <program_executable> <benchmark_name> <output_file>
```

### Problem size scaling

>[!IMPORTANT]
> Provide commentary on possibility of scaling the problem up and down, both in strong (changing number of work units (e.g. CPUs) but keeping constant problem size) and weak (changing problem size but keeping number of work units the same) contexts. If there is existing scaling information (graphs or raw data) available attach the data to this report and add links here.

## 2: Description of working environment

### Hardware information

>[!IMPORTANT]
> For systems with different hardware resources, add the hardware information used, including where applicable the queue information if necessary. Comment on expected normal limit for the hardware, e.g. size of the largest interconnected set of nodes, or memory limitations.

The `<cluster_name>` system based at `<university/organisation>` was used for this assessment.

>[!IMPORTANT]
> Provide processor, memory and cache information as well as interconnect information if (e.g. Infiniband, NVlink - if across multiple nodes) of the system the assessment is to be performed on.
The hardware details for `<cluster_name>` are `[available at](<URL>)`. This information is corroborated by running `cat /proc/cpuinfo` on one of the compute nodes via an interactive session.

There are `<num_nodes>` compute nodes on the system:

| Specification       | per node                                                              |
| ------------------- | --------------------------------------------------------------------- |
| Processors          | `<num_procs>` $\times$ `[<processor_name>](<link-to-online-details>)` |
| Clock speed per CPU | `<freq>`MHz                                                           |
| Sockets             | `<num_sockets>`                                                       |
| Cores               | `<num_cores>`                                                         |
| RAM                 | `<memory_size>`GB `<memory_type>`                                     |
| Local storage       | `<storage_size>`GB `<storage_type>`                                   |

>[!TIP]
> Add details that you can obtain from the system or online information about sockets, NUMA regions, interconnects and cache sizes.

### Libraries and modules

>[!IMPORTANT]
> Provide information on the libraries that need to be installed or modules that must be loaded based on the compilation information provided by the submitter.

### Assessment tools

> [!IMPORTANT]
> Limit pre-assessment tools to very low runtime, mostly just focus on whether the program is running as expected. Do not check for correctness of benchmarks as that is domain specific knowledge.

1. Pre-assessment:
   - `<tool_1>`
   - `<tool_2>`

> [!IMPORTANT]
> High level assessment tools and techniques which are expected to be useful, like global measures such as wall time.

<!-- markdownlint-disable MD029 -->
2. High-level assessment:
   - `<tool_1>`
   - `<tool_2>`

>[!IMPORTANT]
> If additional information is provided you can address low level assessment (will likely require privileges on host). Only address this section if confident enough domain information has been provided with respect to scaling in compute and memory with problem size.

3. Low-level assessment:
   - `<tool_1>`
   - `<tool_2>`

<!-- markdownlint-enable MD029 -->

## 3: Compiler setup and optimisations

>[!IMPORTANT]
> Based on the compilation information provided by submitter, comment on the following (where applicable):
>
> - package manager (e.g. `spack`)
> - build toolchain (e.g. `cmake`)
> - main compiler version (e.g. GCC 11)
> - compiler optimisations (e.g. -O3, `--fast-math`)
> - additional accelerator libraries and versions (e.g. SYCL revision 11, Kokkos 5.1)
> - any feature sets which are toggled on (e.g. vectorisation)
>
> Add additional information about the impact of optimisations on convergence or correctness of results if provided by submitter. Also include any issues you may face when building the program.

Build instructions from the user `<build_toolchain>` to build the `<program_name>` with `<optimisation_level>`.

>[!tip]
> MAQAO should present missed compiler optimisation opportunities. Increasing the optimisation level may require re-converging the system to confirm accuracy. This may be outside the scope of the assessment.

## 4: Computational complexity and scaling

>[!IMPORTANT]
> Add information about scaling provided by submitter:
>
> - scaling of work required as problem size increases
> - scaling of memory required as problem size increases
> - scaling of time required as problem size increases
> - scaling of work required as work units increases
> - scaling of memory required as work units increases
> - scaling of time required as work units increases

The `<parameter>` value can be varied to increase the problem size for scaling tests.

## 5: Memory, storage and I/O

>[!IMPORTANT]
> Comment on the expected in memory size of the program at runtime, including data. An estimate of this information should be provided as part of the submission. For jobs submitted to Hamilton as part of early assessment, the Hamilton dashboard can be used to gauge memory usage, see [Hamilton Portal Performance](https://www.durham.ac.uk/research/institutes-and-centres/advanced-research-computing/hamilton-supercomputer/usage/portal/performance/).

According to the submitter, the expected memory required for the benchmark is `<memory_size>`GB.

>[!IMPORTANT]
> Comment on the expected storage requirements of the program, are there large amounts of temporary files (either in quantity or in total size)? An estimate of this information should be provided as part of the submission. A program that produces a large amount of temporary checkpoint files should have checkpoints turned off where possible.

The benchmark also outputs files totalling `<storage_size>`MB.

>[!IMPORTANT]
> Comment on amount of I/O benchmark produces, excessive I/O will result in an inaccurate performance assessment and may result in rejection. Comment on when the I/O is performed.

The benchmark writes to a file after every `<n>` iterations.

## 6: Additional comments from submitter

>[!IMPORTANT]
> Include any additional information from the submitter that does not fit the previous sections.

## 7: Pre-assessment outcome

>[!IMPORTANT]
> Indicate whether the assessment will proceed to the high-level stage. If the assessment is rejected here, comment on why and how to proceed.
