from flask import Flask, render_template_string, request, jsonify, session
from flask_socketio import SocketIO, emit
import json
import os
from datetime import datetime
import random

app = Flask(__name__)
app.secret_key = os.urandom(24)
socketio = SocketIO(app, cors_allowed_origins="*")

# Mock Database
users_db = {
    "admin@spiritconnect.com": {"password": "admin123", "name": "Admin User", "role": "admin", "streak": 42},
    "john@example.com": {"password": "john123", "name": "John Doe", "role": "user", "streak": 12}
}

prayers_db = [
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

posts_db = [
    {"id": 1, "title": "Finding Peace in Chaos", "verse": "Philippians 4:7", 
     "explanation": "The peace of God, which transcends all understanding...", 
     "audio": "sermon1.mp3", "tags": ["Peace", "Anxiety"], "lang": "en", 
     "image": "https://images.unsplash.com/photo-1507692049790-de58293a469d"}
]

# HTML Template - DIRECT OPEN CONCEPT
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SpiritConnect - Spiritual Wellness App</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdn.jsdelivr.net/npm/lucide-static@latest/font/lucide.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        * { font-family: 'Inter', sans-serif; }
        .animate-in { animation: fadeIn 0.3s ease-out; }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        .slide-in-up { animation: slideInUp 0.3s ease-out; }
        @keyframes slideInUp { from { transform: translateY(20px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
        .pb-safe { padding-bottom: env(safe-area-inset-bottom); }
    </style>
</head>
<body class="bg-gradient-to-br from-slate-50 to-blue-50">
    <div id="app" class="min-h-screen">
        <!-- DIRECT APP OPEN - NO INITIAL LOGIN -->
        <div class="flex-1 flex flex-col">
            <!-- Top Bar - No Login Required -->
            <div class="bg-white/80 backdrop-blur-md px-6 py-4 flex justify-between items-center shadow-sm sticky top-0 z-50 border-b border-slate-200/50">
                <div class="flex items-center space-x-2">
                    <div class="p-2 rounded-lg bg-gradient-to-r from-purple-600 to-indigo-600 text-white shadow-lg">
                        <i data-lucide="heart" class="w-5 h-5" fill="white"></i>
                    </div>
                    <div>
                        <h1 class="text-xl font-bold bg-gradient-to-r from-purple-700 to-indigo-700 bg-clip-text text-transparent">SpiritConnect</h1>
                        <div class="flex items-center text-[10px] text-green-600 font-bold">
                            <i data-lucide="users" class="w-3 h-3 mr-1"></i>
                            <span>{{ liveCount }} praying now</span>
                        </div>
                    </div>
                </div>
                
                <!-- Login/Register Button at Top Right -->
                <div class="flex items-center space-x-3">
                    <div class="hidden md:flex items-center space-x-1 bg-slate-100 px-3 py-1.5 rounded-full text-sm">
                        <span>🌍</span>
                        <span class="font-medium">Global</span>
                    </div>
                    <button @click="showAuthModal = true" class="bg-gradient-to-r from-purple-500 to-indigo-500 text-white px-4 py-2 rounded-full text-sm font-bold shadow-lg hover:shadow-xl transition-shadow">
                        <i data-lucide="log-in" class="w-4 h-4 inline mr-1"></i>
                        Sign In
                    </button>
                </div>
            </div>

            <!-- Main Content - Accessible to All -->
            <main class="flex-1 overflow-y-auto pb-24">
                <!-- Hero Section -->
                <div class="relative overflow-hidden bg-gradient-to-br from-indigo-900 via-purple-800 to-pink-700 rounded-b-3xl p-8 text-white mb-6">
                    <div class="absolute top-0 right-0 w-64 h-64 bg-white/10 rounded-full -mr-32 -mt-32"></div>
                    <div class="relative z-10 max-w-2xl mx-auto text-center">
                        <h2 class="text-4xl font-serif mb-3">"Be still, and know that I am God"</h2>
                        <p class="opacity-90 mb-6 font-medium text-lg">— Psalm 46:10</p>
                        <div class="bg-white/10 backdrop-blur-md p-5 rounded-2xl border border-white/20 text-sm leading-relaxed inline-block">
                            Take a moment to breathe. You're not alone. Join thousands in prayer.
                        </div>
                    </div>
                </div>

                <!-- Prayer Wall - Public Access -->
                <div class="px-4">
                    <div class="flex justify-between items-center mb-6">
                        <h2 class="text-2xl font-bold text-slate-800">Live Prayer Wall</h2>
                        <div class="flex items-center text-sm text-slate-600">
                            <i data-lucide="activity" class="w-4 h-4 mr-1 text-green-500"></i>
                            <span>Real-time updates</span>
                        </div>
                    </div>

                    <!-- Prayer Cards -->
                    <div class="space-y-4">
                        <div v-for="prayer in prayers" :key="prayer.id" class="bg-white rounded-2xl shadow-lg border border-slate-100 p-5 hover:shadow-xl transition-shadow">
                            <div class="flex justify-between items-start mb-3">
                                <div class="flex items-center space-x-3">
                                    <div class="h-10 w-10 rounded-full bg-gradient-to-r from-blue-100 to-purple-100 flex items-center justify-center text-slate-700 font-bold">
                                        {{ prayer.user.charAt(0) }}
                                    </div>
                                    <div>
                                        <h4 class="font-bold text-slate-800">{{ prayer.user }}</h4>
                                        <p class="text-xs text-slate-500">{{ prayer.timestamp }}</p>
                                    </div>
                                </div>
                                <span :class="{
                                    'prayer-badge-emergency': prayer.type === 'EMERGENCY',
                                    'prayer-badge-critical': prayer.type === 'CRITICAL FINAL CALL',
                                    'prayer-badge-needs': prayer.type === 'NEEDS'
                                }" class="px-3 py-1 rounded-full text-xs font-bold border">
                                    <i v-if="prayer.type === 'EMERGENCY'" data-lucide="alert-triangle" class="w-3 h-3 inline mr-1"></i>
                                    {{ prayer.type }}
                                </span>
                            </div>

                            <h3 class="text-lg font-bold text-slate-900 mb-2">{{ prayer.title }}</h3>
                            <p class="text-slate-600 mb-4">{{ prayer.body }}</p>

                            <!-- Prayer Actions - Anyone can pray -->
                            <div class="grid grid-cols-3 gap-3">
                                <button @click="prayFor(prayer.id)" 
                                        class="flex items-center justify-center space-x-2 bg-gradient-to-r from-green-500 to-emerald-500 text-white p-3 rounded-xl hover:shadow-lg transition">
                                    <i data-lucide="heart" class="w-5 h-5"></i>
                                    <span class="font-bold">I Prayed ({{ prayer.count }})</span>
                                </button>
                                <button @click="setReminder(prayer.id)" 
                                        class="flex items-center justify-center space-x-2 bg-gradient-to-r from-blue-500 to-indigo-500 text-white p-3 rounded-xl hover:shadow-lg transition">
                                    <i data-lucide="clock" class="w-5 h-5"></i>
                                    <span class="font-bold">Remind Me</span>
                                </button>
                                <button @click="sharePrayer(prayer.id)" 
                                        class="flex items-center justify-center space-x-2 bg-gradient-to-r from-purple-500 to-pink-500 text-white p-3 rounded-xl hover:shadow-lg transition">
                                    <i data-lucide="share-2" class="w-5 h-5"></i>
                                    <span class="font-bold">Share</span>
                                </button>
                            </div>
                        </div>
                    </div>

                    <!-- Add New Prayer - Public -->
                    <div class="mt-8 bg-gradient-to-r from-white to-blue-50 rounded-2xl p-6 border border-slate-200">
                        <h3 class="font-bold text-slate-800 mb-4 text-lg">Share Your Prayer Request</h3>
                        <div class="space-y-4">
                            <input v-model="newPrayer.title" placeholder="Prayer title..." 
                                   class="w-full p-3 border border-slate-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent">
                            <textarea v-model="newPrayer.body" placeholder="Share your prayer need..." rows="3"
                                      class="w-full p-3 border border-slate-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent"></textarea>
                            <div class="flex space-x-3">
                                <button @click="setPrayerType('NEEDS')" 
                                        :class="{'bg-emerald-500 text-white': newPrayer.type === 'NEEDS', 'bg-emerald-100 text-emerald-700': newPrayer.type !== 'NEEDS'}"
                                        class="px-4 py-2 rounded-lg font-medium">Needs</button>
                                <button @click="setPrayerType('CRITICAL FINAL CALL')"
                                        :class="{'bg-orange-500 text-white': newPrayer.type === 'CRITICAL FINAL CALL', 'bg-orange-100 text-orange-700': newPrayer.type !== 'CRITICAL FINAL CALL'}"
                                        class="px-4 py-2 rounded-lg font-medium">Critical</button>
                                <button @click="setPrayerType('EMERGENCY')"
                                        :class="{'bg-red-500 text-white': newPrayer.type === 'EMERGENCY', 'bg-red-100 text-red-700': newPrayer.type !== 'EMERGENCY'}"
                                        class="px-4 py-2 rounded-lg font-medium">Emergency</button>
                            </div>
                            <button @click="submitPrayer" 
                                    class="w-full bg-gradient-to-r from-indigo-600 to-purple-600 text-white py-3 rounded-xl font-bold text-lg hover:shadow-xl transition">
                                <i data-lucide="upload" class="w-5 h-5 inline mr-2"></i>
                                Submit Prayer Request
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Spiritual Content Section -->
                <div class="px-4 mt-10">
                    <h2 class="text-2xl font-bold text-slate-800 mb-6">Daily Inspiration</h2>
                    <div class="grid md:grid-cols-2 gap-6">
                        <div v-for="post in posts" :key="post.id" class="bg-white rounded-2xl shadow-lg overflow-hidden">
                            <img :src="post.image" class="w-full h-48 object-cover">
                            <div class="p-6">
                                <h3 class="font-bold text-xl mb-2">{{ post.title }}</h3>
                                <p class="text-slate-600 mb-3">{{ post.verse }}</p>
                                <p class="text-slate-700">{{ post.explanation.substring(0, 100) }}...</p>
                                <div class="flex items-center justify-between mt-4">
                                    <div class="flex space-x-2">
                                        <span v-for="tag in post.tags" class="bg-blue-100 text-blue-700 px-2 py-1 rounded-full text-xs">
                                            {{ tag }}
                                        </span>
                                    </div>
                                    <button class="text-indigo-600 font-bold">Read More →</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Live Stats -->
                <div class="px-4 mt-10">
                    <div class="bg-gradient-to-r from-indigo-500 to-purple-600 rounded-2xl p-6 text-white">
                        <h3 class="font-bold text-xl mb-4">Live Community Impact</h3>
                        <div class="grid grid-cols-3 gap-4">
                            <div class="text-center">
                                <div class="text-3xl font-bold">{{ totalPrayers }}</div>
                                <div class="text-sm opacity-90">Prayers Today</div>
                            </div>
                            <div class="text-center">
                                <div class="text-3xl font-bold">{{ liveCount }}</div>
                                <div class="text-sm opacity-90">Active Now</div>
                            </div>
                            <div class="text-center">
                                <div class="text-3xl font-bold">{{ countries }}</div>
                                <div class="text-sm opacity-90">Countries</div>
                            </div>
                        </div>
                    </div>
                </div>
            </main>

            <!-- Bottom Navigation -->
            <div class="fixed bottom-0 left-0 right-0 bg-white/90 backdrop-blur-md border-t border-slate-200 px-6 py-3 flex justify-around items-center z-40 pb-safe">
                <button @click="activeTab = 'home'" :class="{'text-indigo-600': activeTab === 'home'}" class="flex flex-col items-center">
                    <i data-lucide="home" class="w-6 h-6"></i>
                    <span class="text-xs mt-1">Home</span>
                </button>
                <button @click="activeTab = 'prayer'" :class="{'text-indigo-600': activeTab === 'prayer'}" class="flex flex-col items-center">
                    <i data-lucide="heart" class="w-6 h-6"></i>
                    <span class="text-xs mt-1">Prayer</span>
                </button>
                <button @click="showAuthModal = true" class="flex flex-col items-center">
                    <div class="bg-gradient-to-r from-indigo-500 to-purple-500 p-3 rounded-full -mt-6 shadow-lg">
                        <i data-lucide="plus" class="w-6 h-6 text-white"></i>
                    </div>
                    <span class="text-xs mt-1">New Prayer</span>
                </button>
                <button @click="activeTab = 'media'" :class="{'text-indigo-600': activeTab === 'media'}" class="flex flex-col items-center">
                    <i data-lucide="play-circle" class="w-6 h-6"></i>
                    <span class="text-xs mt-1">Media</span>
                </button>
                <button @click="showAuthModal = true" :class="{'text-indigo-600': activeTab === 'profile'}" class="flex flex-col items-center">
                    <i data-lucide="user" class="w-6 h-6"></i>
                    <span class="text-xs mt-1">Profile</span>
                </button>
            </div>
        </div>

        <!-- Authentication Modal (Login/Register) - Only shows when clicked -->
        <div v-if="showAuthModal" class="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4 animate-in">
            <div class="bg-white w-full max-w-md rounded-2xl overflow-hidden">
                <!-- Tabs -->
                <div class="flex border-b">
                    <button @click="authMode = 'login'" 
                            :class="{'border-b-2 border-indigo-600 text-indigo-600': authMode === 'login'}"
                            class="flex-1 py-4 font-bold text-center">Login</button>
                    <button @click="authMode = 'register'"
                            :class="{'border-b-2 border-indigo-600 text-indigo-600': authMode === 'register'}"
                            class="flex-1 py-4 font-bold text-center">Register</button>
                </div>

                <div class="p-6">
                    <!-- Login Form -->
                    <div v-if="authMode === 'login'">
                        <h3 class="text-xl font-bold mb-6">Welcome Back</h3>
                        <div class="space-y-4">
                            <input v-model="loginEmail" type="email" placeholder="Email" 
                                   class="w-full p-3 border rounded-xl">
                            <input v-model="loginPassword" type="password" placeholder="Password" 
                                   class="w-full p-3 border rounded-xl">
                            <button @click="handleLogin" 
                                    class="w-full bg-indigo-600 text-white py-3 rounded-xl font-bold">
                                Sign In
                            </button>
                            <p class="text-center text-sm text-slate-500">
                                Demo: admin@spiritconnect.com / admin123
                            </p>
                        </div>
                    </div>

                    <!-- Register Form -->
                    <div v-if="authMode === 'register'">
                        <h3 class="text-xl font-bold mb-6">Join SpiritConnect</h3>
                        <div class="space-y-4">
                            <input v-model="registerName" type="text" placeholder="Full Name" 
                                   class="w-full p-3 border rounded-xl">
                            <input v-model="registerEmail" type="email" placeholder="Email" 
                                   class="w-full p-3 border rounded-xl">
                            <input v-model="registerPassword" type="password" placeholder="Password" 
                                   class="w-full p-3 border rounded-xl">
                            <input v-model="registerConfirm" type="password" placeholder="Confirm Password" 
                                   class="w-full p-3 border rounded-xl">
                            <button @click="handleRegister" 
                                    class="w-full bg-gradient-to-r from-green-500 to-emerald-600 text-white py-3 rounded-xl font-bold">
                                Create Account
                            </button>
                        </div>
                    </div>
                </div>

                <div class="p-4 border-t text-center">
                    <button @click="showAuthModal = false" class="text-slate-500 font-medium">
                        Continue without account
                    </button>
                </div>
            </div>
        </div>

        <!-- Admin Panel Modal (Only for logged in admins) -->
        <div v-if="showAdminPanel && user && user.role === 'admin'" class="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4">
            <div class="bg-white w-full max-w-4xl h-[80vh] rounded-2xl flex flex-col">
                <div class="p-4 border-b flex justify-between items-center">
                    <h3 class="text-xl font-bold">Admin Dashboard</h3>
                    <button @click="showAdminPanel = false" class="text-slate-500">
                        <i data-lucide="x" class="w-5 h-5"></i>
                    </button>
                </div>
                <div class="flex-1 overflow-y-auto p-6">
                    <div class="grid md:grid-cols-2 gap-6">
                        <!-- Manage Prayers -->
                        <div class="border rounded-xl p-4">
                            <h4 class="font-bold mb-3">Manage Prayer Requests</h4>
                            <div class="space-y-3">
                                <div v-for="prayer in prayers" class="flex items-center justify-between border-b pb-2">
                                    <div>
                                        <div class="font-medium">{{ prayer.title }}</div>
                                        <div class="text-xs text-slate-500">{{ prayer.user }} • {{ prayer.count }} prayers</div>
                                    </div>
                                    <button @click="deletePrayer(prayer.id)" class="text-red-500">
                                        <i data-lucide="trash-2" class="w-4 h-4"></i>
                                    </button>
                                </div>
                            </div>
                        </div>

                        <!-- Add Content -->
                        <div class="border rounded-xl p-4">
                            <h4 class="font-bold mb-3">Add Spiritual Content</h4>
                            <div class="space-y-3">
                                <input v-model="adminContent.title" placeholder="Title" class="w-full p-2 border rounded">
                                <textarea v-model="adminContent.body" placeholder="Content" rows="3" class="w-full p-2 border rounded"></textarea>
                                <button @click="addContent" class="w-full bg-indigo-600 text-white p-2 rounded font-bold">
                                    Publish Content
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Vue.js and Socket.io -->
    <script src="https://cdn.jsdelivr.net/npm/vue@3/dist/vue.global.js"></script>
    <script src="https://cdn.socket.io/4.7.4/socket.io.min.js"></script>
    <script>
        const { createApp, ref, computed, onMounted } = Vue;
        
        createApp({
            setup() {
                // App State
                const user = ref(null);
                const showAuthModal = ref(false);
                const authMode = ref('login');
                const showAdminPanel = ref(false);
                const activeTab = ref('home');
                
                // Live Data
                const liveCount = ref(487);
                const totalPrayers = ref(142 + 24 + 89);
                const countries = ref(42);
                
                // Prayer Data
                const prayers = ref(%s);
                const posts = ref(%s);
                
                // New Prayer Form
                const newPrayer = ref({
                    title: '',
                    body: '',
                    type: 'NEEDS'
                });
                
                // Auth Forms
                const loginEmail = ref('');
                const loginPassword = ref('');
                const registerName = ref('');
                const registerEmail = ref('');
                const registerPassword = ref('');
                const registerConfirm = ref('');
                
                // Admin Content
                const adminContent = ref({
                    title: '',
                    body: ''
                });
                
                // Initialize Lucide icons
                onMounted(() => {
                    lucide.createIcons();
                    
                    // Simulate live updates
                    setInterval(() => {
                        liveCount.value += Math.floor(Math.random() * 5) - 2;
                        if (liveCount.value < 450) liveCount.value = 450;
                        if (liveCount.value > 550) liveCount.value = 550;
                    }, 5000);
                });
                
                // Methods
                const handleLogin = () => {
                    // Mock login
                    if (loginEmail.value === 'admin@spiritconnect.com' && loginPassword.value === 'admin123') {
                        user.value = {
                            email: 'admin@spiritconnect.com',
                            name: 'Admin User',
                            role: 'admin',
                            streak: 42
                        };
                        showAuthModal.value = false;
                        alert('Admin login successful!');
                    } else if (loginEmail.value && loginPassword.value) {
                        user.value = {
                            email: loginEmail.value,
                            name: 'John Doe',
                            role: 'user',
                            streak: 12
                        };
                        showAuthModal.value = false;
                        alert('Login successful!');
                    } else {
                        alert('Please enter credentials');
                    }
                };
                
                const handleRegister = () => {
                    if (registerPassword.value !== registerConfirm.value) {
                        alert('Passwords do not match');
                        return;
                    }
                    user.value = {
                        email: registerEmail.value,
                        name: registerName.value,
                        role: 'user',
                        streak: 0
                    };
                    showAuthModal.value = false;
                    alert('Registration successful!');
                };
                
                const prayFor = (prayerId) => {
                    const prayer = prayers.value.find(p => p.id === prayerId);
                    if (prayer) {
                        prayer.count++;
                        totalPrayers.value++;
                        alert('Thank you for praying! 🙏');
                    }
                };
                
                const setReminder = (prayerId) => {
                    alert('Reminder set for this prayer request ⏰');
                };
                
                const sharePrayer = (prayerId) => {
                    alert('Prayer shared! 📤');
                };
                
                const setPrayerType = (type) => {
                    newPrayer.value.type = type;
                };
                
                const submitPrayer = () => {
                    if (!newPrayer.value.title || !newPrayer.value.body) {
                        alert('Please fill all fields');
                        return;
                    }
                    
                    const newPrayerObj = {
                        id: prayers.value.length + 1,
                        user: user.value ? user.value.name : 'Anonymous',
                        type: newPrayer.value.type,
                        title: newPrayer.value.title,
                        body: newPrayer.value.body,
                        count: 0,
                        timestamp: 'Just now',
                        status: 'active'
                    };
                    
                    prayers.value.unshift(newPrayerObj);
                    newPrayer.value = { title: '', body: '', type: 'NEEDS' };
                    alert('Prayer request submitted! 🙏');
                };
                
                const deletePrayer = (prayerId) => {
                    if (confirm('Delete this prayer request?')) {
                        prayers.value = prayers.value.filter(p => p.id !== prayerId);
                    }
                };
                
                const addContent = () => {
                    if (!adminContent.value.title || !adminContent.value.body) {
                        alert('Please fill all fields');
                        return;
                    }
                    
                    const newPost = {
                        id: posts.value.length + 1,
                        title: adminContent.value.title,
                        verse: 'Admin Content',
                        explanation: adminContent.value.body,
                        audio: '',
                        tags: ['Admin'],
                        lang: 'en',
                        image: 'https://images.unsplash.com/photo-1507692049790-de58293a469d'
                    };
                    
                    posts.value.unshift(newPost);
                    adminContent.value = { title: '', body: '' };
                    alert('Content published!');
                };
                
                // Automatically show admin panel if admin logs in
                Vue.watch(user, (newUser) => {
                    if (newUser && newUser.role === 'admin') {
                        setTimeout(() => {
                            showAdminPanel.value = true;
                        }, 1000);
                    }
                });
                
                return {
                    user,
                    showAuthModal,
                    authMode,
                    showAdminPanel,
                    activeTab,
                    liveCount,
                    totalPrayers,
                    countries,
                    prayers,
                    posts,
                    newPrayer,
                    loginEmail,
                    loginPassword,
                    registerName,
                    registerEmail,
                    registerPassword,
                    registerConfirm,
                    adminContent,
                    handleLogin,
                    handleRegister,
                    prayFor,
                    setReminder,
                    sharePrayer,
                    setPrayerType,
                    submitPrayer,
                    deletePrayer,
                    addContent
                };
            }
        }).mount('#app');
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE % (
        json.dumps(prayers_db), 
        json.dumps(posts_db)
    ))

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    if email in users_db and users_db[email]['password'] == password:
        session['user'] = {
            'email': email,
            'name': users_db[email]['name'],
            'role': users_db[email]['role']
        }
        return jsonify({'success': True, 'user': session['user']})
    return jsonify({'success': False, 'error': 'Invalid credentials'})

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    
    if email in users_db:
        return jsonify({'success': False, 'error': 'User already exists'})
    
    users_db[email] = {
        'password': data.get('password'),
        'name': data.get('name'),
        'role': 'user',
        'streak': 0
    }
    
    session['user'] = {
        'email': email,
        'name': data.get('name'),
        'role': 'user'
    }
    
    return jsonify({'success': True, 'user': session['user']})

@app.route('/api/prayers', methods=['GET', 'POST'])
def prayers():
    if request.method == 'POST':
        data = request.json
        new_prayer = {
            'id': len(prayers_db) + 1,
            'user': data.get('user', 'Anonymous'),
            'type': data.get('type', 'NEEDS'),
            'title': data.get('title'),
            'body': data.get('body'),
            'count': 0,
            'timestamp': 'Just now',
            'status': 'active'
        }
        prayers_db.insert(0, new_prayer)
        socketio.emit('new_prayer', new_prayer)
        return jsonify({'success': True, 'prayer': new_prayer})
    
    return jsonify({'prayers': prayers_db})

@app.route('/api/pray/<int:prayer_id>', methods=['POST'])
def pray(prayer_id):
    for prayer in prayers_db:
        if prayer['id'] == prayer_id:
            prayer['count'] += 1
            socketio.emit('prayer_update', prayer)
            return jsonify({'success': True, 'count': prayer['count']})
    return jsonify({'success': False, 'error': 'Prayer not found'})

@app.route('/api/stats')
def stats():
    return jsonify({
        'live_count': random.randint(450, 550),
        'total_prayers': sum(p['count'] for p in prayers_db),
        'countries': 42
    })

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('live_count', {'count': len(prayers_db)})

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)
