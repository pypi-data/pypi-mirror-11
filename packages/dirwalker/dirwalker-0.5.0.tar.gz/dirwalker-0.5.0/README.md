# dirwalker

[![PyPi Version][pypi ver image]][pypi ver link]
[![Build Status][travis image]][travis link]
[![Coverage Status][coveralls image]][coveralls link]
[![License Badge][license image]][LICENSE.txt]

[dirwalker][] is a Python (2.6+/3.3+) package that walks multiple-level
directories searching for files with the given extensions.

## Requirements

* Python standard `os` module

## Usage

```python
import dirwalker
# Search with recursing subdirectories
dirwalker.find_filenames_with_extensions(
    '/Users/me/dev/search_directory',
    ['txt', '.csv'])
# Search without recursing subdirectories
dirwalker.find_filenames_with_extensions(
    '/Users/me/dev/search_directory',
    ['txt', '.csv'],
    recurse=False)
```

## Contributing

[dirwalker][] is developed using [Scott Chacon][]'s [GitHub Flow][]. To
contribute, fork [dirwalker][], create a feature branch, and then submit
a pull request.  [GitHub Flow][] is summarized as:

- Anything in the `master` branch is deployable
- To work on something new, create a descriptively named branch off of
  `master` (e.g., `new-oauth2-scopes`)
- Commit to that branch locally and regularly push your work to the same
  named branch on the server
- When you need feedback or help, or you think the branch is ready for
  merging, open a [pull request][].
- After someone else has reviewed and signed off on the feature, you can
  merge it into master.
- Once it is merged and pushed to `master`, you can and *should* deploy
  immediately.


# License

[dirwalker] is released under the MIT license. Please see the
[LICENSE.txt] file for more information.

[coveralls image]: https://img.shields.io/coveralls/questrail/dirwalker.svg
[coveralls link]: https://coveralls.io/r/questrail/dirwalker
[dirwalker]: https://github.com/questrail/dirwalker
[github flow]: http://scottchacon.com/2011/08/31/github-flow.html
[LICENSE.txt]: https://github.com/questrail/dirwalker/blob/master/LICENSE.txt
[license image]: http://img.shields.io/pypi/l/dirwalker.svg
[pull request]: https://help.github.com/articles/using-pull-requests
[pypi ver image]: http://img.shields.io/pypi/v/dirwalker.svg
[pypi ver link]: https://pypi.python.org/pypi/dirwalker/
[scott chacon]: http://scottchacon.com/about.html
[sdf guide]: http://cp.literature.agilent.com/litweb/pdf/5963-1715.pdf
[travis image]: http://img.shields.io/travis/questrail/dirwalker/master.svg
[travis link]: https://travis-ci.org/questrail/dirwalker
