
# Staking Risks

import streamlit as st


# Dictionaries for scoring
security_audits_values = {0: 10, 1: 8, 2: 6, 3: 4, 4: 2, 5: 1}
avg_operator_reputation_values = {"Unknown": 10, "Established": 5, "Renowned": 1}

# Function definitions
def avg_validator_uptime(uptime):
    if uptime == "Good Uptime (Greater than 98%)":
        return 1
    elif uptime == "Average Uptime (97% to 98%)":
        return 5
    else:
        return 10

def total_steth(steth):
    if steth > 20000000:
        return 1
    elif steth > 15000000:
        return 3
    elif steth > 9000000:
        return 5
    elif steth > 5000000:
        return 7
    elif steth > 2000000:
        return 9
    else:
        return 10

def number_validators(validators):
    if validators > 200000:
        return 1
    elif validators > 150000:
        return 3
    elif validators > 100000:
        return 5
    elif validators > 50000:
        return 7
    elif validators > 20000:
        return 9
    else:
        return 10


# Centralization Risks
def market_share_central_risk(market_share_risk):
    if market_share_risk == "More than 50%":
        return 10
    elif market_share_risk == "Between 30% and 40%":
        return 8
    elif market_share_risk == "Between 20% and 30%":
        return 6
    elif market_share_risk == "Between 10% and 20%":
        return 4
    elif market_share_risk == "Less than than 10%":
        return 2
    
def barrier_entry_central_risk(barrier_entry_risk):
    if barrier_entry_risk == "High Barrier - 16 ETH Deposit":
        return 7
    elif barrier_entry_risk == "Low Barrier - 8 ETH Deposit":
        return 3
    

# Weight factors
security_audits_weight = 4 * 4 
avg_validator_uptime_weight = 2 * 3
total_steth_weight = 1 * 2
number_validators_weight = 2 * 3
market_share_central_risk_weight = 3 * 5
barrier_entry_central_risk_weight = 1 * 2
avg_operator_reputation_score_weight = 2 * 2

# Risk score calculation function
def weighted_risk_scores(security_audits, uptime, steth, validators, market_share_risk, barrier_entry_risk, avg_operator_reputation):

    security_audit_score = security_audits_values.get(security_audits, 0)
    avg_validator_uptime_score = avg_validator_uptime(uptime)
    total_steth_score = total_steth(steth)
    number_validators_score = number_validators(validators)
    market_share_central_risk_score = market_share_central_risk(market_share_risk)
    barrier_entry_central_risk_score = barrier_entry_central_risk(barrier_entry_risk)
    avg_operator_reputation_score = avg_operator_reputation_values.get(avg_operator_reputation, 0)

    # Calculate the total risk score
    total_risk_score = (security_audit_score * security_audits_weight +
                        avg_validator_uptime_score * avg_validator_uptime_weight +
                        total_steth_score * total_steth_weight +
                        number_validators_score * number_validators_weight +
                        market_share_central_risk_score * market_share_central_risk_weight +
                        barrier_entry_central_risk_score * barrier_entry_central_risk_weight +
                        avg_operator_reputation_score * avg_operator_reputation_score_weight)

    max_security_audit_score = 10  # Assuming worst case for security audit is 0 audits
    max_avg_validator_uptime_score = 10   # Assuming worst case for business model is "Pure Wallet"
    max_total_steth_score = 10         # Assuming worst case for AVS type is "Hyperscale"
    max_number_validators_score = 10    # Assuming worst case for restaking modality is "LST LP Restaking"
    max_market_share_central_risk_score = 10  # Assuming worst case for operator attack risk
    max_barrier_entry_central_risk_score = 10  # Assuming worst case for operator attack risk
    max_avg_operator_reputation_score = 10  # Assuming worst case for operator attack risk

    # Calculate the maximum possible risk score
    max_possible_risk_score = (
        max_security_audit_score * security_audits_weight +
        max_avg_validator_uptime_score * avg_validator_uptime_weight +
        max_total_steth_score * total_steth_weight +
        max_number_validators_score * number_validators_weight +
        max_market_share_central_risk_score * market_share_central_risk_weight +
        max_barrier_entry_central_risk_score * barrier_entry_central_risk_weight +
        max_avg_operator_reputation_score * avg_operator_reputation_score_weight)

    # Normalize the risk score
    normalized_risk_score = (total_risk_score / max_possible_risk_score) * 10
    normalized_risk_score = round(normalized_risk_score, 2)

    return normalized_risk_score



