from ply import lex, yacc
import numpy as np

class Expression:

    def __init__(self, children, optype) -> None:
        
        self.children = children
        self.optype = optype


    def calc_ids(self, voc):

        ops = {
            'OR': np.logical_or, 
            'AND': np.logical_and
        }

        first, second = [
            child.calc_ids(voc)
            for child in self.children
        ]
        min_size = min(
            first.shape[0], second.shape[0] 
        )

        first = first[:min_size]
        second = second[:min_size]

        return ops[self.optype](first, second)
            

class Term_Not:

    def __init__(self, child) -> None:
        
        self.child = child


    def calc_ids(self, voc):

        return np.logical_not(
            self.child.calc_ids(voc)
        )


class WORD:
    def __init__(self, child) -> None:
        self.child = child

    def calc_ids(self, voc):

        ids = voc(self.child)
        b = np.zeros(np.max(ids)+1, dtype=np.bool_)
        b[ids]=True

        return np.array(
            self.child.calc_ids(voc)
        )
    



def main():
    tokens = [
        'WORD', 'OR', 'AND', 'NOT', 'LPARENT', 'RPARENT'
    ]

    t_OR = r'OR'
    t_AND = r'AND'
    t_NOT = r'NOT'
    t_LPARENT = r'\('
    t_RPARENT = r'\)'
    t_ignore  = ' \t'
    t_WORD = r'((?!AND)(?!OR)(?!NOT)[a-zA-Z]+)'
    def t_error(t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # precedence = (
    #     ('left', 'OR'),
    #     ('left', 'AND'),
    #     ('right', 'NOT'),
    # )

    def p_expression_binop(p):
        '''
        expression : expression OR term
                   | expression AND term
        '''
        p[0] = ((p[1], p[3]), p[2])


    def p_expression_term(p):
        '''
        expression : term
        '''
        p[0] = p[1]
    

    def p_term_uop(p):
        '''
        term : NOT factor
        '''
        p[0] = (p[2], p[1])


    def p_term(p):
        '''
        term : factor
        '''
        p[0] = p[1]


    def p_factor(p):
        '''
        factor : WORD
        '''
        p[0] = (p[1], 'WORD')


    def p_factor_group(p):
        '''
        factor : LPARENT expression RPARENT
        '''
        p[0] = (p[2], 'parentesses')


    def p_error(p):
        print("Syntax error in input!")

    lexer  = lex.lex()       # Return lexer object
    parser = yacc.yacc() 

    while True:
        try:
            s = input('calc > ')
        except EOFError:
            break
        if not s: continue
        result = parser.parse(s, lexer)
        print(result)

    # parser.parse('x AND NOT (y AND x)')

    # while True:
    #     tok = lexer.token()
    #     if not tok:
    #         break      # No more input
    #     print(tok)
    # class Node:

    #     def __init__(tekens, optype) -> None:

if __name__=='__main__':
    main()