import sys
import os
import hashlib
import pickle
import os
import subprocess

from IPython.core.error import UsageError
from IPython.core.magic import Magics, magics_class, cell_magic

memopath = os.path.join(os.getcwd(), 'xmemo')


def hash_anything(x):
    return hashlib.sha256(pickle.dumps(x)).hexdigest()

def file_is_pointer_file(x):
    if os.path.exists(x):
        with open(x, 'rb') as f:
            rl = f.readline()
            return rl.startswith(b"# xet version 0")
    else:
        return False

def materialize_pointer_file(x):
    print(f"Materializing {x}.pickle")
    try:
        subprocess.run(["git-xet", "materialize", x], check=True)
        return True
    except:
        print(f"A memorized file exists at {x}, but we are unable to materialize it. Falling back to executing the cell normally")
        return False
    
@magics_class
class XMemoMagics(Magics):
    """Memoization for python variables.

    Provides the %xmemo magic."""

    @cell_magic
    def xmemo(self, line, cell):
        '''
        putting 

           %%xmemo input=v1,v2 output=v3,v4

        will pickle/memoize the output variables at the end of execution.
        Any content changes to the inputs, or cell code will force reevaluation
        of the cell. Otherwise the outputs will simply be unpickled from the memo.

        Note the python hash is used to identify changes. This may not be completely
        reliable for all purposes. The memo is stored in the xmemo/ directory
        '''
        # parse the argument list
        args = line.strip().split(' ')
        inputvars = []
        outputvars = []
        ip = self.shell
        
        for arg in args:
            k,v = arg.split('=')
            if k == 'input':
                inputvars = [x.strip() for x in v.split(',')]
            elif k == 'output':
                outputvars = [x.strip() for x in v.split(',')]
            else:
                raise RuntimeError(f'Unexpected xmemo key type {k}')
       
        inputhashes = [hash_anything(line), hash_anything(cell)] + [hash_anything(ip.ev(i)) for i in inputvars]
        inputhashstr = hash_anything(inputhashes)
        memo_file = os.path.join(memopath, inputhashstr + '.pickle')
        try:
            if os.path.exists(memo_file):
                if file_is_pointer_file(memo_file):
                    materialize_pointer_file(memo_file)
                with open(memo_file, 'rb') as f:
                    print(f"Loading from {inputhashstr}.pickle")
                    ovars = {v:pickle.load(f) for v in outputvars}
                    for k,v in ovars.items():
                        ip.user_ns[k] = v
                    return
        except:
            pass

        ret = ip.run_cell(cell)
        if ret.success:
            os.makedirs(memopath, exist_ok=True)
            with open(memo_file, 'wb') as f:
                for v in outputvars:
                    pickle.dump(ip.user_ns[v], f)

   
def load_ipython_extension(ip):
    """Load the extension in IPython."""
    ip.register_magics(XMemoMagics) 

#def load_ipython_extension(shell):
#    '''Registers the skip magic when the extension loads.'''
#    shell.register_magic_function(xmemo, 'line_cell')

#def unload_ipython_extension(shell):
#    '''Unregisters the skip magic when the extension unloads.'''
#    del shell.magics_manager.magics['cell']['xmemo']
