import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date
import time

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Vakyadharam - Spiritual Prayer Platform",
    page_icon="🙏",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.vakyadharam.com/help',
        'Report a bug': 'https://www.vakyadharam.com/bug',
        'About': '### Vakyadharam Prayer Platform 2026\nSpiritual support community'
    }
)

# ==================== CSS STYLING ====================
st.markdown("""
<style>
    /* Modern 2026 Design */
    .main-header {
        font-size: 3rem;
        color: #4B0082;
        text-align: center;
        padding: 20px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
        font-weight: 800;
    }
    
    .sub-header {
        font-size: 1.5rem;
        color: #555;
        text-align: center;
        margin-bottom: 40px;
    }
    
    /* Prayer Cards */
    .prayer-card {
        padding: 25px;
        border-radius: 20px;
        background: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        margin: 15px 0;
        border: 2px solid #f0f0f0;
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .prayer-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.12);
        border-color: #667eea;
    }
    
    .general-card { border-top: 5px solid #4CAF50; }
    .emergency-card { border-top: 5px solid #FF9800; }
    .critical-card { border-top: 5px solid #F44336; }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 12px 30px;
        border-radius: 25px;
        font-weight: 600;
        font-size: 16px;
        cursor: pointer;
        transition: all 0.3s;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    .emergency-btn > button {
        background: linear-gradient(45deg, #FF9800 0%, #FF5722 100%);
    }
    
    .critical-btn > button {
        background: linear-gradient(45deg, #F44336 0%, #D32F2F 100%);
    }
    
    /* Footer */
    .footer {
        background: linear-gradient(90deg, #1a237e 0%, #311b92 100%);
        color: white;
        padding: 20px;
        margin-top: 40px;
        border-radius: 15px;
    }
    
    /* Mobile Icons */
    .mobile-icons {
        display: flex;
        justify-content: space-around;
        padding: 15px 0;
        margin-top: 20px;
        background: #f8f9fa;
        border-radius: 15px;
    }
    
    /* Form Styling */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 10px 15px;
    }
    
    .stTextArea > div > div > textarea {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 15px;
    }
    
    /* Badge */
    .badge {
        display: inline-block;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
        margin-left: 10px;
    }
    
    .badge-new { background: #4CAF50; color: white; }
    .badge-praying { background: #2196F3; color: white; }
    .badge-answered { background: #9C27B0; color: white; }
</style>
""", unsafe_allow_html=True)

# ==================== SIDEBAR ====================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4322/4322991.png", width=100)
    st.markdown("# 🙏 Vakyadharam")
    st.markdown("### Spiritual Prayer Platform")
    st.markdown("---")
    
    # User Profile
    st.markdown("### 👤 Your Profile")
    user_name = st.text_input("Your Name", "Devotee")
    
    # Settings
    st.markdown("### ⚙️ Settings")
    notifications = st.checkbox("Push Notifications", True)
    theme = st.selectbox("Theme", ["Light", "Dark", "Spiritual"])
    language = st.selectbox("Language", ["English", "Telugu", "Hindi", "Tamil"])
    
    # AI Integration
    st.markdown("### 🤖 AI Integration")
    ai_services = st.multiselect(
        "Select AI Assistants:",
        ["ChatGPT", "DeepSeek", "Google AI", "Spiritual AI"]
    )
    
    # Database Connection
    if st.button("🔗 Connect Database"):
        with st.spinner("Connecting to SQL Server..."):
            time.sleep(2)
            st.success("✅ Database Connected")
    
    st.markdown("---")
    st.markdown("**📱 Mobile App 2026 Edition**")
    st.caption("Version 2.6.1 | Professional Grade")

# ==================== HEADER ====================
st.markdown('<h1 class="main-header">🙏 VAKYADHARAM PRAYER PLATFORM</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Spiritual Support • Community Prayer • Divine Connection</p>', unsafe_allow_html=True)

# Stats Row
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Today's Prayers", "1,247", "+128")
with col2:
    st.metric("Prayers Answered", "892", "73%")
