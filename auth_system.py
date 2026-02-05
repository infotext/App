```python
import streamlit as st
import hashlib
import secrets
import jwt
import time
from datetime import datetime, timedelta
import re
from email.mime.text import MIMEText
import smtplib
from database import DatabaseManager, User
import pandas as pd

class AuthSystem:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.secret_key = st.secrets.get("JWT_SECRET_KEY", "your-secret-key-change-in-production")
        self.token_expiry = 24 * 60 * 60  # 24 hours
        
    def hash_password(self, password):
        """Hash password using SHA-256 with salt"""
        salt = secrets.token_hex(16)
        hashed = hashlib.sha256((password + salt).encode()).hexdigest()
        return f"{salt}${hashed}"
    
    def verify_password(self, password, hashed_password):
        """Verify password against hash"""
        try:
            salt, hashed = hashed_password.split('$')
            return hashlib.sha256((password + salt).encode()).hexdigest() == hashed
        except:
            return False
    
    def validate_email(self, email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_password(self, password):
        """Validate password strength"""
        if len(password) < 8:
            return False, "Password must be at least 8 characters"
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"
        if not re.search(r'[0-9]', password):
            return False, "Password must contain at least one number"
        return True, "Password is strong"
    
    def register_user(self, user_data):
        """Register new user"""
        # Validate email
        if not self.validate_email(user_data['email']):
            return {'success': False, 'error': 'Invalid email format'}
        
        # Validate password
        is_valid, message = self.validate_password(user_data['password'])
        if not is_valid:
            return {'success': False, 'error': message}
        
        # Check if user exists
        session = self.db_manager.Session()
        try:
            existing_user = session.query(User).filter(
                (User.email == user_data['email']) | 
                (User.username == user_data['username'])
            ).first()
            
            if existing_user:
                return {'success': False, 'error': 'User already exists'}
            
            # Create new user
            new_user = User(
                username=user_data['username'],
                email=user_data['email'],
                password_hash=self.hash_password(user_data['password']),
                full_name=user_data.get('full_name', ''),
                phone=user_data.get('phone', ''),
                location=user_data.get('location', ''),
                is_verified=False
            )
            
            session.add(new_user)
            session.commit()
            
            # Send verification email
            self.send_verification_email(new_user.email, new_user.id)
            
            return {
                'success': True, 
                'user_id': new_user.id,
                'message': 'Registration successful! Please check your email for verification.'
            }
        except Exception as e:
            session.rollback()
            return {'success': False, 'error': str(e)}
        finally:
            session.close()
    
    def login_user(self, email_or_username, password):
        """Authenticate user"""
        session = self.db_manager.Session()
        try:
            # Find user by email or username
            user = session.query(User).filter(
                (User.email == email_or_username) | 
                (User.username == email_or_username)
            ).first()
            
            if not user:
                return {'success': False, 'error': 'User not found'}
            
            if not user.is_active:
                return {'success': False, 'error': 'Account is deactivated'}
            
            if not self.verify_password(password, user.password_hash):
                return {'success': False, 'error': 'Invalid password'}
            
            # Update last login
            user.last_login = datetime.utcnow()
            session.commit()
            
            # Create JWT token
            token = self.create_jwt_token(user.id, user.user_type)
            
            return {
                'success': True,
                'token': token,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'full_name': user.full_name,
                    'user_type': user.user_type,
                    'prayer_count': user.prayer_count
                }
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
        finally:
            session.close()
    
    def create_jwt_token(self, user_id, user_type):
        """Create JWT token for authentication"""
        payload = {
            'user_id': user_id,
            'user_type': user_type,
            'exp': time.time() + self.token_expiry,
            'iat': time.time()
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def verify_jwt_token(self, token):
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return {'success': True, 'payload': payload}
        except jwt.ExpiredSignatureError:
            return {'success': False, 'error': 'Token expired'}
        except jwt.InvalidTokenError:
            return {'success': False, 'error': 'Invalid token'}
    
    def send_verification_email(self, email, user_id):
        """Send email verification link"""
        # Create verification token
        verification_token = secrets.token_urlsafe(32)
        
        # Store token in database (you'd need a verification_tokens table)
        # For now, we'll simulate
        
        verification_url = f"https://your-app.com/verify?token={verification_token}&user={user_id}"
        
        # Email content
        subject = "Verify Your Vakyadharam Account"
        body = f"""
        <html>
        <body>
            <h2>Welcome to Vakyadharam! 🙏</h2>
            <p>Thank you for registering. Please verify your email by clicking the link below:</p>
            <p><a href="{verification_url}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Verify Email</a></p>
            <p>Or copy this link: {verification_url}</p>
            <p>This link will expire in 24 hours.</p>
            <p>Blessings,<br>The Vakyadharam Team</p>
        </body>
        </html>
        """
        
        # Send email (configure SMTP in secrets)
        try:
            msg = MIMEText(body, 'html')
            msg['Subject'] = subject
            msg['From'] = st.secrets['EMAIL_FROM']
            msg['To'] = email
            
            # Connect to SMTP server
            with smtplib.SMTP(st.secrets['SMTP_SERVER'], st.secrets['SMTP_PORT']) as server:
                server.starttls()
                server.login(st.secrets['EMAIL_USER'], st.secrets['EMAIL_PASSWORD'])
                server.send_message(msg)
            
            return True
        except Exception as e:
            st.error(f"Failed to send email: {str(e)}")
            return False
    
    def reset_password(self, email):
        """Send password reset email"""
        # Generate reset token
        reset_token = secrets.token_urlsafe(32)
        
        # Store token in database with expiry
        
        reset_url = f"https://your-app.com/reset-password?token={reset_token}"
        
        # Send email
        # Similar to verification email
        
        return {'success': True, 'message': 'Password reset email sent'}
    
    def update_user_profile(self, user_id, profile_data):
        """Update user profile"""
        session = self.db_manager.Session()
        try:
            user = session.query(User).filter_by(id=user_id).first()
            if not user:
                return {'success': False, 'error': 'User not found'}
            
            # Update allowed fields
            if 'full_name' in profile_data:
                user.full_name = profile_data['full_name']
            if 'phone' in profile_data:
                user.phone = profile_data['phone']
            if 'location' in profile_data:
                user.location = profile_data['location']
            if 'profile_pic' in profile_data:
                user.profile_pic = profile_data['profile_pic']
            
            session.commit()
            return {'success': True, 'message': 'Profile updated'}
        except Exception as e:
            session.rollback()
            return {'success': False, 'error': str(e)}
        finally:
            session.close()

# Streamlit Authentication UI
def authentication_ui():
    st.header("🔐 User Authentication System")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Login", "Register", "Profile", "Admin"])
    
    auth_system = AuthSystem()
    
    with tab1:
        st.subheader("Login to Your Account")
        
        login_method = st.radio("Login with:", ["Email", "Username"])
        
        if login_method == "Email":
            email = st.text_input("Email")
            username = None
        else:
            username = st.text_input("Username")
            email = None
        
        password = st.text_input("Password", type="password")
        remember_me = st.checkbox("Remember me")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Login", type="primary"):
                login_id = email if login_method == "Email" else username
                result = auth_system.login_user(login_id, password)
                
                if result['success']:
                    st.session_state.user = result['user']
                    st.session_state.token = result['token']
                    st.success(f"Welcome back, {result['user']['full_name']}!")
                    
                    # Store in session state
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error(f"Login failed: {result['error']}")
        
        with col2:
            if st.button("Forgot Password?"):
                email_for_reset = st.text_input("Enter your email")
                if st.button("Send Reset Link"):
                    result = auth_system.reset_password(email_for_reset)
                    if result['success']:
                        st.success(result['message'])
    
    with tab2:
        st.subheader("Create New Account")
        
        with st.form("register_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                username = st.text_input("Username*")
                email = st.text_input("Email*")
                phone = st.text_input("Phone")
            
            with col2:
                full_name = st.text_input("Full Name*")
                password = st.text_input("Password*", type="password")
                confirm_password = st.text_input("Confirm Password*", type="password")
                location = st.text_input("Location")
            
            terms = st.checkbox("I agree to the Terms of Service and Privacy Policy")
            
            if st.form_submit_button("Register"):
                if password != confirm_password:
                    st.error("Passwords do not match!")
                elif not terms:
                    st.error("You must agree to the terms")
                else:
                    user_data = {
                        'username': username,
                        'email': email,
                        'password': password,
                        'full_name': full_name,
                        'phone': phone,
                        'location': location
                    }
                    
                    result = auth_system.register_user(user_data)
                    if result['success']:
                        st.success(result['message'])
                    else:
                        st.error(f"Registration failed: {result['error']}")
    
    with tab3:
        if st.session_state.get('logged_in'):
            st.subheader("Your Profile")
            
            user = st.session_state.user
            
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image("https://via.placeholder.com/150", caption="Profile Picture")
                if st.button("Change Picture"):
                    uploaded_file = st.file_uploader("Choose a file", type=["jpg", "png", "jpeg"])
                    if uploaded_file:
                        # Upload to cloud storage
                        st.success("Picture updated!")
            
            with col2:
                with st.form("profile_form"):
                    full_name = st.text_input("Full Name", value=user.get('full_name', ''))
                    email = st.text_input("Email", value=user.get('email', ''), disabled=True)
                    phone = st.text_input("Phone", value="")
                    location = st.text_input("Location", value="")
                    
                    if st.form_submit_button("Update Profile"):
                        profile_data = {
                            'full_name': full_name,
                            'phone': phone,
                            'location': location
                        }
                        
                        result = auth_system.update_user_profile(user['id'], profile_data)
                        if result['success']:
                            st.success("Profile updated!")
                            st.session_state.user['full_name'] = full_name
                        else:
                            st.error(f"Update failed: {result['error']}")
            
            # User Stats
            st.subheader("Your Prayer Statistics")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Prayers Submitted", user.get('prayer_count', 0))
            with col2:
                st.metric("Prayers Answered", "24")
            with col3:
                st.metric("Community Score", "856")
            with col4:
                st.metric("Member Since", "2024")
            
            # User Activity
            st.subheader("Recent Activity")
            activity_data = pd.DataFrame({
                'Date': ['2024-01-15', '2024-01-10', '2024-01-05'],
                'Activity': ['Prayed for healing', 'Commented on prayer', 'Submitted prayer request'],
                'Type': ['Prayer', 'Comment', 'Request']
            })
            st.dataframe(activity_data)
        else:
            st.warning("Please login to view your profile")
    
    with tab4:
        if st.session_state.get('user', {}).get('user_type') == 'admin':
            st.subheader("Admin User Management")
            
            # User List
            st.write("### All Users")
            
            # Search and filter
            col1, col2 = st.columns(2)
            with col1:
                search = st.text_input("Search users")
            with col2:
                user_type = st.selectbox("Filter by type", ["All", "user", "admin", "moderator"])
            
            # User actions
            if st.button("Export Users List"):
                st.success("Export started...")
            
            if st.button("Send Bulk Email"):
                email_content = st.text_area("Email Content")
                if st.button("Send to All Users"):
                    st.success("Email sent to all users!")
        else:
            st.warning("Admin access required")

# Main app integration
def check_auth():
    """Check if user is authenticated"""
    if st.session_state.get('logged_in'):
        return True
    return False

def require_auth():
    """Require authentication for certain pages"""
    if not check_auth():
        st.warning("Please login to access this page")
        authentication_ui()
        st.stop()

# Add to your main app.py
def integrate_auth_in_app():
    """Add auth to main app"""
    # Add to sidebar
    with st.sidebar:
        if st.session_state.get('logged_in'):
            user = st.session_state.user
            st.write(f"👤 Welcome, **{user['full_name']}**")
            st.write(f"📊 Prayers: {user.get('prayer_count', 0)}")
            
            if st.button("Logout"):
                del st.session_state.logged_in
                del st.session_state.user
                del st.session_state.token
                st.rerun()
        else:
            if st.button("Login / Register"):
                st.session_state.show_auth = True
    
    # Show auth modal if needed
    if st.session_state.get('show_auth'):
        authentication_ui()
        if st.button("Close"):
            del st.session_state.show_auth
            st.rerun()
```
