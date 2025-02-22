"""`streamlit-minter` application."""

import sys
from pathlib import Path

# Necessary for Streamlit Cloud deployment
sys.path.append(str(Path(__file__).parents[2]))


from typing import Literal

import streamlit as st
from algosdk.transaction import AssetConfigTxn
from pera_wallet import pera_wallet
from streamlit_state import State, callback, state

from streamlit_minter.utils import create_asset_config_txn, encode_txn

BTC_TOTAL = 2_100_000_000_000_000
BTC_DECIMALS = 8

JS_MAX_SAFE_INTEGER = 9_007_199_254_740_991


def account(
    prev_txn_id: State[str | None], acfg_txn: State[AssetConfigTxn | None]
) -> tuple[Literal['mainnet', 'testnet'], str | None]:
    """An expander section for the blockchain account and wallet interactions.

    Args:
        prev_txn_id (State[str | None]): The previous transaction ID state function.
        acfg_txn (State[AssetConfigTxn | None]): Transaction object state function.

    Returns:
        tuple[Literal['mainnet', 'testnet'], str | None]: The selected network and connected address.
    """
    with st.expander('Account', expanded=True):
        network: Literal['mainnet', 'testnet'] = st.selectbox(
            label='Network',
            options=('mainnet', 'testnet'),
            index=0,
            format_func={'mainnet': 'MainNet', 'testnet': 'TestNet'}.get,
            on_change=callback,
            args=(acfg_txn, None),
        )

        wallet = pera_wallet(
            network=network,
            transactions_to_sign=encode_txn(txn) if (txn := acfg_txn()) else [],
        )
        connected_address, signed_txn_id = wallet or (None, None)

        st.caption(f'Connected address: {connected_address}' if connected_address else 'Connect your wallet to begin.')

        if signed_txn_id:
            prev_txn_id = prev_txn_id(signed_txn_id)
            acfg_txn = acfg_txn(None)

            st.success(
                f'View your transaction on [lora](https://lora.algokit.io/{network}/transaction/{signed_txn_id}) the explorer.',
                icon='🥳',
            )

        return network, connected_address


def asset_form(
    network: Literal['mainnet', 'testnet'],
    address: str,
    prev_txn_id: State[str | None],
    acfg_txn: State[AssetConfigTxn | None],
    asset_name_key: str = 'asset_name',
    unit_name_key: str = 'unit_name',
    total_key: str = 'total',
    decimals_key: str = 'decimals',
) -> None:
    """A form to create an asset configuration transaction.

    Args:
        network (Literal['mainnet', 'testnet']): The network to use.
        address (str): The address of the transaction signer.
        prev_txn_id (State[str | None]): The previous transaction ID state function.
        acfg_txn (State[AssetConfigTxn  |  None]): The transaction object state function.
        asset_name_key (str, optional): The asset name state key. Defaults to 'asset_name'.
        unit_name_key (str, optional): The unit name state key. Defaults to 'unit_name'.
        total_key (str, optional): The total state key. Defaults to 'total'.
        decimals_key (str, optional): The decimals state key. Defaults to 'decimals'.
    """
    with st.expander('Asset Parameters', expanded=acfg_txn() is None and prev_txn_id() is None):
        with st.form('asset_form', border=False):
            st.text_input('Asset Name', value='Bitcoin', max_chars=32, key=asset_name_key)
            st.text_input('Unit Name', value='BTC', max_chars=8, key=unit_name_key)
            st.number_input(
                label='Total',
                min_value=0,
                # Max uint64 is > the max safe integer in JavaScript
                max_value=JS_MAX_SAFE_INTEGER,
                step=1,
                value=BTC_TOTAL,
                key=total_key,
            )
            st.number_input(
                label='Decimals',
                min_value=0,
                max_value=19,
                step=1,
                value=BTC_DECIMALS,
                key=decimals_key,
            )

            st.form_submit_button(
                'Create Asset',
                on_click=callback,
                args=(
                    acfg_txn,
                    lambda _: create_asset_config_txn(
                        network=network,
                        sender=address,
                        asset_name=state(asset_name_key),
                        unit_name=state(unit_name_key),
                        total=state(total_key),
                        decimals=state(decimals_key),
                    ),
                ),
            )


def transaction_details(txn: AssetConfigTxn) -> None:
    """Renders transaction details as JSON in the siderbar.

    Args:
        txn (AssetConfigTxn): The transaction to render.
    """
    with st.sidebar:
        st.header('Transaction Details')
        st.json(txn.dictify())


if __name__ == '__main__':
    st.title('Asset Minter')
    top = st.container()

    prev_txn_id = state('prev_txn_id')
    acfg_txn = state('acfg_txn')
    network, connected_address = account(prev_txn_id=prev_txn_id, acfg_txn=acfg_txn)
    if connected_address:
        with top:
            asset_form(network=network, address=connected_address, prev_txn_id=prev_txn_id, acfg_txn=acfg_txn)
        if txn := acfg_txn():
            transaction_details(txn)