with col3:
    st.metric("Active Users", "5,821", "+312")
with col4:
    st.metric("Prayer Groups", "47", "+3")

st.markdown("---")

# ==================== 3 PRAYER CARDS ====================
st.markdown("## 📿 Select Prayer Type")

col1, col2, col3 = st.columns(3)

with col1:
    with st.container():
        st.markdown('<div class="prayer-card general-card">', unsafe_allow_html=True)
        st.markdown("### 📖 General Prayer Needs")
        st.markdown("For daily life, health, family, blessings")
        st.markdown("**Examples:**")
        st.markdown("- Job opportunities")
        st.markdown("- Family harmony")
        st.markdown("- Health and wellness")
        st.markdown("- Academic success")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Button with custom CSS
        st.markdown('<div class="stButton">', unsafe_allow_html=True)
        if st.button("🙏 Request General Prayer", key="general_btn"):
            st.session_state.prayer_type = "General Prayer Needs"
            st.session_state.show_form = True
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    with st.container():
        st.markdown('<div class="prayer-card emergency-card">', unsafe_allow_html=True)
        st.markdown("### 🚨 Emergency Prayer")
        st.markdown("Urgent situations needing immediate prayer")
        st.markdown("**Examples:**")
        st.markdown("- Medical emergencies")
        st.markdown("- Accident victims")
        st.markdown("- Natural disasters")
        st.markdown("- Urgent decisions")
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown('<div class="stButton emergency-btn">', unsafe_allow_html=True)
        if st.button("🆘 Request Emergency Prayer", key="emergency_btn"):
            st.session_state.prayer_type = "Emergency Prayer"
            st.session_state.show_form = True
        st.markdown('</div>', unsafe_allow_html=True)

with col3:
    with st.container():
        st.markdown('<div class="prayer-card critical-card">', unsafe_allow_html=True)
        st.markdown("### ⚠️ Critical Condition")
        st.markdown("Serious illnesses, accidents, life-threatening")
        st.markdown("**Examples:**")
        st.markdown("- ICU patients")
        st.markdown("- Terminal illness")
        st.markdown("- Life-saving surgery")
        st.markdown("- Critical operations")
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown('<div class="stButton critical-btn">', unsafe_allow_html=True)
        if st.button("💔 Request Critical Prayer", key="critical_btn"):
            st.session_state.prayer_type = "Critical Condition"
            st.session_state.show_form = True
        st.markdown('</div>', unsafe_allow_html=True)

