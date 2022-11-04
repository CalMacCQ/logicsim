from logicsim import (
    LogicSim,
    is_classical_predicate,
    ls_gateset_pred,
    prepare_classical_circuit,
)
from pytket import Circuit, OpType, Qubit
from pytket.circuit import CircBox, ToffoliBox, QControlBox


def test_LogicSim_class() -> None:
    my_ls = LogicSim(4)
    assert my_ls.qubits == 4
    assert my_ls.qstate == [1, 0, 0, 0]
    assert my_ls.hamming_weight == 1


def test_valid_circuit() -> None:
    pass


def test_x() -> None:
    ls1 = LogicSim(2)
    circ1 = Circuit(2).X(0).X(1).X(0)
    output1 = ls1.run_circuit(circ1)
    assert output1 == [1, 1]


def test_cx() -> None:
    ls2 = LogicSim(2)
    circ2 = Circuit(2).CX(0, 1)
    output2 = ls2.run_circuit(circ2)
    assert output2 == [1, 1]

    ls3 = LogicSim(3)
    circ3 = Circuit(3).CX(0, 1).CX(1, 2).X(0).CX(2, 0)
    output3 = ls3.run_circuit(circ3)
    assert output3 == [1, 1, 1]


def test_ccx() -> None:
    ls4 = LogicSim(4)
    circ4 = Circuit(4).X(1).add_gate(OpType.CCX, [0, 1, 2])
    output4 = ls4.run_circuit(circ4)
    assert output4 == [1, 1, 1, 0]


def test_cnx() -> None:
    ls5 = LogicSim(4)
    circ5 = Circuit(4).X(1).X(2).add_gate(OpType.CnX, [0, 1, 2, 3])
    output5 = ls5.run_circuit(circ5)
    assert output5 == [1, 1, 1, 1]


def test_bigger_circuit() -> None:
    ls6 = LogicSim(6)
    circ6 = (
        Circuit(6)
        .X(1)
        .X(2)
        .add_gate(OpType.CnX, [0, 1, 2, 3])
        .X(1)
        .add_gate(OpType.CCX, [2, 3, 4])
        .add_gate(OpType.CnX, [4, 3, 2, 1])
    )
    output6 = ls6.run_circuit(circ6)
    assert output6 == [1, 1, 1, 1, 1, 0]


def test_intger_con() -> None:
    ls_int = LogicSim(5)
    circ_int = Circuit(5)
    circ_int.X(1).add_gate(OpType.CCX, [0, 1, 2])
    output_int = ls_int.run_circuit(circ_int)
    assert output_int == [1, 1, 1, 0, 0]


def test_prepare_circuit_pass() -> None:
    ls_comp = LogicSim(4)
    my_circ = Circuit(4)
    permutation = {(0, 0): (1, 1), (1, 1): (0, 0)}
    tb = ToffoliBox(n_qubits=2, permutation=permutation)
    my_circ.add_toffolibox(tb, [0, 1])
    sub_circ = Circuit(3).CX(0, 1).add_gate(OpType.CCX, [0, 1, 2])
    cb = CircBox(sub_circ)
    qcntrl = QControlBox(cb, 1)
    my_circ.add_qcontrolbox(qcntrl, [0, 1, 2, 3])
    prepare_classical_circuit.apply(my_circ)
    assert ls_gateset_pred.verify(my_circ)


test_x()
test_cx()
test_ccx()
test_cnx()
test_bigger_circuit()
test_intger_con()
test_LogicSim_class()
test_prepare_circuit_pass()
print("all tests pass")
