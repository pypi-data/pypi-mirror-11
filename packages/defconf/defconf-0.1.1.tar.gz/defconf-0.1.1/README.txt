[![Build Status](https://travis-ci.org/dgarros/defconf.svg?branch=master)](https://travis-ci.org/dgarros/defconf)

# Defconf
Python Library/tool to easily define and validate the format and content of a configuration file

To build a robust application, it takes a lot of effort to properly check and
validate everything that can goes wrong within an input file filled by users:
- Wrong option name : login VS username,
- Wrong type : string instead of integer,
- Mandatory information missing
- Value not conform (ip address not valid etc ..)

All this complexity is often not completely managed by the application has it
require a LOT of work:
Defconf is here to help, it will:
+ Validate the format of the configuration file (list, dict, string)
+ Validate all names and track unsupported options
+ Validate content type (integer, string, bool, list, dict)
+ Validate the value with REGEX or pre-define list
+ Populate default value if information is missing

## How does it work
Create a definition file to define how your configuration should look like

For this simple configuration file
```yaml
http_server: [ 192.168.0.1, 192.168.0.2 ]
password: pwd!!
port: 4444
```

A corresponding defconf file will looks like this
```yaml
validate:
  main:
    http_server: { type: list, validate: ip_addr, mandatory: 1 }
    password:    { type: string, validate: valid_password, mandatory: 1 }
    port:        { type: integer, values: [4444, 2580], default: 4444 }

regex:
  ip_addr: ^(\d+)\.(\d+)\.(\d+)\.(\d+)$
  valid_password: ^[A-Za-z0-9\!]+$
```
For each option on the configuration file, we can define:
- type => [string, integer, bool, dict, list]
- mandatory => [0, 1]
- values => List of supported values (only for integer, string and list type)
- validate => Advance validation with Regex or with another validate block (nested dict)
- default => Default value if option is not defined

Detail example available here :
- [Configuration file - myconfig.yml]( https://github.com/dgarros/defconf/blob/master/myconfig.yml)
- [Definition file - myconfig.def.yml]( https://github.com/dgarros/defconf/blob/master/myconfig.def.yml)

#### From CLI (within project folder)
    python defconf.py myconfig.yml myconfig.def.yml

#### From python
```python
import defconf

definition = yaml.load( open('myconfig.def.yml') )
config = yaml.load( open('myconfig.yml') )
defconf.validate_config( config, definition, 'myconfig' )
```

## Installation
    git clone https://github.com/dgarros/defconf

## Enhancements list
- Support JSON file in addition to YAML
- Improve exception handling to catch as many issue as possible in one shot
- Create example config file from Definition file
- Create definition file for definition files :)
- Create a module and publish

## Support
Bug and issues can be open on Github [https://github.com/dgarros/defconf/issues]

## How to contribute
- Use it and share your config/def files
- Report issue
- Add unit tests
- Improve documentation
