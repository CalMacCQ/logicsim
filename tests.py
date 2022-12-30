from pytket import Circuit, OpType
from pytket.circuit import CircBox, ToffoliBox, QControlBox
from pytket.utils import compare_unitaries

from logicsim import LogicSim
from gateset import is_classical_predicate, ls_gateset_pred, compilation_sequence


def test_class() -> None:
    my_ls = LogicSim(4)
    assert my_ls.qubits == 4
    assert my_ls.qstate == [0, 0, 0, 0]

    my_ls1 = LogicSim(5)
    hcirc = Circuit(5).X(1).X(2)
    output = my_ls1.run_circuit(hcirc)
    assert output == [0, 1, 1, 0, 0]


def test_x() -> None:
    ls1 = LogicSim(2)
    circ1 = Circuit(2).X(0).X(1).X(0)
    output1 = ls1.run_circuit(circ1)
    assert output1 == [0, 1]


def test_cx() -> None:
    ls2 = LogicSim(2)
    circ2 = Circuit(2).X(0).CX(0, 1)
    c_circ = ls2.compile_classical_circuit(circ=circ2)
    output2 = ls2.run_circuit(c_circ)
    assert output2 == [1, 1]

    ls3 = LogicSim(3)
    circ3 = Circuit(3).X(0).CX(0, 1).CX(1, 2).X(0).CX(2, 0)
    c_circ3 = ls3.compile_classical_circuit(circ3)
    output3 = ls3.run_circuit(c_circ3)
    assert output3 == [1, 1, 1]


def test_ccx() -> None:
    ls4 = LogicSim(4)
    circ4 = Circuit(4).X(0).X(1).add_gate(OpType.CCX, [0, 1, 2])
    c_circ4 = ls4.compile_classical_circuit(circ4)
    output4 = ls4.run_circuit(c_circ4)
    assert output4 == [1, 1, 1, 0]


def test_cnx() -> None:
    ls5 = LogicSim(4)
    circ5 = Circuit(4).X(0).X(1).X(2).add_gate(OpType.CnX, [0, 1, 2, 3])
    c_circ5 = ls5.compile_classical_circuit(circ5)
    output5 = ls5.run_circuit(c_circ5)
    assert output5 == [1, 1, 1, 1]


def test_bigger_circuit() -> None:
    ls6 = LogicSim(6)
    circ6 = (
        Circuit(6)
        .X(0)
        .X(1)
        .X(2)
        .add_gate(OpType.CnX, [0, 1, 2, 3])
        .X(1)
        .add_gate(OpType.CCX, [2, 3, 4])
        .add_gate(OpType.CnX, [4, 3, 2, 1])
    )
    c_circ6 = ls6.compile_classical_circuit(circ6)
    output6 = ls6.run_circuit(c_circ6)
    assert output6 == [1, 1, 1, 1, 1, 0]


def another_test_circuit() -> None:
    ls = LogicSim(5)
    circ = Circuit(5)
    circ.X(0).X(1).add_gate(OpType.CCX, [0, 1, 2])
    c_circ = ls.compile_classical_circuit(circ)
    output = ls.run_circuit(c_circ)
    assert output == [1, 1, 1, 0, 0]


def test_compilation_pass() -> None:
    my_circ = Circuit(4)
    permutation = {(0, 0): (1, 1), (1, 1): (0, 0)}
    tb = ToffoliBox(n_qubits=2, permutation=permutation)
    sub_circ = Circuit(3)
    sub_circ.CX(0, 1).add_gate(OpType.CCX, [0, 1, 2])
    cb = CircBox(sub_circ)
    qcntrl = QControlBox(cb, 1)
    my_circ.add_qcontrolbox(qcntrl, [0, 1, 2, 3])
    assert is_classical_predicate.verify(my_circ)
    unitary_before = my_circ.get_unitary()
    compilation_sequence.apply(my_circ)
    unitary_after = my_circ.get_unitary()
    assert compare_unitaries(unitary_before, unitary_after)
    assert ls_gateset_pred.verify(my_circ)


def test_suspicious_circuit() -> None:
    manual_circ = Circuit(2).X(1).CX(1, 0).X(1).CX(0, 1).X(1).CX(1, 0).X(1)
    mysim = LogicSim(2)
    c_manual_circ = mysim.compile_classical_circuit(manual_circ)
    res = mysim.run_circuit(c_manual_circ)
    assert res == [1, 1]


if __name__ == "__main__":
    test_class()
    test_x()
    test_cx()
    test_ccx()
    test_cnx()
    test_bigger_circuit()
    another_test_circuit()
    test_compilation_pass()
    test_suspicious_circuit()
    print("tests passed")
