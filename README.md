# AirSheaf
Simple implementation and examples for the paper Sheaf-theoretic self-filtering network of low-cost sensors for local air quality monitoring: A causal approach

## Environment setup

```sh
conda env create -f airsheaf.yml
```

## Contents
This repo contains the Python implementation of a generic sheaf as well as the implementation of a specific sensor network constructed in the accompanied article along with the three examples. The following is the structure of this repo:

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
├── README.md

## How to cite?
~~~bibtex
@article{pham2022sheafair,
  title={Sheaf-theoretic self-filtering network of low-cost sensors for local air quality monitoring: A causal approach},
  author={Pham, Anh-Duy and Le, Chuong D and Pham, Hoang V and Tran, Thinh G and Vo, Dat T and Tran, Chau L and Le, An D and Vo, Hien B},
  journal={},
  year={2022}
}