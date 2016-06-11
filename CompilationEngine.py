# responsible for

from JackTokenizer import JackTokenizer
operators = ['+', '-', '*', '/', '&amp;', '|', '&lt;', '&gt;', '=']
keyword_const = ["true" , "false", "null", "this"]

class CompilationEngine:

    def __init__(self, inputFile, outputFile):
        self.XMLFile = open(outputFile, 'w')
        self.tokenizer = JackTokenizer(inputFile)
        self.CompileClass()

    def __writeToken(self, token, value):
        self.XMLFile.write("<" + token + "> " + value + " </" + token + ">\n")

    def CompileClass(self):
        self.XMLFile.write("<class>\n")
        self.__writeToken("keyword", self.tokenizer.keyWord())
        self.tokenizer.advance()
        self.__writeToken("identifier", self.tokenizer.identifier())
        self.tokenizer.advance()
        self.__writeToken("symbol", self.tokenizer.symbol())
        self.tokenizer.advance()

        while self.tokenizer.keyWord() == "static" or self.tokenizer.keyWord() == "field":
            self.CompileClassVarDec()

        while self.tokenizer.keyWord() == "constructor" or self.tokenizer.keyWord() == "function" or self.tokenizer.keyWord() == "method":
            self.CompileSubroutine()

        self.__writeToken("symbol", self.tokenizer.symbol())
        self.tokenizer.advance()
        self.XMLFile.write("</class>\n")

    def CompileClassVarDec(self):
        self.XMLFile.write("<classVarDec>\n")

        self.__writeToken("keyword", self.tokenizer.keyWord())
        self.tokenizer.advance()
        self.compileType()
        self.__writeToken("identifier", self.tokenizer.identifier())
        self.tokenizer.advance()

        # add the rest of var names, if there are
        while self.tokenizer.symbol() == ",":
            self.__writeToken("symbol", self.tokenizer.symbol())
            self.tokenizer.advance()
            self.__writeToken("identifier", self.tokenizer.identifier())
            self.tokenizer.advance()

        self.__writeToken("symbol", self.tokenizer.symbol())
        self.tokenizer.advance()
        self.XMLFile.write("</classVarDec>\n")

    def CompileSubroutine(self):
        self.XMLFile.write("<subroutineDec>\n")

        # constructor | function | method
        self.__writeToken("keyword", self.tokenizer.keyWord())
        self.tokenizer.advance()

        # void | type
        self.compileType()

        # subrotineName
        self.__writeToken("identifier", self.tokenizer.identifier())
        self.tokenizer.advance()

        # ( parameterList )
        self.__writeToken("symbol", self.tokenizer.symbol())
        self.tokenizer.advance()
        self.compileParameterList()
        self.__writeToken("symbol", self.tokenizer.symbol())
        self.tokenizer.advance()

        # subrotineBody
        self.compileSubroutineBody()

        self.XMLFile.write("</subroutineDec>\n")

    def compileParameterList(self):
        self.XMLFile.write("<parameterList>\n")
        if self.tokenizer.tokenType() != 1:

            # type varName
            self.compileType()
            self.__writeToken("identifier", self.tokenizer.identifier())
            self.tokenizer.advance()

            # (, type varName)*
            while self.tokenizer.symbol() == ",":
                self.__writeToken("symbol", self.tokenizer.symbol())
                self.tokenizer.advance()
                self.compileType()
                self.__writeToken("identifier", self.tokenizer.identifier())
                self.tokenizer.advance()

        self.XMLFile.write("</parameterList>\n")

    def compileSubroutineBody(self):
        self.XMLFile.write("<subroutineBody>\n")
        # {
        self.__writeToken("symbol", self.tokenizer.symbol())
        self.tokenizer.advance()

        # varDec*
        while self.tokenizer.keyWord() == "var":
            self.compileVarDec()

        # statements
        self.compileStatements()

        # }
        self.__writeToken("symbol", self.tokenizer.symbol())
        self.tokenizer.advance()

        self.XMLFile.write("</subroutineBody>\n")

    def compileVarDec(self):
        self.XMLFile.write("<varDec>\n")

        # var
        self.__writeToken("keyword", self.tokenizer.keyWord())
        self.tokenizer.advance()

        # type
        self.compileType()

        # varName
        self.__writeToken("identifier", self.tokenizer.identifier())
        self.tokenizer.advance()

        # (, varName)*
        while self.tokenizer.symbol() == ",":
            self.__writeToken("symbol", self.tokenizer.symbol())
            self.tokenizer.advance()
            self.__writeToken("identifier", self.tokenizer.identifier())
            self.tokenizer.advance()

        # ;
        self.__writeToken("symbol", self.tokenizer.symbol())
        self.tokenizer.advance()

        self.XMLFile.write("</varDec>\n")

    def compileStatements(self):
        self.XMLFile.write("<statements>\n")
        while self.tokenizer.tokenType() == 0:
            if self.tokenizer.keyWord() == "let":
                self.compileLet()
            elif self.tokenizer.keyWord() == "if":
                self.compileIf()
            elif self.tokenizer.keyWord() == "while":
                self.compileWhile()
            elif self.tokenizer.keyWord() == "do":
                self.compileDo()
            elif self.tokenizer.keyWord() == "return":
                self.compileReturn()
        self.XMLFile.write("</statements>\n")

    def compileDo(self):
        self.XMLFile.write("<doStatement>\n")

        # do
        self.__writeToken("keyword", self.tokenizer.keyWord())
        self.tokenizer.advance()

        self.compileSubRoutineCall()

        # ;
        self.__writeToken("symbol", self.tokenizer.symbol())
        self.tokenizer.advance()

        self.XMLFile.write("</doStatement>\n")

    def compileLet(self):
        self.XMLFile.write("<letStatement>\n")

        # let
        self.__writeToken("keyword", self.tokenizer.keyWord())
        self.tokenizer.advance()

        # varName
        self.__writeToken("identifier", self.tokenizer.identifier())
        self.tokenizer.advance()

        # ([ expression ])?
        if self.tokenizer.symbol() == "[":
            self.__writeToken("symbol", self.tokenizer.symbol())
            self.tokenizer.advance()
            self.CompileExpression()
            self.__writeToken("symbol", self.tokenizer.symbol())
            self.tokenizer.advance()

        # =
        self.__writeToken("symbol", self.tokenizer.symbol())
        self.tokenizer.advance()

        # expression
        self.CompileExpression()

        # ;
        self.__writeToken("symbol", self.tokenizer.symbol())
        self.tokenizer.advance()

        self.XMLFile.write("</letStatement>\n")

    def compileWhile(self):
        self.XMLFile.write("<whileStatement>\n")

        # while
        self.__writeToken("keyword", self.tokenizer.keyWord())
        self.tokenizer.advance()

        # ( expression )
        self.__writeToken("symbol", self.tokenizer.symbol())
        self.tokenizer.advance()
        self.CompileExpression()
        self.__writeToken("symbol", self.tokenizer.symbol())
        self.tokenizer.advance()

        # {
        self.__writeToken("symbol", self.tokenizer.symbol())
        self.tokenizer.advance()

        # statements
        self.compileStatements()

        # }
        self.__writeToken("symbol", self.tokenizer.symbol())
        self.tokenizer.advance()

        self.XMLFile.write("</whileStatement>\n")

    def compileReturn(self):
        self.XMLFile.write("<returnStatement>\n")

        # return
        self.__writeToken("keyword", self.tokenizer.keyWord())
        self.tokenizer.advance()

        # expression?
        # if (self.tokenizer.tokenType() != 1 and self.tokenizer.symbol() != ";") \
        #         or (self.tokenizer.tokenType() == 1 and (self.tokenizer.symbol() == "-" or self.tokenizer.symbol() == "~")):
        if self.isTerm():
            self.CompileExpression()

        # ;
        self.__writeToken("symbol", self.tokenizer.symbol())
        self.tokenizer.advance()

        self.XMLFile.write("</returnStatement>\n")

    def compileIf(self):
        self.XMLFile.write("<ifStatement>\n")
        #if
        self.__writeToken("keyword", self.tokenizer.keyWord())
        self.tokenizer.advance()
        # ( expression )
        self.__writeToken("symbol", self.tokenizer.symbol())
        self.tokenizer.advance()
        self.CompileExpression()
        self.__writeToken("symbol", self.tokenizer.symbol())
        self.tokenizer.advance()

        # { statements }
        self.__writeToken("symbol", self.tokenizer.symbol())
        self.tokenizer.advance()
        self.compileStatements()
        self.__writeToken("symbol", self.tokenizer.symbol())
        self.tokenizer.advance()

        if self.tokenizer.tokenType() == 0 and self.tokenizer.keyWord() == "else":
            # else
            self.__writeToken("keyword", self.tokenizer.keyWord())
            self.tokenizer.advance()

            # { statements }
            self.__writeToken("symbol", self.tokenizer.symbol())
            self.tokenizer.advance()
            self.compileStatements()
            self.__writeToken("symbol", self.tokenizer.symbol())
            self.tokenizer.advance()

        self.XMLFile.write("</ifStatement>\n")

    def CompileExpression(self):
        self.XMLFile.write("<expression>\n")
        #term
        self.CompileTerm()
        # (op term)*
        while self.tokenizer.tokenType() == 1 and self.tokenizer.symbol() in operators :
            self.__writeToken("symbol", self.tokenizer.symbol())
            self.tokenizer.advance()
            self.CompileTerm()

        self.XMLFile.write("</expression>\n")

    def CompileTerm(self):
        self.XMLFile.write("<term>\n")
        if self.tokenizer.tokenType() == 3:
            self.__writeToken("integerConstant", self.tokenizer.intVal())
            self.tokenizer.advance()

        elif self.tokenizer.tokenType() == 4:
            self.__writeToken("stringConstant", self.tokenizer.stringVal())
            self.tokenizer.advance()

        elif self.tokenizer.tokenType() == 0:
            self.__writeToken("keyword", self.tokenizer.keyWord())
            self.tokenizer.advance()

        elif self.tokenizer.tokenType() == 2:

            if self.tokenizer.tokens[self.tokenizer.currentToken +1] == '[':
                self.__writeToken("identifier", self.tokenizer.identifier())
                self.tokenizer.advance()
                # [ expression ]
                self.__writeToken("symbol", self.tokenizer.symbol())
                self.tokenizer.advance()
                self.CompileExpression()
                self.__writeToken("symbol", self.tokenizer.symbol())
                self.tokenizer.advance()

            elif self.tokenizer.tokens[self.tokenizer.currentToken +1] == '(' or self.tokenizer.tokens[self.tokenizer.currentToken +1] == '.':
                self.compileSubRoutineCall()

            else :
                self.__writeToken("identifier", self.tokenizer.identifier())
                self.tokenizer.advance()
        elif self.tokenizer.tokenType() == 1 and self.tokenizer.symbol() == '(':
            # ( expression )
            self.__writeToken("symbol", self.tokenizer.symbol())
            self.tokenizer.advance()
            self.CompileExpression()
            self.__writeToken("symbol", self.tokenizer.symbol())
            self.tokenizer.advance()
        else:
            self.__writeToken("symbol", self.tokenizer.symbol())
            self.tokenizer.advance()
            self.CompileTerm()

        self.XMLFile.write("</term>\n")



    def compileSubRoutineCall(self):
        # subroutineName  | (className | varName)
        self.__writeToken("identifier", self.tokenizer.identifier())
        self.tokenizer.advance()

        if self.tokenizer.symbol() == '(':
            # ( expressionList )
            self.__writeToken("symbol", self.tokenizer.symbol())
            self.tokenizer.advance()
            self.CompileExpressionList()
            self.__writeToken("symbol", self.tokenizer.symbol())
            self.tokenizer.advance()
        else:
            # .
            self.__writeToken("symbol", self.tokenizer.symbol())
            self.tokenizer.advance()

            # subroutineName
            self.__writeToken("identifier", self.tokenizer.identifier())
            self.tokenizer.advance()

            # ( expressionList )
            self.__writeToken("symbol", self.tokenizer.symbol())
            self.tokenizer.advance()
            self.CompileExpressionList()
            self.__writeToken("symbol", self.tokenizer.symbol())
            self.tokenizer.advance()

    def CompileExpressionList(self):
        self.XMLFile.write("<expressionList>\n")
        # (expression
        if self.isTerm():
            # (, expression)
            self.CompileExpression()
            while self.tokenizer.symbol() == ',':
                self.__writeToken("symbol", self.tokenizer.symbol())
                self.tokenizer.advance()
                self.CompileExpression()
        self.XMLFile.write("</expressionList>\n")

    def isTerm(self):
        if self.tokenizer.tokenType() == 3 or self.tokenizer.tokenType() == 4:
            return True
        if self.tokenizer.tokenType() == 0 and self.tokenizer.keyWord() in keyword_const:
            return True
        if self.tokenizer.tokenType() == 1 and self.tokenizer.symbol() == '(' :
            return True
        if self.tokenizer.tokenType() == 1 and (self.tokenizer.symbol() == '-' or self.tokenizer.symbol() == '~'):
            return True
        if self.tokenizer.tokenType() == 2:
            return True
        return False

    def compileType(self):
        if self.tokenizer.tokenType() == 0:
            self.__writeToken("keyword", self.tokenizer.keyWord())
        else:
            self.__writeToken("identifier", self.tokenizer.identifier())
        self.tokenizer.advance()