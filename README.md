#tinyconfig

The configuration file parser you never asked for.

## Synopsis

I really like SQLAlchemy's declarative modeling and want to use that style to
handle configuration files.
This is my proof of concept implementation.

## Requirements

* Python 3.4 or later

It might work on Python 3.3 too but I haven't tried it.

## Installation

To install, run

    git clone https://github.com/ericbean/tinyconfig.git
    python3 setup.py install

## Usage

### A bare minimum example

    >>>from tinyconfig import ConfigDict, Option, boolean, parse_file
    >>>
    >>>class myconfig(ConfigDict):
    >>>    myopt = Option('sometext')
    >>>
    >>>conf = myconfig()
    >>>conf['myopt']
    'sometext'
    >>>f = open('myproject.cfg')
    >>>parse_file(f, conf)
    >>>conf['myopt']
    'Hello, world'

### Usage details

#### ConfigDict

ConfigDict is a subclass of `dict` and behaves identically, except it takes no
parameters.
To use ConfigDict, simply subclass it, assign some Options as class variables
and use as you would any other `dict`.

#### Option

`Option(default, name=None, type=str, required=False)`

You can specify a type with the type argument.
It can be any function or class that accepts a single str parameter.
If type isn't specified it defaults to str.

Eg. `ip = Option(1.2, type=float)`

For booleans, the boolean helper function will accept `true`, `yes`, `on`, and
`1` for true values. All other values, including none at all be will considered
false.

Eg. `opt = Option(False, type=boolean)`

For a container type, just make the default the type you want.
It can be empty or have some preset values.
The type argument will be used to convert the values inside the container.
Container types currently require the object to have either an append or add
method.

Eg. `opt = Option([2,3,5,7], type=int)`

The name argument sets the name of the option as it will appear in the
ConfigDict and in configuration files. Mostly this is intended to help where an
option isn't a valid python identifier.

Eg. `host_address = Option('::1', name='host-address')`

The required argument currently does nothing and can be ignored entirely.

#### parse_file

`parse_file(fileobj, ConfigDict)`

Call parse_file to parse an open fileobj and store the options in the specified
ConfigDict instance.

### Structure of a config file

Your config file should look something like this:

    # this is the config file for MyProject
    # you can use quoted strings
    myopt="Hello, world"
    # boolean values can be true/false yes/no, on/off, 1,0
    someopt=on
    # multiple values can be done as well
    another=11,13, 17 19 #leaving the commas out or mixing them is ok
    # in fact you can leave the = out altogether
    another 23, 29, 31

## Credits

Eric Beanland

## License

Released under the MIT License
