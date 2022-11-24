import re
from antlr4 import *
import antlr4
from ExprLexer import ExprLexer
from ExprParser import ExprParser
from ExprVisitor import ExprVisitor
from antlr4.error.ErrorListener import ErrorListener, ConsoleErrorListener


class ArgumentNumberMismatch(Exception):
    pass


class UnknowFunctionCallException(Exception):
    pass


class FuncionReDeclarationException(Exception):
    pass


class TooManyIterationsException(Exception):
    pass


class LexerException(Exception):
    pass


class ErrorThrower(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise LexerException()


class TreeVisitor(ExprVisitor):

    # Visit a parse tree produced by ExprParser#root.
    def visitRoot(self, ctx: ExprParser.RootContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ExprParser#fun_declaration.
    def visitFun_declaration(self, ctx: ExprParser.Fun_declarationContext):
        l = list(ctx.getChildren())
        fun_name = l[0].getText()
        if functions.get(fun_name) is not None:
            raise FuncionReDeclarationException
        fun_params = self.visit(l[1])
        fun_block = l[2]
        return {"name": fun_name, "params": fun_params, "block": fun_block}

    # Visit a parse tree produced by ExprParser#expr.
    def visitExpr(self, ctx: ExprParser.ExprContext):
        l = list(ctx.getChildren())
        if len(l) == 1:
            if isinstance(l[0], antlr4.tree.Tree.TerminalNode):
                if re.match("[+-]?\d+$", l[0].getText()):
                    return int(l[0].getText())  # NUMBER
                return 0  # call_stack[-1].get(l[0].getText(), 0)  # IDENT or 0
            return self.visit(l[0])  # fun_call
        if len(l) == 2:  # negative num
            return -int(l[1].getText())

        if l[0].getText() == "(":
            return self.visit(l[1])  # expression

        match l[1].getSymbol().type:
            case ExprParser.MES:
                return self.visit(l[0]) + self.visit(l[2])
            case ExprParser.MENYS:
                return self.visit(l[0]) - self.visit(l[2])
            case ExprParser.PER:
                return self.visit(l[0]) * self.visit(l[2])
            case ExprParser.ENTRE:
                return self.visit(l[0]) // self.visit(l[2])
            case ExprParser.A_LA:
                return pow(self.visit(l[0]), self.visit(l[2]))

    # Visit a parse tree produced by ExprParser#block.
    def visitBlock(self, ctx: ExprParser.BlockContext):
        l = list(ctx.getChildren())
        for i in range(1, len(l) - 2):  # handle logical_expr | show
            res = self.visit(l[i])
            if res is not None:
                return res
        if isinstance(l[-2], ExprParser.ExprContext):  # it's an expr
            return self.visit(l[-2])
        else:  # it's a logical_expr | show
            res = self.visit(l[-2])
            if res is not None:
                return res
        return None

    # Visit a parse tree produced by ExprParser#fun_call.
    def visitFun_call(self, ctx: ExprParser.Fun_callContext):
        l = list(ctx.getChildren())
        fun_name = l[0].getText()
        function = functions.get(fun_name)
        if function != None:
            param_keys = function["params"]
            param_values = self.visit(l[1])
            if len(param_keys) != len(param_values):
                raise ArgumentNumberMismatch
            call_stack.append(dict(zip(param_keys, param_values)))
            fun_val = self.visit(function["block"])
            call_stack.pop()
            return fun_val
        else:
            raise UnknowFunctionCallException

    # Visit a parse tree produced by ExprParser#declare_params.
    def visitDeclare_params(self, ctx: ExprParser.Declare_paramsContext):
        params = list(ctx.getChildren())
        return [param.getText() for param in params]

    # Visit a parse tree produced by ExprParser#logical_expr.
    def visitLogical_expr(self, ctx: ExprParser.Logical_exprContext):
        return self.visitChildren(ctx)  # if_expr, while_expr or assignment

    def visitShow(self, ctx: ExprParser.ShowContext):
        l = list(ctx.getChildren())
        if (l[1].getText())[0] != '"':
            print("> ", call_stack[-1].get(l[1].getText(), 0))
        else:
            print("> ", l[1].getText()[1:-1])
        return None

    # Visit a parse tree produced by ExprParser#call_params.
    def visitCall_params(self, ctx: ExprParser.Call_paramsContext):
        params = list(ctx.getChildren())
        return [self.visit(param) for param in params]  # each param is an expression

    # Visit a parse tree produced by ExprParser#if_expr.
    def visitIf_expr(self, ctx: ExprParser.If_exprContext):
        l = list(ctx.getChildren())
        for i in range(1, len(l)):
            if (
                l[i].getText() != "if" and l[i].getText() != "else"
            ):  # we can have else if else if... else
                ret = self.visit(
                    l[i]
                )  # condition_block unless we reach last else, block
                if ret is not False:
                    if ret is not None:
                        return ret
                    break
        return None

    # Visit a parse tree produced by ExprParser#while_expr.
    def visitWhile_expr(self, ctx: ExprParser.While_exprContext):
        l = list(ctx.getChildren())
        res = self.visit(l[1])
        it = 0
        while res is not False:
            if res is not None:
                return res
            res = self.visit(l[1])
            if it == 10000:
                raise TooManyIterationsException
            it += 1
        return None

    # Visit a parse tree produced by ExprParser#assignment.
    def visitAssignment(self, ctx: ExprParser.AssignmentContext):
        l = list(ctx.getChildren())
        call_stack[-1][l[0].getText()] = self.visit(l[2])
        return None

    # Visit a parse tree produced by ExprParser#condition_block.
    def visitCondition_block(self, ctx: ExprParser.Condition_blockContext):
        l = list(ctx.getChildren())
        if self.visit(l[0]):  # check condition
            return self.visit(l[1])  # if condition we visit block
        return False

    # Visit a parse tree produced by ExprParser#condition.
    def visitCondition(self, ctx: ExprParser.ConditionContext):
        l = list(ctx.getChildren())
        if len(l) == 1:
            if isinstance(l[0], antlr4.tree.Tree.TerminalNode):
                if l[0].getText().isdigit():
                    return int(l[0].getText())  # NUMBER
                return call_stack[-1].get(l[0].getText(), 0)
            return self.visit(l[0])  # Then this is a function call

        if len(l) == 2:
            return -int(l[1].getText())

        if l[0].getText() == "(":
            return self.visit(l[1])

        match l[1].getSymbol().type:
            case ExprParser.LT:
                return self.visit(l[0]) < self.visit(l[2])
            case ExprParser.LE:
                return self.visit(l[0]) <= self.visit(l[2])
            case ExprParser.GT:
                return self.visit(l[0]) > self.visit(l[2])
            case ExprParser.GE:
                return self.visit(l[0]) >= self.visit(l[2])
            case ExprParser.EQ:
                return self.visit(l[0]) == self.visit(l[2])
            case ExprParser.NE:
                return self.visit(l[0]) != self.visit(l[2])


functions = {}
call_stack = []

while True:
    try:
        input_stream = InputStream(
            (input("? "))
            # "# funció que rep dos enters i en torna el seu maxim comu divisor \n Euclides a b{  while a != b  {    if a > b    {      a <- a - b    }    else    {      b <- b - a    } }  a}Euclides 6 8"
            # "DOS { 2 } Suma2 x { DOS + x } Suma2 3"
            # "Fibo n{    if n < 2 { n }   (Fibo n-1) + (Fibo n-2)}Fibo 4"
        )
        lexer = ExprLexer(input_stream)
        lexer = ExprLexer(input_stream)
        lexer.addErrorListener(ErrorThrower())
        token_stream = CommonTokenStream(lexer)
        parser = ExprParser(token_stream)
        tree = parser.root()
        visitor = TreeVisitor()
        ans = visitor.visit(tree)
        if isinstance(ans, int):
            print(ans)
        else:
            if ans is None:
                print(None)
            elif functions.get(ans["name"]) is None:
                functions[ans["name"]] = {
                    "params": ans["params"],
                    "block": ans["block"],
                }
    except ZeroDivisionError:
        print("Zero division attempt")
    except TooManyIterationsException:
        print("Probably stuck in while loop")
    except FuncionReDeclarationException:
        print("This function name is already used")
    except UnknowFunctionCallException:
        print("You are calling an undefined function")
    except ArgumentNumberMismatch:
        print("The number of arguments doesn't match the function signature")
    except LexerException:
        print("Lexer failed")
