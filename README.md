# Paging and Process Scheduling

## Project Description

The project consists of two parts, each implementing different algorithms:
1. **Memory Paging Algorithms (FIFO and LRU)** - Implementation of memory management algorithms.
2. **Process Scheduling Algorithms (FCFS and SJF)** - Implementation of process scheduling algorithms in operating systems.

## Files

### 1. **FIFO and LRU - Paging Algorithms**
#### File: `fifo_lru.py`

#### Features:
- **FIFO (First In, First Out)**: Removes the oldest page from the queue when there is no space for a new one.
- **LRU (Least Recently Used)**: Removes the least recently used page when the queue reaches maximum capacity.
- Generates random page sequences and saves them to a file.
- Simulates paging algorithms and writes the results to a file.

### 2. **FCFS and SJF - Scheduling Algorithms**
#### File: `fcfs_sjf.py`

#### Features:
- **Implementation of scheduling algorithms**:
  - **FCFS (First-Come, First-Served)**: Processes are executed in the order of their arrival.
  - **SJF (Shortest Job First)**: Processes are sorted by their shortest execution time.
- Generates random processes.
- Exports results to text files and visualizes the outcomes with charts.
