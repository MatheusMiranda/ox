from ox.automata import DFA


has_a = DFA(
    start='err',
    valid={'ok'},
    states={'err', 'ok'},
    transitions={
        ('err', 'a'): 'ok',
        ('err', 'b'): 'err',
        ('ok', 'a'): 'ok',
        ('ok', 'b'): 'ok',
    },
    description="Checks if a string of a's and b's has an a.",
)

print(
    has_a.validate('bbba'),
    has_a.validate('bb'),
    has_a.validate('abbb'),
)


has_ab = DFA(
    start='none',
    valid={'ok'},
    states={'none', 'has-a', 'has-b', 'ok'},
    transitions={
        ('none', 'a'): 'has-a',
        ('none', 'b'): 'has-b',
        ('none', 'c'): 'none',
        
        ('has-a', 'a'): 'has-a',
        ('has-a', 'b'): 'ok',
        ('has-a', 'c'): 'has-a',
        
        ('has-b', 'a'): 'ok',
        ('has-b', 'b'): 'has-b',
        ('has-b', 'c'): 'has-b',

        ('ok', 'a'): 'ok',
        ('ok', 'b'): 'ok',
        ('ok', 'c'): 'ok',
    },
    description="Checks if a string of a's, b's and c's have both a and b.",
)

print(
    has_ab.validate('bbba'),
    has_ab.validate('bbcc'),
    has_ab.validate('abc'),
)