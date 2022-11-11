from pytket import Circuit, OpType

from gateset import apply_x, apply_cx, apply_ccx, apply_cnx
from gateset import ls_gateset_pred


class LogicSim:
    """Simulator Class for classical logic circuits"""

    def __init__(self, n_qubits: int):
        self.qubits = n_qubits
        self.qstate = [0] * n_qubits  # state initalised at |00...0>

    def run_circuit(self, circ: Circuit) -> Circuit:
        """Processes a classical circuit and returns tape/ the ket for the quantum state"""
        assert ls_gateset_pred.verify(circ)
        for cmd in circ.get_commands():
            qubit_list = cmd.qubits
            if cmd.op.type == OpType.X:
                apply_x(self.qstate, qubit_list)
            elif cmd.op.type == OpType.CX:
                apply_cx(self.qstate, qubit_list)
            elif cmd.op.type == OpType.CCX:
                apply_ccx(self.qstate, qubit_list)
            elif cmd.op.type == OpType.CnX:
                apply_cnx(self.qstate, qubit_list)
        return self.qstate
