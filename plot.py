#!/usr/bin/env python3

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import os
import math
import sys

# Axes settings
mpl.rcParams['axes.labelsize'] = '10'
mpl.rcParams['axes.titlesize'] = '12'
mpl.rcParams['xtick.labelsize'] = '6'
mpl.rcParams['ytick.labelsize'] = '6'

# Legend settings
mpl.rcParams['legend.fontsize'] = '8'
mpl.rcParams['legend.frameon'] = 'true'
mpl.rcParams['legend.fancybox'] = 'true'
mpl.rcParams["legend.borderpad"] = '0.5'
mpl.rcParams['legend.framealpha'] = '0.8'
mpl.rcParams['legend.edgecolor'] = 'gray'
mpl.rcParams['legend.facecolor'] = 'w'
mpl.rcParams['legend.labelspacing'] = '0.5'
mpl.rcParams["legend.borderaxespad"] = '1'
mpl.rcParams['patch.linewidth'] = 0.5

# Resolution of figure
mpl.rcParams['savefig.dpi'] = '300'

# Define line colors and widths
line_colors  = ['b', 'r', 'g', 'm', 'c', 'y']
line_widths  = [0.5, 0.4, 0.3, 0.25, 0.2]
marker_style = ['o', '+', 'x', 's', 'o']
marker_size  = [0.5, 0.8, 0.6, 0.2]


#--------------------------------------------------------------------------------------------------
# INPUTS
#--------------------------------------------------------------------------------------------------
# Directory to store plots
plot_directory = 'plots'

# Inputs for comparison plots
comparison_directory = 'results/comparison'           # Inputs for comparison plots
comparison_case_name = ['mach_0p2', 'mach_0p4']       # Folder names for comparison cases
comparison_plot_labels = ['Mach 0.2', 'Mach 0.4']     # Plot labels for comparison cases

# Inputs for inputs for parallel benchmarking plots
benchmark_directory = 'results/scaling'               # Inputs for scaling plots
benchmark_partitions = [4, 8, 16, 32]                 # Scaling partitions used in ascending order (starting from reference case).
                                                      # Also used for case directory structure inside benchmark_directory
benchmark_plot_labels = ['4 cores', '8 cores', '16 cores', '32 cores']  # Plot labels for scaling cases


#--------------------------------------------------------------------------------------------------
# CASE DIRECTORIES
#--------------------------------------------------------------------------------------------------
# Setup comparison case directories
comparison_case_directory = {}
for i in range(len(comparison_case_name)):
  comparison_case_directory[i] = comparison_directory+ '/' +comparison_case_name[i]

# Setup scaling case directories
scaling_case_directory = {}
for i in range(len(benchmark_partitions)):
  scaling_case_directory[i] = benchmark_directory+ '/' +str(benchmark_partitions[i])


#--------------------------------------------------------------------------------------------------
# SIZE OF CASE DIRECTORIES
#--------------------------------------------------------------------------------------------------
# Number of cases to compare
comparison_cases = len(comparison_case_name)
scaling_cases = len(benchmark_partitions)

if comparison_cases != len(comparison_plot_labels):
  sys.exit("Please enter same size for 'comparison_case_name' and 'comparison_plot_labels'")


#--------------------------------------------------------------------------------------------------
# Function to plot figure
#--------------------------------------------------------------------------------------------------
def plot_xy(directory, labels, results_file, x, x_label, y, y_label, y_scale, figure, marker_size):
  data = {}
  for i in range(len(directory)):
    data[i] = np.loadtxt(directory[i]+ '/' +results_file)
    plt.plot(data[i][:,x], data[i][:,y], marker=marker_style[i], ms=marker_size, color=line_colors[i], lw=line_widths[i], label=labels[i])
    plt.legend()

  save_plot(x_label, y_label, y_scale, figure)


#--------------------------------------------------------------------------------------------------
# Function to plot total simulation run times for parallel benchmark cases
#--------------------------------------------------------------------------------------------------
def total_runTimes(directory, labels, results_file, x_label, y_label, y_scale, figure):
  data = {}
  for i in range(len(directory)):
    data[i] = np.loadtxt(directory[i]+ '/' +results_file)
    plt.plot(range(1, len(data[i])+1), data[i], marker=marker_style[i], ms=marker_size[i], color=line_colors[i], lw=line_widths[i], label=labels[i])
    plt.legend()

  save_plot(x_label, y_label, y_scale, figure)


#--------------------------------------------------------------------------------------------------
# Function to plot parallel speedup
#--------------------------------------------------------------------------------------------------
def plot_parallel_speedup(directory, results_file, x_label, y_label, y_scale, figure, marker_size):

  data = []
  ideal = []
  data_ref = min(np.loadtxt(directory[0]+ '/' +results_file))
  for i in range(scaling_cases):
    data.append(data_ref/min(np.loadtxt(directory[i]+ '/' +results_file)))
    ideal.append(benchmark_partitions[i] / benchmark_partitions[0])

  plt.plot(benchmark_partitions, data, marker=marker_style[0], ms=marker_size, color=line_colors[0], lw=line_widths[0], label='Actual speedup')
  plt.plot(benchmark_partitions, ideal, '-o', color='k', ms=0., lw=line_widths[0], label='Ideal speedup')
  plt.legend()
  save_plot(x_label, y_label, y_scale, figure)


