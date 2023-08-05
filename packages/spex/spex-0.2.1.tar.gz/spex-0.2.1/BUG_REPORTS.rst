Submitting bug reports
######################

Spex uses voodoo and tricks to make itself work, somethings these things break.

If a test fails
---------------
When tests fail, please capture the following from the test suite

```
GLOB sdist-make: /home/greg/work/spex/setup.py
py27 inst-nodeps: /home/greg/work/spex/.tox/dist/spex-0.1.0.zip
py27 runtests: PYTHONHASHSEED='3431726178'
```

This should let us reproduce test-case failures
