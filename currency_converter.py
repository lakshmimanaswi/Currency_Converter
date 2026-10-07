import streamlit as st
import requests
from datetime import datetime


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Lakshmi Manaswi Currency Converter",
    page_icon="💱",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

/* Main application background */
.stApp {
    background: #F8FAFC;
}

/* Main headings */
h1 {
    color: #111827 !important;
}

h2 {
    color: #111827 !important;
}

h3 {
    color: #111827 !important;
}

/* Normal text */
p {
    color: #334155 !important;
}

/* Labels */
label {
    color: #1E293B !important;
}

/* Selectbox and number input labels */
div[data-testid="stWidgetLabel"] p {
    color: #1E293B !important;
    font-weight: 600;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #172033;
}

/* Sidebar text */
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: white !important;
}

/* Metric cards */
div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 6px 20px rgba(15, 23, 42, 0.07);
}

/* Metric labels */
div[data-testid="stMetric"] label {
    color: #64748B !important;
}

/* Metric values */
div[data-testid="stMetricValue"] {
    color: #111827 !important;
}

/* Buttons */
div[data-testid="stButton"] button {
    border-radius: 12px;
    font-weight: 700;
}

/* Primary button */
div[data-testid="stButton"] button[kind="primary"] {
    background: #4F46E5;
    color: white;
    border: none;
}

/* Container borders */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: white;
    border-radius: 18px;
    border: 1px solid #E2E8F0;
}