#--------------------------------------------------------------------------------------------------
# Function to plot parallel efficiency
#--------------------------------------------------------------------------------------------------
def plot_parallel_efficiency(directory, results_file, x_label, y_label, y_scale, figure, marker_size):

  data = []
  ideal = []
  data_ref = min(np.loadtxt(directory[0]+ '/' +results_file))
  for i in range(scaling_cases):
    data.append(data_ref/min(np.loadtxt(directory[i]+ '/' +results_file))/benchmark_partitions[i]*benchmark_partitions[0]*100)
    ideal.append(benchmark_partitions[i] / benchmark_partitions[i]*100)

  plt.plot(benchmark_partitions, data, marker=marker_style[0], ms=marker_size, color=line_colors[0], lw=line_widths[0], label='Actual efficiency')
  plt.plot(benchmark_partitions, ideal, '-o', color='k', ms=0., lw=line_widths[0], label='Ideal efficiency')
  plt.legend()
  save_plot(x_label, y_label, y_scale, figure)


#--------------------------------------------------------------------------------------------------
# Function to plot minimum simulation run times from a set of simulations
#--------------------------------------------------------------------------------------------------
def plot_bar_chart_minimum(directory, results_file, x_label, y_label, y_scale, figure):
  data = {}
  for i in range(scaling_cases):
    data[i] = min(np.loadtxt(directory[i]+ '/' +results_file))
    plt.bar(str(benchmark_partitions[i]), data[i], 0.75, label=benchmark_plot_labels[i], color=line_colors[i], alpha=0.7)

  save_plot(x_label, y_label, y_scale, figure)


#--------------------------------------------------------------------------------------------------
# Function to save plot
#--------------------------------------------------------------------------------------------------
def save_plot(x_label, y_label, y_scale, fig_name):
  plt.yscale(y_scale)
  plt.xlabel(x_label)
  plt.ylabel(y_label)
  plt.grid(which='major', ls=':', lw='0.75', color='k', alpha=0.3)
  plt.legend(loc='best')
  #plt.legend(loc='upper right') # You can defined a specific legend location
  plt.savefig(plot_directory+ '/' +fig_name, bbox_inches='tight')
  plt.close(1)


#--------------------------------------------------------------------------------------------------
# Combine and delete individual plots
#--------------------------------------------------------------------------------------------------
def combine_plots(plots_individual, plot_combined):
  os.system("cd " +plot_directory+ " && montage " +plots_individual+ " -geometry +0+0 " +plot_combined)

  # Delete individual plots
  split = plots_individual.split(" ")
  for i in range(len(split)):
    os.system("rm " +plot_directory+ "/" +split[i])


#--------------------------------------------------------------------------------------------------
# Create directory to store plots if it doesn't exist
#--------------------------------------------------------------------------------------------------
def create_directory(plot_folder):
  cwd = os.getcwd()
  plot_directory = cwd+ "/" +plot_folder
  if os.path.isdir(plot_directory):
    print("Overwriting existing directory " +plot_directory+ " to store plots ...")
    os.system("rm -r " +plot_directory+ "/*")
  else:
    print("Creating directory to store plots ...")
    os.system("mkdir " +plot_directory)


#--------------------------------------------------------------------------------------------------
# MAIN PROGRAM
#--------------------------------------------------------------------------------------------------

def main():

  # Create directory to store plots
  create_directory(plot_directory)

  # Residuals
  print("Generating residual plot ...")
  plot_xy(comparison_case_directory, comparison_plot_labels, 'residuals.txt', 0, 'Iterations', 1, 'RMS residual', 'log', 'residuals.png', 0)

  # Total simulation run times
  print("Generating total simulation run time plot ...")
  total_runTimes(scaling_case_directory, benchmark_plot_labels, 'simulationTimes.txt', 'Runs', 'Total runtime (sec)', 'linear', 'total_runtimes.png')

  # Minimum simulation run times
  print("Generating minimum simulation run time bar plot ...")
  plot_bar_chart_minimum(scaling_case_directory, 'simulationTimes.txt', 'Number of processors', 'Minimum runtime (sec)', 'linear', 'minimum_runtimes.png')

  # Scaling
  print("Generating parallel benchmarking speedup plot ...")
  plot_parallel_speedup(scaling_case_directory, 'simulationTimes.txt', 'Number of processors', 'Speed up', 'linear', 'speedup.png', 2)

  # Parallel efficiency
  print("Generating parallel benchmarking efficiency plot ...")
  plot_parallel_efficiency(scaling_case_directory, 'simulationTimes.txt', 'Number of processors', 'Parallel efficiency (%)', 'linear', 'efficiency.png', 2)

  # Combine plots
  print("Combining plots ...")
  combine_plots('total_runtimes.png minimum_runtimes.png', 'simulation_runtimes.png')
  combine_plots('speedup.png efficiency.png', 'parallel_benchmarking.png')

  print("Plotting completed!")

if __name__ == '__main__': main()