# ==================== PRAYER REQUEST FORM ====================
if st.session_state.get('show_form', False):
    st.markdown("---")
    st.markdown(f"## 📝 {st.session_state.prayer_type} Request Form")
    
    with st.form("prayer_request_form", clear_on_submit=True):
        # Personal Details
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Your Full Name*", user_name)
            email = st.text_input("Email Address")
            phone = st.text_input("Mobile Number")
        
        with col2:
            location = st.text_input("City/Country")
            age = st.number_input("Age", min_value=1, max_value=120, value=30)
            anonymous = st.checkbox("Submit anonymously")
        
        # Prayer Details
        st.markdown("### Prayer Details")
        prayer_title = st.text_input("Prayer Title*", placeholder="e.g., Healing from illness")
        
        prayer_details = st.text_area(
            "Detailed Description*",
            height=150,
            placeholder="Please describe your prayer request in detail. Be as specific as possible..."
        )
        
        # 3 OPTIONS AS YOU REQUESTED
        st.markdown("### 🙌 How would you like to respond?")
        response_option = st.radio(
            "Select one option:",
            [
                "✅ **I prayed for this request** - Click if you've prayed",
                "💬 **Leave a comment/encouragement** - Share supportive words",
                "✨ **Say: 'Amen / Praise / Bless / Heal'** - Spiritual affirmation"
            ],
            index=0
        )
        
        # Comment box if selected
        if "comment" in response_option.lower():
            comment = st.text_area("Your comment or words of encouragement:", height=100)
        
        # Media Upload Section
        st.markdown("### 🎵 Optional Media Attachment")
        media_type = st.radio(
            "Add media:",
            ["None", "Audio Recording", "Video Message", "YouTube Link", "Image"]
        )
        
        if media_type != "None":
            if media_type == "Audio Recording":
                audio_file = st.file_uploader("Upload audio file", type=["mp3", "wav", "m4a"])
                if audio_file:
                    st.audio(audio_file)
            elif media_type == "Video Message":
                video_file = st.file_uploader("Upload video file", type=["mp4", "mov", "avi"])
                if video_file:
                    st.video(video_file)
            elif media_type == "YouTube Link":
                youtube_url = st.text_input("YouTube Video URL")
                if youtube_url:
                    st.video(youtube_url)
            elif media_type == "Image":
                image_file = st.file_uploader("Upload image", type=["jpg", "png", "jpeg"])
                if image_file:
                    st.image(image_file, caption="Prayer image", width=300)
        
        # Submit Button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submitted = st.form_submit_button("📤 Submit Prayer Request", use_container_width=True)
        
        if submitted:
            with st.spinner("🕊️ Submitting your prayer to the divine network..."):
                time.sleep(2)
                
                # Success Animation
                st.balloons()
                st.success(f"🎉 **Thank you {name}!** Your {st.session_state.prayer_type} has been submitted to our prayer community.")
                
                # Prayer Receipt
                with st.expander("📋 View Prayer Receipt & Details", expanded=True):
                    prayer_id = f"PRAY{np.random.randint(10000, 99999)}"
                    
                    receipt_data = {
                        "Prayer ID": prayer_id,
                        "Submitted By": "Anonymous" if anonymous else name,
                        "Prayer Type": st.session_state.prayer_type,
                        "Submission Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Status": "⏳ Active - Community is praying",
                        "Response Option": response_option.split("**")[1].split("**")[0],
                        "Estimated Prayers": f"{np.random.randint(10, 100)}+ people will pray"
                    }
                    
                    for key, value in receipt_data.items():
                        st.write(f"**{key}:** {value}")
                    
                    # Progress bar
                    st.progress(0.3, text="Prayer progress: Gathering community...")
                
                # AI Generated Response
                if ai_services:
                    with st.chat_message("assistant"):
                        st.markdown("### 🤖 AI Spiritual Guidance:")
                        
                        ai_responses = {
                            "General Prayer Needs": f"Dear {name}, may divine grace surround you and your family. Your faith in sharing this request is the first step toward manifestation. Remember: 'Faith can move mountains.'",
                            "Emergency Prayer": f"{name}, in this urgent moment, may emergency grace flow to you. The community stands with you. 'God is our refuge and strength, an ever-present help in trouble.' - Psalm 46:1",
                            "Critical Condition": f"Divine healing energy is now directed toward this situation, {name}. Every prayer adds light. 'He heals the brokenhearted and binds up their wounds.' - Psalm 147:3"
                        }
                        
                        st.write(ai_responses.get(st.session_state.prayer_type, "May peace be with you."))
                        
                        # Suggested Actions
                        st.markdown("**Suggested actions:**")
                        st.markdown("1. **Deep breathing** - 5 minutes daily")
                        st.markdown("2. **Gratitude journal** - Write 3 things you're thankful for")
                        st.markdown("3. **Meditation** - 10 minutes of silent reflection")
                        st.markdown("4. **Community connect** - Share with prayer groups")
                
                # Push Notification Simulation
                if notifications:
                    st.info("🔔 **Push notification** sent to 1,247 prayer warriors")
                
                # Reset form state
                st.session_state.show_form = False

# ==================== DAILY BLOG SECTION ====================
st.markdown("---")
st.markdown("## 📖 Daily Spiritual Blog & Unlimited Posts")

# Create tabs for unlimited posts
tab_titles = ["Today's Message", "Scripture", "Testimonies", "Teachings", "Q&A", "Meditation", "More+"]
tabs = st.tabs(tab_titles)

