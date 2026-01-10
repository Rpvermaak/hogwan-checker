import streamlit as st
import pandas as pd

@st.cache_data
def load_combined_data():
    try:
        # Load both files
        green_df = pd.read_csv('data/greenlist.csv')
        black_df = pd.read_csv('data/blacklist.csv')
        
        # Add a status column to identify them
        green_df['Status'] = '🟢 Green List'
        black_df['Status'] = '🔴 Black List'
        
        # Combine them into one big table
        combined = pd.concat([green_df, black_df], ignore_index=True)
        return combined
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()  # Return empty dataframe

df = load_combined_data()

if df.empty:
    st.error("No data loaded. Please check the CSV files.")
else:
    st.title("Korea Hagwon Search")

# Search Bar
query = st.text_input("Enter Hagwon name or region")

if query:
    # This searches across all columns (Name, Location, etc.)
    mask = df.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)
    results = df[mask]
    
    if not results.empty:
        # Displaying results with the Status column clearly visible
        st.dataframe(results, use_container_width=True)
    else:
        st.write("No matches found.")

# --- FOOTER SECTION ---
st.divider() # Adds a clean horizontal line

# Using columns to organize the footer
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### ⚖️ Legal Disclaimer & Data Attribution")
    st.markdown("**Data Source**")
    st.caption(
        "The information provided on this platform is aggregated from public records and community-contributed lists, primarily sourced from Tokyo Jon’s Hagwon Blacklist. This website acts solely as a search interface to make these public records more accessible to the teaching community."
    )
    st.markdown("**Disclaimer of Liability**")
    st.caption(
        "No Verification: The developers of this website do not verify, validate, or investigate the claims made in the 'Green List' or 'Black List.' All entries are the subjective opinions and personal experiences of the original anonymous posters.\n\n"
        "Accuracy: Information is provided 'as is' for informational purposes only. We do not guarantee that the information is current, accurate, or complete. Hagwons may change ownership, management, or practices after a post is made.\n\n"
        "No Endorsement: Inclusion on the 'Green List' does not constitute an endorsement, and inclusion on the 'Black List' does not constitute a factual finding of misconduct by this website.\n\n"
        "Legal Responsibility: Users are encouraged to perform their own due diligence before signing any employment contract. This website and its creators shall not be held liable for any damages, legal disputes, or employment issues arising from the use of this data.\n\n"
        "Removal Requests: As this site is a secondary aggregator, users wishing to dispute or remove a specific post should contact the original source at Tokyo Jon’s."
    )

with col2:
    st.markdown("### 🔗 Source")
    # This creates a clickable link to the original site
    st.link_button("Tokyo Jon's Blacklist", "https://blacklist.tokyojon.com/")
    st.link_button("Tokyo Jon's Greenlist", "https://greenlist.tokyojon.com/")

st.info("💡 Tip: Always cross-reference multiple sources before signing a contract.", icon="ℹ️")