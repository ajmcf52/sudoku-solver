# Sudoku Solver & Algorithm Analysis

A Python project comparing approaches to solving
standard 9x9 Sudoku puzzles.

## Goals

- Validate puzzle input.
- Implement and test multiple solving approaches.
- Compare runtime and search effort.
- Document results and algorithmic tradeoffs.

## Challenges

### Threaded benchmarking

Near the end of the project, I implemented a 'Live benchmark progress' label inside the main
app view--this would function to keep the user updated on app activity during benchmarks. Depending on puzzle count, a benchmark can take anywhere from 10-20 seconds to 2-3 minutes, so I decided that notifying the user of current status was important.

#### Symptom

I extended the use of an event queue so that text updates could be appended from inside the `run_benchmark()` function. Upon doing so, the app would seemingly load the puzzle batch, but then zero progress would follow. No live updates from the benchmark progress label--according to the GUI, I was stuck in "Standby" mode.

#### Cause

This silent failure was a bit difficult to work through. I traced the benchmark call progression from button handler, to the threaded worker, all the way until the loading print statement and running the benchmark. Upon looking at the arguments of the `run_benchmark()` function, I realized that two positional arguments were swapped; `rep_count` had taken the place of `event_queue`, and vice versa.

#### Why it stayed silent

I had placed type annotations for each of the two problematic arguments, `int` and `queue.Queue`. Due to the nature of Python's behavior, however, these annotations are not enforced at runtime.

So within the while-loop of puzzle #1 in `run_benchmark()`, the comparison of `reps` to `rep_count` kept failing, as `rep_count` was actually of type `queue.Queue` and not `int`. In reality, the app was continually solving puzzle #1 with solver #1 over and over again. 

#### Fix

Relying on variable position in a function call that has optional arguments, I've learned, is asking for trouble and can be easy to miss, especially in Python, where type annotations do not provide runtime type enforcement.

Spotting the arguments being out of order, I added named arguments to avoid the possiblity of this happening again. 

Particularly when a function is being altered to extend its functionality (i.e. new argument is being added) is when named arguments become crucial to desirable app behavior.

## Status

Finishing touches on the application.