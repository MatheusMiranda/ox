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

    | opt.Type(1)
    | opt.Variable(2)

    | opt.Equal(2)
    | opt.NotEqual(2)
    | opt.GreaterThan(2)
    | opt.LessThan(2)
    | opt.GreaterEqual(2)
    | opt.LessEqual(2)

    | opt.AndOp(2)
    | opt.OrOp(2)
    | opt.NotOp(1)

## ----

    | opt.NameAttrib(2)
    | opt.Block(1)
    | opt.ForBlock(4)
    | opt.WhileBlock(2)
    | opt.DoWhileBlock(2)
    | opt.SimpleStatement(1)

    | opt.IfBlock(2)
    | opt.ElseIfBlock(2)
    | opt.ElseBlock(1)

    | opt.FunDef(4)
    | opt.FunReturn(1)
    | opt.Arg(2)
    | opt.FunArg(1)
)

Number, Boolean, Name = Node.Number, Node.Boolean, Node.Name

Add, Mul, Div, Sub = Node.Add, Node.Mul, Node.Div, Node.Sub

Type, Variable = Node.Type, Node.Variable

Equal, NotEqual, GreaterThan, LessThan, GreaterEqual, LessEqual = \
Node.Equal, Node.NotEqual, Node.GreaterThan, Node.LessThan, Node.GreaterEqual, \
Node.LessEqual

AndOp, NotOp, OrOp = Node.AndOp, Node.NotOp, Node.OrOp

NameAttrib = Node.NameAttrib

Block = Node.Block

ForBlock, WhileBlock, DoWhileBlock = \
    Node.ForBlock, Node.WhileBlock, Node.DoWhileBlock

IfBlock, ElseIfBlock, ElseBlock = \
    Node.IfBlock, Node.ElseIfBlock, Node.ElseBlock

FunDef, FunReturn = Node.FunDef, Node.FunReturn

FunArg = Node.FunArg
Arg = Node.Arg

FunCall = Node.FunCall

SimpleStatement = Node.SimpleStatement

context = SimpleNamespace(tokens=[], indent=0)

def source(ast):
    """
    Emite código em JavaScript a partir da árvore sintática
    """

    for element in ast:
        visit(context, element)

    return ''.join(context.tokens)

def visit(context, ast):
    match_function = Node.match_fn(**methods)
    match_function(ast)

