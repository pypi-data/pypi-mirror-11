# HDIdx: Indexing High-Dimensional Data

## What is `HDIdx`?

`HDIdx` is a python package for approximate nearest neighbor (ANN) search in high-dimensional space.
The current version implements following seacrching algorithms: 

- `Product Quantization`[1].
- `Spectral Hashing`[2].

## Installation

`HDIdx` can be installed via `pip`:

```bash
[sudo] pip install hdidx
```

By default, `HDIdx` use kmeans algorithm provided by `SciPy`. To be more efficient, you can instll python extensions provided by `OpenCV`, which can be installed via `apt-get` on Ubuntu. For other Linux distributions, e.g. CentOS, you need to compile it from source.

```bash
[sudo] apt-get install python-opencv
```

`HDIdx` will detect `OpenCV` automatically and use it if available.

## Example

Here is a simple example. See this [notebook](http://nbviewer.ipython.org/gist/wanji/c08693f06ef744feef50) for more examples.

```python
# import necessary packages

import hdidx
import numpy as np

# generating sample data
ndim = 256     # dimension of features
ndb = 10000    # number of dababase items
nqry = 120     # number of queries

X_db = np.random.random((ndb, ndim)).astype(np.float64)
X_qry = np.random.random((nqry, ndim)).astype(np.float32)

# create Product Quantization Indexer
idx = hdidx.indexer.PQIndexer()
# build indexer
idx.build({'vals': X_db, 'nsubq': 8})
# add database items to the indexer
idx.add(X_db)
# searching in the database, and return top-100 items for each query
idx.search(X_qry, 100)
```

## Reference
```
[1] Jegou, Herve, Matthijs Douze, and Cordelia Schmid.
    "Product quantization for nearest neighbor search."
    Pattern Analysis and Machine Intelligence, IEEE Transactions on 33.1 (2011): 117-128.
[2] Weiss, Yair, Antonio Torralba, and Rob Fergus.
    "Spectral hashing."
    In Advances in neural information processing systems, pp. 1753-1760. 2009.
```
