﻿#                    _       ____    ____  _______
#                   / \     |_   \  /   _||_   __ \
#                  / _ \      |   \/   |    | |__) |
#                 / ___ \     | |\  /| |    |  ___/ 
#               _/ /   \ \_  _| |_\/_| |_  _| |_ 
#              |____| |____||_____||_____||_____|
# 
#                Automatic Mathematical Parser
#                       By Ini Oguntola
#
# Parses and evaluates any numerical mathematical expression, 
# with support for complex numbers and mathematical constants, as well 
# as scientific notation and a wide range of mathematical functions.

import math
import cmath
import decimal
import funcEval

precision = 12
funcEval.precision = precision
_operatorSet = {"+", "-", "*", "/", "%", "^", "!"}
_digits = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}
openBrackets = {"(", "{", "["}
closeBrackets = {")", "}", "]"}

# Private Implementation Helper Methods

def _indexOfSpecificCharacters(string, characters):
        return next((i for i, char in enumerate(string) if char in characters), -1)

def _indexOfSpecificOperators(expression, operators):
        # Skips the first character when searching for operators
        index = _indexOfSpecificCharacters(expression[1:], operators) + 1
        if index == 0:
                return -1
        return index

def _indexOfOperator(expression):
        return _indexOfSpecificOperators(expression, _operatorSet)
        
def _indexOfPreviousCharacters(expression, characters, currentIndex):
        index = -1
        for char in characters:
                if expression[:currentIndex].rfind(char) > index:
                        index = expression[:currentIndex].rfind(char)
        return index
        
def _indexOfPreviousOperator(expression, currentIndex):
        # Iterates until the next index is the index you're looking for, then returns the index of the operator before it
        lastIndex = -1
        nextIndex = _indexOfSpecificOperators(expression, _operatorSet)
        while nextIndex < currentIndex and nextIndex != lastIndex:
                lastIndex = nextIndex
                nextIndex = _indexOfSpecificOperators(expression[nextIndex + 1:], _operatorSet) + nextIndex + 1
                if nextIndex == lastIndex:
                        break
        return lastIndex

def _pemdas(expression, operators):
        while _indexOfSpecificOperators(expression, operators) != -1:
                # Returns the current expression if all that's left is a complex number
                if expression.find(">") > expression.rfind("<"):
                        if expression[0] == "<" and expression[len(expression) - 1] == ">":
                                return expression[1 : len(expression) - 1]
                        elif expression[:2] == "-<" and expression[len(expression) - 1] == ">":
                                return eval("-1*(" + expression[2 : len(expression) - 1] + ")")
                        
                # Finds the next operator of the given type, along with the operators before and after it
                if operators == {"^"}:
                        # Adjusted to account for exponents being right-associative
                        currentIndex = expression.rfind("^")
                        # Keeps precedence of power over unary negation by counting leading minus signs as operators
                        previousIndex = _indexOfPreviousCharacters(expression, _operatorSet, currentIndex)
                else:
                        currentIndex = _indexOfSpecificOperators(expression, operators)
                        previousIndex = _indexOfPreviousOperator(expression, currentIndex)
                currentOperator = expression[currentIndex : currentIndex + 1]
                nextIndex = _indexOfOperator(expression[currentIndex + 1:]) + currentIndex + 1
                if nextIndex == currentIndex:
                        nextIndex = len(expression)

                # Skips previous operator if operator is part of a complex number expression
                if previousIndex != -1 and previousIndex < _indexOfPreviousCharacters(expression, {">"}, currentIndex):
                        previousIndex = _indexOfPreviousCharacters(expression[:expression[:previousIndex].rfind("<")], _operatorSet, previousIndex)

                # Skips current operator if the operator is part of a complex number expression (the +/- in "a +/- bi")
                if expression.find(">") != -1 and _indexOfOperator(expression[expression.find(">"):]) > 0 and currentIndex > expression.find("<") and currentIndex < expression.find(">"):
                        currentIndex = _indexOfOperator(expression[expression.find(">"):]) + expression.find(">")
                        currentOperator = expression[currentIndex : currentIndex + 1]
                        nextIndex = _indexOfOperator(expression[currentIndex + 1:]) + currentIndex + 1
                        if nextIndex == currentIndex:
                                nextIndex = len(expression)
                                
                # Skips next operator if operator is part of a complex number expression
                if expression[currentIndex : nextIndex].find("<") != -1:
                        tempNext = nextIndex + expression[nextIndex:].find(">")
                        nextIndex += _indexOfOperator(expression[expression[nextIndex:].find(">") + nextIndex:]) + expression[nextIndex:].find(">")
                        if nextIndex == tempNext - 1:
                                nextIndex = len(expression)
                             
                # Replaces all "i"s with "j"s to be parsed as complex numbers
                expression = expression[:previousIndex + 1] + expression[previousIndex + 1 : nextIndex].replace("i", "j") + expression[nextIndex:] 

                # Parses the string to find values in the expression at the operator
                firstNum = complex(expression[previousIndex + 1 : currentIndex].replace("<", "").replace(">", "").replace("--", ""))
                secondNum = 0
                try:
                        secondNum = complex(expression[currentIndex + 1 : nextIndex].replace("<", "").replace(">", "").replace("--", ""))
                except:
                        pass
                result = 0

                # Calculates result based on operator and values and substitutes it into the expression
                if currentOperator == "^":
                        result = firstNum ** secondNum
                elif currentOperator == "%":
                        if secondNum == 0:
                                return "Error: Cannot Divide By Zero."
                        result = firstNum + (math.ceil((-firstNum / secondNum).real) + complex(0, 1) * math.ceil((-firstNum / secondNum).imag)) * secondNum
                elif currentOperator == "/":
                        if secondNum == 0:
                                return "Error: Cannot Divide By Zero."
                        result = firstNum / secondNum
                elif currentOperator == "*":
                        result = firstNum * secondNum
                elif currentOperator == "-":
                        result = firstNum - secondNum
                elif currentOperator == "+":
                        result = firstNum + secondNum
                        
                if currentOperator == "!":
                        if firstNum.imag == 0 and firstNum.real < 0 and firstNum.real == int(firstNum.real):
                                return "Error: The factorial function is not defined on the negative integers."
                        result = funcEval.gamma(firstNum + 1)
                        expression = expression[:previousIndex + 1] + ('{0:.' + str(precision + 5) + 'f}').format(result) + expression[currentIndex + 1:]
                else:
                        expression = expression[:previousIndex + 1] + complexFormat(result) + expression[nextIndex:]
        return expression
        