# Streamlit app setup
def main():
    st.set_page_config(layout="wide")

    st.image("images/lidologo.png")

    st.title("Staking Risk Simulator")
    st.title("Lido (stETH): Protocol Perspective")

    
    st.write("  \n")

    # Creating two major columns
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        # AVS TVL & Total Restaked
        st.markdown("""
                <style>
                .header-style {
                    font-size: 18px;
                    font-weight: bold;
                    margin-bottom: 0px;  /* Adjust the space below the header */
                }
                .stExpander {
                    border: none !important;
                    box-shadow: none !important;
                }
                </style>
                """, unsafe_allow_html=True)

            # Displaying the custom styled header
        st.markdown('<p class="header-style">Total stETH (in units)</p>', unsafe_allow_html=True)

        st.write("  \n")

        total_steth_input = st.number_input(" ", min_value=0, max_value=10000000000, value=0, step=1000000)

            # The expander without a visible outline
        with st.expander("Logic"):
                st.markdown("""
                    The **TVL/Total Restaked** risk logic herein is set so that the greater the *(AVS Total Restaked/2) : AVS TVL* ratio, the safer the AVS is, and vice-versa.
                    
                    To take the simplest scenario of the single-AVS restaking by operators [(Section 3.4.1 of EigenLayer's Whitepaper)](https://docs.eigenlayer.xyz/overview/intro/whitepaper) to begin with: an AVS appears to be most secure when the amount of restaked ETH is at least double the total locked value (TVL) and a 50% quorum is required for a collusion attack to capture the TVL, as any successful attack would result in at least half of the attacker's stake being slashed. If *AVS Total Restaked* increases from there compared to the *AVS TVL*, the risk gets reduced even further. If both variables are under $100K, we consider it the maximum risk scenario.

                    Accordingly, the main goal is to maintain the *CfC (Cost from Corruption)* ***above*** *the PfC (Profit from Corruption)* to desincentivize colluding, malicious operators to perform an attack. Appropriate bridges and oracles could be built to restrict the transaction flow within the period of slashing or to have bonds on the transacted value to maximize CfC/minimize PfC.

                    Understanding what a reduced risk level should be is not useful for operator-collusion cases only, but also for increasing the [CVS (Cost to Violate Safety) and the CVL (Cost to Violate Liveness)](https://www.blog.eigenlayer.xyz/dual-staking/), i.e. in a Dual Staking Model and Veto Dual Staking context, for example, which are useful to maintain the health of the AVS dual token pool (or AVS TVL, in other words).               
                            """)

        ###################        
        st.write("  \n")
        st.write("  \n")


        # AVS Business Model
        st.markdown("""
            <style>
            .header-style {
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 0px;  /* Adjust the space below the header */
            }
            .stExpander {
                border: none !important;
                box-shadow: none !important;
            }
            </style>
            """, unsafe_allow_html=True)

        # Displaying the custom styled header
        st.markdown('<p class="header-style">Number of stETH Validators</p>', unsafe_allow_html=True)

        # Dropdown menu
        number_validators_input = st.number_input("  ", min_value=0, max_value=10000000000, value=0, step=1000000)

        # https://beaconcha.in/pools 100K

        # The expander without a visible outline
        with st.expander("Logic"):
            st.markdown("""
                Ordering the **Business Models** from EigenLayer [(Section 4.6 of EigenLayer's Whitepaper)](https://docs.eigenlayer.xyz/overview/intro/whitepaper) by risk: 
                
                - ***Pay in the Native Token of the AVS*** is the most risky, as the entire fee structure is dependent on the AVS's native token (\$AVS), tying closely to its market performance and the AVS's ongoing profitability;
                - ***Dual Staking Utility***, with a high risk too because it depends on both ETH restakers and $AVS stakers, which introduces complexities in security and token value dynamics;
                - ***Tokenize the Fee*** model comes with moderate risk involving payments in a neutral denomination (like ETH) and distributing a portion of fees to holders of the AVS's token, thus partly dependent on the AVS token's value;
                - ***Pure Wallet*** represents the lowest risk, relying on straightforward service fees paid in a neutral denomination, like ETH.

                Thus, the risk of each model is influenced by its reliance on the AVS's native token and the complexities of its fee and security structures.
            """)
        
        ###################
        st.write("  \n")
        st.write("  \n")


        # Number of Security Audits
        st.markdown("""
            <style>
            .header-style {
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 0px;  /* Adjust the space below the header */
            }
            .stExpander {
                border: none !important;
                box-shadow: none !important;
            }
            </style>
            """, unsafe_allow_html=True)

        # Displaying the custom styled header
        st.markdown('<p class="header-style">Average Validator Uptime</p>', unsafe_allow_html=True)

        # https://www.coinbase.com/cloud/discover/insights-analysis/when-less-is-more

        # Dropdown menu
        avg_validator_uptime_input = st.selectbox("   ", ["Good Uptime (> 98%)", "Average Uptime (97% to 98%)", "Poor Uptime (< 97%)"])


        # The expander without a visible outline
        with st.expander("Logic"):
            st.markdown("""
                Accounting for the **number of Security Audits** performed onto an AVS provides a good insight into the reliability and robustness of their code structure.
                
                While this input is purely quantitative, in terms of the number of audits performed, a strong correlation exists with its underlying smart contract risks (and the risk of honest nodes getting slashed), and, as a result, rewards an AVS is confident to emit and Restakers and Operators to opt into it. 
                        """)

    with col2:
        # AVS Type
        st.markdown("""
            <style>
            .header-style {
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 0px;  /* Adjust the space below the header */
            }
            .stExpander {
                border: none !important;
                box-shadow: none !important;
            }
            </style>
            """, unsafe_allow_html=True)

        # Displaying the custom styled header
        st.markdown('<p class="header-style">Centralization Risk</p>', unsafe_allow_html=True)

        st.write("  \n")

        col3, col4 = st.columns([3, 3])

        with col3:
                market_share_central_risk_input = st.selectbox("**As a Function of Protocol Market Share**", ["More than 50%", "Between 30% and 40%", "Between 20% and 30%", "Between 10% and 20%", "Less than than 10%"])

        with col4:
                barrier_entry_central_risk_input = st.selectbox("**As a Function of Validator Barrier to Entry**", ["High Barrier - 16 ETH Deposit", "Low Barrier - 8 ETH Deposit"])

        with st.expander("Logic"):
            st.markdown("""
                In designing modules for maximal security and minimal centralization risk, EigenLayer suggests two approaches: **Hyperscale and Lightweight AVS** [(Section 3.6 of EigenLayer's Whitepaper)](https://docs.eigenlayer.xyz/overview/intro/whitepaper).

                **Hyperscale AVS** involves distributing the computational workload across many nodes, allowing for high overall throughput and reducing incentives for centralized validation. This horizontal scaling minimizes validation costs and amortization gains for any central operator. 

                On the other hand, the **Lightweight** approach focuses on tasks that are redundantly performed by all operators but are inexpensive and require minimal computing infrastructure.

                While it does depend on the needs of an AVS, the Hyperscale-type is more robust and secure due to its decentralized nature, particularly for new-born AVSs. Therefore, it was categorized as the safest AVS type in our simulator.                    
                        """)
            


        ###################
        st.write("  \n")
        st.write("  \n")


        # Number of Security Audits
        st.markdown("""
            <style>
            .header-style {
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 0px;  /* Adjust the space below the header */
            }
            .stExpander {
                border: none !important;
                box-shadow: none !important;
            }
            </style>
            """, unsafe_allow_html=True)

        # Displaying the custom styled header
        st.markdown('<p class="header-style">Number of Security Audits</p>', unsafe_allow_html=True)

        # Dropdown menu
        security_audits_input = st.number_input("    ", min_value=0, max_value=5, step=1)

        # The expander without a visible outline
        with st.expander("Logic"):
            st.markdown("""
                Accounting for the **number of Security Audits** performed onto an AVS provides a good insight into the reliability and robustness of their code structure.
                
                While this input is purely quantitative, in terms of the number of audits performed, a strong correlation exists with its underlying smart contract risks (and the risk of honest nodes getting slashed), and, as a result, rewards an AVS is confident to emit and Restakers and Operators to opt into it. 
                        """)
            

        ###################
        st.write("  \n")
        st.write("  \n")


        # AVS Average Operator Reputation
        st.markdown("""
            <style>
            .header-style {
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 0px;  /* Adjust the space below the header */
            }
            </style>
            """, unsafe_allow_html=True)

        # Displaying the custom styled header
        st.markdown('<p class="header-style">Average Operators\' Reputation</p>', unsafe_allow_html=True)

        # Select slider for average operator reputation
        avg_operator_reputation_input = st.selectbox("     ", ["Unknown", "Established", "Renowned"])

        # The expander with more information (optional)
        with st.expander("Logic"):
            st.markdown("""
                Although being a purely qualitative metric, the **Average Reputation of Operators** that the AVS chose to be opted in to validate its modules offers a useful glimpse into the AVS’s security profile. The user should consider operators’ historical slashing record and the overall validation and uptime performance, which are crucial in assessing overall operator-related risk for an AVS, including potential malicious collusions.                        
                        """)
            
    
    risk_score = weighted_risk_scores(security_audits_input, avg_validator_uptime_input, total_steth_input, number_validators_input, market_share_central_risk_input, barrier_entry_central_risk_input, avg_operator_reputation_input)

        

