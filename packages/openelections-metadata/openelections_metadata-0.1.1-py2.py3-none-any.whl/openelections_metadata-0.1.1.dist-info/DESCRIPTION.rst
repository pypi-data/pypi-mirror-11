# Metadata

A Python library that provides a thin wrapper to the [OpenElections Metadata API](http://docs.openelections.net/metadata-api/), which contains information about elections and the nature and availability of results data. The [API provides JSON endpoints for individual states](http://blog.openelections.net/an-improved-metadata-api/) and Metadata provides a way to search for and filter elections within a state.

Metadata has been tested under Python 2.7.X.

## Installation

```
pip install openelections-metadata
```

## Usage

Metadata offers two classes, `Request` and `Election`, for accessing the information in the API. You do not need an API key.

### Request

To make a request, you'll need to specify the state you're interested in and any or none of three optional parameters: `start_date`, `end_date` and `offset`. Metadata uses the two dates as a range; it will search for elections on or after the `start_date` and on or before the `end_date`. For example, to make a request for elections that occurred in Maryland in 2014, you would do the following:

```python
>>> import metadata
>>> r = metadata.Request('MD', '2014-01-01')
```

`Request` objects retain details about the parameters and also save the API url and the JSON response, if needed. Calling the `parse` method on the `Request` object creates individual `Election` objects, which have the same attributes as the API, with one addition - it has a `generated_filename` attribute that we use in the data processing pipeline.

```python
>>> elections = r.parse()
>>> elections[0]
<metadata.election.Election object at 0x103ffff10>
>>> elections[0].start_date
u'2014-11-04'
>>> elections[0].race_type
u'general'
```

## Running tests

```
python setup.py test
```

## Issues

To report an bug or request a feature, please [create a new issue](https://github.com/openelections/metadata/issues) describing the situation, providing as much detail as possible. We welcome contributions: feel free to fork the code and submit pull requests.

License
-------

Metadata is released under the MIT License.


