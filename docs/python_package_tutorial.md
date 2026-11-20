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

## Example

:::{code} python
from NGPIris import HCPHandler, HCIHandler

hcp_h = HCPHandler("path/to/credentials.json")

hci_h = HCIHandler("path/to/credentials.json")
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

---

```{eval-rst}
.. autoclass:: NGPIris.HCIHandler
  :no-index:
  :no-index-entry:
```

:::
