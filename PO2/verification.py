# # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  Framework for Automaten en Formele Talen           #
#  Written by Robin Visser, based on work by          #
#  Bas van den Heuvel and Daan de Graaf               #
#  This work is licensed under a Creative Commons     #
#  “Attribution-ShareAlike 4.0 International”         #
#   license.                                          #
# # # # # # # # # # # # # # # # # # # # # # # # # # # #

from PDA import PDA
import sys


def verify_movement(trace):
    """
    Creates and uses a PDA to verify proper Turing machine (TM) movement in a
    single execution trace
    trace: A list of events (tokens)
    returns: True if the trace behaviour is valid, False otherwise
    """

    # Build and explain your PDA here... (see PDA.py)
    # Characters for initial stack symbol and epsilon: ⊥ , ϵ
    Q = ['s1', 's2']
    Sigma = ['MLEFT', 'MRIGHT', 'READ', 'WRITE', 'BLANK', 'LEM', 'SYMBOL', 'ϵ']
    Gamma = ['⊥', 'MRIGHT']
    delta = [(('s1', 'MRIGHT', '⊥'), ('s1', ['MRIGHT', '⊥'])),
             (('s1', 'MRIGHT', 'MRIGHT'), ('s1', ['MRIGHT', 'MRIGHT'])),
             (('s1', 'MLEFT', 'MRIGHT'), ('s1', 'ϵ')),
             (('s1', 'MLEFT', '⊥'), ('s2', 'ϵ'))]
    s = 's1'
    F = ['s1']
    pda_type = 'final_state'

    my_pda = PDA(Q, Sigma, Gamma, delta, s, F, pda_type, verbose=False)

    # Note: you can use my_pda.transition(symbol) to test a single transition.

    return my_pda.transition_all(trace)


def verify_lem(trace):
    """
    Creates and uses a PDA to verify Turing machine (TM) left endmarker for a
    single execution trace
    trace: A list of events (tokens)
    returns: True if the trace behaviour is valid, False otherwise
    """

    # Build and explain your PDA here... (see PDA.py)
    # Characters for initial stack symbol and epsilon: ⊥ , ϵ
    Q = ['s0', 's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8']
    Sigma = ['MLEFT', 'MRIGHT', 'READ', 'WRITE', 'BLANK', 'LEM', 'SYMBOL', 'ϵ']
    Gamma = ['MRIGHT', '⊥']
    delta = [(('s0', 'READ', '⊥'), ('s1', '⊥')),
             (('s1', 'LEM', '⊥'), ('s2', '⊥')),
             (('s1', 'ϵ', '⊥'), ('s8', '⊥')),
             (('s2', 'WRITE', '⊥'), ('s3', '⊥')),
             (('s3', 'LEM', '⊥'), ('s4', '⊥')),
             (('s3', 'ϵ', '⊥'), ('s8', '⊥')),
             (('s4', 'MRIGHT', '⊥'), ('s5', ['MRIGHT', '⊥'])),
             (('s4', 'MLEFT', '⊥'), ('s8', 'ϵ')),
             (('s5', 'MRIGHT', '⊥'), ('s5', ['MRIGHT', '⊥'])),
             (('s5', 'MLEFT', '⊥'), ('s5', 'ϵ')),
             (('s5', 'ϵ', '⊥'), ('s4', 'ϵ')),
             (('s5', 'WRITE', '⊥'), ('s6', '⊥')),
             (('s5', 'LEM', '⊥'), ('s4', '⊥')),
             (('s6', 'LEM', '⊥'), ('s4', 'ϵ')),
             (('s6', 'ϵ',  '⊥'), ('s5', '⊥'))]
    s = 's0'
    F = ['s2', 's3', 's6', 's7', 's8']
    pda_type = 'final_state'

    my_pda = PDA(Q, Sigma, Gamma, delta, s, F, pda_type, verbose=False)

    # Note: you can use my_pda.transition(symbol) to test a single transition.

    return not my_pda.transition_all(trace)


def main(path):
    """
    Reads multiple tokenized traces from the file at 'path' and feeds them to
    the various verification functions.
    """
    # Read and parse traces.
    fo = open(path, encoding='utf-8')
    with fo as f:
        traces = [trace.split() for trace in [line.rstrip('\n') for line in f]]
    fo.close()

    # Verify traces using verification functions
    valid = traces
    for trace in valid:
        print("Trace          : \"" + str(trace) + "\"")
        print("Verify movement: " + str(verify_movement(trace)))
    valid = [trace for trace in valid if verify_movement(trace)]
    for trace in valid:
        print("Trace          : \"" + str(trace) + "\"")
        print("Verify LEM     : " + str(verify_lem(trace)))
    valid = [trace for trace in valid if verify_lem(trace)]

    # Print the remaining valid trace(s)
    print("Remaining trace(s):")
    for trace in valid:
        print(trace)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('RuntimeError: Use `python3 verification.py \
                 tokenized_traces.txt`')
    source = sys.argv[1]
    main(source)
