```python
import psycopg2
import mysql.connector
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import json

Base = declarative_base()

# SQLAlchemy Models
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True)
    email = Column(String(200), unique=True)
    password_hash = Column(String(255))
    full_name = Column(String(200))
    phone = Column(String(20))
    location = Column(String(200))
    profile_pic = Column(String(500))
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)
    prayer_count = Column(Integer, default=0)
    user_type = Column(String(20), default='user')  # user, admin, moderator
    notification_token = Column(Text)

class PrayerRequest(Base):
    __tablename__ = 'prayer_requests'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    prayer_type = Column(String(50))  # general, emergency, critical
    title = Column(String(200))
    description = Column(Text)
    urgency_level = Column(Integer)  # 1-10
    is_anonymous = Column(Boolean, default=False)
    status = Column(String(50), default='pending')  # pending, praying, answered
    answered_details = Column(Text)
    answered_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    prayer_count = Column(Integer, default=0)  # how many people prayed
    tags = Column(String(500))  # JSON string of tags
    media_urls = Column(Text)  # JSON string of media URLs

class PrayerResponse(Base):
    __tablename__ = 'prayer_responses'
    
    id = Column(Integer, primary_key=True)
    prayer_id = Column(Integer)
    user_id = Column(Integer)
    response_type = Column(String(50))  # prayed, comment, amen
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_anonymous = Column(Boolean, default=False)

class BlogPost(Base):
    __tablename__ = 'blog_posts'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    content = Column(Text)
    author_id = Column(Integer)
    category = Column(String(100))
    tags = Column(String(500))
    featured_image = Column(String(500))
    view_count = Column(Integer, default=0)
    is_published = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

class Notification(Base):
    __tablename__ = 'notifications'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    title = Column(String(200))
    message = Column(Text)
    notification_type = Column(String(50))
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    action_url = Column(String(500))

class DatabaseManager:
    def __init__(self, db_type='postgresql'):
        self.db_type = db_type
        self.engine = None
        self.Session = None
        
    def connect(self):
        """Connect to database using Streamlit secrets"""
        try:
            if self.db_type == 'postgresql':
                connection_string = (
                    f"postgresql://{st.secrets['DB_USER']}:{st.secrets['DB_PASSWORD']}"
                    f"@{st.secrets['DB_HOST']}:{st.secrets['DB_PORT']}"
                    f"/{st.secrets['DB_NAME']}"
                )
            else:  # mysql
                connection_string = (
                    f"mysql+mysqlconnector://{st.secrets['DB_USER']}:{st.secrets['DB_PASSWORD']}"
                    f"@{st.secrets['DB_HOST']}:{st.secrets['DB_PORT']}"
                    f"/{st.secrets['DB_NAME']}"
                )
            
            self.engine = create_engine(connection_string)
            self.Session = sessionmaker(bind=self.engine)
            Base.metadata.create_all(self.engine)
            
            st.success("✅ Database connected successfully!")
            return True
        except Exception as e:
            st.error(f"Database connection failed: {str(e)}")
            return False
    
    def add_prayer_request(self, prayer_data):
        """Add new prayer request to database"""
        session = self.Session()
        try:
            new_prayer = PrayerRequest(
                user_id=prayer_data.get('user_id'),
                prayer_type=prayer_data.get('prayer_type'),
                title=prayer_data.get('title', ''),
                description=prayer_data.get('description', ''),
                urgency_level=prayer_data.get('urgency_level', 5),
                is_anonymous=prayer_data.get('is_anonymous', False),
                tags=json.dumps(prayer_data.get('tags', [])),
                media_urls=json.dumps(prayer_data.get('media_urls', []))
            )
            
            session.add(new_prayer)
            session.commit()
            
            # Update user's prayer count
            if prayer_data.get('user_id'):
                user = session.query(User).filter_by(id=prayer_data['user_id']).first()
                if user:
                    user.prayer_count += 1
                    session.commit()
            
            return {'success': True, 'prayer_id': new_prayer.id}
        except Exception as e:
            session.rollback()
            return {'success': False, 'error': str(e)}
        finally:
            session.close()
    
    def get_prayer_requests(self, filters=None, limit=50):
        """Get prayer requests with filters"""
        session = self.Session()
        try:
            query = session.query(PrayerRequest)
            
            if filters:
                if filters.get('prayer_type'):
                    query = query.filter(PrayerRequest.prayer_type == filters['prayer_type'])
                if filters.get('user_id'):
                    query = query.filter(PrayerRequest.user_id == filters['user_id'])
                if filters.get('status'):
                    query = query.filter(PrayerRequest.status == filters['status'])
                if filters.get('date_from'):
                    query = query.filter(PrayerRequest.created_at >= filters['date_from'])
                if filters.get('date_to'):
                    query = query.filter(PrayerRequest.created_at <= filters['date_to'])
            
            query = query.order_by(PrayerRequest.created_at.desc())
            prayers = query.limit(limit).all()
            
            # Convert to list of dictionaries
            result = []
            for prayer in prayers:
                prayer_dict = {c.name: getattr(prayer, c.name) for c in prayer.__table__.columns}
                
                # Parse JSON fields
                if prayer_dict.get('tags'):
                    prayer_dict['tags'] = json.loads(prayer_dict['tags'])
                if prayer_dict.get('media_urls'):
                    prayer_dict['media_urls'] = json.loads(prayer_dict['media_urls'])
                
                result.append(prayer_dict)
            
            return {'success': True, 'data': result, 'count': len(result)}
        except Exception as e:
            return {'success': False, 'error': str(e)}
        finally:
            session.close()
    
    def add_prayer_response(self, response_data):
        """Add prayer response (I prayed, comment, amen)"""
        session = self.Session()
        try:
            new_response = PrayerResponse(
                prayer_id=response_data['prayer_id'],
                user_id=response_data.get('user_id'),
                response_type=response_data['response_type'],
                comment=response_data.get('comment', ''),
                is_anonymous=response_data.get('is_anonymous', False)
            )
            
            session.add(new_response)
            
            # Update prayer count
            prayer = session.query(PrayerRequest).filter_by(id=response_data['prayer_id']).first()
            if prayer:
                prayer.prayer_count += 1
                prayer.updated_at = datetime.utcnow()
            
            session.commit()
            return {'success': True, 'response_id': new_response.id}
        except Exception as e:
            session.rollback()
            return {'success': False, 'error': str(e)}
        finally:
            session.close()
    
    def get_dashboard_stats(self):
        """Get dashboard statistics"""
        session = self.Session()
        try:
            total_prayers = session.query(PrayerRequest).count()
            answered_prayers = session.query(PrayerRequest).filter_by(status='answered').count()
            total_users = session.query(User).count()
            today_prayers = session.query(PrayerRequest).filter(
                PrayerRequest.created_at >= datetime.today().date()
            ).count()
            
            prayer_types = session.query(
                PrayerRequest.prayer_type,
                psycopg2.sql.SQL('count(*)')
            ).group_by(PrayerRequest.prayer_type).all()
            
            return {
                'success': True,
                'stats': {
                    'total_prayers': total_prayers,
                    'answered_prayers': answered_prayers,
                    'answer_rate': (answered_prayers / total_prayers * 100) if total_prayers > 0 else 0,
                    'total_users': total_users,
                    'today_prayers': today_prayers,
                    'prayer_types': dict(prayer_types)
                }
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
        finally:
            session.close()
    
    def backup_database(self):
        """Create database backup"""
        # This would implement backup logic
        pass

# Streamlit Database UI
def database_management_ui():
    st.header("🗄️ Database Management")
    
    db_type = st.selectbox("Database Type", ["PostgreSQL", "MySQL"])
    db_manager = DatabaseManager(db_type.lower())
    
    if st.button("🔗 Connect to Database"):
        if db_manager.connect():
            st.session_state.db_connected = True
            st.session_state.db_manager = db_manager
    
    if st.session_state.get('db_connected'):
        st.success("Database Connected!")
        
        # Dashboard Stats
        if st.button("📊 Get Dashboard Statistics"):
            stats = db_manager.get_dashboard_stats()
            if stats['success']:
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Prayers", stats['stats']['total_prayers'])
                with col2:
                    st.metric("Answered Prayers", stats['stats']['answered_prayers'])
                with col3:
                    st.metric("Answer Rate", f"{stats['stats']['answer_rate']:.1f}%")
                with col4:
                    st.metric("Total Users", stats['stats']['total_users'])
        
        # Prayer Requests Table
        if st.button("📋 View Prayer Requests"):
            prayers = db_manager.get_prayer_requests(limit=20)
            if prayers['success']:
                df = pd.DataFrame(prayers['data'])
                st.dataframe(df[['id', 'prayer_type', 'urgency_level', 'status', 'created_at', 'prayer_count']])
        
        # Export Data
        if st.button("📥 Export Data"):
            prayers = db_manager.get_prayer_requests()
            if prayers['success']:
                df = pd.DataFrame(prayers['data'])
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name="prayer_requests.csv",
                    mime="text/csv"
                )
```
