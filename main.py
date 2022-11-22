import sys
from antlr4 import *
from ExprLexer import ExprLexer
from ExprParser import ExprParser

input_stream = InputStream(
    # "Fibo n{    if n < 2 { n <- 2 n }  (Fibo n-1) + (Fibo n-2)}Fibo 4"
    "Euclides a b{  while a != b  {    if a > b    {      a <- a - b    }    else    {      b <- b - a    } }  a}Euclides 6 8"
)
lexer = ExprLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = ExprParser(token_stream)
tree = parser.root()
print(tree.toStringTree(recog=parser))
