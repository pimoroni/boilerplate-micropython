# Boilerplate MicroPython

A starting point for a `mip`-installable MicroPython library that is also
published to PyPI, and so installable from Thonny's Tools -> Manage Packages.

## Getting Started

Rename `src/boilerplate.py` and the class inside it, then update the name and
`[tool.hatch.version]` path in `pyproject.toml`, the URL in `package.json`, and
the imports in `tests/`.

Install the development dependencies and the pre-commit hooks with:

```
make dev-deps
```

`make` on its own lists the other targets.

## Layout

A single-file driver lives at `src/<name>.py`, which is what `mip` installs and
what the wheel exposes as a top-level module. A driver needing more than one
file just adds them alongside; `make package.json` picks up everything in
`src/`.

## package.json

Describes the package to `mip`. The format is documented at
https://docs.micropython.org/en/latest/reference/packages.html#writing-publishing-packages

`make package.json` regenerates the file from the contents of `src/`. It
preserves any `deps` you have added by hand, which is how one library depends on
another:

```json
"deps": [
  ["github:pimoroni/ioexpander-micropython", "main"]
]
```

Its version has to match the library version. `make check` enforces this, as
does the publish workflow.

## pyproject.toml

Describes the Python package, which is built with `uv build` and published to
PyPI. It also holds the ruff, codespell and check-manifest settings.

## Tests

Tests run under CPython, not MicroPython. `tests/conftest.py` mocks the
`machine` and `micropython` modules and adds MicroPython's `ticks_ms` and
`sleep_ms` family to CPython's `time`, so a driver can be exercised unmodified.

Model the device's register file in a fake i2c or SPI object and assert against
it, rather than mocking the driver's own calls. `tests/test_setup.py` has a
starting point.

## QA

`make pre-commit` runs ruff, codespell and the whitespace hooks. `make qa` runs
the packaging checks: check-manifest, a build, and twine. Both run in CI, along
with the tests.

## Publishing

`.github/workflows/publish.yml` builds and uploads on a published release, using
PyPI trusted publishing. It needs a pending publisher configured on PyPI for the
project, pointing at this repository, the `publish.yml` workflow and the `pypi`
environment, and that environment has to exist in the repository settings.
