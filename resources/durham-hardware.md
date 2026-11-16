# Durham hardware systems information

The following are hardware tables for systems based at Durham which are frequently used for the assessments.

## Hamilton

The hardware details for Hamilton are [available here](https://www.durham.ac.uk/research/institutes-and-centres/advanced-research-computing/hamilton-su/computer/systems/). This information is corroborated by running `cat /proc/cpuinfo` on one of the compute nodes via an interactive session:

| Specification | Details |
| -------------- | ------------------------------------------------ |
| Number of compute nodes | Standard: 120; High-memory: 2 |
| Processors / node | 2 $\times$ [AMD EPYC 7702 64-Core Processors](https://www.amd.com/en/support/downloads/drivers.html/processors/epyc/epyc-7002-series/amd-epyc-7702.html) |
| Clock speed / CPU | Base: 2000 MHz; Boost: 3350 MHz |
| Sockets / node | 2 |
| Cores / node | 128 |
| NUMA domains | 8 / node (4 / socket), each with a dedicated memory channel and further split into 4 groups containing 4 cores each |
| Cache | 16 MB L3 cache / 4-core chiplet, 512 KB of L2 cache / core and 32 KB of L1 cache / core |
| Chiplets / NUMA domain | 4 |
| Simultaneous Multithreading | Disabled
| RAM / node | Standard: 256 GB DDR4 (246 GB available to users); High-memory: 2 TB DDR4 |
| Local storage | 400GB SSD |
| Interconnect | Infiniband HDR 200GB/s high /formance interconnect, with a 2.6:1 fat tree topology formed of non-blocking islands of up to 26 nodes |

Hamilton also has one GPU node with the following configuration verified with `cat /proc/cpuinfo` and `nvidia-smi`:

| Specification | Details |
| ------------- | ------- |
| Processors | [2 AMD EPYC 9555 64-Core Processors](https://www.amd.com/en/products/processors/server/epyc/9005-series/amd-epyc-9555.html) |
| GPUs | 8 NVIDIA H200 NVL |
| RAM | 2.2 TB |
| Local storage | 3 TB NVMe |

## Bede

The hardware details for Bede are [available here](https://bede-documentation.readthedocs.io/en/latest/hardware/index.html). This information is corroborated by running `cat /proc/cpuinfo` on one of the compute nodes via an interactive session:

| Specification               | Details                                                                              |
| --------------------------- | ------------------------------------------------------------------------------------ |
| Processors / node           | 2 $\times$ [POWER9 CPU](https://www.redbooks.ibm.com/redbooks.nsf/pages/power9?Open) |
| Clock speed / CPU           | Base: 2700 MHz; Boost: 3800 MHz                                                      |
| Sockets / node              | 2                                                                                    |
| Cores / socket              | 40                                                                                   |
| NUMA domains / socket       | 1                                                                                    |
| Cache                       | 32KB L1i/32KB L1d / core, 512KB L2 / core and 10MB L3 Cache size / 4-core chiplet    |
| Simultaneous Multithreading | 4 threads / core                                                                     |
| RAM / node                  | 512GB DDR4                                                                           |
| GPUs / node                 | 4 $\times$ [Nvidia Tesla V100 32GB](https://images.nvidia.com/content/technologies/volta/pdf/volta-v100-datasheet-update-us-1165301-r5.pdf) |
| GPU interconnect            | [NVLink](https://www.nvidia.com/en-gb/data-center/nvlink/) 2.0                       |
| Interconnect                | 2 $\times$ Mellanox EDR (100Gbit/s) InfiniBand ports, organised in a 2:1 block fat tree topology |

Additionally, there is the `infer` partition with Tesla T4 GPUs and 7 Grace Hopper nodes in a separate partition.

## COSMA

### `gn002` and `gn003`

The [Grace Hopper GH200 testbed on COSMA](https://cosma.readthedocs.io/en/latest/nvidiagpu.html#gh200-shareing) contains two nodes, with `gn002` accessible via `ssh` and `gn003` via SLURM queue, both with the following specifications:

| Specification | Details |
| ------------------------- | ---------------------------------------------------------------------------- |
| Processor | 1 $\times$ [NVIDIA GH200 Grace Hopper Superchip](https://dam-cdn.nvd.orangelogic.com/AssetLink/tkno03fa645gb7f33w60rf200d330420.pdf) with a [72-core ARM Grace CPU](https://resources.nvidia.com/en-us-grace-cpu/data-center-datasheet?xs=1123791#page=1) and an [H100 GPU](https://www.nvidia.com/en-gb/data-center/h100/) |
| Clock speed per CPU | Base: 3.1 GHz, all-core SIMD: 3.0 GHz |
| L1 Cache | 64KB i-cache + 64KB d-cache |
| L2 Cache | 1MB / core |
| L3 Cache | 114MB |
| RAM | 480GB (unified) LPDDR5X |
| Interconnect | [NVLink-C2C](https://www.nvidia.com/en-gb/data-center/nvlink-c2c/) |

### `gn004`

The [H100 testbed on COSMA](https://cosma.readthedocs.io/en/latest/nvidiagpu.html#gh200-shareing) is on 1 node, `gn004`. This is accessible via `ssh` from 08:00 to 19:00 UK time and via SLURM on the `hardwarelab-gpu` partition outside those hours. It has the following specifications:

| Specification               | Details                                                                              |
| --------------------------- | ------------------------------------------------------------------------------------ |
| Processor | 2 $\times$ [Intel Xeon Gold 6530 32-core Processors](https://www.intel.com/content/www/us/en/products/sku/237249/intel-xeon-gold-6530-processor-160m-cache-2-10-ghz/specifications.html) |
| Clock speed / CPU           | Base: 2100 MHz; Boost: 4000 MHz                                                      |
| Sockets / node              | 2                                                                                    |
| Cores / socket              | 32                                                                                   |
| NUMA domains / node       | 4                                                                                    |
| Cache                       | 2MiB L1i/3MiB L1d / core, 128MiB L2 / core and 320MiB L3 Cache size / processor    |
| RAM / node                  | 510GB                                                                           |
| GPUs / node | 1 $\times$ [NVIDIA H100 GPU](https://resources.nvidia.com/en-us-hopper-architecture/nvidia-h100-tensor-c) |

### `gn005`

The [RTX PRO 6000 testbed on COSMA](https://cosma.readthedocs.io/en/latest/nvidiagpu.html#rtx-pro-6000) is on 1 node, `gn005`. This is accessible via `ssh` from 08:00 to 19:00 UK time and via SLURM on the `hardwarelab-gpu` partition outside those hours. It has the following specifications:

| Specification               | Details                                                                              |
| --------------------------- | ------------------------------------------------------------------------------------ |
| Processor | 2 $\times$ [128-core AMD EPYC 9745 (Turin) Processor](https://www.amd.com/en/products/processors/server/epyc/9005-series/amd-epyc-9745.html) |
| Clock speed / CPU           | Base: 2400 MHz; Boost: 3700 MHz                                                      |
| Sockets / node              | 2                                                                                    |
| Cores / socket              | 128                                                                                   |
| NUMA domains / node       | 8                                                                                    |
| Cache                       | 8MiB L1i/12MiB L1d / core, 256MiB L2 / core and 512MiB L3 Cache size / processor    |
| Simultaneous Multithreading | 2 threads / core                                                                     |
| RAM / node                  | 2.3TB                                                                           |
| GPUs / node | 1 $\times$ [NVIDIA RTX PRO 6000 Blackwell Server Edition](https://www.nvidia.com/en-gb/data-center/rtx-pro-6000-blackwell-server-edition/) |
