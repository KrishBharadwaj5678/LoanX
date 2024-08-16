import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Mortgage Calculator",
    page_icon="icon.png",
    menu_items={
        "About":
        """LoanX offers a powerful and user-friendly mortgage calculator to help you understand your total payments, view a detailed payment schedule, and track your monthly payoff progress."""
    })

st.write("<h2 style='color:lightgreen;'>Simplify Your Mortgage Journey</h2>",
         unsafe_allow_html=True)

amount = st.number_input("Amount Of Loan You Want To Borrow?", value=100000)

duration = st.select_slider("Duration Of The Loan", options=list(range(1, 51)))

rate = st.select_slider("Rate Of Interest (P.A)", options=list(range(1, 101)))

btn = st.button("Calculate")
if btn:
         interest = rate / 100  #Interest Rate
         air = interest / 12  #Annual Interest Rate
         n_of_pay = 12 * duration  #Number of Payments
         top_cal = amount * air  #Top Calculation
         bott_cal = 1 - (1 / (1 + air)**n_of_pay)  #Bottom Calculation
         monthly_payment = top_cal / bott_cal  #Monthly Payment
         trp = monthly_payment * n_of_pay  #Total Repayment
         cum_inr = trp - amount  #Cumulative Interest

         # Total Payments
         st.write("<h2 style=color:#FF8343;>Total Payments Summary</h2>",
                  unsafe_allow_html=True)

         def showDetails(label, value):
                  st.write(f"<li style=font-size:27px;>{label}: ₹{value}</li>",
                           unsafe_allow_html=True)

         showDetails("Loan Amount", amount)

         showDetails("Estimated Monthly Payment",
                     '{:.2f}'.format(monthly_payment))

         showDetails("Cumulative Interest", '{:.2f}'.format(cum_inr))

         showDetails("Total of all payments", '{:.2f}'.format(trp))

         main_lst = []
         main_lst.append([
             "Month", "Starting Balance", "Principal", "Interest",
             "Ending Balance"
         ])

         # Payment Schedule
         current_balance = amount
         chart_data = []
         months = []

         for i in range(1, n_of_pay + 1):
                  month = i
                  starting_balance = current_balance
                  interest = current_balance * air
                  principal = monthly_payment - interest
                  current_balance = current_balance - principal

                  chart_data.append(round(current_balance))
                  months.append(month)

                  main_lst.append([
                      month, "{:.2f}".format(starting_balance),
                      "{:.2f}".format(principal), "{:.2f}".format(interest),
                      "{:.2f}".format(current_balance)
                  ])

         st.write("<h2 style=color:#FF8343;>Payment Schedule</h2>",
                  unsafe_allow_html=True)

         pd_Data = pd.DataFrame(main_lst)

         data_html = pd_Data.to_html(index=False, header=False, escape=False)

         chart = pd.DataFrame({"Balance": chart_data, "Months": months})

         st.write(data_html, unsafe_allow_html=True)

         # Monthly PauOff Graph
         st.write("<h2 style=color:#FF8343;>Monthly Payoff Progress</h2>",
                  unsafe_allow_html=True)

         st.bar_chart(chart, x="Months", y="Balance")
