# Generated from c:\Users\mique\Documents\cole\LP\Python\Practica\funx.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .funxParser import funxParser
else:
    from funxParser import funxParser

# This class defines a complete generic visitor for a parse tree produced by funxParser.

class funxVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by funxParser#root.
    def visitRoot(self, ctx:funxParser.RootContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by funxParser#fun_declaration.
    def visitFun_declaration(self, ctx:funxParser.Fun_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by funxParser#expr.
    def visitExpr(self, ctx:funxParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by funxParser#declare_params.
    def visitDeclare_params(self, ctx:funxParser.Declare_paramsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by funxParser#block.
    def visitBlock(self, ctx:funxParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by funxParser#fun_call.
    def visitFun_call(self, ctx:funxParser.Fun_callContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by funxParser#show.
    def visitShow(self, ctx:funxParser.ShowContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by funxParser#logical_expr.
    def visitLogical_expr(self, ctx:funxParser.Logical_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by funxParser#call_params.
    def visitCall_params(self, ctx:funxParser.Call_paramsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by funxParser#if_expr.
    def visitIf_expr(self, ctx:funxParser.If_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by funxParser#while_expr.
    def visitWhile_expr(self, ctx:funxParser.While_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by funxParser#assignment.
    def visitAssignment(self, ctx:funxParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by funxParser#condition_block.
    def visitCondition_block(self, ctx:funxParser.Condition_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by funxParser#condition.
    def visitCondition(self, ctx:funxParser.ConditionContext):
        return self.visitChildren(ctx)



del funxParser