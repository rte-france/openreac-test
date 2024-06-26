# Openreac-test

The purpose of this repository is to test the AMPL code of the version SNAPSHOT-0.8.0 of [powsybl-optimizer](https://github.com/powsybl/powsybl-optimizer/tree/main) github repository.

---
## Getting started

### AMPL 

For this project, you must have [AMPL](https://ampl.com/) installed on your machine. AMPL is a proprietary tool that works as an optimization modelling language, and it can be interfaced with many solvers. 

### Non-linear solver

To run the models implemented in AMPL, you'll need a non-linear optimization solver. By default, the AMPL code is configured to run [Knitro](https://www.artelys.com/solvers/knitro/), which is a proprietary non-linear solver, but you are free to configure a different one.

If you chose to run Knitro, you must have `knitroampl` in your path, after the installation of the solver is done and that you got a valid licence.

### Python

The tests of the repository are fully written in Python.

---
## 1 Tests

### 1.1 Golden master

#### 1.1.1 How it works

To test a refactoring of the AMPL code, a golden master is used to check that there is no change in the displays and results produced by the execution of the new code.

The directories used to test the golden master are:

```
openreac-test
└─── ampl
    └─── divided
└─── python
    └─── golden_master
        └─── test
        └─── resources
```

To test the golden master, run the following test in the `python/golden_master/test/` directory:

```bash
pytest test_golden_master.py
```

For each test `t` located in the resources directory (`python/golden_master/resources/`), the AMPL network data and OpenReac parameters files are copied/pasted into the `output/t` directory, along with the modified AMPL code (from `ampl/divided/`). This code is then executed, and the printings/results are compared with the expected ones, also located in the golden master's resources. If a difference is observed (apart from certain indicators, excluded from the comparison because they depend on the execution time/date), the test `t` is considered as failed.

#### 1.1.2 How to add a test

To add a test, simply run OpenReac on a network, and copy/paste the contents of the AMPL execution directory (input and output) into the golden master resources.

### 1.2 Functionnal blocks

#### 1.2.1 How it works

The directories used to test the various functional blocks making of the AMPL code are:

```
openreac-test
└─── ampl
    └─── divided
    └─── input
    └─── output
└─── python
    └─── ampl_divided
        └─── test
        └─── resources
```

To test a block $b$, just run the corresponding pytest, in the `python/ampl_divided/test/` directory:

```bash
pytest b_test.py
```

When block $b$ is tested, the functional blocks producing results from a pre-processing or optimization problem, and which precede $b$, are imported rather than being produced by an execution. This makes it possible to isolate and test the behavior of the block $b$. 

This is achieved by modifying the AMPL file `reactiveopf.run` for each specific test, by replacing the lines executing the blocks preceding the $b$ block being tested by processes importing previously calculated results. These importers are located in the `ampl/input/` directory. 

So, to test the block $b$ on a network, the results of the various blocks preceding the block $b$ must first be stored in the resources. See [1.2.2](#112-how-to-add-a-test) for more details.


#### 1.2.2 How to add a test

To add a test, and be able to run the various functional blocks on it, you can follow the following steps:
- execute the `get_all_open_reac_output` method (in `python/ampl_divided/test/utils.py`) on a network. This will add the export processes from `ampl/output/` in `reactiveopf.run` to get the results of the blocks.
- store the results of the various functional blocks (exported in .txt format) in the directory `python/ampl_divided/resources/n/`, where `n` is the identifier of the test network.
- add the unit test in the python files of the block that you want to test (for example, `dcopf_test.py` and `acopf.py`), following the example of other test networks.