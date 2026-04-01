# TEMPLATE FOR PREASSESSMENT OF PROGRAMS

AS PART OF SHAREing. FOR ASSESSORS WORKING ON SHAREing AND ARC-Durham.

The section headings are numbered to correspond to the performance analysis workbook section 3 (i.e. Section 1 in the workbook is Section 1 in this template), but the workbook should not be necessary to perform a pre-assessment using this template. This template is not exhaustive, but should provide the framework for completing a pre-assessment using the information submitted via the pre-assessment submission form, [linked here](https://forms.office.com/Pages/ResponsePage.aspx?id=i9hQcmhLKUW-RNWaLYpvlIUXnqx3D81Bt-KemxGOyY5UOU9RQkFSOE5UU1Y1QVZNS0QyNlFYNjRNOS4u), by the submitter of the project for assessment.

ALL RIGHTS RESERVED.
Andrew Naden, The University of Durham.

## Objective of pre-assessment

Test submission/internal review/external review
If part of a larger project or funding add that information here.
Add assessor's name, optionally contact details.

e.g.
A test submission of **\<benchmark name\>**, available at **\<repository/website\>** version tested **\<version number\>** performed by **\<assessor name\>** of **\<assessor affiliation\>** on **\<date\>**.

## Disclaimer for testing

This is not a commentary on code quality, but an indicator of the quality of the current SHAREing testing methodology as of this date, **\<date\>**.

## Disclaimer for assessment

This forms only a preliminary assessment of submission suitability and does not guarantee a full assessment. The pre-assessment will be provided to the submitter with information on how to continue to assessment or rejection.

## Completed (place an x inside the box when complete)

- [ ] 1: Benchmark setup
- [ ] 2: Description of working environment
- [ ] 3: Compiler setup
- [ ] 4: Code complexity
- [ ] 5: I/O
- [ ] 6: Hardware information
- [ ] 7: Code Separation
- [ ] 8: Historic optimisations

## 1: Benchmark setup

This section should be composed of information provided by the submitter, unless there is a specific issue with compatibility on the machine the assessor is testing on, in which case additional information should be noted. The 4th subsection (1.4) should comment on the suitability of the benchmark in terms of expected capacity for weak/strong scaling testing.

1. Provide commands to fetch and build program, e.g.

    ```bash
    spack install <program name>@<version number>
    
    or 
    
    git clone <repository> && make release
    
    ```

    a. Include version numbers where possible for the main program.

2. Provide commands to fetch benchmark, unless provided directly by submitter, in which case attach with this document.

    ```bash
    git clone <benchmark repository>
    ```

3. Provide instructions on how to run the benchmark and the expected output.
    a. this output should be minimal in order to test the performance of the working performance of the program rather than I/O saturation.

    For example.

    ```bash
    cd <benchmark folder>
    mpirun -np 24 <program executable> <benchmark name> data.out
    
    ```

4. Provide commentary on possibility of scaling the problem up and down, both in strong (changing number of work units (e.g. CPUs) but keeping constant problem size) and weak (changing problem size but keeping number of work units the same) contexts.

5. If there is existing scaling information (graphs or raw data) available attach the data to this report and add links here.

## 2: Description of working environment

### 1. Name of the computer/cluster

- a. For systems with different hardware resources, add the hardware information used, including where applicable the queue information if necessary.
- b. Comment on expected normal limit for the hardware, e.g. size of the largest interconnected set of nodes, or memory limitations.

### 2. List Assessment tools used in pre-assessment and expected to be used in high level assessment

- a. Limit pre-assessment tools to very low runtime, mostly just focus on whether the program is running as expected. Do not check for correctness of benchmarks as that is domain specific knowledge.

- b. High level assessment techniques which are expected to be useful
  - i. Global measures, such as wall time.
- c. If additional information is provided you can address low level assessment (will likely require privileges on host)
  - i. Only address this section if confident enough domain information has been provided with respect to scaling in compute and memory with problem size.

## 3: Compiler Setup

Predominantly provided by submitter, include all which apply:

- a. package manager (e.g. `spack`)
- b. build toolchain (e.g. `cmake`)
- c. main compiler version (e.g. GCC 11)
- d. compiler optimisations (e.g. -O3, `--fast-math`)
- e. additional accelerator libraries and versions (e.g. SYCL revision 11, Kokkos 5.1)
- f. any feature sets which are toggled on (e.g. vectorisation)

Add additional information about convergence or correctness if provided by submitter.

MAQAO should present missed compiler optimisation opportunities.

Increasing optimisation level may require the system to be reconverged to confirm accuracy. This may be outside the scope of the assessment.

## 4: Code Complexity

Add information about scaling provided by submitter:

- a. scaling of work required as problem size increases
- b. scaling of memory required as problem size increases
- c. scaling of time required as problem size increases
- d. scaling of work required as work units increases
- e. scaling of memory required as work units increases
- f. scaling of time required as work units increases

## 5: Memory, Storage and I/O

Comment on the expected in memory size of the program at runtime, including data. An estimate of this information should be provided as part of the submission. For jobs submitted to Hamilton as part of early assessment, the Hamilton dashboard can be used to gauge memory usage, see [Hamilton Portal Performance](https://www.durham.ac.uk/research/institutes-and-centres/advanced-research-computing/hamilton-supercomputer/usage/portal/performance/).
Comment on the expected storage requirements of the program, are there large amounts of temporary files (either in quantity or in total size)? An estimate of this information should be provided as part of the submission. A program that produces a large amount of temporary checkpoint files should have checkpoints turned off where possible.
Comment on amount of I/O benchmark produces, excessive I/O will result in an inaccurate performance assessment and may result in rejection.
Comment on when the I/O is performed.

## 6: Hardware information

Provide processor, memory and cache information as well as interconnect information if (e.g. Infiniband, NVlink - if across multiple nodes) of the system the assessment is to be performed on.

e.g.
AMD EPYC 7702 64-Core Processor on 1 node - Hamilton.

```txt
processor       : 0-63
model name      : AMD EPYC 7702 64-Core Processor
microcode       : 0x830107d
cpu MHz         : 1996.204
cache size      : 512 KB

MemTotal:       263152912 kB   //~250GB per node
MemFree:        256995420 kB
MemAvailable:   258291956 kB
```

## 7: Code separation

Only if sufficient additional information about code layout is provided by submitter.

## 8: Historic optimisations

Only if sufficient additional information about code optimisation is provided by submitter.
