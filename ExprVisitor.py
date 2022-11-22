# Generated from c:\Users\mique\Documents\cole\LP\Python\Practica\Expr.g by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .ExprParser import ExprParser
else:
    from ExprParser import ExprParser

# This class defines a complete generic visitor for a parse tree produced by ExprParser.

class ExprVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by ExprParser#root.
    def visitRoot(self, ctx:ExprParser.RootContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#fun_declaration.
    def visitFun_declaration(self, ctx:ExprParser.Fun_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#expr.
    def visitExpr(self, ctx:ExprParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#declare_params.
    def visitDeclare_params(self, ctx:ExprParser.Declare_paramsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#block.
    def visitBlock(self, ctx:ExprParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#fun_call.
    def visitFun_call(self, ctx:ExprParser.Fun_callContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#logical_expr.
    def visitLogical_expr(self, ctx:ExprParser.Logical_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#call_params.
    def visitCall_params(self, ctx:ExprParser.Call_paramsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#if_expr.
    def visitIf_expr(self, ctx:ExprParser.If_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#while_expr.
    def visitWhile_expr(self, ctx:ExprParser.While_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#assignment.
    def visitAssignment(self, ctx:ExprParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#condition_block.
    def visitCondition_block(self, ctx:ExprParser.Condition_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#condition.
    def visitCondition(self, ctx:ExprParser.ConditionContext):
        return self.visitChildren(ctx)



del ExprParser