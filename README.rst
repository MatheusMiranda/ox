Ox is a simplified API to the excellent PLY_ library. 

.. PLY: http://www.dabeaz.com/ply/


Why Ox?
=======

PLY is a powerful and reasonably efficient pure Python implementation of 
Yacc/Bison. Its API is a little bit awkward from a Python point of view and it 
does a lot of magic under the hood. Ox wraps main PLY functionality into an API
that aims to be more explicit while still being easy to use. 

It can be useful for production code, but just like PLY, it was created as a 
tool for a introductory compilers course. One explicit goal of Ox is to make the
boundaries of the different phases of compilation sharper and to make each step
more easily pluggable into each other. This pedagogical approach is good for
teaching but it is often not the most efficient or practical way to implement 
real compilers.
 
 
What about the name?
====================

PLY is a Pythonic implementation/interpretation of Yacc. The most widespread
Yacc implementation is of course GNU Bison. We decided to keep the bovine 
theme alive and decided to call it Ox. 


Usage
=====
 
Compilation is usually broken in a few steps:

1) Tokenization/lexical analysis: a string of source code is broken into a 
   list of tokens. In Ox, a lexer function is any function that receives a 
   string input and return a list of tokens.
2) Parsing: the list of tokens is converted to a syntax tree. In Ox, the parser
   function is usually derived from a grammar in BNF form. It receives a list
   of tokens and outputs an arbitrary parse tree.
3) Semantic analysis: the parse tree is scanned for semantic errors (e.g. 
   invalid variable names, invalid type signatures, etc). The parse tree is 
   often converted to a different representation in this process.
4) Code optimization: many optimizations are applied in order to generate 
   efficient internal representations. This is highly dependent on the source
   language and on the target language and it tends to be the largest part of 
   a parser in real compiler.
5) Code generation: the intermediate representation is used to emit code in the
   target language. The target language is often a low level language such as
   assembly or machine code. Nothing prevents us to emmit Python or Javascript,
   however.   

Ox is mostly concerned with steps 1 and 2. The library may evolve in the future
to steps 3 onwards, but they tend to be very application specific and usually
a generic tool such as Ox do not offer much help.

While you can implement a lexer function manually, Ox help us to build a lexer 
by simply providing a list of token names associated with their corresponding
regular expressions:

.. code-block:: python
    
    import ox
    
    lexer_rules = [
        ('NUMBER', r'\d+(\.\d*)?'),
        ('PLUS', r'\+'),
        ('MINUS', r'\-'),
        ('MUL', r'\*'),
        ('DIV', r'\/'),
    ] 
    
    lexer = ox.make_lexer(lexer_rules)


This declares a tokenizer function that receives a string of source code and
returns a list of tokens:
 
>>> lexer('21 + 21')
[NUMBER(21), PLUS(+), NUMBER(21)]
 
The next step, of course, is to pass this list of tokens to a parser in order to 
generate the parse tree. We can easily declare a parser in Ox from a mapping 
of grammar rules to handler functions.

Each handler function receives a number of inputs from the grammar rule and
return an AST node. In the example bellow, we return tuples to build our AST
as a LISP-like S-expr. 

.. code-block:: python

    binop = lambda x, op, y: (op, x, y)
    number = lambda x: ('atom', float(x))
    
Now the rules:

.. code-block:: python

    parser_rules = [
        ('expr : expr PLUS term', binop),
        ('expr : expr MINUS term', binop),
        ('expr : term', None),
        ('term : term MUL atom', binop),
        ('term : term DIV atom', binop),
        ('term : atom', None),
        ('atom : NUMBER', number),
    ]
    
    token_names = [tk_name for tk_name, _ in lexer_rules]
    parser = ox.make_parser(parser_rules, token_names) 
    
The parser takes a list of tokens and convert it to an AST:

>>> parser(lexer('2 + 2 * 20'))
('+', ('atom', 2.0), ('*', ('atom', 2.0), ('atom', 20.0)))


The AST is easier to evaluate than the original string expression. We can
write a simple evaluator as follows:

.. code-block:: python

    import operator as op

    operations = {'+': op.add, '-': op.sub, '*': op.mul, '/': op.truediv}
    
    def eval(ast):
        head, *tail = ast
        if head == 'atom':
            return tail[0]
        else:
            func = operations[head]
            args = (eval(x) for x in tail)
            return func(*args)

    def eval_loop():
        expr = input('expr: ')
        
        tokens = lexer(expr)
        ast    = parser(tokens)
        value  = eval(ast)
        
        print('result:', value)

The eval function receives an AST, but we can easily compose it with the other
functions in order to accept string inputs. (Ox functions understands sidekick's 
pipeline operators to compose functions. The arrow operator ``>>`` simply passes 
the output of each function to the input of the next function in the pipeline).

>>> eval_input = lexer >> parser >> eval
>>> eval_input('2 + 2 * 20')
42.0

That's it. Call the `eval_loop()` at the end of the script and you have a nice 
calculator written with only a few lines of Python! 
