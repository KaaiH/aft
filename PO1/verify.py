# # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  Framework for Automaten en Formele Talen           #
#  Written by Robin Visser, based on work by          #
#  Bas van den Heuvel and Daan de Graaf               #
#  This work is licensed under a Creative Commons     #
#  “Attribution-ShareAlike 4.0 International”         #
#   license.                                          #
# # # # # # # # # # # # # # # # # # # # # # # # # # # #

from FA import FA
import lexer as lexer
import sys


def create_fa():
    """
    Creates the finite automaton (FA) for step verification
    Characters for left endmarker and BLANK: ⊢ , ⊔
    """
    Q = ['start', 's1', 's2', 's3', 's4', 's5']
    Sigma = ['SPACE', 'MLEFT', 'MRIGHT', 'READ', 'WRITE', 'BLANK', 'LEM',
             'SYMBOL']
    delta = {'start': {'READ': 's1'},
             's1': {'SYMBOL': 's2',
                    'LEM': 's2',
                    'BLANK': 's2'},
             's2': {'WRITE': 's3'},
             's3': {'SYMBOL': 's4',
                    'LEM': 's4',
                    'BLANK': 's4'},
             's4': {'MLEFT': 's5',
                    'MRIGHT': 's5'},
             's5': {'READ': 's1'}}
    s = 'start'
    F = ['start', 's5']

    M = FA(Q, Sigma, delta, s, F, verbose=False)

    return M


def verify_steps(fa, lexed_trace):
    """
    The verification function steps through the lexed trace and feeds the token
    portion of tuple to the fa. Either filter out SPACE tokens or adjust the FA
    fa: The finite automaton
    lexed_trace: A list of tuples of the form (event, token).
    returns: True if the trace is valid, false otherwise.
    """
    fa.reset()
    for (_, token) in lexed_trace:
        if token == 'SPACE':
            continue
        fa.transition(token)
    return fa.is_final()


def main(path):
    """
    Reads multiple traces from the file at 'path' and feeds them first to the
    lexer and then to verify_steps.
    """

    fo = open(path, encoding='utf-8')
    with fo as f:
        traces = [line.rstrip('\n') for line in f]
    fo.close()

    M_lexer = lexer.create_fa()
    M_verify = create_fa()

    for trace in traces:
        M_lexer.reset()
        M_verify.reset()
        print("Trace : \"" + trace + "\"")
        lexed_trace = lexer.lexer(M_lexer, trace)
        print("Lexer : " + str(lexer.lexer(M_lexer, trace)))
        print("Verify: " + str(verify_steps(M_verify, lexed_trace)))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('RuntimeError: Use `python3 verify.py traces.txt`')
    source = sys.argv[1]
    main(source)
