import multiprocessing
import numpy as np
from qubit_thread import *
from shared_dict import get_threads_for_ids, set_thread_with_id, \
                        send_all_threads, stop_all_threads, change_ids_queue

manager = multiprocessing.Manager()
def new_qubit(id):
    q = multiprocessing.Queue()
    thread = QubitThread(id, q)
    p = multiprocessing.Process(target=thread.run, args=())
    set_thread_with_id(id, p, q)
    p.start()

def stop_all():
    send_all_threads(None)
    stop_all_threads()

def X_gate(q_id):
    """
    Applys the Pauli X gate to the Qubit with q_id.
    """
    x = np.array([[0,1],[1,0]], dtype=np.csingle)
    q = get_threads_for_ids([q_id])[0]
    q.put([SINGLE_GATE, x, q_id])

def Y_gate(q_id):
    """
    Applys the Pauli Y gate to the Qubit with q_id.
    """
    x = np.array([[0,0-1j],[0+1j,0]], dtype=np.csingle)
    q = get_threads_for_ids([q_id])[0]
    q.put([SINGLE_GATE, x, q_id])

def Z_gate(q_id):
    """
    Applys the Pauli Z gate to the Qubit with q_id.
    """
    x = np.array([[1,0],[0,-1]], dtype=np.csingle)
    q = get_threads_for_ids([q_id])[0]
    q.put([SINGLE_GATE, x, q_id])

def H_gate(q_id):
    """
    Applys the Hadamard gate to the Qubit with q_id.
    """
    x = np.array([[0.5,0.5],[0.5,-0.5]], dtype=np.csingle)
    q = get_threads_for_ids([q_id])[0]
    q.put([SINGLE_GATE, x, q_id])


def merge_qubits(q_id1, q_id2):
    l = get_threads_for_ids([q_id1, q_id2])
    if len(l) == 1:
        return # Already merged
    else:
        print("has to be merged")
        q1 = l[0]
        q2 = l[1]
        merge_q = manager.Queue()
        q1.put([MERGE_SEND, merge_q])
        q2.put([MERGE_ACCEPT, merge_q])
        change_ids_queue(q_id1, q2)
        print("Merged successfull!")


def cnot_gate(q_id1, q_id2):
    """
    Applys a controlled X gate, where the gate is applied to
    q_id1 and controlled by q_id2.
    """
    x = np.array([[0,1],[1,0]], dtype=np.csingle)
    merge_qubits(q_id1, q_id2)
    q = get_threads_for_ids([q_id1])[0]
    q.put([CONTROLLED_GATE, x, q_id1, q_id2])


def measure(id):
    ret = manager.Queue()
    q = get_threads_for_ids([id])[0]
    q.put([MEASURE, id, ret])
    res = ret.get()
    return res