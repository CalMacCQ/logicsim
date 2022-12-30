"Gateset and circuit transformations for classical simulator"
from pytket import Circuit, OpType, Qubit
from pytket.passes import CustomPass, DecomposeBoxes, RemoveRedundancies
from pytket.predicates import GateSetPredicate

logicsim_gateset = {OpType.X, OpType.CX, OpType.CCX, OpType.CnX}
ls_gateset_pred = GateSetPredicate(logicsim_gateset)
classical_boxes = {
    OpType.CircBox,
    OpType.ToffoliBox,
    OpType.QControlBox,
}


is_classical_predicate = GateSetPredicate(logicsim_gateset | classical_boxes)


def _flip(bit: int) -> int:
    """flip a bit"""
    assert bit in {0, 1}
    return int(not bit)


# This function should be unnecesary if I define the gates such that they act on qubit
# instead of the tape.
def _qubit_list_to_index_list(qubit_list: list[Qubit]) -> list:
    """
    Helper function - converts a list of qubits to a list of qubit indices
    e.g. [Qubit(0), Qubit(1)] -> [0, 1]
    """
    index_list = [qubit.index[0] for qubit in qubit_list]
    return index_list


# Note I'm using lists to represent the statevector/tape - may be worth making my own state class.
def apply_x(tape: list, qubit_list: list) -> list:
    """Apply the Pauli X gate to an input state"""
    assert len(qubit_list) == 1
    target = qubit_list[0].index[0]
    tape[target] = _flip(tape[target])
    return tape


# gates could be applied to a list of qubits not just an index - Maybe cleaner


def apply_cnx(tape: list, qubit_list: list) -> list:
    """Apply a CnX gate to an input state"""
    control_indices = _qubit_list_to_index_list(qubit_list[:-1])
    target_index = qubit_list[-1].index[0]
    control_vals = [tape[index] for index in control_indices]
    if sum(control_vals) == len(
        control_vals
    ):  # If all control bits are 1 flip the target
        tape[target_index] = _flip(tape[target_index])
    return tape


def classical_circuit_transform(circ: Circuit) -> Circuit:
    """transform function to define a pass to decompose classical boxes"""
    assert is_classical_predicate.verify(circ)
    circ_prime = circ.copy()
    DecomposeBoxes().apply(circ_prime)
    RemoveRedundancies().apply(circ_prime)
    if not ls_gateset_pred.verify(circ_prime):
        raise RuntimeError("unable to convert to classical gateset")

    for cmd in circ.get_commands():
        qubit_list = cmd.qubits
        if cmd.op.type == OpType.CX or OpType.CCX:
            circ_prime.add_gate(OpType.CnX, qubit_list)

    return circ_prime


prepare_classical_circuit = CustomPass(
    classical_circuit_transform
)  # pass to decompose boxes into classical gateset