def _format(expression):
        expression = expression.replace(" ", "")
        expression = expression.lower()
        expression = expression.replace("×", "*")
        expression = expression.replace("÷", "/")
        expression = expression.replace("--", "+")
        expression = expression.replace("+-", "-")
        expression = expression.replace(")(", ")*(")
        expression = expression.replace("mod", "%")

        # Substitutes in values for mathematical constants
        for index in xrange(0, len(expression)):
                if expression[index] == "e":
                        if index == 0 and expression[index + 1] in _operatorSet:
                                expression = expression.replace("e", ('{0:.' + str(precision + 5) + 'f}').format(math.e))
                        elif index == len(expression) - 1 and expression[index - 1] in _operatorSet:
                                expression = expression.replace("e", ('{0:.' + str(precision + 5) + 'f}').format(math.e))
                        elif expression[index + 1] in {"+", "-", "*", "/", "%", "^", "!"} and expression[index - 1] in _operatorSet:
                                expression = expression.replace("e", ('{0:.' + str(precision + 5) + 'f}').format(math.e))
                        index += 17
        expression = expression.replace("π", ('{0:.' + str(precision + 5) + 'f}').format(math.pi))
        expression = expression.replace("pi", ('{0:.' + str(precision + 5) + 'f}').format(math.pi))

        expression = noScientificNotation(expression)
        
        # Turns "number(expression)" into "number * (expression)"
        symbols = openBrackets.union({"pi", "π"})
        for digit in _digits:
                for symbol in symbols:
                        expression = expression.replace(digit + symbol, digit + "*" + symbol)

        # Parses mathematical functions
        expression = expression.replace("sine", "sin").replace("cosine", "cos").replace("tangent", "tan")
        expression = expression.replace("cosecant", "csc").replace("secant", "sec").replace("cotangent", "cot")
        expression = expression.replace("arc", "a").replace("sqrt", "sqr")
        expression = funcEval.evaluateFunctions(expression)
        return expression

# Public Methods

