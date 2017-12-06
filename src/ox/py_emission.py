from sidekick import opt
from types import SimpleNamespace

Node = (
    opt.Number(1)
    | opt.Boolean(1)
    | opt.Name(1)
    | opt.Add(2)
    | opt.Mul(2)
    | opt.Div(2)
    | opt.Sub(2)
    | opt.FunCall(2)

    | opt.Equal(2)
    | opt.NotEqual(2)
    | opt.GreaterThan(2)
    | opt.LessThan(2)
    | opt.GreaterEqual(2)
    | opt.LessEqual(2)

    | opt.AndOp(2)
    | opt.OrOp(2)
    | opt.NotOp(1)

    | opt.NameAttrib(2)
    | opt.Block(1)
    | opt.ForBlock(3)
    | opt.WhileBlock(2)
    | opt.SimpleStatement(1)

    | opt.IfBlock(2)
    | opt.ElifBlock(2)
    | opt.ElseBlock(1)

    | opt.FunDef(3)
    | opt.FunReturn(1)
    | opt.Arg(2)
    | opt.FunArg(1)
)

Number, Boolean, Name = Node.Number, Node.Boolean, Node.Name

Add, Mul, Div, Sub =  Node.Add, Node.Mul, Node.Div, Node.Sub

Equal, NotEqual, GreaterThan, LessThan, GreaterEqual, LessEqual = \
Node.Equal, Node.NotEqual, Node.GreaterThan, Node.LessThan, Node.GreaterEqual, \
Node.LessEqual

AndOp, NotOp, OrOp = Node.AndOp, Node.NotOp, Node.OrOp

NameAttrib = Node.NameAttrib

Block = Node.Block

ForBlock, WhileBlock = Node.ForBlock, Node.WhileBlock

IfBlock, ElifBlock, ElseBlock = Node.IfBlock, Node.ElifBlock, Node.ElseBlock

FunDef, FunReturn = Node.FunDef, Node.FunReturn

FunArg = Node.FunArg
Arg = Node.Arg

FunCall = Node.FunCall

SimpleStatement = Node.SimpleStatement

ctx = SimpleNamespace(tokens=[], indent=0)

def source(ast):
    """
    Emite código python a partir da árvore sintática.
    """
    visit(ctx, ast)
    return ''.join(ctx.tokens)

def visit(ctx, ast):

    match_function = Node.match_fn(**methods)
    match_function(ast)