#########################################
#########################################
#########################################


    st.write("  \n")
    st.write("  \n")
    st.write("  \n")

    # Determine the color and background color based on the risk score
    if risk_score >= 7.5:
        color = "#d32f2f"  # Red color for high risk
        background_color = "#fde0dc"  # Light red background
    elif risk_score <= 2.5:
        color = "#388e3c"  # Green color for low risk
        background_color = "#ebf5eb"  # Light green background
    else:
        color = "black"  # Black color for medium risk
        background_color = "#ffffff"  # White background


    st.markdown(
    f"""
    <div style="
        border: 2px solid {color};
        border-radius: 5px;
        padding: 10px;
        text-align: center;
        margin: 10px 0;
        background-color: {background_color};">
        <h2 style="color: black; margin:0; font-size: 1.5em;">AVS Risk Score: <span style="font-size: 1.2em; color: {color};">{risk_score:.2f}</span></h2>
    </div>
    """, 
    unsafe_allow_html=True
    )

    st.write("  \n")
    st.write("  \n")


    st.write("""
            The **AVS Risk Score** ranges from 0 to 10, where 0 indicates the lowest level of risk and 10 represents the highest possible risk.
            
            The Risk Score is calculated based on the risk level of each input parameter as well as their weighting, which is determined by the **Likelihood** and **Impact** of that risk to the AVS. 
            For example, the Likelihood of a Security Audit posing a risk and its Impact on the integrity of the AVS are both greater than the Likelihood and Impact to an AVS of, say, its *Average Operator Reputation* and the *AVS Type* chosen. The Simulator takes these nuances into account.
             
            We arrive at the final AVS Risk Score through a 0 to 10 normalization of the sum of all the calculated risks per input.
            
            * * *
            
            It's important to bear in mind that this Simulator was built from an AVS perspective *alone*. 

            For a deeper dive, please visit the [source code](https://github.com/bmvicente/eigensimulators/blob/master/avsrisk/eigenavsrisk.py).
            """)


    st.write("  \n")
    st.write("  \n")
    st.write("  \n")
    st.write("  \n")
    st.write("  \n")
    st.write("  \n")
    st.write("  \n")
    st.write("  \n")
    st.write("  \n")
    st.write("  \n")
    st.write("  \n")
    st.write("  \n")
    st.write("  \n")
    st.write("  \n")
    st.write("  \n")
    st.write("  \n")



    #col11, col12, col13 = st.columns([2,1,2])

    #with col11:
    #    st.write("")

    #with col12:
    #    st.image("images/tokensight.png", width=250)

    #with col13:
    #    st.write("")
    
    
    image_url = 'https://img.freepik.com/free-vector/twitter-new-2023-x-logo-white-background-vector_1017-45422.jpg'
    link = 'https://twitter.com/tokensightxyz'
    markdown = f"""
    <a href="{link}" target="_blank">
        <img src="{image_url}" alt="Alt Text" style="display:block; margin-left: auto; margin-right: auto; width: 4%;">
    </a>
    """    
    st.markdown(markdown, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

