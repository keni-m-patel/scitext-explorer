# scitext-explorer
This README will outline all packages, setup, etc necessary to run the introductory notebooks. 
There is also a sample README template in the `My_First_Notebook` folder to help you format README files
in the future.

## Getting Started
### Prerequisites
The stadard `re`, `matplotlib`, `numpy`, and `pandas` modules should be installed with python already. Please check for `re` by running:

```
conda search regex
```

If it is not installed, run:

```
conda install regex
```

### Installing
To get the environment up and running for these notebooks, Please run the following:

```
conda create --name intro python regex pandas matplotlib
```

and when conda asks you to proceed, type `y` and hit enter.

```
proceed ([y]/n)?
```

to activate your environment, type:

```
activate intro
```

### Author
Brian Friederich