class Options:

    def __init__(self, ctx):
        self.ctx = ctx

    def number(self, value):
        ctx.tokens.append(str(value))

    def name(self, data):
        ctx.tokens.append(data)

    def boolean(self, condition):
        ctx.tokens.append(condition)

    def add(self, first_argument, second_argument):
        ctx.tokens.append('(')
        visit(ctx, first_argument)
        ctx.tokens.append(' + ')
        visit(ctx, second_argument)
        ctx.tokens.append(')')

    def sub(self, first_argument, second_argument):
        ctx.tokens.append('(')
        visit(ctx, first_argument)
        ctx.tokens.append(' - ')
        visit(ctx, second_argument)
        ctx.tokens.append(')')

    def mul(self, first_argument, second_argument):
        ctx.tokens.append('(')
        visit(ctx, first_argument)
        ctx.tokens.append(' * ')
        visit(ctx, second_argument)
        ctx.tokens.append(')')

    def div(self, first_argument, second_argument):
        ctx.tokens.append('(')
        visit(ctx, first_argument)
        ctx.tokens.append(' / ')
        visit(ctx, second_argument)
        ctx.tokens.append(')')

    def equal(self, first_argument, second_argument):
        visit(ctx, first_argument)
        ctx.tokens.append(' == ')
        visit(ctx, second_argument)

    def notequal(self, first_argument, second_argument):
        visit(ctx, first_argument)
        ctx.tokens.append(' != ')
        visit(ctx, second_argument)

    def greaterthan(self, first_argument, second_argument):
        visit(ctx, first_argument)
        ctx.tokens.append(' > ')
        visit(ctx, second_argument)

    def lessthan(self, first_argument, second_argument):
        visit(ctx, first_argument)
        ctx.tokens.append(' < ')
        visit(ctx, second_argument)

    def greaterequal(self, first_argument, second_argument):
        visit(ctx, first_argument)
        ctx.tokens.append(' >= ')
        visit(ctx, second_argument)

    def lessequal(self, first_argument, second_argument):
        visit(ctx, first_argument)
        ctx.tokens.append(' <= ')
        visit(ctx, second_argument)

    def andop(self, first_argument, second_argument):
        visit(ctx, first_argument)
        ctx.tokens.append(' and ')
        visit(ctx, second_argument)

    def orop(self, first_argument, second_argument):
        visit(ctx, first_argument)
        ctx.tokens.append(' or ')
        visit(ctx, second_argument)

    def notop(self, argument):
        ctx.tokens.append(' not ')
        visit(ctx, argument)

    def nameattrib(self, first_argument, second_argument):
        ctx.tokens.append(first_argument)
        ctx.tokens.append(' = ')
        visit(ctx, second_argument)
        ctx.tokens.append('\n')

    def block(self, block):
        if not block:
            block.append(Name('pass'))

        for node in block:
            ctx.tokens.append('    ' * ctx.indent)
            visit(ctx, node)

    def forblock(self, counter, iterable, block):
        ctx.tokens.append('for ')
        visit(ctx, counter)
        ctx.tokens.append(' in ')
        visit(ctx, iterable)
        ctx.tokens.append(':\n')
        ctx.indent += 1
        visit(ctx, block)
        ctx.indent -= 1

    def whileblock(self, condition, block):
        ctx.tokens.append('while (')
        visit(ctx, condition)
        ctx.tokens.append('):\n')
        ctx.indent += 1
        visit(ctx, block)
        ctx.indent -= 1

    def ifblock(self, condition, block):
        ctx.tokens.append('    ' * ctx.indent)
        ctx.tokens.append('if ')
        visit(ctx, condition)
        ctx.tokens.append(' :\n')
        ctx.indent += 1
        visit(ctx, block)
        ctx.indent -= 1
        ctx.tokens.append('    ' * ctx.indent)

    def elseblock(self, block):
        ctx.tokens.append('    ' * ctx.indent)
        ctx.tokens.append('else:\n')
        ctx.indent += 1
        visit(ctx, block)
        ctx.indent -= 1
        ctx.tokens.append('    ' * ctx.indent)

    def elifblock(self, condition, block):
        ctx.tokens.append('    ' * ctx.indent)
        ctx.tokens.append('elif ')
        visit(ctx, condition)
        ctx.tokens.append(' :\n')
        ctx.indent += 1
        visit(ctx, block)
        ctx.indent -= 1
        ctx.tokens.append('    ' * ctx.indent)
        ctx.tokens.append('\n')

    def funarg(self, arguments):
        if not arguments:
            block.append(Name('pass'))

        counter = 0

        for node in arguments:
            visit(ctx, node)

            if(counter >= 0 and counter < len(arguments) - 1):
                ctx.tokens.append(', ')

            counter += 1

    def arg(self, type_attribute, name):
        ctx.tokens.append(name)

    def funcall(self, function_name, arguments):
        visit(ctx, function_name)
        context.tokens.append('(')
        visit(ctx, arguments)
        context.tokens.append(')')

    def fundef(self, function_name, arguments, block):
        ctx.tokens.append('def ')
        visit(ctx, function_name)
        ctx.tokens.append('(')
        visit(ctx, arguments)
        ctx.tokens.append('):\n')
        ctx.indent += 1
        visit(ctx, block)
        ctx.indent -= 1
        ctx.tokens.append('\n')

    def funreturn(self, _return):
        ctx.indent += 1
        ctx.tokens.append('return')
        visit(ctx, _return)

    def simplestatement(self, statement):
        visit(ctx, statement)

options = Options(ctx)
functions_in_Options = [func for func in dir(Options) if not func.startswith('_')]
methods = {option: getattr(options, option) for option in functions_in_Options}

returnf = SimpleStatement(FunReturn(Add(Number(2), Number(40))))
# Testa o codigo
expr1 = SimpleStatement(NameAttrib('x', (Add(Name('x'), Number(1)))))
expr2 = SimpleStatement(NameAttrib('y', Number(42)))
block2 = Block([expr1, expr2])
expr3 = WhileBlock(OrOp(AndOp(Equal(Name('x'), Boolean('true')), Equal(Name('y'), Number(10))),\
    AndOp(Equal(Name('x'), Number(2)), Equal(Name('y'), Number(10)))), block2)

expr4 = ForBlock(Name('x'), Number(2), block2)
block = Block([expr1, expr2, expr3, expr4, returnf])

test1 = Arg('int', 't1')
test2 = Arg('int', 't2')

expr = FunDef(Name('teste'),FunArg([test1,test2]),block)

print(source(expr))
