"""
A specification of the grammatical semantics for grako's
generated parser for the FPE DSL
"""


def strip_block_comments(text):
    "Strips text of block comments"
    import re
    block_comment_re = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE
    )
    return re.sub(block_comment_re, '', text)


class Semantics:
    "Semantics for the FPE DSL implemented in grako"

    def __init__(self):
        self.parameters = {}
        self.sequences = {}
        self.sequence_counter = 0

    def readout(self, ast):
        return {"programs": [p for l in ast["programs"] for p in l],
                "defaults": ast["defaults"],
                "hold": ast["hold"]}

    def parameter(self, ast):
        self.parameters[ast["name"]] = ast["value"]

    def sequence(self, ast):
        new_sequencer_counter_val = \
            self.sequence_counter + \
            sum(s["steps"]
                for s in ast["value"]
                if "steps" in s)
        self.sequences[ast["name"]] = {
            "sequence": ast["value"],
            "start": self.sequence_counter,
            "end": new_sequencer_counter_val - 1
        }
        self.sequence_counter = new_sequencer_counter_val

    def frame(self, ast):
        out = ast["body"]
        for d in out:
            d["frame"] = True
        return out

    def single_step(self, _):
        return {"steps": 1}

    def state_changes(self, ast):
        return dict(zip(ast[::2], ast[1::2]))

    def steps(self, ast):
        return {"steps": sum(i for x in ast for i in x.values())}

    def signal(self, ast):
        state_changes, steps = ast
        if state_changes == {}:
            return steps
        else:
            return ast

    def subsequence(self, ast):
        return self.sequences[ast]["sequence"]

    @staticmethod
    def sequence_body(ast):
        def merge_sequences(s1, s2):
            if "steps" in s1[-1] and "steps" in s2[0]:
                return s1[:-1] + \
                       [{"steps": s1[-1]["steps"] + s2[0]["steps"]}] + \
                       s2[1:]
            else:
                return s1 + s2

        return reduce(merge_sequences, ast)

    @staticmethod
    def constant(ast):
        return int(ast)

    def predefined_symbol(self, ast):
        return self.parameters[ast]

    def value(self, ast):
        return ast["value"]

    def term(self, ast):
        val, ops = ast
        for op, val2 in zip(ops[::2], ops[1::2]):
            if op == "*":
                val *= val2
            elif op == "/":
                val /= val2
            else:
                raise Exception("Unsupported term operation: " + op)
        return val

    def expression(self, ast):
        val, ops = ast
        for op, val2 in zip(ops[::2], ops[1::2]):
            if op == "-":
                val -= val2
            elif op == "+":
                val += val2
            else:
                raise Exception("Unsupported expression operation: " + op)
        return val
