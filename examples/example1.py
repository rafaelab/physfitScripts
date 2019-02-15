import sys
sys.path.insert(0, '../../')

from physfitScripts.interactiveGraph import InteractiveGraph
from physfitScripts.equation import Equation

# ____________________________________________________________________________________________
#
def testInteractiveGraph():
    """
    Simple test
    """        
    def f(t, csi):
        b = 1.2
        c = .4
        return csi + b * t + c * t * t

    eq = Equation(f, ['t'], ['csi', 'b', 'c'])
    g = InteractiveGraph(eq, xmin = -5, xmax = 5, ymin = -10, ymax = 10, vmin = -5, vmax = 5, scale = 'lin')
    g.plotInteractivePyGraph()
    g.plotStaticPyGraph(1)
    js = g.assembleJS()
    print(js)

# ____________________________________________________________________________________________
#
if __name__ == '__main__':
    testInteractiveGraph()