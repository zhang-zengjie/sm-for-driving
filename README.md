# State Machine Generation for Autonomous Driving

**Author:** Zengjie Zhang (z.zhang3@tue.nl)

A Python project demonstrating how to generate a state machine for the decision-making of an autonomous vehicle from temporal logic specifications. The automatically generated state machine can be used as an alternative to a conventional rule-based program.

## Information

## Installation

### System Requirements

**Operating system**
 - *Windows* (compatible in general, succeed on 11)

**Python Environment**
 - Python version: test passed on `python=3.12`
 - **Recommended**: IDE ([VS code](https://code.visualstudio.com/) or [Pycharm](https://www.jetbrains.com/pycharm/)) and [Conda](https://www.anaconda.com/)
 - Required additional packages: `tulip` and `cvxopt`. Follow the `Quick Installation` for detailed configurations.


### Quick Installation
 
1. Install conda following this [instruction](https://conda.io/projects/conda/en/latest/user-guide/install/index.html);

2. Open the conda shell, and create an independent project environment;
```
conda create -n sm-for-driving python=3.12
```

3. In the same shell, activate the created environment
```
conda activate sm-for-driving
```

4. In the same shell, within the `sm-for-driving` environment, install the dependencies `tulip` and `cvxopt`:
 ```
pip install tulip
pip install cvxopt
```

### Running Instructions

- Run the main script `main.py`; This will generate a table file `sm_tables.json`;
- Run the script `machine`; This will translate the table file `sm_tables.json` into a state machine and produce the temporal logic.