with tabs[0]:
    st.markdown(f"### 📅 Daily Message - {date.today().strftime('%B %d, %Y')}")
    st.markdown("""
    #### The Power of Collective Prayer
    
    When we pray together, something miraculous happens. Our individual prayers merge into 
    a powerful stream of spiritual energy that can move mountains.
    
    **Today's Reflection:**
    > "For where two or three gather in my name, there am I with them." - Matthew 18:20
    
    **Practice for today:**
    1. Find 5 minutes of quiet time
    2. Visualize your prayer being answered
    3. Send loving energy to someone in need
    4. Practice gratitude for 3 blessings
    
    **Community Challenge:** Pray for 3 people today that you don't know personally.
    """)
    
    # Blog interaction
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Views", "2,847")
    with col2:
        st.metric("Shares", "156")
    with col3:
        st.metric("Comments", "89")

with tabs[1]:
    st.markdown("### 📜 Scripture of the Day")
    scriptures = [
        {
            "verse": "Philippians 4:6-7",
            "text": "Do not be anxious about anything, but in every situation, by prayer and petition, with thanksgiving, present your requests to God. And the peace of God, which transcends all understanding, will guard your hearts and your minds in Christ Jesus.",
            "theme": "Peace"
        },
        {
            "verse": "Psalm 34:17-18",
            "text": "The righteous cry out, and the LORD hears them; he delivers them from all their troubles. The LORD is close to the brokenhearted and saves those who are crushed in spirit.",
            "theme": "Comfort"
        },
        {
            "verse": "Jeremiah 29:12",
            "text": "Then you will call on me and come and pray to me, and I will listen to you.",
            "theme": "Promise"
        }
    ]
    
    for scripture in scriptures:
        with st.expander(f"{scripture['verse']} - {scripture['theme']}"):
            st.markdown(f"**{scripture['verse']}**")
            st.markdown(f"> {scripture['text']}")
            st.markdown(f"*Theme: {scripture['theme']}*")

with tabs[2]:
    st.markdown("### 🌟 Recent Prayer Testimonies")
    
    testimonies = pd.DataFrame({
        "Name": ["Rajesh", "Priya", "Arun", "Sunita", "Kumar"],
        "Prayer": ["Healing from cancer", "Job after 2 years", "Family reconciliation", "Fertility blessing", "Financial breakthrough"],
        "Result": ["✅ Complete remission", "✅ Dream job secured", "✅ Reunited after 5 years", "✅ Baby boy born", "✅ Debt free"],
        "Days": ["45", "30", "120", "280", "90"],
        "Prayers Received": ["1,247", "892", "2,156", "3,421", "1,089"]
    })
    
    st.dataframe(testimonies, use_container_width=True)
    
    # Add testimony button
    if st.button("➕ Share Your Testimony"):
        with st.form("testimony_form"):
            testimony = st.text_area("Your testimony:")
            if st.form_submit_button("Submit"):
                st.success("Testimony submitted for review!")

with tabs[3]:
    st.markdown("### 🧘 Spiritual Teachings")
    st.video("https://www.youtube.com/watch?v=zP2AaNWs3d8")
    
    teachings = [
        "The Art of Mindful Prayer",
        "Forgiveness as Healing",
        "Gratitude Changes Everything",
        "Meditation Techniques",
        "Understanding Divine Timing"
    ]
    
    for teaching in teachings:
        st.markdown(f"- **{teaching}**")
        st.caption(f"45 min teaching • {np.random.randint(100, 1000)} views")

