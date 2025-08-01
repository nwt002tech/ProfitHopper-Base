import streamlit as st
from datetime import datetime

def initialize_trip_state():
    # Initialize only if not already set
    if 'session_log' not in st.session_state:
        st.session_state.session_log = []
    if 'current_trip_id' not in st.session_state:
        st.session_state.current_trip_id = 1
    if 'casino_list' not in st.session_state:
        st.session_state.casino_list = sorted([
            "L'auberge Lake Charles",
            "Golden Nugget Lake Charles",
            "Caesar's Horseshoe Lake Charles",
            "Delta Downs",
            "Island View",
            "Paragon Marksville",
            "Coushatta"
        ])
    if 'trip_settings' not in st.session_state:
        st.session_state.trip_settings = {
            'casino': st.session_state.casino_list[0] if st.session_state.casino_list else "",
            'starting_bankroll': 100.0,
            'num_sessions': 10
        }
    # Initialize trip-specific bankroll tracking
    if 'trip_bankrolls' not in st.session_state:
        st.session_state.trip_bankrolls = {1: 100.0}

def get_current_trip_sessions():
    return [s for s in st.session_state.session_log 
            if s['trip_id'] == st.session_state.current_trip_id]

def get_trip_profit(trip_id=None):
    trip_id = trip_id or st.session_state.current_trip_id
    sessions = [s for s in st.session_state.session_log 
               if s['trip_id'] == trip_id]
    return sum(s['profit'] for s in sessions)

def get_current_bankroll():
    # Get current trip's starting bankroll
    starting = st.session_state.trip_settings['starting_bankroll']
    
    # Calculate profit for current trip
    current_trip_profit = get_trip_profit(st.session_state.current_trip_id)
    
    return starting + current_trip_profit

def get_session_bankroll():
    current_bankroll = get_current_bankroll()
    completed_sessions = len(get_current_trip_sessions())
    remaining_sessions = max(1, st.session_state.trip_settings['num_sessions'] - completed_sessions)
    
    return current_bankroll / remaining_sessions

def render_sidebar():
    with st.sidebar:
        st.header("Trip Settings")
        
        # Trip ID display
        st.markdown(f"""
        <div style="display:flex; align-items:center; margin-bottom:20px;">
            <span style="font-weight:bold; margin-right:10px;">Current Trip ID:</span>
            <span class="trip-id-badge">{st.session_state.current_trip_id}</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Casino selection
        new_casino = st.text_input("Add New Casino")
        if new_casino and new_casino not in st.session_state.casino_list:
            st.session_state.casino_list.append(new_casino)
            st.session_state.casino_list.sort()
            st.session_state.trip_settings['casino'] = new_casino
            st.success(f"Added {new_casino} to casino list")
        
        casino = st.selectbox("Casino", 
                             options=st.session_state.casino_list,
                             index=st.session_state.casino_list.index(
                                 st.session_state.trip_settings['casino']
                             ) if st.session_state.trip_settings['casino'] in st.session_state.casino_list else 0,
                             key='casino_select')
        st.session_state.trip_settings['casino'] = casino
        
        # Bankroll and sessions
        starting_bankroll = st.number_input("Starting Bankroll ($)", 
                                           min_value=0.0, 
                                           value=st.session_state.trip_settings['starting_bankroll'],
                                           step=100.0,
                                           format="%.2f",
                                           key='bankroll_input')
        st.session_state.trip_settings['starting_bankroll'] = starting_bankroll
        
        num_sessions = st.number_input("Number of Sessions", 
                                      min_value=1, 
                                      value=st.session_state.trip_settings['num_sessions'],
                                      step=1,
                                      key='session_count_input')
        st.session_state.trip_settings['num_sessions'] = num_sessions
        
        # New trip button
        if st.button("Start New Trip"):
            st.session_state.current_trip_id += 1
            st.session_state.session_log = []
            # Initialize bankroll for new trip
            st.session_state.trip_bankrolls[st.session_state.current_trip_id] = (
                st.session_state.trip_settings['starting_bankroll']
            )
            st.success(f"Started new trip! Trip ID: {st.session_state.current_trip_id}")
            st.rerun()
        
        st.markdown("---")
        
        # Trip summary
        st.subheader("Trip Summary")
        trip_sessions = get_current_trip_sessions()
        trip_profit = get_trip_profit()
        current_bankroll = get_current_bankroll()
        
        st.markdown(f"**Casino:** {st.session_state.trip_settings['casino']}")
        st.markdown(f"**Starting Bankroll:** ${st.session_state.trip_settings['starting_bankroll']:,.2f}")
        st.markdown(f"**Current Bankroll:** ${current_bankroll:,.2f}")
        st.markdown(f"**Sessions Completed:** {len(trip_sessions)}/{st.session_state.trip_settings['num_sessions']}")
        
        st.markdown("---")
        st.warning("""
        **Gambling Risk Notice:**  
        - These strategies don't guarantee profits  
        - Never gamble with money you can't afford to lose  
        - Set strict loss limits before playing  
        - Gambling addiction help: 1-800-522-4700
        """)