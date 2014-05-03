from __future__ import print_function
from pprint import pprint
import sys
sys.path.append( 'external/pycparser' )
from pycparser import c_parser, c_ast, parse_file

# Portable cpp path for Windows and Linux/Unix
CPPPATH = '../utils/cpp.exe' if sys.platform == 'win32' else 'cpp'

class IdVisitor(c_ast.NodeVisitor):
    def __init__(self):
        self.idList_ = []
    def visit_ID(self, node):
        self.idList_.append( node.name )

def idDefs(filename):
    ast = parse_file(
        filename,
        use_cpp=True,
        cpp_path=CPPPATH, 
        cpp_args=[ "-nostdinc" ]
    )
    # c.f. http://stackoverflow.com/questions/10353902/any-way-to-get-the-c-preproccessor-to-ignore-all-includes 
    v = IdVisitor()
    v.visit(ast)
    print( v.idList_ )

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = 'c_files/hash.c'
    idDefs(filename)

