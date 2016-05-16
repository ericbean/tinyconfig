#tinyconfig

The configuration file parser you never asked for.https://github.com/ericbean/tinyconfig.githttps://github.com/ericbean/tinyconfig.githttps://github.com/ericbean/tinyconfig.git

## Synopsis

I really like SQLAlchemy's declarative modeling and want to use that style to handle configuration files.
This is my proof of concept implementation.

## Installation

To install, run

    git clone https://github.com/ericbean/tinyconfig.git
    python3 setup.py install

## Usage

### The bare minimum example

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
You can specify a type with the type argument.
It can be any function or class that accepts a single str parameter.

For booleans, use the boolean function in tinyconfig.

Eg: `opt = Option(False, type=boolean)`

For a container type, just make the default the type you want.
It can be empty or have some preset values.
The type argument will be used to convert the values inside the container.
Container types currently require the object to have either an append or add method.

Eg: `opt = Option([2,3,5,7], type=int)`

For completeness, here's the signature for Option.

`Option(default, name=None, type=str, required=False)`

* The required argument currently does nothing.

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
