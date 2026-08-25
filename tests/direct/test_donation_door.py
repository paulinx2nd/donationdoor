"""Direct tests for need matching, reservations, and recipient decisions."""

import json


NEEDS = {
    "needs": [
        {"id": "COATS", "description": "Clean adult winter coats suitable for below-freezing weather.", "quantity": 5},
        {"id": "SOAP", "description": "Factory-sealed unscented personal soap bars.", "quantity": 20},
    ]
}
OFFERS = {
    "offers": [
        {"id": "BOX-A", "description": "Three clean insulated adult winter coats in wearable condition.", "quantity": 3},
        {"id": "BOX-B", "description": "Ten sealed unscented personal soap bars.", "quantity": 10},
    ]
}


def _board(contract, direct_vm, recipient):
    direct_vm.sender = recipient
    return contract.publish_board("SHELTER-A", "Shelter public needs", NEEDS)


def _batch(contract, direct_vm, donor, board_id):
    direct_vm.sender = donor
    return contract.open_batch(board_id, "DONATION-1", OFFERS)


def _reserve(contract, direct_vm, donor, batch_id, matches):
    direct_vm.sender = donor
    direct_vm.mock_llm(r".*Match donated items.*", json.dumps({"matches": matches}))
    contract.reserve_matches(batch_id)


def test_board_initializes_quantity_counters(contract, direct_vm, direct_bob):
    board_id = _board(contract, direct_vm, direct_bob)
    board = contract.get_board(board_id)
    assert board["needs"][0]["requested"] == 5
    assert board["needs"][0]["reserved"] == 0


def test_duplicate_offer_identifiers_are_rejected(contract, direct_vm, direct_alice, direct_bob):
    board_id = _board(contract, direct_vm, direct_bob)
    direct_vm.sender = direct_alice
    bad = {"offers": [OFFERS["offers"][0], OFFERS["offers"][0]]}
    with direct_vm.expect_revert("duplicate_offer_id"):
        contract.open_batch(board_id, "BAD", bad)


def test_consensus_reserves_deterministic_quantities(contract, direct_vm, direct_alice, direct_bob):
    board_id = _board(contract, direct_vm, direct_bob)
    batch_id = _batch(contract, direct_vm, direct_alice, board_id)
    _reserve(
        contract,
        direct_vm,
        direct_alice,
        batch_id,
        [{"offer_id": "BOX-A", "need_id": "COATS"}, {"offer_id": "BOX-B", "need_id": "SOAP"}],
    )
    batch = contract.get_batch(batch_id)
    board = contract.get_board(board_id)
    assert batch["allocations"][0]["quantity"] == 3
    assert board["needs"][0]["reserved"] == 3
    assert board["needs"][1]["reserved"] == 10


def test_only_recipient_decides_reservations(contract, direct_vm, direct_alice, direct_bob):
    board_id = _board(contract, direct_vm, direct_bob)
    batch_id = _batch(contract, direct_vm, direct_alice, board_id)
    _reserve(contract, direct_vm, direct_alice, batch_id, [{"offer_id": "BOX-A", "need_id": "COATS"}])
    with direct_vm.expect_revert("only_recipient"):
        contract.decide_reservation(batch_id, "BOX-A", True)


def test_acceptance_moves_reserved_to_accepted_and_closes(contract, direct_vm, direct_alice, direct_bob):
    board_id = _board(contract, direct_vm, direct_bob)
    batch_id = _batch(contract, direct_vm, direct_alice, board_id)
    _reserve(contract, direct_vm, direct_alice, batch_id, [{"offer_id": "BOX-A", "need_id": "COATS"}])
    direct_vm.sender = direct_bob
    contract.decide_reservation(batch_id, "BOX-A", True)
    board = contract.get_board(board_id)
    assert board["needs"][0]["reserved"] == 0
    assert board["needs"][0]["accepted"] == 3
    direct_vm.sender = direct_alice
    contract.close_batch(batch_id)
    assert contract.get_batch(batch_id)["status"] == "CLOSED"


def test_board_cannot_close_with_pending_reservation(contract, direct_vm, direct_alice, direct_bob):
    board_id = _board(contract, direct_vm, direct_bob)
    batch_id = _batch(contract, direct_vm, direct_alice, board_id)
    _reserve(contract, direct_vm, direct_alice, batch_id, [{"offer_id": "BOX-A", "need_id": "COATS"}])
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("board_has_reservations"):
        contract.close_board(board_id)


def test_model_cannot_match_offer_twice(contract, direct_vm, direct_alice, direct_bob):
    board_id = _board(contract, direct_vm, direct_bob)
    batch_id = _batch(contract, direct_vm, direct_alice, board_id)
    direct_vm.mock_llm(
        r".*Match donated items.*",
        json.dumps({"matches": [{"offer_id": "BOX-A", "need_id": "COATS"}, {"offer_id": "BOX-A", "need_id": "SOAP"}]}),
    )
    with direct_vm.expect_revert("offer_matched_twice"):
        contract.reserve_matches(batch_id)
    assert contract.get_batch(batch_id)["status"] == "OPEN"