# ==================== AUDIO/VIDEO PLAYER ====================
st.markdown("---")
st.markdown("## 🎵 Spiritual Media Center")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🕊️ Peaceful Meditation Music")
    
    # Audio Player
    audio_options = [
        {"title": "Guided Meditation", "duration": "15:00"},
        {"title": "Healing Frequencies", "duration": "30:00"},
        {"title": "Chanting for Peace", "duration": "45:00"},
        {"title": "Sleep Meditation", "duration": "60:00"}
    ]
    
    for audio in audio_options:
        with st.expander(f"🎵 {audio['title']} ({audio['duration']})"):
            st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
            col_a, col_b = st.columns(2)
            with col_a:
                st.button(f"▶️ Play", key=f"play_{audio['title']}")
            with col_b:
                st.button(f"⬇️ Download", key=f"dl_{audio['title']}")

with col2:
    st.markdown("### 📺 Inspirational Videos")
    
    # Video Player
    video_options = [
        {"title": "Morning Prayer", "duration": "10:24", "views": "12K"},
        {"title": "Healing Testimonies", "duration": "25:15", "views": "45K"},
        {"title": "Scripture Explained", "duration": "18:30", "views": "32K"},
        {"title": "Meditation Guide", "duration": "42:10", "views": "67K"}
    ]
    
    selected_video = st.selectbox(
        "Choose a video:",
        [f"{v['title']} ({v['duration']}) - {v['views']} views" for v in video_options]
    )
    
    # YouTube embed
    st.video("https://www.youtube.com/watch?v=zP2AaNWs3d8")
    
    # YouTube Links Input
    st.markdown("### Add YouTube Links")
    youtube_links = st.text_area(
        "Enter YouTube URLs (one per line):",
        "https://www.youtube.com/watch?v=zP2AaNWs3d8\nhttps://www.youtube.com/watch?v=JxS5E-kZc2s\nhttps://www.youtube.com/watch?v=7NK_JOkuSVY",
        height=100
    )

# ==================== DATABASE & API INTEGRATION ====================
st.markdown("---")
st.markdown("## 🔗 Advanced Features")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🗄️ Database Integration")
    
    if st.button("🔄 Connect to SQL Server"):
        with st.spinner("Establishing secure connection..."):
            time.sleep(3)
            
            # Simulated database data
            prayer_data = pd.DataFrame({
                "ID": range(1, 11),
                "Name": ["Anil", "Sunita", "Ravi", "Meena", "Kumar", "Priya", "Arun", "Sita", "Raj", "Lakshmi"],
                "Prayer Type": ["General", "Emergency", "Critical", "General", "Emergency", "General", "Critical", "General", "Emergency", "General"],
                "Date": pd.date_range(start="2024-01-01", periods=10),
                "Status": ["Answered", "Praying", "Praying", "Answered", "Praying", "Answered", "Praying", "Answered", "Praying", "Answered"],
                "Prayer Count": [45, 128, 89, 67, 156, 34, 201, 56, 178, 42]
            })
            
            st.success("✅ SQL Server Connected Successfully")
            st.dataframe(prayer_data, use_container_width=True)
            
            # Database Stats
            st.metric("Total Records", len(prayer_data))
            st.metric("Answered Prayers", len(prayer_data[prayer_data["Status"] == "Answered"]))

with col2:
    st.markdown("### 🤖 AI Integration Panel")
    
    ai_service = st.selectbox(
        "Select AI Service:",
        ["ChatGPT-4", "DeepSeek", "Google Gemini", "Custom Spiritual AI"]
    )
    
    ai_prompt = st.text_area(
        "Ask AI for spiritual guidance:",
        "How can I strengthen my prayer life?",
        height=100
    )
    
    if st.button("🔄 Get AI Response"):
        with st.spinner(f"Consulting {ai_service}..."):
            time.sleep(2)
            
            with st.chat_message("assistant"):
                st.markdown(f"### {ai_service} Response:")
                st.markdown("""
                Based on spiritual wisdom and AI analysis:
                
                1. **Consistency is key** - Pray at the same time daily
                2. **Quality over quantity** - 5 minutes of focused prayer is better than 30 distracted minutes
                3. **Journal your prayers** - Record requests and answers
                4. **Join prayer groups** - Community amplifies spiritual energy
                5. **Practice gratitude** - Start each prayer with thanks
                
                *"Prayer is not asking. It is a longing of the soul." - Mahatma Gandhi*
                """)
            
            st.success(f"✅ {ai_service} response generated")

