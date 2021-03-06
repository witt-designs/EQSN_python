from eqsn import EQSN


def test_non_destructive_measurement():
    q_sim = EQSN()
    id1 = str(1)
    q_sim.new_qubit(id1)
    q_sim.H_gate(id1)
    m = q_sim.measure(id1, non_destructive=True)
    m2 = q_sim.measure(id1)
    print("Measured %d." % m)
    assert m == m2
    print("Test was successfull!")
    q_sim.stop_all()
    print("Stopped succesfully!")
    exit(0)


if __name__ == "__main__":
    test_non_destructive_measurement()
