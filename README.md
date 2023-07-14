<hr>

<h1><p align="center"> Plots for scientific computing
</p></h1>

<br/>

## 1. Introduction
<p align="justify">
This repository provides 2D plot templates for output from scientific computing codes focusing on parallel benchmarking data.
</p>

<br/>
<hr>

## 2. How to use this program?
Assign the directory where you want the plots to be stored in the source file `plot.py`.
```python
plot_directory = 'plots'    # Directory to store plots
```

### Comparison plots
Comparison plots can be generated from output data of various simulations. The inputs to the code are as follows:
```python
comparison_directory   = 'results/comparison'         # Root directory for comparative input data
comparison_case_name   = ['mach_0p2', 'mach_0p4']     # Folder names for comparison cases
comparison_plot_labels = ['Mach 0.2', 'Mach 0.4']     # Plot labels for comparison cases
```
The `plot_xy()` function can then be used to generate the figure by reading appropriate column data from text files.
<p align="center">
    <img src="/docs/residuals.png" width="50%">
</p>

### Parallel benchmarking plots
Parallel benchmarking plots can also be generated by giving the following inputs.
```python
benchmark_directory = 'results/scaling'     # Root directory for benchmark input data
benchmark_partitions = [4, 8, 16, 32]       # Partition list and folder names for benchmark cases used in ascending order (starting from reference case).
benchmark_plot_labels = ['4 cores', '8 cores', '16 cores', '32 cores']  # Plot labels for benchmark cases
```
The total simulation run times can be plotted by using the function `total_runTimes()` from parallel benchmark data set.
The minimum of these times for each partitioned run can be plotted as well with `plot_bar_chart_minimum()` function.
<p align="center">
    <img src="/docs/simulation_runtimes.png" width="100%">
</p>

The most important data to plot for parallel benchmarking is the speedup and efficiency which can be obtained with `plot_parallel_speedup()` and `plot_parallel_efficiency()` functions.
<p align="center">
    <img src="/docs/parallel_benchmarking.png" width="100%">
</p>

<br/>
<hr>

## 3. How to run this program?
This program is written using python version 3 and it can be obtained by cloning this repository.
```
git clone https://github.com/jibranhaider/plotting
```

The program can then be executed by running the python script inside the cloned directory.
```
python3 plot.py
```

<br/>
<hr>

## 4. Author
This code is written by [Jibran Haider](http://jibranhaider.com/).


<br/>
<hr>

## 5. License
This program is released under the MIT License. More details can be found in the [LICENSE](LICENSE) file.
