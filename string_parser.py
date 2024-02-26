from ply import lex, yacc
import numpy as np


class Expression:

    def __init__(self, children, optype) -> None:
        
        self.children = children
        self.optype = optype


    def calc_ids(self, voc):

        ops = {
            'OR': self.calc_or, 
            'AND': self.calc_and
        }

        first, second = [
            child.calc_ids(voc)
            for child in self.children
        ]
        if first.shape[0] > second.shape[0]:
            second, first = first, second

        return ops[self.optype](first, second)
    

    def calc_or(self, first, second):
        first = np.concatenate(
            (first,
             np.zeros(
                second.shape[0]-first.shape[0], 
                dtype=np.bool_)
            ))
        
        return np.logical_or(first, second)
            

    def calc_and(self, first, second):
        second = second[:first.shape[0]]
        return np.logical_and(first, second)




class Term_Not:

    def __init__(self, child) -> None:
        
        self.child = child


    def calc_ids(self, voc):

        return np.logical_not(
            self.child.calc_ids(voc)
        )


class Word:
    def __init__(self, child) -> None:
        self.child = child.lower()

    def calc_ids(self, voc):
        ids = voc[self.child]
        boolmask = np.zeros(np.max(ids)+1, dtype=np.bool_)
        boolmask[ids]=True
        return boolmask
    

def get_parser():
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


    def p_expression_binop(p):
        '''
        expression : expression OR term
                   | expression AND term
        '''
        p[0] = Expression((p[1], p[3]), p[2])


    def p_expression_term(p):
        '''
        expression : term
        '''
        p[0] = p[1]
    

    def p_term_uop(p):
        '''
        term : NOT factor
        '''
        p[0] = Term_Not(p[2])


    def p_term(p):
        '''
        term : factor
        '''
        p[0] = p[1]


    def p_factor(p):
        '''
        factor : WORD
        '''
        p[0] = Word(p[1])


    def p_factor_group(p):
        '''
        factor : LPARENT expression RPARENT
        '''
        p[0] = p[2]


    def p_error(p):
        print("Syntax error in input!")


    lexer  = lex.lex()       # Return lexer object
    parser = yacc.yacc() 
    return parser, lexer



def test():

    parser, lexer = get_parser()
    voc = {
        'x':[1, 2, 3, 5, 7], 
        'y':[3, 8, 10], 
        'z':[7, 4, 8, 9]
    }

    s_and_ans = {
        'x AND y': np.array([0, 0, 0, 1, 0, 0, 0, 0,], dtype=np.bool_),
        'y AND x': np.array([0, 0, 0, 1, 0, 0, 0, 0,], dtype=np.bool_),
        'y AND x AND z': np.array([0, 0, 0, 0, 0, 0, 0, 0,], dtype=np.bool_),
        'NOT y AND x AND z': np.array([0, 0, 0, 0, 0, 0, 0, 1,], dtype=np.bool_),
        'NOT y': np.array([1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0], dtype=np.bool_),

        'x OR y': np.array([0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1], dtype=np.bool_),
        'y OR x': np.array([0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1], dtype=np.bool_),
    }


    for s, ans in s_and_ans.items():
        result = parser.parse(s, lexer).calc_ids(voc)
        if all(result == ans):
            print("Test "+ s + ' passed')
        else:
            print("Test "+ s + ' NOT passed')
            print(f'ans {result} \ncorrect {ans}')


if __name__=="__main__":

    test()