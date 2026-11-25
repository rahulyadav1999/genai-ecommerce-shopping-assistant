
import streamlit as st
from chatbot import FlipkartChatbot


# -----------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------

st.set_page_config(
    page_title="Flipkart AI Shopping Assistant",
    page_icon="🛍️",
    layout="centered"
)


# -----------------------------------------
# CUSTOM CSS
# -----------------------------------------

st.markdown(
    """
    <style>

    .main-title {
        font-size: 32px;
        font-weight: 700;
        color: #2874F0;
        text-align: center;
    }

    .subtitle {
        text-align: center;
        color: #777777;
        font-size: 16px;
        margin-bottom: 25px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# -----------------------------------------
# DISPLAY PRODUCT CARDS
# -----------------------------------------

def display_products(products):

    st.markdown("### 🛍️ Recommended Products")

    columns = st.columns(2)

    for index, product in enumerate(products):

        with columns[index % 2]:

            with st.container(border=True):

                st.markdown(f"**{product['title']}**")

                st.caption(f"Brand: {product['brand']}")

                st.markdown(f"### ₹{product['price']:,}")

                discount = round(product['discount'] * 100)

                st.caption(f"Discount: {discount}%")

                st.write(
                    f"⭐ {product['avg_rating']} "
                    f"({product['total_ratings']} ratings)"
                )

                st.link_button(
                    "View Product ↗",
                    product["product_link"],
                    use_container_width=True
                )


# -----------------------------------------
# INITIALIZE CHATBOT
# -----------------------------------------

@st.cache_resource
def load_chatbot():
    return FlipkartChatbot()


# -----------------------------------------
# INITIALIZE CHAT HISTORY
# -----------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# -----------------------------------------
# SIDEBAR
# -----------------------------------------

with st.sidebar:

    st.title("🛍️ Shopping Assistant")

    st.write(
        "Your AI-powered shopping assistant. "
        "Ask questions about products, prices, ratings, "
        "and store policies."
    )

    st.divider()

    st.subheader("What can I help you with?")

    st.markdown(
        """
        - Search shoes by brand
        - Find products within your budget
        - Compare product ratings
        - Ask about returns
        - Ask about refunds
        - Ask about shipping
        """
    )

    st.divider()

    if st.button("🗑️ Clear Chat", use_container_width=True):

        st.session_state.messages = []

        st.rerun()


# -----------------------------------------
# MAIN CHAT INTERFACE
# -----------------------------------------

st.markdown(
    '<div class="main-title">Flipkart AI Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Ask me about products, prices, ratings and store policies.'
    '</div>',
    unsafe_allow_html=True
)


# -----------------------------------------
# DISPLAY CHAT HISTORY
# -----------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        if message.get("type") == "products":

            display_products(message["content"])

        else:

            st.markdown(message["content"])


# -----------------------------------------
# USER INPUT
# -----------------------------------------

user_question = st.chat_input("Ask me something...")


if user_question:

    # Display customer question

    with st.chat_message("user"):

        st.markdown(user_question)

    st.session_state.messages.append({
        "role": "user",
        "content": user_question
    })


    # Generate chatbot response

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                # Initialize chatbot
                bot = load_chatbot()

                # Get chatbot response
                response = bot.chat(user_question)

                # Display product cards or text response

                if isinstance(response, list):

                    if response:
                        display_products(response)

                    else:
                        st.markdown(
                            "Sorry, I couldn't find matching "
                            "products in our catalogue."
                        )

                        response = (
                            "Sorry, I couldn't find matching "
                            "products in our catalogue."
                        )

                    st.session_state.messages.append({
                        "role": "assistant",
                        "type": "products" if response else "text",
                        "content": response
                    })

                else:

                    st.markdown(response)

                    st.session_state.messages.append({
                        "role": "assistant",
                        "type": "text",
                        "content": response
                    })


            except Exception as e:

                error_message = (
                    "Sorry, something went wrong while "
                    "processing your question. Please try again."
                )

                st.error(error_message)

                print("Chatbot Error:", e)

                st.session_state.messages.append({
                    "role": "assistant",
                    "type": "text",
                    "content": error_message
                })
