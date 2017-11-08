import numpy as np
from inspect import getsourcelines

# ____________________________________________________________________________________________
#
class Equation:
    """
    ABOUT
    -----
    Python equation to be used for the plotting.

    EXAMPLE
    --------
      def f(t, csi):
          b = 1.2
          c = .4
          return csi + b * t + c * t * t
  
      eq = Equation(f, ['t'], ['csi', 'b', 'c'])
      jsEq = eq.convert2JS()
    """
    def __init__(self, f, variables, parameters):
        """
        ABOUT
        -----
        Declare equation with its variable and parameters.
        Note that for now 

        INPUT
        -----
          variables: array of strings containing the name of the variables (for now just one)
          parameters: array of strings containing the names of the parameters to be varied (for now just one)
        """
        self.function = f
        self.variables = variables
        self.parameters = parameters
        self.functionStr = self.ConvertFunctionToString()

    def __str__(self):
        """
        """
        return self.functionStr

    def convertFunctionToString(self):
        """
        ABOUT
        -----
        Converts a function to its associated function.

        INPUT
        -----

        OUTPUT
        -----
        String corresponding to function.
        This string could simply be written into another file for later execution.
        """
        lines = getsourcelines(self.function)[0]
        res = ''
        for line in lines:
            res += line
        return res

    def convert2JS(self, indentation = '    ', newIndentation = '        '):
        """
        ABOUT
        ------
        Function to convert the notation from numpy to JS.
        Important conventions:
          - always use numpy or math namespaces
          - numpy functions are always named "np.func"
          - one constant per line in the beginning of the file for naming convention
          - f should be clean and indented accordingly (4 spaces by default)

        INPUT
        ------
          indentation: size of indentation (default = 4)

        OUTPUT
        ------
        Convert function to Java Script-style function for the website.
        """
        lines = getsourcelines(self.function)[0]
    

        # Create a dictionary to convert np notation to js notation
        py2jsDict = {}
        functions1 = ['sqrt', 'log10',  'sin', 'cos', 'tan', 'atan2', 'acos', 'asin', 'exp', 'abs', 'log(', 'atan(']
        for f in functions1:
            py2jsDict['np.%s' % f] = 'Math.%s' % f
        py2jsDict['pow'] = 'Math.pow'
        py2jsDict['np.pi'] = 'Math.PI'
        py2jsDict['np.e'] = 'Math.E'
        
        res = ''
        for i, line in enumerate(lines):
            if 'def' not in line:
                if indentation in line and 'return' not in line: # skip def
                    line = line.replace(indentation, '').replace('\n', '')
                    res += '%svar %s;\n' % (newIndentation, line)
                if indentation in line and 'return' in line: 
                    line = line.replace(indentation, '').replace('\n', '')
                    res += '%s%s;\n' % (newIndentation, line)

        for key in py2jsDict.keys():
            if key in res:
                res = res.replace(key, py2jsDict[key])

        return res
