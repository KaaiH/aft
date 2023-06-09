# # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  Framework for Automaten en Formele Talen           #
#  Written by Robin Visser, based on work by          #
#  Bas van den Heuvel and Daan de Graaf               #
#  This work is licensed under a Creative Commons     #
#  “Attribution-ShareAlike 4.0 International”         #
#   license.                                          #
# # # # # # # # # # # # # # # # # # # # # # # # # # # #

from TM import TM
import sys


def extract_input(trace, trace_tokenized=None):
    """
    Determines (and returns) the input string given to the TM that caused it to
    perform the computation that produced the given trace.
    trace:            a single TM trace (as a string with spaces).
    trace_tokenized:  optional, the same trace tokenized (as a list of tokens).
    returns:          the input (as a string without spaces)
    """

    ### Your code + explanation here
    input = []
    index = 0
    read = set()
    new_input = 0
    for x in trace:
        match x:
            case " ":
                continue
            case "⊔":
                new_input = 0
                continue
            case "⊢":
                new_input = 0
                continue
            case "-":
                if index not in read:
                    new_input = index
                read.add(index)
                continue
            case "+":
                continue
            case "<":
                index -= 1
                continue
            case ">":
                index += 1
                continue

        if new_input != 0:
            input.append((index, x))
            new_input = 0


    # Characters for left endmarker and BLANK: ⊢ , ⊔

    input.sort()
    print(input)
    print(''.join([s[1] for s in input]))
    return ''.join([s[1] for s in input])


def extract_output(trace, trace_tokenized=None):
    """
    Determines (and returns) the tape output produced by the TM when performing
    the computation that produced the given trace. The ouput is the longest
    possible string _after_ the left endmarker that does not end in
    a BLANK ('⊔').
    trace:            a single TM trace (as a string with spaces).
    trace_tokenized:  optional, the same trace tokenized (as a list of tokens).
    returns:          the output (as a string without spaces)
    """

    ### Your code + explanation here
    # Characters for left endmarker and BLANK: ⊢ , ⊔

    return None


def reverse_manually():
    """
    The original TM was designed to: <your answer here>

    The algorithm used by the original TM works as follows: <your answer here>

    returns: A TM object of no more than 20 states, capable of reproducing the
             traces given by the assignment.
    """

    ### Your reverse-engineered TM + explanation here

    Q = ['t', 'r']
    Sigma = ['0', '1', '|']
    Gamma = ['0', '1', '|', '⊔', '⊢']
    delta = []
    s = ''
    t = 't'
    r = 'r'

    tm = TM(Q, Sigma, Gamma, delta, s, t, r, verbose=True)

    return tm


def reverse_generic(traces, traces_tokenized=None):
    """
    Recreates (reverse-engineers) a TM which behaves identically to the TM that
    produced the supplied list of traces. Note: 'behaves identically' implies
    that the recreated TM must produce (given the same input) the exact same
    execution traces as the original.
    traces:           a list of traces produced by the original TM.
    traces_tokenized: optional, tokenized versions of the original traces.
    returns:          a TM object capable of reproducing the traces given
                      the same input.
    """

    ### Your code + explanation here

    Q = ['t', 'r']
    Sigma = []
    Gamma = ['⊔', '⊢']
    delta = []
    s = ''
    t = 't'
    r = 'r'

    tm = TM(Q, Sigma, Gamma, delta, s, t, r, verbose=True)

    return tm


def main(path_traces=None, path_tokenized=None):
    """
    Area to test different parts of your implementation.

    The present code is just an example, feel free to modify at will.
    While it is strongly recommended to write some tests here, the code
    produced will not directly influence your grade.
    """

    """ Input/output extraction """
    test_traces = [
                  '- ⊢ + ⊢ > - 0 + 1 > - 0 + 1 < - 1 + ⊔ > - 1 + ⊔ > - ⊔ + a '
                  '>',
                  '- ⊢ + ⊢ > - a + ⊢ < - ⊢ + ⊢ > - ⊢ + ⊔ > - b + ⊔ < - ⊔ '
                  '+ ⊢ > - ⊔ + ⊔ > - ⊔ + ⊢ <'
                  ]

    correct_inputs = [
                      '00',
                      'ab'
                     ]

    correct_outputs = [
                       '⊔⊔a',
                       '⊢⊔⊢'
                      ]

    # Only test input/output extraction functions that do not return "None"
    for idx in range(len(test_traces)):
        feedback = ""
        extracted_input = extract_input(test_traces[idx])
        if extracted_input is not None and \
           extracted_input != correct_inputs[idx]:
            feedback += "\nextracted input: \'" + extracted_input + "\'"\
                        "incorrect! (expected: \'" + correct_inputs[idx]\
                        + "\')"
        extracted_output = extract_output(test_traces[idx])
        if extracted_output is not None and \
           extracted_output != correct_outputs[idx]:
            feedback += "\nextracted output: \'" + extracted_output + "\'"\
                        "incorrect! (expected: \'" + correct_outputs[idx]\
                        + "\')"
        if feedback:
            feedback = test_traces[idx] + feedback
            print(feedback)

    """ Reverse engineering """
    # Read execution traces (as strings with spaces), if available.
    if path_traces:
        fo = open(path_traces, encoding='utf-8')
        with fo as f:
            traces = [trace for trace in [line.rstrip('\n') for line in f]]
        fo.close()

    # Read tokenized traces (as lists of tokens, excluding 'SPACE'),
    # if available.
    if path_tokenized:
        fo = open(path_tokenized, encoding='utf-8')
        with fo as f:
            traces_tokenized = [trace.split() for trace in [line.rstrip('\n')
                                for line in f]]
        fo.close()

    # Scratchpad, try to Reverse engineer the TM using the framework!

    # Examples:
    # print(traces[0])
    # print(extract_input(traces[0]))
    # print(extract_output(traces[0]))
    # TM.visualize(extract_input(traces[0]), traces[0])

    # Validate your solution by checking if it produces the original traces
    # given the original inputs...

    #tm = reverse_manually()
    #for trace in traces:
    #    tm.set_input(extract_input(trace))
    #    tm.transition_all()
    #    produced_trace = tm.get_execution_trace()
    #    if trace != produced_trace:
    #        print("TM produced an incorrect trace!")
    #        print("original: " + trace)
    #        print("TM:       " + produced_trace)
    #        input("Press enter to continue...")


if __name__ == '__main__':
    if len(sys.argv) > 2:
        path_traces = sys.argv[1]
        path_tokenized = sys.argv[2]
        main(path_traces, path_tokenized)
    elif len(sys.argv) > 1:
        path_traces = sys.argv[1]
        main(path_traces)
    else:
        main()
