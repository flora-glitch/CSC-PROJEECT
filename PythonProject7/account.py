import streamlit as st
from current import CurrentAccount

st.set_page_config(page_title="Current Account", layout="centered")

account = CurrentAccount(100000000)

st.title("Current Account")

with st.form("current_form"):
    amount = st.number_input("Enter Amount", min_value=0)
    operation = st.selectbox("Choose Operation", ["Deposit", "Withdraw"])
    submit = st.form_submit_button("Submit")

if submit:
    if operation == "Deposit":
        success = account.deposit(amount)
    else:
        success = account.withdraw(amount)

    if success:
        st.success(f" Transaction successful. New Balance: ₦{account.balance:.2f}")
    else:
        st.error(" Transaction failed. Check amount or overdraft limit.")







