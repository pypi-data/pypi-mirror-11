# Resea SDK
[![Build Status](https://travis-ci.org/resea/sdk.svg?branch=master)](https://travis-ci.org/resea/sdk)
[![PyPI version](https://badge.fury.io/py/reseasdk.svg)](http://badge.fury.io/py/reseasdk)

A development tools for Resea.

## Installation
```
# pip3 install reseasdk
```

## Quickstart

### Building an OS
```
$ reseasdk new hello       # create a project directory
$ cd hello                 # move into the created directory
$ edit config.release.yml  # edit build config for building
$ reseasdk build           # build
```

### Developing a application
```
$ edit package.yml     # edit project configuration
$ reseasdk scaffold    # generate boilerplate code
$ edit                 # write code
$ edit config.test.yml # edit build config for testing
$ reseasdk test        # build and run tests
```

## Files
### package.yml
It contains information for a package: name, type, required packages,
interface/data type/config definitions, etc.

### config.yml
`config.*.yml` contains build configuration.
- `config.release.yml`: used in `build` command
- `config.test.yml`: used in `test` command
- `config.global.yml`: Default config applied to all packages. This file is used
  in special libraries to define build rules.

#### Configration defined by SDK
- `BUILTIN_APPS`: A list of applications to be embeded in an executable.
- `TEST`: A boolean. If it is `yes`, SDK includes test code in an executable.
- `HAL`: HAL library.
- `STARTUP_WITH_THREAD`: If it is `yes`, Resea starts applications in a new
  thread separately. If it is `no`, the application except `early_startup`
  applications is started by calling `STARTUP()` directly. It is useful for
  developing application for Arduino.

## Commands
### Creating new project
- **new**: create a project directory

### Building / Testing
- **build:** build a executable
- **test:** build and test an executable
- **clean:** remove intermediate files such as `*.o`
- **log:** print kernel log omitted in tests

### Unimplemented
- **debug:** test an executable in a debugger
- **analyze:** analyze kernel log
- **sync:** download required packages and update build config
- **search:** search for packages
- **release:** create new version
- **gendocs:** generate web pages from documentation and source code
- **scaffold:** generate boilerplates
- **scancode:** analyze source code
