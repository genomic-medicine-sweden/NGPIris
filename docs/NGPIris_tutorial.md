# NGPIris beginner's tutorial

```{contents} Outline of the tutorial
:depth: 3
:backlinks: none
:local:
```

---

## Introduction

Welcome to the {py:mod}`NGPIris` beginner's tutorial! In this tutorial, we will show you how to get started with {py:mod}`NGPIris`.

We will start by discussing the terminology used and what the purpose of {py:mod}`NGPIris` is. Then we will cover how to install {py:mod}`NGPIris`, followed by an introduction on how to use the {term}`CLI` and Python package respectively.

What follows after that are some example use cases of {py:mod}`NGPIris` both in the {term}`CLI` and as the Python code counterpart.

:::{tip}
Throughout this tutorial, there will be tabs for either viewing the {term}`CLI` version or the Python version of a given example in sections like _[](#communicating-with-ngpr)_ and _[](#communicating-with-ngpi)_. This is useful for comparing how {term}`CLI` corresponds to a Python implementation.
:::

### Terminology

:::{tip}
If you stumble upon terms that are unfamiliar to you, you can most likely find a definition in the [](./glossary.rst).
:::

Within the {term}`NGP`, we have the {term}`NGPr` and the {term}`NGPi` which will be our main focus for this tutorial. For information about these services, please see the respective definitions in the [](./glossary.rst).

The most important take-away is that when we refer to the {term}`HCP` we also refer to the {term}`NGPr` and vice versa. Similarly, when we refer to the {term}`HCI` we also refer to the {term}`NGPi` and vice versa.

:::{important}

```{math}
\text{"HCP"} \Leftrightarrow \text{"NGPr"}

\text{"HCI"} \Leftrightarrow \text{"NGPi"}
```

:::

### The purpose of {py:mod}`NGPIris`

## Installing {py:mod}`NGPIris`

### Prerequisites

- NGPr creds

## How to use the {term}`CLI`

See [_The NGPIris CLI_](NGPIris.cli) for more extensive information about the {term}`CLI`.

## How to use the Python package

For more extensive information about IRIS Python package, see [_NGPIris base package_](NGPIris_base).

(communicating-with-ngpr)=

## The basics of communicating with NGPr

### Upload and download objects

::::{tab-set}

:::{tab-item} CLI
:sync: cli

```{code} console
iris
```

:::

:::{tab-item} Python
:sync: python

```{code} python
x = 1
```

:::

::::

### List objects

::::{tab-set}

:::{tab-item} CLI
:sync: cli

```{code} console
iris
```

:::

:::{tab-item} Python
:sync: python

```{code} python
x = 1
```

:::

::::

### Delete objects

::::{tab-set}

:::{tab-item} CLI
:sync: cli

```{code} console
iris
```

:::

:::{tab-item} Python
:sync: python

```{code} python
x = 1
```

:::

::::

(communicating-with-ngpi)=

## The basics of communicating with NGPi
