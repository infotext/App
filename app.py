import streamlit as st
import json
import random
from datetime import datetime, timedelta
import time
import requests

# Page configuration
st.set_page_config(
    page_title="SpiritConnect - Spiritual Wellness App",
    page_icon="🙏",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    /* Custom CSS for better UI */
    .stApp {
        max-width: 100% !important;
        padding: 0 !important;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 0 0 20px 20px;
        color: white;
        margin-bottom: 2rem;
    }
    
    .prayer-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
        border: 1px solid #e2e8f0;
    }
    
    .badge-emergency {
        background: #fed7d7;
        color: #c53030;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: bold;
        display: inline-flex;
        align-items: center;
        gap: 0.25rem;
    }
    
    .badge-critical {
        background: #feebc8;
        color: #c05621;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: bold;
        display: inline-flex;
        align-items: center;
        gap: 0.25rem;
    }
    
    .badge-needs {
        background: #c6f6d5;
        color: #22543d;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: bold;
        display: inline-flex;
        align-items: center;
        gap: 0.25rem;
    }
    
    .stats-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
    }
    
    .action-button {
        width: 100%;
        padding: 0.75rem;
        border-radius: 10px;
        border: none;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s;
        margin-top: 0.5rem;
    }
    
    .action-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .login-modal {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        max-width: 400px;
        margin: auto;
    }
    
    .user-avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
    }
    
    .tab-button {
        padding: 0.75rem 1.5rem;
        border: none;
        background: none;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.3s;
        border-bottom: 3px solid transparent;
    }
    
    .tab-button.active {
        border-bottom: 3px solid #667eea;
        color: #667eea;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'user' not in st.session_state:
    st.session_state.user = None
if 'prayers' not in st.session_state:
    st.session_state.prayers = [
        {"id": 1, "user": "Sarah J.", "type": "CRITICAL FINAL CALL", "title": "Emergency Surgery", 
         "body": "My father is going into heart surgery in 1 hour. Please pray for stability.", 
         "count": 142, "timestamp": "10m ago", "status": "active"},
        {"id": 2, "user": "Community", "type": "NEEDS", "title": "Peace for the Week", 
         "body": "Feeling overwhelmed with work and family balance.", 
         "count": 24, "timestamp": "2h ago", "status": "active"},
        {"id": 3, "user": "David K.", "type": "EMERGENCY", "title": "Accident Recovery", 
         "body": "Friend involved in car crash. Critical condition.", 
         "count": 89, "timestamp": "15m ago", "status": "active"}
    ]
if 'posts' not in st.session_state:
    st.session_state.posts = [
        {"id": 1, "title": "Finding Peace in Chaos", "verse": "Philippians 4:7", 
         "explanation": "The peace of God, which transcends all understanding...", 
         "audio": "sermon1.mp3", "tags": ["Peace", "Anxiety"], "lang": "en", 
         "image": "https://images.unsplash.com/photo-1507692049790-de58293a469d"}
    ]
if 'live_count' not in st.session_state:
    st.session_state.live_count = 487
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "home"
if 'show_login' not in st.session_state:
    st.session_state.show_login = False
if 'show_admin' not in st.session_state:
    st.session_state.show_admin = False

# Simulate live count updates
if 'last_update' not in st.session_state:
    st.session_state.last_update = datetime.now()

if (datetime.now() - st.session_state.last_update).seconds > 5:
    change = random.randint(-3, 5)
    st.session_state.live_count = max(450, min(550, st.session_state.live_count + change))
    st.session_state.last_update = datetime.now()

# Prayer Card Component
def prayer_card(prayer):
    with st.container():
        st.markdown(f"""
        <div class="prayer-card">
            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
                <div style="display: flex; align-items: center; gap: 0.75rem;">
                    <div class="user-avatar">{prayer['user'][0]}</div>
                    <div>
                        <div style="font-weight: bold; color: #2d3748;">{prayer['user']}</div>
                        <div style="font-size: 0.75rem; color: #718096;">{prayer['timestamp']}</div>
                    </div>
                </div>
                <div class="badge-{prayer['type'].split()[0].lower() if 'EMERGENCY' in prayer['type'] else prayer['type'].lower().split()[0]}">
                    {'⚠️' if prayer['type'] == 'EMERGENCY' else '🔥' if 'CRITICAL' in prayer['type'] else '🙏'}
                    {prayer['type']}
                </div>
            </div>
            
            <h3 style="margin: 0.5rem 0; color: #1a202c;">{prayer['title']}</h3>
            <p style="color: #4a5568; margin-bottom: 1.5rem;">{prayer['body']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button(f"🙏 Pray ({prayer['count']})", key=f"pray_{prayer['id']}", use_container_width=True):
                prayer['count'] += 1
                st.session_state.prayers = [p if p['id'] != prayer['id'] else prayer for p in st.session_state.prayers]
                st.success(f"Prayed for {prayer['user']}'s request! 🙏")
                st.rerun()
        with col2:
            if st.button("⏰ Remind", key=f"remind_{prayer['id']}", use_container_width=True):
                st.info(f"Reminder set for {prayer['title']}")
        with col3:
            if st.button("📤 Share", key=f"share_{prayer['id']}", use_container_width=True):
                st.info("Prayer request shared!")

# Header
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 1rem;">
        <div style="font-size: 1.5rem; font-weight: bold; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            SpiritConnect 🙏
        </div>
        <div style="font-size: 0.75rem; background: #e2e8f0; padding: 0.25rem 0.75rem; border-radius: 15px; color: #4a5568;">
            🔥 Live: {live_count} praying
        </div>
    </div>
    """.format(live_count=st.session_state.live_count), unsafe_allow_html=True)

with col3:
    if st.session_state.user:
        user = st.session_state.user
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 0.5rem; justify-content: end;">
            <div style="text-align: right;">
                <div style="font-weight: bold; font-size: 0.9rem;">{user['name']}</div>
                <div style="font-size: 0.75rem; color: #718096;">{user['role'].title()}</div>
            </div>
            <div class="user-avatar">{user['name'][0]}</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Logout", key="logout_btn", type="secondary"):
            st.session_state.user = None
            st.rerun()
    else:
        if st.button("🔐 Login / Register", key="login_btn", type="primary"):
            st.session_state.show_login = True
            st.rerun()

# Tabs
st.markdown("""
<div style="display: flex; gap: 0; border-bottom: 2px solid #e2e8f0; margin: 1.5rem 0;">
    <button class="tab-button {active_home}" onclick="window.parent.document.querySelector('section[data-testid=\"stAppViewContainer\"] iframe').contentWindow.parent.postMessage({{'type': 'change_tab', 'tab': 'home'}}, '*')">🏠 Home</button>
    <button class="tab-button {active_prayer}" onclick="window.parent.document.querySelector('section[data-testid=\"stAppViewContainer\"] iframe').contentWindow.parent.postMessage({{'type': 'change_tab', 'tab': 'prayer'}}, '*')">🙏 Prayer Wall</button>
    <button class="tab-button {active_media}" onclick="window.parent.document.querySelector('section[data-testid=\"stAppViewContainer\"] iframe').contentWindow.parent.postMessage({{'type': 'change_tab', 'tab': 'media'}}, '*')">🎵 Media</button>
    <button class="tab-button {active_profile}" onclick="window.parent.document.querySelector('section[data-testid=\"stAppViewBlockContainer\"] iframe').contentWindow.parent.postMessage({{'type': 'change_tab', 'tab': 'profile'}}, '*')">👤 Profile</button>
</div>
""".format(
    active_home="active" if st.session_state.active_tab == "home" else "",
    active_prayer="active" if st.session_state.active_tab == "prayer" else "",
    active_media="active" if st.session_state.active_tab == "media" else "",
    active_profile="active" if st.session_state.active_tab == "profile" else ""
), unsafe_allow_html=True)

# JavaScript for tab switching
st.markdown("""
<script>
window.addEventListener('message', function(event) {
    if (event.data.type === 'change_tab') {
        window.parent.document.querySelectorAll('[data-testid="stAppViewContainer"] button[kind="secondary"]')[0].click();
        setTimeout(() => {
            Streamlit.setComponentValue({tab: event.data.tab});
        }, 100);
    }
});
</script>
""", unsafe_allow_html=True)

# Home Tab
if st.session_state.active_tab == "home":
    # Hero Section
    st.markdown("""
    <div class="main-header">
        <h1 style="margin: 0; font-size: 2.5rem; font-weight: 300;">"Be still, and know that I am God"</h1>
        <p style="margin: 0.5rem 0 1.5rem 0; font-size: 1.2rem; opacity: 0.9;">— Psalm 46:10</p>
        <div style="background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); padding: 1rem; border-radius: 10px; border: 1px solid rgba(255,255,255,0.2);">
            In the rush of modern life, stillness is not just the absence of noise, but the presence of focus. 
            Take a moment to breathe today.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats
    col1, col2, col3 = st.columns(3)
    with col1:
        total_prayers = sum(p['count'] for p in st.session_state.prayers)
        st.markdown(f"""
        <div class="stats-card">
            <div style="font-size: 2.5rem; font-weight: bold;">{total_prayers}</div>
            <div>Prayers Today</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stats-card">
            <div style="font-size: 2.5rem; font-weight: bold;">{st.session_state.live_count}</div>
            <div>Active Now</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="stats-card">
            <div style="font-size: 2.5rem; font-weight: bold;">42</div>
            <div>Countries</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.subheader("Active Prayer Requests")
    for prayer in st.session_state.prayers[:2]:
        prayer_card(prayer)
    
    # Spiritual Content
    st.subheader("Daily Inspiration")
    for post in st.session_state.posts[:2]:
        with st.expander(f"📖 {post['title']} - {post['verse']}", expanded=False):
            st.write(post['explanation'])
            st.caption(f"Tags: {', '.join(post['tags'])}")

# Prayer Wall Tab
elif st.session_state.active_tab == "prayer":
    st.title("🙏 Prayer Wall")
    st.caption(f"Join {st.session_state.live_count} people praying right now")
    
    # New Prayer Form
    with st.form("new_prayer_form"):
        st.subheader("Share Your Prayer Request")
        prayer_title = st.text_input("Prayer Title", placeholder="What do you need prayer for?")
        prayer_body = st.text_area("Details", placeholder="Share your prayer need...", height=100)
        
        prayer_type = st.radio(
            "Prayer Type",
            ["NEEDS", "CRITICAL FINAL CALL", "EMERGENCY"],
            horizontal=True
        )
        
        submitted = st.form_submit_button("Submit Prayer Request", type="primary")
        if submitted and prayer_title and prayer_body:
            new_prayer = {
                "id": len(st.session_state.prayers) + 1,
                "user": st.session_state.user['name'] if st.session_state.user else "Anonymous",
                "type": prayer_type,
                "title": prayer_title,
                "body": prayer_body,
                "count": 0,
                "timestamp": "Just now",
                "status": "active"
            }
            st.session_state.prayers.insert(0, new_prayer)
            st.success("Prayer request submitted! 🙏")
            st.rerun()
    
    st.divider()
    
    # All Prayers
    for prayer in st.session_state.prayers:
        prayer_card(prayer)

# Media Tab
elif st.session_state.active_tab == "media":
    st.title("🎵 Media Center")
    
    tab1, tab2 = st.tabs(["🎵 Audio Sermons", "📺 Video Sanctuary"])
    
    with tab1:
        st.subheader("Recent Sermons")
        for post in st.session_state.posts:
            with st.container():
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                width: 60px; height: 60px; border-radius: 10px; 
                                display: flex; align-items: center; justify-content: center; color: white;">
                        🎵
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.write(f"**{post['title']}**")
                    st.caption(post['verse'])
                    if st.button("▶️ Play", key=f"play_{post['id']}"):
                        st.info(f"Playing: {post['title']}")
    
    with tab2:
        st.subheader("Featured Videos")
        col1, col2 = st.columns(2)
        videos = [
            {"title": "Sunday Service: Hope", "duration": "1:15:20"},
            {"title": "Morning Prayer Short", "duration": "0:59"}
        ]
        
        for i, video in enumerate(videos):
            with (col1 if i % 2 == 0 else col2):
                st.image("https://images.unsplash.com/photo-1510936111840-65e151ad71bb?w=400", 
                        caption=video['title'])
                st.caption(f"Duration: {video['duration']}")
                if st.button("▶️ Watch", key=f"watch_{i}"):
                    st.info(f"Playing: {video['title']}")

# Profile Tab
elif st.session_state.active_tab == "profile":
    if st.session_state.user:
        user = st.session_state.user
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown(f"""
            <div style="text-align: center;">
                <div class="user-avatar" style="width: 80px; height: 80px; margin: auto; font-size: 2rem;">
                    {user['name'][0]}
                </div>
                <h2>{user['name']}</h2>
                <div style="background: #e2e8f0; padding: 0.25rem 1rem; border-radius: 15px; display: inline-block;">
                    {user['role'].title()}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.subheader("My Stats")
            col_stats1, col_stats2, col_stats3 = st.columns(3)
            with col_stats1:
                st.metric("🔥 Streak", f"{user.get('streak', 0)} days")
            with col_stats2:
                st.metric("🙏 Prayers", "42")
            with col_stats3:
                st.metric("🌟 Impact", "High")
        
        if user['role'] == 'admin':
            st.divider()
            st.subheader("Admin Dashboard")
            
            if st.button("Open Admin Panel", type="primary"):
                st.session_state.show_admin = True
            
            # Quick admin actions
            col_admin1, col_admin2 = st.columns(2)
            with col_admin1:
                with st.expander("Add Content"):
                    title = st.text_input("Content Title")
                    body = st.text_area("Content Body")
                    if st.button("Publish", key="publish_content"):
                        new_post = {
                            "id": len(st.session_state.posts) + 1,
                            "title": title,
                            "verse": "Admin Content",
                            "explanation": body,
                            "audio": "",
                            "tags": ["Admin"],
                            "lang": "en",
                            "image": "https://images.unsplash.com/photo-1507692049790-de58293a469d"
                        }
                        st.session_state.posts.append(new_post)
                        st.success("Content published!")
            
            with col_admin2:
                with st.expander("Manage Prayers"):
                    for prayer in st.session_state.prayers[:3]:
                        st.write(f"**{prayer['title']}** - {prayer['count']} prayers")
                        if st.button(f"Delete", key=f"del_{prayer['id']}"):
                            st.session_state.prayers = [p for p in st.session_state.prayers if p['id'] != prayer['id']]
                            st.rerun()
    else:
        st.warning("Please login to view your profile")
        if st.button("Login Now", type="primary"):
            st.session_state.show_login = True
            st.rerun()

# Login Modal
if st.session_state.show_login:
    with st.container():
        st.markdown("""
        <div style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; 
                    background: rgba(0,0,0,0.5); display: flex; align-items: center; 
                    justify-content: center; z-index: 9999;">
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            login_tab, register_tab = st.tabs(["🔐 Login", "📝 Register"])
            
            with login_tab:
                with st.form("login_form"):
                    st.subheader("Welcome Back")
                    login_email = st.text_input("Email", key="login_email")
                    login_password = st.text_input("Password", type="password", key="login_password")
                    
                    col_login1, col_login2 = st.columns(2)
                    with col_login1:
                        login_submit = st.form_submit_button("Sign In", type="primary")
                    with col_login2:
                        if st.form_submit_button("Cancel"):
                            st.session_state.show_login = False
                            st.rerun()
                    
                    if login_submit:
                        # Demo login - in real app, connect to database
                        if login_email == "admin@spiritconnect.com" and login_password == "admin123":
                            st.session_state.user = {
                                "email": login_email,
                                "name": "Admin User",
                                "role": "admin",
                                "streak": 42
                            }
                            st.session_state.show_login = False
                            st.success("Admin login successful!")
                            st.rerun()
                        elif login_email and login_password:
                            st.session_state.user = {
                                "email": login_email,
                                "name": "John Doe",
                                "role": "user",
                                "streak": 12
                            }
                            st.session_state.show_login = False
                            st.success("Login successful!")
                            st.rerun()
                        else:
                            st.error("Please enter credentials")
                
                st.caption("Demo: admin@spiritconnect.com / admin123")
            
            with register_tab:
                with st.form("register_form"):
                    st.subheader("Join SpiritConnect")
                    reg_name = st.text_input("Full Name", key="reg_name")
                    reg_email = st.text_input("Email", key="reg_email")
                    reg_password = st.text_input("Password", type="password", key="reg_password")
                    reg_confirm = st.text_input("Confirm Password", type="password", key="reg_confirm")
                    
                    col_reg1, col_reg2 = st.columns(2)
                    with col_reg1:
                        reg_submit = st.form_submit_button("Create Account", type="primary")
                    with col_reg2:
                        if st.form_submit_button("Cancel"):
                            st.session_state.show_login = False
                            st.rerun()
                    
                    if reg_submit:
                        if reg_password != reg_confirm:
                            st.error("Passwords do not match")
                        elif reg_name and reg_email and reg_password:
                            st.session_state.user = {
                                "email": reg_email,
                                "name": reg_name,
                                "role": "user",
                                "streak": 0
                            }
                            st.session_state.show_login = False
                            st.success("Registration successful! Welcome to SpiritConnect! 🙏")
                            st.rerun()
                        else:
                            st.error("Please fill all fields")

# Admin Panel
if st.session_state.show_admin and st.session_state.user and st.session_state.user['role'] == 'admin':
    with st.container():
        st.markdown("""
        <div style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; 
                    background: rgba(0,0,0,0.7); display: flex; align-items: center; 
                    justify-content: center; z-index: 10000;">
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            with st.container():
                st.markdown("""
                <div style="background: white; padding: 2rem; border-radius: 15px; max-height: 80vh; overflow-y: auto;">
                """, unsafe_allow_html=True)
                
                st.title("👑 Admin Dashboard")
                
                tab_admin1, tab_admin2, tab_admin3 = st.tabs(["📊 Analytics", "📝 Manage Content", "👥 Users"])
                
                with tab_admin1:
                    st.subheader("Live Analytics")
                    col_a1, col_a2, col_a3 = st.columns(3)
                    with col_a1:
                        st.metric("Total Users", "1,254", "+12%")
                    with col_a2:
                        st.metric("Active Prayers", len(st.session_state.prayers), "+3")
                    with col_a3:
                        st.metric("Engagement", "87%", "+5%")
                    
                    st.subheader("Prayer Analytics")
                    for prayer in st.session_state.prayers:
                        st.progress(min(prayer['count'] / 200, 1.0), 
                                  text=f"{prayer['title']}: {prayer['count']} prayers")
                
                with tab_admin2:
                    st.subheader("Manage Prayer Requests")
                    for prayer in st.session_state.prayers:
                        col_m1, col_m2, col_m3 = st.columns([3, 1, 1])
                        with col_m1:
                            st.write(f"**{prayer['title']}**")
                            st.caption(f"By {prayer['user']} • {prayer['count']} prayers")
                        with col_m2:
                            if st.button("Edit", key=f"edit_{prayer['id']}"):
                                st.info("Edit feature coming soon")
                        with col_m3:
                            if st.button("Delete", key=f"admin_del_{prayer['id']}"):
                                st.session_state.prayers = [p for p in st.session_state.prayers if p['id'] != prayer['id']]
                                st.rerun()
                    
                    st.divider()
                    st.subheader("Add New Content")
                    with st.form("admin_content_form"):
                        content_title = st.text_input("Title")
                        content_body = st.text_area("Content", height=150)
                        content_type = st.selectbox("Type", ["Inspiration", "Devotional", "Teaching"])
                        
                        if st.form_submit_button("Publish Content", type="primary"):
                            new_content = {
                                "id": len(st.session_state.posts) + 1,
                                "title": content_title,
                                "verse": f"Admin: {content_type}",
                                "explanation": content_body,
                                "audio": "",
                                "tags": [content_type],
                                "lang": "en",
                                "image": "https://images.unsplash.com/photo-1507692049790-de58293a469d"
                            }
                            st.session_state.posts.append(new_content)
                            st.success("Content published successfully!")
                
                with tab_admin3:
                    st.subheader("User Management")
                    st.info("User management features coming in next update")
                
                if st.button("Close Admin Panel", type="secondary"):
                    st.session_state.show_admin = False
                    st.rerun()

# Footer
st.markdown("---")
col_f1, col_f2, col_f3 = st.columns(3)
with col_f2:
    st.markdown("""
    <div style="text-align: center; color: #718096; font-size: 0.9rem;">
        <p>SpiritConnect 🙏 • Bringing people together in prayer</p>
        <p>© 2024 • All prayers are confidential and respected</p>
    </div>
    """, unsafe_allow_html=True)

# Auto-refresh for live updates
if st.button("🔄 Refresh", key="refresh_btn"):
    st.rerun()

# Auto-refresh every 30 seconds
if st.session_state.active_tab == "home" or st.session_state.active_tab == "prayer":
    time.sleep(30)
    st.rerun()
