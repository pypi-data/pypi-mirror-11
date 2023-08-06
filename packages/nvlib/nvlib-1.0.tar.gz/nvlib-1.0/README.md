# nvlib
nvlib was created so that we can build tools in python to interface with nVentory. As an external source of truth nVentory is used to assist in automating the provisioning process wether it be in house or in the cloud.

# Summary
First off nVentory is a Ruby on Rails Datacenter Inventory Manager. nvlib is used to interface with the nventory API.

To find out more about setting up the nVentory web service, see https://github.com/nventory/nventory

# Getting started
To get started install nvlib
```
pip install nvlib
```

Create an INI file with settings to connect to your nVentory API

```
[nv]
user: someuser
pass: somepass
url: http://nventory.domain.com/
status: initializing
hardware_profile_id: 1
```

# Usage

```
from nvlib import Nventory
nventory = Nventory(ini_file)
```
