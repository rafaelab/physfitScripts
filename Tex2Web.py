import re
import os

# ____________________________________________________________________________________________
#
class TexDoc:
    """
    ABOUT
    -----
    Create LaTeX document from text file containing it's body.
    Plain text and equations should be used.

    EXAMPLE
    --------
    fi = 'latexContent/Test.txt'
    fo = 'latexContent/Test.tex'
    tex = TexDoc(fi, title = 'This is a test', author = 'Rafa')
    tex.createTexFile(outFile = fo)
    tex.compileTexFile()
    b = tex.convertTex2Website()
    print(b)


    CONVENTIONS
    -----------
    Note that the following syntax should be used in the input file:
      
    This ensures that the files are correctly exported to the website.
    The accordion should end with an equation which will be enclosed between [open][/open]
    No sections/subsection should be used, nor styling.
    """
    def __init__(self, fn, title = '', author = '', date = ''):
        """
        ABOUT
        -----

        INPUT
        -----
          fn: filename
        """
        try:
            theFile = open(fn, 'r')
            self.content = theFile.read()
            print('File %s read!' % fn)
        except IOError:
            print('File %s could not be found.' % fn)

        self.title = title
        self.author = author
        if date == '':
            self.date = date
        else:
            self.date = '\\today'
        self.latexContent = ''
        self.webContent = ''

    def createTexFile(self, outFile = ''):
        """
        ABOUT
        -----
        Uses the information provided to create a TeX file.


        INPUT
        -----
          outFile: name of output file to export TeX

        OUTPUT
        -----
          Returns a string containing the TeX content.
          Also saves it in a file if outFile provided.
        """
        preamble = ''
        preamble += '\\documentclass[12pt]{article}\n'
        preamble += '\\usepackage{amsmath}\n'
        preamble += '\\usepackage{amssymb}\n'
        preamble += '\n\n'

        docInfo = ''
        docInfo += '\\title{%s}\n' % self.title
        docInfo += '\\author{%s}\n' % self.author
        docInfo += '\\date{%s}\n' % self.date
        docInfo += '\n'

        beginDoc = ''
        beginDoc += '\\begin{document}\n'
        beginDoc += '\\maketitle\n'
        beginDoc += '\n'

        endDoc = ''
        endDoc += '\n'
        endDoc += '\\end{document}\n'

        body = self.content

        self.latexContent = preamble + docInfo + beginDoc + body + endDoc
        
        self.latexFile = outFile
        fo = open(self.latexFile, 'w')
        fo.write(self.latexContent)

        return self.latexContent

    def compileTexFile(self, outFile = '', cleanup = True):
        """
        ABOUT
        -----
        Compile the TeX file generated with the function createTexFile.
        
        INPUT
        -----
          cleanup: whether to clean up the folder after generating the pdf.
          outFile: name of pdf output (if different from input latex file)
        """
        if self.latexContent == '':
            self.createTexFile()

        cmd1 = 'pdflatex -interaction=batchmode %s' %  self.latexFile
        os.system(cmd1)
        os.system(cmd1)
        print(cmd1)

        if cleanup:
            auxFiles = ['.log', '.end', '.dvi', '.aux', '.toc', '.nav', '.snm', '.out', '.blg']        
            for x in auxFiles:
                os.system('rm -f *%s' % x)

        if outFile != '':
            cmd2 = 'mv %s %s' % (self.latexFile, outFile)
            os.system(cmd2)

    def convertTex2Website(self):
        """
        ABOUT
        -----
        Uses the information provided to create a TeX file.

        INPUT
        -----

        OUTPUT
        -----
        String containing content to be copied to the website.
        It is also stored as a property of the class.
        """
        accordionTitle = re.findall(r'\[\[(.*?)\]\]', self.content)

        webContent = ''
        accordionCounter = 0
        for line in self.content.splitlines():
            if 'fbox'in line:
                webContent += ''
            elif 'begin{minipage}' in line:
                webContent += '[accordion title=\"%s\"]' % accordionTitle[accordionCounter]
                accordionCounter += 1
            elif 'end{minipage}' in line:
                webContent += '[/accordion]'
            elif 'begin{equation}' in line and '%[open]' in line:
                webContent += '[open]\n'
                webContent += '\\begin{equation}'
            else:
                if '{center}' not in line:
                    webContent += line
            webContent += '\n'
        webContent = webContent.replace('[/accordion]', '[/open]\n[/accordion]')

        self.webContent = webContent

        return webContent


# ____________________________________________________________________________________________
#

