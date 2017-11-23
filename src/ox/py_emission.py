from sidekick import opt
from types import SimpleNamespace


Node = (
    opt.Number(1)
    | opt.Name(1)
    | opt.Add(2) 
    | opt.Mul(2) 
    | opt.Div(2) 
    | opt.Sub(2)

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
    | opt.ForBlock(4)
    | opt.WhileBlock(2)

    | opt.IfBlock(2)
    | opt.ElifBlock(2)
    | opt.ElseBlock(1)
    | opt.FunCall(2)
    | opt.FunDef(3)
    | opt.FunReturn(1)   
)

Number, Name = Node.Number, Node.Name 

Add, Mul, Div, Sub =  Node.Add, Node.Mul, Node.Div, Node.Sub

Equal, NotEqual, GreaterThan, LessThan, GreaterEqual, LessEqual = \
Node.Equal, Node.NotEqual, Node.GreaterThan, Node.LessThan, Node.GreaterEqual, \
Node.LessEqual

AndOp, NotOp, OrOp = Node.AndOp, Node.NotOp, Node.OrOp

NameAttrib = Node.NameAttrib

Block = Node.Block

ForBlock, WhileBlock = Node.ForBlock, Node.WhileBlock

IfBlock, ElifBlock, ElseBlock = Node.IfBlock, Node.ElifBlock, Node.ElseBlock

FunCall = Node.FunCall

FunDef, FunReturn = Node.FunDef, Node.FunReturn

def source(ast):
    """
    Emite código python a partir da árvore sintática.
    """
    
    ctx = SimpleNamespace(tokens=[], indent=0)
    visit(ctx, ast)
    return ''.join(ctx.tokens)


def visit(ctx, ast):
    if ast.number:
        x = str(ast.number_args[0])
        ctx.tokens.append(x)
    
    elif ast.name:
        ctx.tokens.append(ast.name_args[0])

    elif ast.add:
        x, y = ast.add_args
        ctx.tokens.append('(')
        visit(ctx, x)
        ctx.tokens.append(' + ')
        visit(ctx, y)
        ctx.tokens.append(')')

    elif ast.mul:
        x, y = ast.mul_args
        ctx.tokens.append('(')
        visit(ctx, x)
        ctx.tokens.append(' * ')
        visit(ctx, y)
        ctx.tokens.append(')')
    
    elif ast.div:
        x, y = ast.div_args
        ctx.tokens.append('(')
        visit(ctx, x)
        ctx.tokens.append(' / ')
        visit(ctx, y)
        ctx.tokens.append(')') 

     elif ast.sub:
        x, y = ast.sub_args
        ctx.tokens.append('(')
        visit(ctx, x)
        ctx.tokens.append(' - ')
        visit(ctx, y)
        ctx.tokens.append(')') 

    elif ast.equal:
            x, y = ast.equal_args
            visit(ctx, x)
            ctx.tokens.append(' == ')
            visit(ctx, y)

    elif ast.notequal:
        x, y = ast.notequal_args
        visit(ctx, x)
        ctx.tokens.append(' != ')
        visit(ctx, y)

    elif ast.greaterthan:
        x, y = ast.greaterthan_args
        visit(ctx, x)
        ctx.tokens.append(' > ')
        visit(ctx, y)

    elif ast.lessthan:
        x, y = ast.lessthan_args
        visit(ctx, x)
        ctx.tokens.append(' < ')
        visit(ctx, y)

    elif ast.greaterequal:
        x, y = ast.greaterequal_args
        visit(ctx, x)
        ctx.tokens.append(' >= ')
        visit(ctx, y)

    elif ast.lessequal:
        x, y = ast.lessequal_args
        visit(ctx, x)
        ctx.tokens.append(' <= ')
        visit(ctx, y)  

    elif ast.andop:
            x, y = ast.andop_args
            visit(ctx, x)
            ctx.tokens.append(' and ')
            visit(ctx, y)

    elif ast.orop:
        x, y = ast.orop_args
        visit(ctx, x)
        ctx.tokens.append(' or ')
        visit(ctx, y)

    elif ast.notop:
            x = ast.notop_args
            ctx.tokens.append(' not ')
            visit(ctx, x)

    elif ast.nameattrib:
        x, y = ast.nameattrib_args
        ctx.tokens.append(x)
        ctx.tokens.append(' = ')
        visit(ctx, y)    

    elif ast.block:
        block = ast.block_args[0]
        if not block:
            block.append(Name('pass'))        
        for node in block:
            ctx.tokens.append('    ' * ctx.indent)
            visit(ctx, node)
            ctx.tokens.append('\n')

    elif ast.forblock:
        counter, iterable, block = ast.forblock_args
        ctx.tokens.append('for ')
        visit(ctx, counter)
        ctx.tokens.append(' in ')
        visit(ctx, iterable)
        ctx.tokens.append(':\n')
        ctx.indent += 1
        visit(ctx, block)
        ctx.indent -= 1

    elif ast.whileblock:
        condition, block = ast.whileblock_args
        ctx.tokens.append('    ' * ctx.indent)
        ctx.tokens.append('while (')
        visit(ctx, condition)
        ctx.tokens.append(') :\n')
        ctx.indent += 1
        visit(ctx, block)
        ctx.indent -= 1
        ctx.tokens.append('    ' * ctx.indent)
        ctx.tokens.append('\n')

    elif ast.ifblock:
        condition, block = ast.ifblock_args
        ctx.tokens.append('    ' * ctx.indent)
        ctx.tokens.append('if ')
        visit(ctx, condition)
        ctx.tokens.append(':\n')
        ctx.indent += 1
        visit(ctx, block)
        ctx.indent -= 1
        ctx.tokens.append('    ' * ctx.indent)

    elif ast.elseblock:
        block = ast.ifblock_args
        ctx.tokens.append('    ' * ctx.indent)
        ctx.tokens.append('else:\n')
        ctx.indent += 1
        visit(ctx, block)
        ctx.indent -= 1
        ctx.tokens.append('    ' * ctx.indent)

    elif ast.elifblock:
        condition, block = ast.elifblock_args
        ctx.tokens.append('    ' * ctx.indent)
        ctx.tokens.append('elif ')
        visit(ctx, condition)
        ctx.tokens.append('\n')
        ctx.indent += 1
        visit(ctx, block)
        ctx.indent -= 1
        ctx.tokens.append('    ' * ctx.indent)

    elif ast.funcall:
            ...

    elif ast.fundef:
        ...

    elif ast.funreturn:
        ...

    else:
        raise ValueError('node is not supported: %s' % ast)

# Testa o codigo

expr1 = NameAttrib('x', Add(Name('x'), Number(1)))
expr2 = NameAttrib('y', Number(42))
block = Block([expr1, expr2])
expr3 = IfBlock(OrOp(AndOp(Equal(Name('x'), Number(2)), Equal(Name('y'), Number(10))),\
 AndOp(Equal(Name('x'), Number(2)), Equal(Name('y'), Number(10)))), block)

expr = ForBlock(NameAttrib('i', Number(0)), Name('i < 10'), Name('i++'), expr3)

print(expr)
print(source(expr) + '\n' + source(expr))