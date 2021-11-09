# micarraylib

<img src="docs/img/micarraylib.png" height="100px">

Python library to download, standardize, and aggregate existing microphone array recordings. Using micarraylib, one can encode raw microphone array recordings across different datasets to be in the common ambisonics B-format. micarraylib also standardizes annotations to be in a common convention ([Soundata's Events class conventions](https://soundata.readthedocs.io)). 

Additionally, micarraylib organizes metadata (i.e. microphone capsule coordinates and hardware name) to be readily accessible. 

IMPORTANT: This software is fully-functional but still being developed and tested. As a result, it is in its pre-release stage. Use with caution (read [LICENSE](https://github.com/micarraylib/micarraylib/blob/main/LICENSE)). Suggestions, requests, and noted-issues are always welcome. 

## How to install

To install, first clone the repo, then navigate to the `micarraylib` directory, and install with pip in editable mode:

```
$ git clone https://github.com/micarraylib/micarraylib.git

$ cd micarraylib

$ pip install -e .
```

## Example uses

1. Obtaining DCASE task 3 clips and sound event annotations in A and B formats (no ambisonics encoding used since the dataset natively exists in A and B formats).

```
```
The same code works with the 2019, 2020, and 2021 versions of the dataset. Just use the desired year.

2. Obtaining clips for each of the microphone arrays used in the 3D-MARCo dataset in the original A format (raw microphone capsule recordings) and encoding them to B format.
```
```

3.

## Supported datasets

| Dataset name      | micarraylib/soundata identifier  |
| ----------------- | -------------------------------- |
| DCASE task 3 2019 | `tau2019sse`                     |
| DCASE task 3 2020 | `tau2020sse_nigens`              |
| DCASE task 3 2021 | `tau2021sse_nigens`              |
| 3D-MARCo          | `marco`                          |
| EigenScape        | `eigenscape` and `eigenscape_raw`|

## Citing
```
@article{roman2021micarraylib,
  title={Micarraylib: Software for Reproducible 
  Aggregation, Standardization, and Signal 
  Processing of Microphone Array Datasets},
  author={Roman, Iran R and Bello, Juan Pablo},
  year={2021},
}
```
Our DCASE 2021 paper can be found [here](http://dcase.community/documents/workshop2021/proceedings/DCASE2021Workshop_Roman_59.pdf)


## License
Shield: [![CC BY 4.0][cc-by-shield]][cc-by]

This work is licensed under a
[Creative Commons Attribution 4.0 International License][cc-by].

[![CC BY 4.0][cc-by-image]][cc-by]

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg
