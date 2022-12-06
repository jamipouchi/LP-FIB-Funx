from antlr4 import *
import antlr4
from antlr4.error.ErrorListener import ErrorListener
from flask import Flask, render_template, redirect, request
from itertools import islice
from funxLexer import funxLexer

from funxParser import funxParser


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


class TreeVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by ExprParser#root.
    def visitRoot(self, ctx: funxParser.RootContext):

        l = list(ctx.getChildren())
        for child in l:
            if isinstance(child, funxParser.Fun_declarationContext):  # fun declaration
                self.visit(child)
            elif isinstance(child, funxParser.ExprContext):
                return self.visit(child)
            else:
                return "You can only input functions and expressions"

    # Visit a parse tree produced by funxParser#fun_declaration.
    def visitFun_declaration(self, ctx: funxParser.Fun_declarationContext):
        l = list(ctx.getChildren())
        fun_name = l[0].getText()
        if functions.get(fun_name) is not None:
            raise FuncionReDeclarationException(fun_name)
        fun_params = self.visit(l[1])
        fun_block = l[2]
        functions[fun_name] = {
            "params": fun_params,
            "block": fun_block,
        }
        return None

    # Visit a parse tree produced by funxParser#expr.
    def visitExpr(self, ctx: funxParser.ExprContext):
        l = list(ctx.getChildren())
        if len(l) == 1:
            if isinstance(l[0], antlr4.tree.Tree.TerminalNode):
                if l[0].getText().isdigit():
                    return int(l[0].getText())  # NUMBER
                if len(call_stack) > 0:
                    return call_stack[-1].get(l[0].getText(), 0)  # IDENT or 0
                return 0
            return self.visit(l[0])  # fun_call
        if len(l) == 2:  # negative num
            return -int(l[1].getText())

        if l[0].getText() == "(":
            return self.visit(l[1])  # expr

        match l[1].getSymbol().type:
            case funxParser.MES:
                return self.visit(l[0]) + self.visit(l[2])
            case funxParser.MENYS:
                return self.visit(l[0]) - self.visit(l[2])
            case funxParser.PER:
                return self.visit(l[0]) * self.visit(l[2])
            case funxParser.ENTRE:
                return self.visit(l[0]) // self.visit(l[2])
            case funxParser.MOD:
                return self.visit(l[0]) % self.visit(l[2])
            case funxParser.A_LA:
                return pow(self.visit(l[0]), self.visit(l[2]))

    # Visit a parse tree produced by funxParser#block.
    def visitBlock(self, ctx: funxParser.BlockContext):
        l = list(ctx.getChildren())
        for i in range(1, len(l) - 2):  # handle logical_expr | show
            res = self.visit(l[i])
            if res is not None:
                return res
        if isinstance(l[-2], funxParser.ExprContext):  # it's an expr
            return self.visit(l[-2])
        else:  # it's a logical_expr | show
            res = self.visit(l[-2])
            if res is not None:
                return res
        return None

    # Visit a parse tree produced by funxParser#fun_call.
    def visitFun_call(self, ctx: funxParser.Fun_callContext):
        l = list(ctx.getChildren())
        fun_name = l[0].getText()
        function = functions.get(fun_name)
        if function != None:
            param_keys = function["params"]
            param_values = self.visit(l[1])
            if len(param_keys) != len(param_values):
                raise ArgumentNumberMismatch(
                    str(len(param_values)) + "!=" + str(len(param_keys))
                )
            call_stack.append(dict(zip(param_keys, param_values)))
            fun_val = self.visit(function["block"])
            call_stack.pop()
            return fun_val
        else:
            raise UnknowFunctionCallException(fun_name)

    # Visit a parse tree produced by funxParser#declare_params.
    def visitDeclare_params(self, ctx: funxParser.Declare_paramsContext):
        params = list(ctx.getChildren())
        return [param.getText() for param in params]

    # Visit a parse tree produced by funxParser#logical_expr.
    def visitLogical_expr(self, ctx: funxParser.Logical_exprContext):
        return self.visitChildren(ctx)  # if_expr, while_expr or assignment

    def visitShow(self, ctx: funxParser.ShowContext):
        l = list(ctx.getChildren())
        if (l[1].getText())[0] != '"':
            log.append(str(self.visit(l[1])))
        else:
            log.append(l[1].getText()[1:-1])
        return None

    # Visit a parse tree produced by funxParser#call_params.
    def visitCall_params(self, ctx: funxParser.Call_paramsContext):
        params = list(ctx.getChildren())
        return [self.visit(param) for param in params]  # each param is an expr

    # Visit a parse tree produced by funxParser#if_expr.
    def visitIf_expr(self, ctx: funxParser.If_exprContext):
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

    # Visit a parse tree produced by funxParser#while_expr.
    def visitWhile_expr(self, ctx: funxParser.While_exprContext):
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

    # Visit a parse tree produced by funxParser#assignment.
    def visitAssignment(self, ctx: funxParser.AssignmentContext):
        l = list(ctx.getChildren())
        call_stack[-1][l[0].getText()] = self.visit(l[2])
        return None

    # Visit a parse tree produced by funxParser#condition_block.
    def visitCondition_block(self, ctx: funxParser.Condition_blockContext):
        l = list(ctx.getChildren())
        if self.visit(l[0]):  # check condition
            return self.visit(l[1])  # if condition we visit block
        return False

    # Visit a parse tree produced by funxParser#condition.
    def visitCondition(self, ctx: funxParser.ConditionContext):
        l = list(ctx.getChildren())

        if len(l) == 1:  # expr
            return self.visit(l[0])

        if l[0].getText() == "(":
            return self.visit(l[1])

        match l[1].getSymbol().type:
            case funxParser.LT:
                return self.visit(l[0]) < self.visit(l[2])
            case funxParser.LE:
                return self.visit(l[0]) <= self.visit(l[2])
            case funxParser.GT:
                return self.visit(l[0]) > self.visit(l[2])
            case funxParser.GE:
                return self.visit(l[0]) >= self.visit(l[2])
            case funxParser.EQ:
                return self.visit(l[0]) == self.visit(l[2])
            case funxParser.NE:
                return self.visit(l[0]) != self.visit(l[2])
            case funxParser.AND:
                return self.visit(l[0]) and self.visit(l[2])
            case funxParser.OR:
                return self.visit(l[0]) or self.visit(l[2])
            case funxParser.XOR:
                return self.visit(l[0]) != self.visit(l[2])


