from algosdk.transaction import AssetConfigTxn, PaymentTxn, Transaction
from algosdk.encoding import msgpack_encode
from algokit_utils import (
    get_algod_client,
    get_algonode_config,
)
from typing import Literal


def encode_txn(txn: Transaction) -> list[str]:
    """Encodes a transaction object.

    Args:
        txn (Transaction): The transaction object.

    Returns:
        list[str]: The encoded transaction to sign.
    """
    return [msgpack_encode(txn)]


def fee_sink_address(network: Literal["mainnet", "testnet"]) -> str:
    """Returns the fee sink address for the given network.

    Args:
        network (Literal["mainnet", "testnet"]): The network to use.

    Returns:
        str: The fee sink address.
    """
    MAINNET = "Y76M3MSY6DKBRHBL7C3NNDXGS5IIMQVQVUAB6MP4XEMMGVF2QWNPL226CA"
    TESTNET = "A7NMWS3NT3IUDMLVO26ULGXGIIOUQ3ND2TXSER6EBGRZNOBOUIQXHIBGDE"
    return (MAINNET, TESTNET)[network == "testnet"]


def encode_test_payment(
    network: Literal["mainnet", "testnet"], sender: str
) -> list[str]:
    """Constructs a payment transaction to the fee sink address.

    Args:
        network (Literal["mainnet", "testnet"]): The network to use.
        sender (str): Sender address.

    Returns:
        list[str]: The encoded transaction to sign.
    """
    algod = get_algod_client(get_algonode_config(network, "algod", "a" * 64))

    ptxn = PaymentTxn(
        sp=algod.suggested_params(),
        sender=sender,
        receiver=fee_sink_address(network),
        amt=10,
    )
    return encode_txn(ptxn)


def create_asset_config_txn(
    network: Literal["mainnet", "testnet"],
    sender: str,
    asset_name: str,
    unit_name: str,
    total: int,
    decimals: int,
) -> AssetConfigTxn:
    """Constructs an asset configuration transaction.

    Args:
        network (Literal["mainnet", "testnet"]): The network to use.
        sender (str): Sender address.
        asset_name (str): The name of the asset.
        unit_name (str): The name of a unit of this asset.
        total (int): The total number of base units of the asset to create.
        decimals (int): The number of digits to use after the decimal point when displaying the asset.

    Returns:
        AssetConfigTxn: The transaction object.
    """
    algod = get_algod_client(get_algonode_config(network, "algod", "a" * 64))

    return AssetConfigTxn(
        sender=sender,
        sp=algod.suggested_params(),
        index=None,
        total=total,
        default_frozen=False,
        unit_name=unit_name,
        asset_name=asset_name,
        manager=None,
        reserve=None,
        freeze=None,
        clawback=None,
        url=None,
        metadata_hash=None,
        note=None,
        lease=None,
        strict_empty_address_check=False,
        decimals=decimals,
        rekey_to=None,
    )


def encode_asset_config_txn(
    network: Literal["mainnet", "testnet"],
    sender: str,
    asset_name: str,
    unit_name: str,
    total: int,
    decimals: int,
) -> list[str]:
    """Constructs an asset configuration transaction.

    Args:
        network (Literal["mainnet", "testnet"]): The network to use.
        sender (str): Sender address.
        asset_name (str): The name of the asset.
        unit_name (str): The name of a unit of this asset.
        total (int): The total number of base units of the asset to create.
        decimals (int): The number of digits to use after the decimal point when displaying the asset.

    Returns:
        list[str]: The encoded transaction to sign.
    """
    algod = get_algod_client(get_algonode_config(network, "algod", "a" * 64))

    acfg = AssetConfigTxn(
        sender=sender,
        sp=algod.suggested_params(),
        index=None,
        total=total,
        default_frozen=False,
        unit_name=unit_name,
        asset_name=asset_name,
        manager=None,
        reserve=None,
        freeze=None,
        clawback=None,
        url=None,
        metadata_hash=None,
        note=None,
        lease=None,
        strict_empty_address_check=False,
        decimals=decimals,
        rekey_to=None,
    )
    return encode_txn(acfg)