/* Captions */
.stCaption {
    color: #64748B !important;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# CURRENCY INFORMATION
# ============================================================

CURRENCY_INFO = {

    "INR": {
        "name": "Indian Rupee",
        "symbol": "₹",
        "flag": "🇮🇳"
    },

    "USD": {
        "name": "US Dollar",
        "symbol": "$",
        "flag": "🇺🇸"
    },

    "EUR": {
        "name": "Euro",
        "symbol": "€",
        "flag": "🇪🇺"
    },

    "GBP": {
        "name": "British Pound",
        "symbol": "£",
        "flag": "🇬🇧"
    },

    "JPY": {
        "name": "Japanese Yen",
        "symbol": "¥",
        "flag": "🇯🇵"
    },

    "CNY": {
        "name": "Chinese Yuan",
        "symbol": "¥",
        "flag": "🇨🇳"
    },

    "KRW": {
        "name": "South Korean Won",
        "symbol": "₩",
        "flag": "🇰🇷"
    },

    "AUD": {
        "name": "Australian Dollar",
        "symbol": "$",
        "flag": "🇦🇺"
    },

    "CAD": {
        "name": "Canadian Dollar",
        "symbol": "$",
        "flag": "🇨🇦"
    },

    "SGD": {
        "name": "Singapore Dollar",
        "symbol": "$",
        "flag": "🇸🇬"
    },

    "AED": {
        "name": "UAE Dirham",
        "symbol": "د.إ",
        "flag": "🇦🇪"
    },

    "SAR": {
        "name": "Saudi Riyal",
        "symbol": "﷼",
        "flag": "🇸🇦"
    },

    "CHF": {
        "name": "Swiss Franc",
        "symbol": "CHF",
        "flag": "🇨🇭"
    },

    "NZD": {
        "name": "New Zealand Dollar",
        "symbol": "$",
        "flag": "🇳🇿"
    },

    "HKD": {
        "name": "Hong Kong Dollar",
        "symbol": "$",
        "flag": "🇭🇰"
    },

    "THB": {
        "name": "Thai Baht",
        "symbol": "฿",
        "flag": "🇹🇭"
    },

    "MYR": {
        "name": "Malaysian Ringgit",
        "symbol": "RM",
        "flag": "🇲🇾"
    },

    "ZAR": {
        "name": "South African Rand",
        "symbol": "R",
        "flag": "🇿🇦"
    },

    "BRL": {
        "name": "Brazilian Real",
        "symbol": "R$",
        "flag": "🇧🇷"
    },

    "RUB": {
        "name": "Russian Ruble",
        "symbol": "₽",
        "flag": "🇷🇺"
    },

    "MXN": {
        "name": "Mexican Peso",
        "symbol": "$",
        "flag": "🇲🇽"
    },

    "TRY": {
        "name": "Turkish Lira",
        "symbol": "₺",
        "flag": "🇹🇷"
    },

    "IDR": {
        "name": "Indonesian Rupiah",
        "symbol": "Rp",
        "flag": "🇮🇩"
    },

    "PHP": {
        "name": "Philippine Peso",
        "symbol": "₱",
        "flag": "🇵🇭"
    },

    "VND": {
        "name": "Vietnamese Dong",
        "symbol": "₫",
        "flag": "🇻🇳"
    },

    "NOK": {
        "name": "Norwegian Krone",
        "symbol": "kr",
        "flag": "🇳🇴"
    },

    "SEK": {
        "name": "Swedish Krona",
        "symbol": "kr",
        "flag": "🇸🇪"
    },

    "DKK": {
        "name": "Danish Krone",
        "symbol": "kr",
        "flag": "🇩🇰"
    },

    "PLN": {
        "name": "Polish Zloty",
        "symbol": "zł",
        "flag": "🇵🇱"
    },

    "CZK": {
        "name": "Czech Koruna",
        "symbol": "Kč",
        "flag": "🇨🇿"
    },

    "ILS": {
        "name": "Israeli New Shekel",
        "symbol": "₪",
        "flag": "🇮🇱"
    },

    "PKR": {
        "name": "Pakistani Rupee",
        "symbol": "₨",
        "flag": "🇵🇰"
    },

    "BDT": {
        "name": "Bangladeshi Taka",
        "symbol": "৳",
        "flag": "🇧🇩"
    },

    "LKR": {
        "name": "Sri Lankan Rupee",
        "symbol": "Rs",
        "flag": "🇱🇰"
    }
}


# ============================================================
# GET CURRENCY LIST
# ============================================================

@st.cache_data(ttl=3600)
def get_currency_list():

    try:

        response = requests.get(
            "https://api.frankfurter.app/currencies",
            timeout=10
        )

        if response.status_code == 200:

            return dict(
                sorted(response.json().items())
            )

    except Exception:
        pass

    return {
        code: info["name"]
        for code, info in CURRENCY_INFO.items()
    }


# ============================================================
# GET EXCHANGE RATE
# ============================================================

@st.cache_data(ttl=300)
def get_exchange_rate(
    from_currency,
    to_currency
):

    if from_currency == to_currency:
        return 1.0

    try:

        response = requests.get(
            "https://api.frankfurter.app/latest",
            params={
                "from": from_currency,
                "to": to_currency
            },
            timeout=10
        )

        if response.status_code == 200:

            data = response.json()

            return data["rates"][to_currency]

    except Exception:
        return None

    return None


# ============================================================
# HEADER
# ============================================================

st.title("💱 Lakshmi Manaswi Currency Converter")

st.write(
    "🌍 Smart • Fast • Interactive • Live Currency Conversion"
)

st.divider()


# ============================================================
# LOAD CURRENCIES
# ============================================================

currencies = get_currency_list()

currency_codes = list(currencies.keys())


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("💱 Currency Hub")

    st.write("### 🌍 Available Currencies")

    st.info(
        f"{len(currency_codes)} currencies available"
    )

    st.divider()

    st.write("### ⭐ Popular Currencies")

    st.write("🇮🇳 INR — Indian Rupee")
    st.write("🇺🇸 USD — US Dollar")
    st.write("🇪🇺 EUR — Euro")
    st.write("🇬🇧 GBP — British Pound")
    st.write("🇯🇵 JPY — Japanese Yen")
    st.write("🇦🇺 AUD — Australian Dollar")
    st.write("🇨🇦 CAD — Canadian Dollar")
    st.write("🇸🇬 SGD — Singapore Dollar")

    st.divider()

    st.caption(
        "Live exchange rates are retrieved online."
    )


# ============================================================
# CONVERTER
# ============================================================

st.header("💰 Currency Conversion")

with st.container(border=True):

    col1, col2, col3 = st.columns(
        [2, 0.7, 2]
    )

    with col1:

        amount = st.number_input(
            "💵 Enter Amount",
            min_value=0.01,
            value=100.00,
            step=1.00,
            format="%.2f"
        )

        from_currency = st.selectbox(
            "🌐 From Currency",
            currency_codes,
            format_func=lambda code:
                f"{CURRENCY_INFO.get(code, {}).get('flag', '💰')} "
                f"{code} - "
                f"{currencies[code]}",
            index=(
                currency_codes.index("INR")
                if "INR" in currency_codes
                else 0
            )
        )

    with col2:

        st.write("")
        st.write("")

        swap = st.button(
            "⇄",
            use_container_width=True,
            help="Swap currencies"
        )

    with col3:

        to_currency = st.selectbox(
            "🌐 To Currency",
            currency_codes,
            format_func=lambda code:
                f"{CURRENCY_INFO.get(code, {}).get('flag', '💰')} "
                f"{code} - "
                f"{currencies[code]}",
            index=(
                currency_codes.index("USD")
                if "USD" in currency_codes
                else 0
            )
        )


# ============================================================
# SWAP
# ============================================================

if swap:

    from_currency, to_currency = (
        to_currency,
        from_currency
    )


# ============================================================
# CONVERT BUTTON
# ============================================================

st.write("")

button_left, button_center, button_right = st.columns(
    [1, 2, 1]
)

with button_center:

    convert = st.button(
        "💱 Convert Currency",
        type="primary",
        use_container_width=True
    )


# ============================================================
# RESULT
# ============================================================

if convert:

    with st.spinner(
        "🔄 Fetching latest exchange rate..."
    ):

        rate = get_exchange_rate(
            from_currency,
            to_currency
        )

    if rate is None:

        st.error(
            "❌ Could not retrieve the exchange rate. "
            "Please check your internet connection."
        )

    else:

        converted_amount = amount * rate

        from_info = CURRENCY_INFO.get(
            from_currency,
            {
                "name": currencies[from_currency],
                "symbol": from_currency,
                "flag": "💰"
            }
        )

        to_info = CURRENCY_INFO.get(
            to_currency,
            {
                "name": currencies[to_currency],
                "symbol": to_currency,
                "flag": "💰"
            }
        )

        st.divider()

        st.header("🎯 Conversion Result")

        # ----------------------------------------------------
        # THREE MAIN METRICS
        # ----------------------------------------------------

        result1, result2, result3 = st.columns(3)

        with result1:

            st.metric(
                label=(
                    f"{from_info['flag']} "
                    f"{from_currency}"
                ),
                value=(
                    f"{from_info['symbol']}"
                    f"{amount:,.2f}"
                )
            )

        with result2:

            st.metric(
                label="📈 Exchange Rate",
                value=f"{rate:,.6f}"
            )

        with result3:

            st.metric(
                label=(
                    f"{to_info['flag']} "
                    f"{to_currency}"
                ),
                value=(
                    f"{to_info['symbol']}"
                    f"{converted_amount:,.2f}"
                )
            )

        st.write("")

        st.success(
            f"💱 {from_info['symbol']}{amount:,.2f} "
            f"{from_currency} = "
            f"{to_info['symbol']}{converted_amount:,.2f} "
            f"{to_currency}"
        )

        # ----------------------------------------------------
        # CURRENCY DETAILS
        # ----------------------------------------------------

        st.header("💵 Currency Details")

        detail1, detail2 = st.columns(2)

        with detail1:

            with st.container(border=True):

                st.subheader(
                    f"{from_info['flag']} "
                    f"{from_currency}"
                )

                st.write(
                    f"**Currency:** "
                    f"{from_info['name']}"
                )

                st.write(
                    f"**Symbol:** "
                    f"{from_info['symbol']}"
                )

                st.write(
                    "**Role:** Source Currency"
                )

        with detail2:

            with st.container(border=True):

                st.subheader(
                    f"{to_info['flag']} "
                    f"{to_currency}"
                )

                st.write(
                    f"**Currency:** "
                    f"{to_info['name']}"
                )

                st.write(
                    f"**Symbol:** "
                    f"{to_info['symbol']}"
                )

                st.write(
                    "**Role:** Target Currency"
                )

        # ----------------------------------------------------
        # INFORMATION
        # ----------------------------------------------------

        st.header("📊 Conversion Information")

        info1, info2, info3 = st.columns(3)

        with info1:

            st.metric(
                "Exchange Rate",
                f"{rate:,.6f}"
            )

        with info2:

            st.metric(
                "Source",
                from_currency
            )

        with info3:

            st.metric(
                "Target",
                to_currency
            )

        st.caption(
            "🕒 Conversion time: "
            + datetime.now().strftime(
                "%d %B %Y, %I:%M %p"
            )
        )


# ============================================================
# POPULAR CURRENCY PAIRS
# ============================================================

st.divider()

st.header("🌎 Popular Currency Pairs")

popular_pairs = [
    ("INR", "USD"),
    ("USD", "EUR"),
    ("EUR", "GBP"),
    ("USD", "JPY"),
    ("USD", "INR"),
    ("GBP", "INR")
]

pair_columns = st.columns(3)

for index, pair in enumerate(popular_pairs):

    base = pair[0]
    target = pair[1]

    base_info = CURRENCY_INFO.get(
        base,
        {
            "name": currencies.get(base, base),
            "flag": "💰"
        }
    )

    target_info = CURRENCY_INFO.get(
        target,
        {
            "name": currencies.get(target, target),
            "flag": "💰"
        }
    )

    with pair_columns[index % 3]:

        with st.container(border=True):

            st.subheader(
                f"{base_info['flag']} "
                f"{base}  →  "
                f"{target_info['flag']} "
                f"{target}"
            )

            st.write(
                f"{base_info['name']} "
                f"→ "
                f"{target_info['name']}"
            )

            st.caption(
                "Popular international currency pair"
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.subheader(
    "💱 Lakshmi Manaswi Currency Converter"
)

st.write(
    "🌍 International Currency Conversion  •  "
    "⚡ Live Exchange Rates  •  "
    "💻 Built with Streamlit"
)

st.caption(
    "Clean • Interactive • Responsive"
)