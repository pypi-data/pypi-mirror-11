This is a place for Python module and NVDA plugin.

Python module is distributed as Python wheel and
can be built as following.

## Windows wheel

 1. Build RHVoice.dll
 2. Copy RHVoice to this folder
 3. Install wheel

        py -2 -m pip install wheel

        python setup.py bdist_wheel

        # need to create setup.py first
        # [ ] find a way to pack RHVoice.dll there