def noScientificNotation(expression):
        while expression.find("e") > 0 and expression[expression.find("e") - 1] in _digits:
                        index = expression.find("e")
                        # Separate out coefficient and exponent from scientific notation
                        previousOperatorIndex = _indexOfPreviousOperator(expression, index)
                        nextOperatorIndex = _indexOfOperator(expression[index + 1:])
                        if nextOperatorIndex == -1:
                                nextOperatorIndex = _indexOfSpecificCharacters(expression[index:], closeBrackets)
                                if nextOperatorIndex == -1:
                                        nextOperatorIndex = len(expression)
                                else:
                                        nextOperatorIndex += index 
                        else:
                                nextOperatorIndex += index + 1                                
                        coefficient = float(expression[previousOperatorIndex + 1: index])
                        exponent = float(expression[index + 1 : nextOperatorIndex])

                        # Creates new number as string and substitutes it into the expression, readjusting the index for the iterator
                        newNumber = ('{0:.' + str(precision + 5) + 'f}').format(coefficient * (10 ** exponent))
                        expression = expression[:previousOperatorIndex + 1] + newNumber + expression[nextOperatorIndex:]
                        index = previousOperatorIndex + len(newNumber) + 1
        return expression
        
def complexFormat(complexNum):
        if complexNum.imag == 0:
                return '{0:.15f}'.format(complexNum.real)
        elif complexNum.real == 0:
                return '{0:.15f}'.format(complexNum.imag) + "j"
        else:
                num = "<" + '{0:.15f}'.format(complexNum.real) + "+" + '{0:.15f}'.format(complexNum.imag) + "j>"
                return num.replace("+-", "-")

def numberFormat(num):
        if num.find("Error") != -1:
                return num[num.find("Error") : num[num.find("Error"):].find(".") + num.find("Error")]
        
        # Rounds any decimals, removing trailing zeros and representing integers without decimal points
        num = complex(num.replace("i", "j"))
        if num.imag == 0:
                num = ('{0:.' + str(precision) + 'f}').format(num.real)
                # Remove trailing zeroes
                while num[len(num) - 2] != "." and float(num) == float(num[:-1]):
                        num = num[:-1]
                if float(num) == int(float(num)):
                        num = str(int(float(num)))
                return num
        elif num.real == 0:
                num = ('{0:.' + str(precision) + 'f}').format(num.imag)
                # Remove trailing zeroes
                while num[len(num) - 2] != "." and float(num) == float(num[:-1]):
                        num = num[:-1]
                if float(num) == int(float(num)):
                        num = str(int(float(num)))
                return (num + "i").replace("+1i", "+i").replace("-1i", "-i")
        else:
                real = ('{0:.' + str(precision) + 'f}').format(num.real)
                imag = ('{0:.' + str(precision) + 'f}').format(num.imag)
                # Remove trailing zeroes
                while real[len(real) - 2] != "." and float(real) == float(real[:-1]):
                        real = real[:-1]
                while imag[len(imag) - 2] != "." and float(imag) == float(imag[:-1]):
                        imag = imag[:-1]
                if float(real) == int(float(real)):
                        real = str(int(float(real)))
                if float(imag) == int(float(imag)):
                        imag = str(int(float(imag)))
                num = real + "+" + imag + "i"
                num = num.replace("+-", "-")
                return num.replace("+1i", "+i").replace("-1i", "-i")
                
def eval(expression):
        expression = _format(expression)

        # Parenthesis and Brackets
        while _indexOfSpecificCharacters(expression, closeBrackets) != -1:
                # Finds first close bracket symbol, then finds the preceeding open bracket symbol
                closeBracketIndex = _indexOfSpecificCharacters(expression, closeBrackets)
                openBracketIndex = _indexOfPreviousCharacters(expression, {"(", "{", "["}, closeBracketIndex)
                if openBracketIndex < -1:
                        openBracketIndex = -1
                # Evaluates the expression in the brackets and substitutes it into the overall expression
                answer = eval(expression[openBracketIndex + 1 : closeBracketIndex])

                # Accounts for unary negation outside brackets
                if openBracketIndex > 0 and expression[openBracketIndex - 1] == "-":
                        if openBracketIndex > 1 and expression[openBracketIndex - 2] in _operatorSet:
                                answer = eval("-1*(" + answer + ")")
                                openBracketIndex -= 1
                                
                if complex(answer.replace("i", "j")).imag != 0 or complex(answer.replace("i", "j")).real < 0:
                        answer = "<" + answer + ">"
                expression = expression[:openBracketIndex] + answer + expression[closeBracketIndex + 1:]

        # Applies the rest of the order of operations to the expression
        expression = _pemdas(expression, {"!"})
        expression = _pemdas(expression, {"^"})
        expression = _pemdas(expression, {"*", "/", "%"})
        expression = _pemdas(expression, {"+", "-"})
        return numberFormat(expression)
        
def evaluate(expression):
        try:
                return eval(expression)
        except:
                return "Error"