class Options:

    def __init__(self, context):
        self.context = context

    # Arithmetic operators

    def number(self, value):
        context.tokens.append(str(value))

    def name(self, word):
        context.tokens.append(word)

    def type(self, _type):
        context.tokens.append(_type)

    def variable(self, _type, variable_name):
        context.tokens.append('var ')
        visit(context, variable_name)

    def boolean(self, condition):
        context.tokens.append(condition)

    def add(self, first_argument, second_argument):
        context.tokens.append('(')
        visit(context, first_argument)
        context.tokens.append(' + ')
        visit(context, second_argument)
        context.tokens.append(')')

    def sub(self, first_argument, second_argument):
        context.tokens.append('(')
        visit(context, first_argument)
        context.tokens.append(' - ')
        visit(context, second_argument)
        context.tokens.append(')')

    def mul(self, first_argument, second_argument):
        context.tokens.append('(')
        visit(context, first_argument)
        context.tokens.append(' * ')
        visit(context, second_argument)
        context.tokens.append(')')

    def div(self, first_argument, second_argument):
        context.tokens.append('(')
        visit(context, first_argument)
        context.tokens.append(' / ')
        visit(context, second_argument)
        context.tokens.append(')')

    # Comparison operators

    def equal(self, first_argument, second_argument):
        visit(context, first_argument)
        context.tokens.append(' == ')
        visit(context, second_argument)

    def notequal(self, first_argument, second_argument):
        visit(context, first_argument)
        context.tokens.append(' != ')
        visit(context, second_argument)

    def greaterthan(self, first_argument, second_argument):
        visit(context, first_argument)
        context.tokens.append(' > ')
        visit(context, second_argument)

    def lessthan(self, first_argument, second_argument):
        visit(context, first_argument)
        context.tokens.append(' < ')
        visit(context, second_argument)

    def greaterequal(self, first_argument, second_argument):
        visit(context, first_argument)
        context.tokens.append(' >= ')
        visit(context, second_argument)

    def lessequal(self, first_argument, second_argument):
        visit(context, first_argument)
        context.tokens.append(' <= ')
        visit(context, second_argument)

    #

    def andop(self, first_argument, second_argument):
        visit(context, first_argument)
        context.tokens.append(' && ')
        visit(context, second_argument)

    def orop(self, first_argument, second_argument):
        visit(context, first_argument)
        context.tokens.append(' || ')
        visit(context, second_argument)

    def notop(self, first_argument, second_argument):
        context.tokens.append('!')
        visit(context, first_argument)

    #

    def nameattrib(self, first_argument, second_argument):
        context.tokens.append(first_argument)
        context.tokens.append(' = ')
        visit(context, second_argument)

    #

    def block(self, block):
        if not block:
            block.append(Name('pass'))

        for node in block:
            context.tokens.append('    ' * context.indent)
            visit(context, node)

    #

    def forblock(self, counter, condition, iterable, block):
        context.tokens.append('    ' * context.indent)
        context.tokens.append('for (')
        visit(context, counter)
        context.tokens.append('; ')
        visit(context, condition)
        context.tokens.append('; ')
        visit(context, iterable)
        context.tokens.append(') {\n')
        context.indent += 1
        visit(context, block)
        context.indent -= 1
        context.tokens.append('}\n')

    def whileblock(self, condition, block):
        context.tokens.append('    ' * context.indent)
        context.tokens.append('while (')
        visit(context, condition)
        context.tokens.append(') {\n')
        context.indent += 1
        visit(context, block)
        context.indent -= 1
        context.tokens.append('    ' * context.indent)
        context.tokens.append('}\n')

    def dowhileblock(self, block, condition):
        context.tokens.append('    ' * context.indent)
        context.tokens.append('do {\n')
        context.indent += 1
        visit(context, block)
        context.indent -= 1
        context.tokens.append('    ' * context.indent)
        context.tokens.append('} while (')
        visit(context, condition)
        context.tokens.append(')')

    #

    def ifblock(self, condition, block):
        context.tokens.append('    ' * context.indent)
        context.tokens.append('if (')
        visit(context, condition)
        context.tokens.append(') {\n')
        context.indent += 1
        visit(context, block)
        context.indent -= 1
        context.tokens.append('    ' * context.indent)
        context.tokens.append('}\n')

    def elseblock(self, block):
        context.tokens.append('    ' * context.indent)
        context.tokens.append('else {\n')
        context.indent += 1
        visit(context, block)
        context.indent -= 1
        context.tokens.append('    ' * context.indent)
        context.tokens.append('}\n')

    def elseifblock(self, condition, block):
        context.tokens.append('    ' * context.indent)
        context.tokens.append('else if (')
        visit(context, condition)
        context.tokens.append(') {\n')
        context.indent += 1
        visit(context, block)
        context.indent -= 1
        context.tokens.append('    ' * context.indent)
        context.tokens.append('}\n')

    #

    def funarg(self, arguments):
        if not arguments:
            block.append(Name('pass'))

        counter = 0;

        for node in arguments:
            visit(context, node)

            if(counter >= 0 and counter < len(arguments) - 1):
                context.tokens.append(', ')

            counter += 1;

    def arg(self, type_attribute, name):
        context.tokens.append(name)

    #

    def fundef(self, type_return, function_name, arguments, block):
        context.tokens.append('function ')
        visit(context, function_name)
        context.tokens.append('(')
        visit(context, arguments)
        context.tokens.append(') {\n')
        context.indent += 1
        visit(context, block)
        context.indent -= 1
        context.tokens.append('}\n\n')

    def funcall(self, function_name, arguments):
        visit(context, function_name)
        context.tokens.append('(')
        visit(context, arguments)
        context.tokens.append(')')

    def funreturn(self, _return):
        context.tokens.append('return ')
        visit(context, _return)

    def simplestatement(self, statement):
        visit(context, statement)
        context.tokens.append(';\n')

    # def _not_implemented(self, *args):
    #     return NotImplemented
    #
    # error = _not_implemented

options = Options(context)
functions_in_Options = [func for func in dir(Options) if not func.startswith('_')]
methods = {option: getattr(options, option) for option in functions_in_Options}

# options = Options(context)

returnf = SimpleStatement(FunReturn(Add(Number(2), Number(40))))

expr1 = SimpleStatement(NameAttrib('x', Add(Name('x'), Number(1))))
expr2 = SimpleStatement(NameAttrib('y', Number(42)))

block = Block([expr1, expr2, returnf])

expr3 = IfBlock(OrOp(AndOp(Equal(Name('x'), Number(2)), Equal(Name('y'), Number(10))),\
 AndOp(Equal(Name('x'), Number(2)), Equal(Name('y'), Number(10)))), block)


teste1 = Arg('int', 't1')
teste2 = Arg('int', 't2')

expr = [FunDef(Type(''), Name('teste'), FunArg([teste1, teste2]), block), FunDef(Type(''), Name('main'), FunArg([Arg('', '')]), block)]
# expr = ForBlock(NameAttrib('i', Number(0)), Name('i < 10'), Name('i++'), Block([expr2]))
# expr = FunCall(Name('teste'), FunArg([teste1, teste2]))

# expr = ForBlock(NameAttrib('i', Number(0)), Name('i < 10'), Name('i++'), SimpleStatement(Block([expr2])))

print(expr)
print(source(expr))