# ==================== PUSH NOTIFICATIONS ====================
st.markdown("---")
st.markdown("## 🔔 Push Notification System")

notification_col1, notification_col2 = st.columns(2)

with notification_col1:
    st.markdown("### Notification Settings")
    
    enable_push = st.checkbox("Enable Push Notifications", True)
    
    if enable_push:
        st.checkbox("New prayer requests", True)
        st.checkbox("Prayer answered alerts", True)
        st.checkbox("Daily reminders", False)
        st.checkbox("Community updates", True)
        st.checkbox("Emergency alerts", True)
        
        notification_time = st.time_input("Preferred notification time")
        notification_sound = st.selectbox("Notification sound", ["Default", "Bell", "Chime", "Singing Bowl"])

with notification_col2:
    st.markdown("### Test Notifications")
    
    if st.button("📱 Send Test Notification"):
        with st.spinner("Sending test notification to your device..."):
            time.sleep(2)
            st.success("✅ Test notification sent!")
            st.info("Check your mobile device for the test prayer alert")

# ==================== MOBILE FOOTER ICONS ====================
st.markdown("---")
st.markdown('<div class="mobile-icons">', unsafe_allow_html=True)

footer_cols = st.columns(7)
with footer_cols[0]:
    st.markdown("🏠")
    st.caption("Home")
with footer_cols[1]:
    st.markdown("🙏")
    st.caption("Pray")
with footer_cols[2]:
    st.markdown("📖")
    st.caption("Blog")
with footer_cols[3]:
    st.markdown("🎵")
    st.caption("Media")
with footer_cols[4]:
    st.markdown("👥")
    st.caption("Groups")
with footer_cols[5]:
    st.markdown("⚙️")
    st.caption("Settings")
with footer_cols[6]:
    st.markdown("👤")
    st.caption("Profile")

st.markdown('</div>', unsafe_allow_html=True)

# ==================== FINAL FOOTER ====================
st.markdown("---")
st.markdown('<div class="footer">', unsafe_allow_html=True)

footer1, footer2, footer3, footer4 = st.columns(4)

with footer1:
    st.markdown("**📱 Mobile App**")
    st.markdown("iOS & Android")
    st.markdown("Version 2026.2.1")
    st.markdown("Professional Edition")

with footer2:
    st.markdown("**🔗 Connect**")
    st.markdown("Prayer Groups")
    st.markdown("Volunteer")
    st.markdown("Donate")
    st.markdown("Partner")

with footer3:
    st.markdown("**🛠️ Features**")
    st.markdown("Unlimited Posts")
    st.markdown("AI Integration")
    st.markdown("Push Notifications")
    st.markdown("Database API")

with footer4:
    st.markdown("**📞 Support**")
    st.markdown("help@vakyadharam.com")
    st.markdown("24/7 Prayer Line")
    st.markdown("FAQ")
    st.markdown("Contact Us")

st.markdown("---")
st.markdown("© 2026 Vakyadharam Prayer Platform • Professional Spiritual App • All prayers are confidential")
st.markdown("🙏 Your faith matters • 💖 Community support • ✨ Divine blessings")

st.markdown('</div>', unsafe_allow_html=True)

# ==================== SESSION STATE INITIALIZATION ====================
if 'prayer_count' not in st.session_state:
    st.session_state.prayer_count = 0
if 'show_form' not in st.session_state:
    st.session_state.show_form = False
if 'prayer_type' not in st.session_state:
    st.session_state.prayer_type = ""

# ==================== HIDDEN DEVELOPER OPTIONS ====================
with st.sidebar:
    with st.expander("🛠️ Developer Options"):
        if st.button("Clear Session State"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        
        if st.button("Debug Info"):
            st.write("Session State:", st.session_state)
            st.write("Python Version:", sys.version)
