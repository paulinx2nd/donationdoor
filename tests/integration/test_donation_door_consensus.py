"""Five-validator GLSim flow for donation reservations."""

import json
from pathlib import Path

from gltest import get_contract_factory, get_validator_factory
from gltest.accounts import create_accounts
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionStatus
from gltest.utils import extract_contract_address


def _ok(receipt):
    assert tx_execution_succeeded(receipt), json.dumps(receipt, default=str)


def _context():
    response = {"matches": [{"offer_id": "BOX-A", "need_id": "COATS"}]}
    validators = get_validator_factory().batch_create_mock_validators(
        5,
        mock_llm_response={"nondet_exec_prompt": {"Match donated items": json.dumps(response)}},
    )
    return {"validators": [validator.to_dict() for validator in validators]}


def test_five_validator_reserve_accept_and_close():
    recipient_account, donor_account = create_accounts(2)
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "donation_door.py")
    deployed = factory.deploy_contract_tx(args=[], account=recipient_account, wait_transaction_status=TransactionStatus.FINALIZED)
    _ok(deployed)
    address = extract_contract_address(deployed)
    recipient = factory.build_contract(address, account=recipient_account)
    donor = factory.build_contract(address, account=donor_account)
    board_id = f"{str(recipient_account.address).lower()}:SHELTER-A"
    batch_id = f"{str(donor_account.address).lower()}:DONATION-1"
    needs = {"needs": [{"id": "COATS", "description": "Clean adult winter coats suitable for below-freezing weather.", "quantity": 5}]}
    offers = {"offers": [{"id": "BOX-A", "description": "Three clean insulated adult winter coats in wearable condition.", "quantity": 3}]}
    _ok(recipient.publish_board(args=["SHELTER-A", "Shelter public needs", needs]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(donor.open_batch(args=[board_id, "DONATION-1", offers]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(donor.reserve_matches(args=[batch_id]).transact(transaction_context=_context(), wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(recipient.decide_reservation(args=[batch_id, "BOX-A", True]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(donor.close_batch(args=[batch_id]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    board = recipient.get_board(args=[board_id]).call()
    assert board["needs"][0]["accepted"] == 3
    assert donor.get_batch(args=[batch_id]).call()["status"] == "CLOSED"