functions = {}
call_stack = []


def process_query(query):
    try:
        input_stream = InputStream(
            query
            # "# funció que rep dos enters i en torna el seu maxim comu divisor \n Euclides a b{  while a != b  {    if a > b    {      a <- a - b    }    else    {      b <- b - a    } }  a}Euclides 6 8"
            # "DOS { 2 } Suma2 x { DOS + x } Suma2 3"
            # "Fibo n{    if n < 2 { n }   (Fibo n-1) + (Fibo n-2)}Fibo 4"
        )
        lexer = funxLexer(input_stream)
        lexer = funxLexer(input_stream)
        lexer.addErrorListener(ErrorThrower())
        token_stream = CommonTokenStream(lexer)
        parser = funxParser(token_stream)
        tree = parser.root()
        visitor = TreeVisitor()
        ans = visitor.visit(tree)
        return ans

    except ZeroDivisionError:
        return "Zero division attempt"
    except TooManyIterationsException:
        return "Probably stuck in while loop"
    except FuncionReDeclarationException as name:
        return "This function name is already used: " + str(name)
    except UnknowFunctionCallException as name:
        return "You are calling an undefined function: " + str(name)
    except ArgumentNumberMismatch as msg:
        return "The number of arguments doesn't match the function signature: " + str(
            msg
        )
    except LexerException:
        return "Lexer failed"


app = Flask(__name__)

app.secret_key = "abc"

entries = []
log = []


@app.route("/")
def base():
    return render_template(
        "base.html",
        entries=[
            {"idx": i + 1, "val": val}
            for (i, val) in islice(reversed(list(enumerate(entries))), 5)
        ],
        functions=functions,
    )


@app.route(
    "/new-entry",
    methods=["POST"],
)
def handle_entry():
    query = request.form.get("input-box")
    answer = process_query(query)  # process(query)
    entries.append({"query": query, "log": log.copy(), "answer": answer})
    log.clear()
    return redirect("/", code=302)
