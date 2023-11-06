# AirSheaf
Simple implementation and examples for the paper Sheaf-theoretic self-filtering network of low-cost sensors for local air quality monitoring: A causal approach

## Environment setup

```sh
conda env create -f airsheaf.yml
```

## Contents
This repo contains the Python implementation of a generic sheaf as well as the implementation of a specific sensor network constructed in the accompanied article along with the three examples. The following is the structure of this repo:

```
root
├── data
│   └── README.md
├── examples
│   └── __init__.py
│   └── README.md
│   └── ToyExamples.ipynb
├── src
│   └── __init__.py
│   └── README.md
│   └── sheaf.py
├── __init__.py
├── airsheaf.yml
├── LICENSE
└── README.md
```

## How to cite?
~~~bibtex
@article{pham2023sheaf,
author="Pham, Anh-Duy
and Le, An Dinh
and Le, Chuong Dinh
and Pham, Hoang Viet
and Vo, Hien Bich",
editor="Arai, Kohei",
title="Harnessing Sheaf Theory for Enhanced Air Quality Monitoring: Overcoming Conventional Limitations with Topology-Inspired Self-correcting Algorithm",
booktitle="Proceedings of the Future Technologies Conference (FTC) 2023, Volume 1",
year="2023",
publisher="Springer Nature Switzerland",
address="Cham",
pages="102--122",
abstract="Sheaf theory is a potent but intricate tool that is supported by topological theory. It offers more accuracy and adaptability than traditional graph theory when modeling the connections between several characteristics. This is especially valuable in air quality monitoring, where sudden changes in local dust particle density can be hard to measure accurately using commercial instruments. Conventional air quality measurement techniques often depend on calibrating the measurement with standard instruments or calculating the measurement's moving average over a fixed period. However, this can result in an incorrect index at the measurement location, as well as an excessive smoothing effect on the signal. To address this issue, this study proposes a self-correcting algorithm that employs sheaf theory to account for vehicle counts as a local air quality change-causing factor. By deducing the number of vehicles and incorporating it into the recorded PM2.5 index from low-cost air monitoring sensors, we can achieve real-time self-correction. Additionally, the sheaf-theoretic approach enables straightforward scaling to multiple nodes for further filtering effects. By integrating sheaf theory into air quality monitoring, we can overcome the limitations of conventional techniques and provide more precise and dependable results.",
isbn="978-3-031-47454-5"
}
