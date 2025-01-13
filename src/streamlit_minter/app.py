import streamlit as st
from pera_wallet import pera_wallet
from .utils import create_asset_config_txn, encode_txn
from algosdk.transaction import AssetConfigTxn


NETWORK = "testnet"
MY_ADDRESS = "54G6BHF4SMNHGR6NJR3DQ4U7GLM5WKZBRK5BRWJE4OX2R3FZ2YJOJ4YBGQ"

BTC_TOTAL = 2_100_000_000_000_000
BTC_DECIMALS = 8

JS_MAX_SAFE_INTEGER = 9_007_199_254_740_991


if "account" not in st.session_state:
    st.session_state.account = None

if "transaction_id" not in st.session_state:
    st.session_state.transaction_id = None

if "acfg_txn" not in st.session_state:
    st.session_state.acfg_txn = None


def txn_json(txn: AssetConfigTxn):
    with st.container():
        st.caption("Asset Configuration Transaction")
        st.json(txn.dictify())


def account():
    with st.expander("Account", expanded=True):
        if not st.session_state.transaction_id and isinstance(
            st.session_state.acfg_txn, AssetConfigTxn
        ):
            txn_json(st.session_state.acfg_txn)
            transactions_to_sign = encode_txn(st.session_state.acfg_txn)
            st.session_state.acfg_txn = None
        else:
            transactions_to_sign = []

        wallet = pera_wallet(
            network=NETWORK,
            transactions_to_sign=transactions_to_sign,
            key="pera_wallet",
        )
        if wallet is not None:
            st.session_state.account, st.session_state.transaction_id = wallet

        st.caption(
            f"Connected address: {st.session_state.account}"
            if st.session_state.account
            else "Connect your wallet to begin."
        )
        if st.session_state.transaction_id:
            st.caption(
                f"View your transaction on [lora](https://lora.algokit.io/{NETWORK}/transaction/{st.session_state.transaction_id}) the explorer 🥳"
            )
            st.session_state.transaction_id = None


def asset_form():
    with st.form("asset_form"):
        st.write("Asset Parameters")

        asset_name = st.text_input("Asset Name", value="Bitcoin", max_chars=32)
        unit_name = st.text_input("Unit Name", value="BTC", max_chars=8)
        total = st.number_input(
            label="Total",
            min_value=0,
            # Max uint64 is > the max safe integer in JavaScript
            max_value=JS_MAX_SAFE_INTEGER,
            step=1,
            value=BTC_TOTAL,
        )
        decimals = st.number_input(
            label="Decimals",
            min_value=0,
            max_value=19,
            step=1,
            value=BTC_DECIMALS,
        )

        submitted = st.form_submit_button("Create Asset")
        if submitted:
            st.session_state.acfg_txn = create_asset_config_txn(
                network=NETWORK,
                sender=st.session_state.account,
                asset_name=asset_name,
                unit_name=unit_name,
                total=total,
                decimals=decimals,
            )
            st.rerun()


st.title("Algorand Asset Minter")

account()

if not st.session_state.account:
    st.stop()

asset_form()
