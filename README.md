<p align="center">
    <br/>
    <b>Dradis-api is a python wrapper around the <a href="https://dradisframework.com/support/guides/rest_api/">API of Dradis</a>.</b>
    <br/>
    <a href="#goal">Goal</a>
    •
    <a href="#installation">Installation</a>
    •
    <a href="#usage">Usage</a>
    •
    <a href="#supported-endpoints">Supported endpoints</a>
    <br/>
    <sub>Built with ❤ by the <a href="https://twitter.com/NorthwaveLabs">Northwave</a> Red Team</sub>
    <br/>
</p>
<hr>

# Goal

The dradis-api python wrapper provides an easy way to access the [API of dradis](https://dradisframework.com/support/guides/rest_api) from python. This project is based on [pydradis by Novacast](https://github.com/ncatlabs/pydradis).

# Installation

```
pip install .
```

Or directly from the repository:

```
pip install git+ssh://gitlab.local.northwave.nl/redteam/dradis-api.git
```

# Usage

```
from dradis import Dradis

# Define api_token and url

dradis_api = Dradis(api_token, url)
projects = dradis_api.get_all_projects()
...
```

# Supported endpoints

Currently, the following endpoints are fully supported:

- Teams endpoint
- Projects endpoint
- Nodes endpoint
- Issues endpoint
- Evidence endpoint
- Content Blocks endpoint
- Notes endpoint
- Document Properties endpoint
- IssueLibrary endpoint 
- Attachments endpoint

The following endpoints are not fully supported:

- The users endpoint is currently unsupported, feel free to implement support and submit a pull request.
