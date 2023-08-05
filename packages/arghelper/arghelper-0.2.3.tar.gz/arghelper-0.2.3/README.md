# arghelper

[![PyPi Version][pypi ver image]][pypi ver link]
[![Build Status][travis image]][travis link]
[![Coverage Status][coveralls image]][coveralls link]
[![License Badge][license image]][LICENSE.txt]

[arghelper][] is a Python (2.6+) module providing functions to help with
argparse.

## Requirements

- `argparse` module from the [Python Standard Library][]
- `sys` module from the [Python Standard Library][]
- `os` module from the [Python Standard Library][]

## Usage

`arghelper` provides functions to determine if a file or directory
exists:

- `extant_file`
- `extant_dir`

These can be used as follows:

```python
if __name__ == "__main__":
    # Process the arguments
    import argparse
    import arghelper
    parser = argparse.ArgumentParser(
        description='Process the TAFFmat CET files')
    parser.add_argument(
        'config_file',
        help='CSV configuration file.',
        metavar='FILE', type=arghelper.extant_file)
    parser.add_argument(
        'input_dir',
        help='Directory containing input files.',
        metvar='DIR', type=arghelper.extant_dir)
    args = parser.parse.args()
```

A common pattern, for me at least, is to have three positional arguments
consisting of:

1. `config_file` --- A configuration file
2. `input_dir` --- A directory containing input files to be read
3. `output_dir` --- A directory where the output files should be saved

This pattern has been abstracted to a Facade function called
`parse_config_input_output`, which can be used as follows:

```python
if __name__ == "__main__":
    # Process the arguments
    import arghelper
    args = arghelper.parse_config_input_output(sys.argv)
```

## Contributing

[arghelper][] is developed using [Scott Chacon][]'s [GitHub Flow][]. To
contribute, fork [arghelper][], create a feature branch, and then submit
a pull request.  [GitHub Flow][] is summarized as:

- Anything in the `master` branch is deployable
- To work on something new, create a descriptively named branch off of
  `master` (e.g., `new-oauth2-scopes`)
- Commit to that branch locally and regularly push your work to the same
  named branch on the server
- When you need feedback or help, or you think the brnach is ready for
  merging, open a [pull request][].
- After someone else has reviewed and signed off on the feature, you can
  merge it into master.
- Once it is merged and pushed to `master`, you can and *should* deploy
  immediately.

# License

[arghelper][] is released under the MIT license. Please see the
[LICENSE.txt][] file for more information.

[arghelper]: https://github.com/questrail/arghelper
[coveralls image]: http://img.shields.io/coveralls/questrail/arghelper/master.svg
[coveralls link]: https://coveralls.io/r/questrail/arghelper
[github flow]: http://scottchacon.com/2011/08/31/github-flow.html
[LICENSE.txt]: https://github.com/questrail/arghelper/blob/master/LICENSE.txt
[license image]: http://img.shields.io/pypi/l/arghelper.svg
[pull request]: https://help.github.com/articles/using-pull-requests
[pypi ver image]: http://img.shields.io/pypi/v/arghelper.svg
[pypi ver link]: https://pypi.python.org/pypi/arghelper
[python standard library]: https://docs.python.org/2/library/
[scott chacon]: http://scottchacon.com/about.html
[travis image]: http://img.shields.io/travis/questrail/arghelper/master.svg
[travis link]: https://travis-ci.org/questrail/arghelper
