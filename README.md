# micarraylib

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

```
```

## Citing
```
@article{romanmicarraylib,
  title={MICARRAYLIB: SOFTWARE FOR REPRODUCIBLE 
  AGGREGATION, STANDARDIZATION, AND SIGNAL 
  PROCESSING OF MICROPHONE ARRAY DATASETS},
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
