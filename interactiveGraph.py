import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from Equation import Equation

# ____________________________________________________________________________________________
#
class InteractiveGraph:
    """
    ABOUT
    -----
    Class to automatically create code snippets in JS for the website.
    Also allows for python plots.

    
    EXAMPLE
    -------
    The input format is the following:
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
    ---
    The output format is the following:
        SliderGraph({
        equation: function(x, a){
            var hbar = 6.63e-34 / 6.28;
            var c = 3e8;
            var kB = 1.38064852e-23;
            var G = 6.67e-11;
            var b = 45 / 16 / Math.pow(3.14159, 3) * Math.pow(hbar, 3) * Math.pow(c, 5) / G / Math.pow(kB, 4);
            var f = Math.pow(b / a, .25) ;
            var y = Math.pow( Math.pow(10, x) * 365.25 * 86400, -0.5);
            return Math.log10(y * f);
        },
        limits: {
            xmin: 1.,
            xmax: 6.,
            ymin: 3.,
            ymax: 7.
        },
        domain: {
            xmin: 1.,
            xmax: 10.
        },
        axes: {
            x: 'log(t / years)',
            y: 'log(T / K)'
        },
        startPoint: 3,
        sampleSize: 500
        });
    """
    def __init__(self, equation, xmin = None, xmax = None, ymin = None, ymax = None, vmin = -1e10, vmax = 1e10, xLabel = 'x', yLabel = 'y', startPoint = 0, sampleSize = 300, scale = 'lin'):
        """
        ABOUT
        ------
        Initialise the class.

        INPUT
        -----
          equation: instance of Equation object
          (x,y)min, (x,y)max: limits for the canvas
          vmin, vmax: limits of parametersfor slider
          (x, y)label: labels x and y
          startPoint: default position of slider
          sampleSize: number of points to sample the curve
          scale: 
        """
        if scale == 'log':
            xmin, xmax = np.log10(xmin), np.log10(xmax)
            ymin, ymax = np.log10(ymin), np.log10(ymax)
        self.equation = equation
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        self.vmin = vmin
        self.vmax = vmax
        self.xAxisLabel = xLabel
        self.yAxisLabel = yLabel
        self.startPoint = startPoint
        self.sampleSize = sampleSize
        self.scale = scale
        self.setBase()
        self.setEquation()
        self.setLimits()
        self.setDomain()
        self.setAxes()
        self.setSlider()

    def setBase(self, strBaseBegin = '', strBaseEnd = ''):
        """
        ABOUT
        -----
        Define base strings for the JS code.

        INPUT
        -----
          strBaseBegin: custom strBaseBegin member
          strBaseEnd: custom strBaseEnd member

        OUTPUT
        ------
        Example:
          SliderGraph({
            ...
            ...
          });
        """ 
        if strBaseBegin == '':
            self.strBaseBegin  = 'SliderGraph({\n'
        else:
            self.strBaseBegin = strBaseBegin

        if strBaseEnd == '':
            self.strBaseEnd = '});'
        else:
            self.strBaseEnd = strBaseEnd

    def setEquation(self, strEquation = ''):
        """
        ABOUT
        -----
        Define base strings for the JS code.

        INPUT
        -----
          strEquation: string containing equation.

        OUTPUT
        ------
        Example:
          equation: function(x, a){
            var a = 0;
            var b = 1;
            return x * a + b**2 - x**2;
          },
        """ 
        if strEquation == '':
            variable = self.equation.variables[0]
            parameter = self.equation.parameters[0]
            self.strEquation = '    equation: function(%s, %s){\n' % (variable, parameter)
            self.strEquation += self.equation.convert2JS()
            self.strEquation += '    }, \n'
        else:
            self.strEquation = strEquation

    def setLimits(self, xmin = None, xmax = None, ymin = None, ymax = None):
        """
        ABOUT
        -----
        Set the limits of the frame wherein the graph will be plotted.

        INPUT
        -----
          xmin, xmax, ymin, ymax: limits of the frame

        OUTPUT
        ------
        Example
          limits: {
              xmin: -1,
              xmax: +1,
              ymin: -1,
              ymax: +1
          },
        """
        self.strLimits  = '    limits: {\n'

        if xmin == None:
            self.strLimits += '        xmin: %f, \n' % self.xmin
        else:
            self.strLimits += '        xmin: %f, \n' % xmin

        if xmax == None:
            self.strLimits += '        xmax: %f, \n' % self.xmax
        else:
            self.strLimits += '        xmax: %f, \n' % xmax

        if ymin == None:
            self.strLimits += '        ymin: %f, \n' % self.ymin
        else:
            self.strLimits += '        ymin: %f, \n' % ymin

        if ymax == None:
            self.strLimits += '        ymax: %f \n' % self.ymax
        else:
            self.strLimits += '        ymax: %f \n' % ymax

        self.strLimits += '    }, \n'

    def setDomain(self, xmin = None, xmax = None):
        """
        ABOUT
        -----
        Set the domain of the function in order to avoid plotting problems.

        INPUT
        -----
          xminDomain, xmaxDomain: domain of the function to be plotted

        OUTPUT
        ------
        Example
          domain: {
              xmin: -1,
              xmax: +1
          },
        """
        self.strDomain  = '    domain: {\n'

        if xmin == None:
            self.strDomain += '        xmin: %f, \n' % self.vmin
        else:
            self.strDomain += '        xmin: %f, \n' % xmin
        if xmax == None:
            self.strDomain += '        xmax: %f \n' % self.vmax
        else:
            self.strDomain += '        xmax: %f \n' % xmax

        self.strDomain += '    }, \n'
  
    def setAxes(self, xAxisLabel = '', yAxisLabel = ''):
        """
        ABOUT
        -----
        Set the axes name.

        INPUT
        -----
          xAxisLabel, yAxisLabel: name of axes

        OUTPUT
        ------
        Example
          axes: {
              x: 'x-axis',
              y: 'y-axis'
          },
        """
        self.strAxes  = '    axes: {\n'
        if xAxisLabel == '':
            self.strAxes += '        x: \'%s\', \n' % self.xAxisLabel
        else:
            self.strAxes += '        x: \'%s\', \n' % xAxisLabel
        if yAxisLabel == '':
            self.strAxes += '        y: \'%s\'  \n' % self.yAxisLabel
        else:
            self.strAxes += '        y: \'%s\'  \n' % yAxisLabel
        self.strAxes += '    }, \n'

    def setSlider(self, startPoint = None, sampleSize = 0):
        """
        ABOUT
        -----
        Set slider properties.

        INPUT
        ------
          startPoint: default position of slider
          sampleSize: number of points to sample the curve

        OUTPUT
        -------
          startPoint: 0, 
          sampleSize: 300
        """

        self.strSlider = '    startPoint: %i, \n' % self.startPoint
        self.strSlider = '    sampleSize: %i \n' % self.sampleSize

    def assembleJS(self):
        """
        ABOUT
        -----
        Assembles the parts of the JS SliderGraph object.
        """
        self.scriptJS = self.strBaseBegin + self.strEquation + self.strLimits + self.strDomain + self.strAxes + self.strSlider + self.strBaseEnd
        return self.scriptJS

    def plotStaticPyGraph(self, a, batch = False, outputName = ''):
        """
        ABOUT
        -----
        Plot a python graph for a given value of the parameter a.

        INPUT
        -----
          a: parameter of the slide
          batch: if False, displays the graph
          outputName: name of the output file containing the graph

        OUTPUT
        ------
          Nothing is returned.
        """
        if self.scale == 'log':
            x = np.linspace(np.log10(self.xmin), np.log10(self.xmax), self.sampleSize)
            y = np.log10(self.equation.function(10**x, a))
        else:
            x = np.linspace(self.xmin, self.xmax, self.sampleSize)
            y = self.equation.function(x, a) 
        plt.plot(x, y)
        plt.xlabel(self.xAxisLabel)
        plt.ylabel(self.yAxisLabel)
        plt.axis([self.xmin, self.xmax, self.ymin, self.ymax])
        if outputName != '':
            plt.savefig(outputName)
        if not batch:
            plt.show()

    def plotInteractivePyGraph(self, a0 = 0):
        """
        ABOUT
        -----
          Plot python interactive graph with slider.

        INPUT
        -----

        OUTPUT
        ------
        """
        if self.scale == 'log':
            x = np.linspace(np.log10(self.xmin), np.log10(self.xmax), self.sampleSize)
            y = np.log10(self.equation.function(10**x, a0))
        else:
            x = np.linspace(self.xmin, self.xmax, self.sampleSize)
            y = self.equation.function(x, a0) 

        fig, ax = plt.subplots()
        plt.subplots_adjust(left = 0.25, bottom = 0.25)
        l, = plt.plot(x, y)
        plt.axis([self.xmin, self.xmax, self.ymin, self.ymax])
        plt.xlabel(self.xAxisLabel)
        plt.ylabel(self.yAxisLabel)

        aSlider = plt.axes([0.25, 0.10, 0.65, 0.03])
        sliderLabel = self.equation.parameters[0]
        slider = Slider(aSlider, sliderLabel, self.vmin, self.vmax, valinit = a0)

        def update(a):
            y = self.equation.function(x, a) 
            l.set_ydata(y)
            fig.canvas.draw_idle()
        slider.on_changed(update)
        
        plt.show()

# ____________________________________________________________________________________________
#
def test():
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
