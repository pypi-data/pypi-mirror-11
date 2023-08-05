cfn-params
==========

A CloudFormation stack parameter utility.

Installation
------------

Install via pip::

    pip install cfnparams
    which cfn-params

Motivation
----------

``cfn-params`` overcomes some limitations of the AWS CLI when handling stack paramaters, such as:

* Simultaneously specifying both parameter arguments and parameter files,
  e.g. ``--parameters ParameterKey=foo,ParameterValue=bar --parameters file://params.json``
* Overly verbose JSON format

Features
--------

Parameters can be:

* specified on the CLI
* specified in the AWS CLI JSON format
* specified as Python dictionaries
* resolved from the outputs of other stacks


Parameter Specification
-----------------------

Command Line
^^^^^^^^^^^^

The same format as the AWS CLI is supported, however you must specify each
parameter in its own argument e.g.::

    --parameters ParameterKey=foo,ParameterValue=bar --parameters ParameterKey=baz,ParameterValue=quux


JSON files
^^^^^^^^^^

The same format as the AWS CLI is supported, with the ability to specify as
many input files as you like, e.g.::

    --parameters file://path/to/params.json


Python dictionaries
^^^^^^^^^^^^^^^^^^^

Specified the same way JSON files are, but must have the extension ``.py``::

    --parameters file://path/to/params.py

e.g.::

    {
        # Values must be strings as required by CFN
        'Key': 'Value',

        # All Python builtins are available:
        'FortyTwo': str(6 * 7),
        'MyCommaDelimitedList': ', '.join(['hello', 'world']),
    }



Output parameter resolution
---------------------------

When using the Python parameter format, a local method ``GetOutput(stack, output)`` is available for use, e.g.::

    {
        'foo': GetOutput('other-stack', 'foo'),
    }


Stack lookup and resolution
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If a dependent stack is referenced in a parameter, ``cfn-params`` will use the
``DescribeStacks`` API to resolve the parameter from the list of stack outputs.

The lookup process will:

1. Attempt to find a stack with the exact name specified
2. Optionally, use ``--resolve-tags`` to filter existing stack to find a fallback match.


The ``--resolve-tags`` argument is a list of tag key/value pairs to filter by.

e.g. if you want to only look for stacks in your staging environment::

    --resolve-tags Key=Environment,Value=staging
