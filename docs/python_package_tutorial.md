# The NGPIris Python package tutorial

:::{contents} Outline of the tutorial
:depth: 2
:backlinks: none
:local:
:::

---

:::{important}
This tutorial was written for version v5.7.0
:::

## Introduction

Welcome to the {py:mod}`NGPIris` Python package tutorial!

In this tutorial, we will describe some ways of using {py:mod}`NGPIris` two primary classes: {py:class}`~NGPIris.HCPHandler` and {py:class}`~NGPIris.HCIHandler`. We will show you how to take advantage of {py:mod}`NGPIris` [type safety](https://en.wikipedia.org/wiki/Type_safety) in its classes, methods and other implementations.

:::{tip}
This tutorial will feature code examples and, for your convenience, we will also include a dropdown box containing datatypes and class information that are relevant for each example. For the full documentation, see [](package_docs).
:::

## {term}`NGPr`/{term}`HCP` examples

:::{code} python
from NGPIris import HCPHandler

hcp_h = HCPHandler("path/to/credentials.json")
:::

:::{dropdown} Show datatypes and classes
:animate: fade-in-slide-down
:icon: code
:color: primary

```{eval-rst}
.. autoclass:: NGPIris.HCPHandler
  :no-index:
  :no-index-entry:
```

:::

## {term}`NGPi`/{term}`HCI` examples

:::{code} python
from NGPIris import HCIHandler

hci_h = HCIHandler("path/to/credentials.json")
:::

:::{dropdown} Show datatypes and classes
:animate: fade-in-slide-down
:icon: code
:color: primary

```{eval-rst}
.. autoclass:: NGPIris.HCIHandler
  :no-index:
  :no-index-entry:
```

:::
