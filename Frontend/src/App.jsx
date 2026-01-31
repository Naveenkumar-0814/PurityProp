import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { ChatProvider } from './context/ChatContext';
import Sidebar from './components/Sidebar';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import AIChat from './pages/AIChat';
import Properties from './pages/Properties';

// Import CSS
import './styles/premium.css';
import './styles/chat.css';

// Placeholder components
const Valuation = () => (
    <div className="placeholder-page">
        <div className="placeholder-icon">📏</div>
        <h2 className="placeholder-title">Land Valuation</h2>
        <p className="placeholder-description">
            Calculate property values and market rates in Tamil Nadu
        </p>
        <span className="coming-soon-badge">Coming Soon</span>
    </div>
);

const Documents = () => (
    <div className="placeholder-page">
        <div className="placeholder-icon">📄</div>
        <h2 className="placeholder-title">Documents Manager</h2>
        <p className="placeholder-description">
            Manage and track your property documents securely
        </p>
        <span className="coming-soon-badge">Coming Soon</span>
    </div>
);

const Approvals = () => (
    <div className="placeholder-page">
        <div className="placeholder-icon">✅</div>
        <h2 className="placeholder-title">Approvals & Compliance</h2>
        <p className="placeholder-description">
            Track TNRERA, DTCP, and CMDA approvals
        </p>
        <span className="coming-soon-badge">Coming Soon</span>
    </div>
);

// Protected Route Component
const ProtectedRoute = ({ children }) => {
    const { isAuthenticated, loading } = useAuth();

    if (loading) {
        return (
            <div className="loading-container">
                <div className="loading-spinner"></div>
                <p>Loading...</p>
            </div>
        );
    }

    return isAuthenticated ? children : <Navigate to="/login" replace />;
};

// Main Layout with Sidebar
const MainLayout = ({ children }) => {
    return (
        <div className="app-container">
            <Sidebar />
            <div className="main-content">
                <div className="main-header">
                    <h1 className="font-['Cormorant_Garamond'] font-light text-2xl tracking-[0.10em] text-[#eeeef2]">
                        PurityProp
                    </h1>
                    <div className="header-actions">
                        {/* Future: Add notifications, settings, etc. */}
                    </div>
                </div>
                {children}
            </div>
        </div>
    );
};

// Main App Component
function App() {
    return (
        <AuthProvider>
            <ChatProvider>
                <BrowserRouter>
                    <Routes>
                        {/* Auth Routes */}
                        <Route path="/login" element={<Login />} />
                        <Route path="/register" element={<Register />} />

                        {/* Protected Routes with Sidebar */}
                        <Route
                            path="/dashboard"
                            element={
                                <ProtectedRoute>
                                    <MainLayout>
                                        <Dashboard />
                                    </MainLayout>
                                </ProtectedRoute>
                            }
                        />
                        <Route
                            path="/chat"
                            element={
                                <ProtectedRoute>
                                    <MainLayout>
                                        <AIChat />
                                    </MainLayout>
                                </ProtectedRoute>
                            }
                        />
                        <Route
                            path="/properties"
                            element={
                                <ProtectedRoute>
                                    <MainLayout>
                                        <Properties />
                                    </MainLayout>
                                </ProtectedRoute>
                            }
                        />
                        <Route
                            path="/valuation"
                            element={
                                <ProtectedRoute>
                                    <MainLayout>
                                        <Valuation />
                                    </MainLayout>
                                </ProtectedRoute>
                            }
                        />
                        <Route
                            path="/documents"
                            element={
                                <ProtectedRoute>
                                    <MainLayout>
                                        <Documents />
                                    </MainLayout>
                                </ProtectedRoute>
                            }
                        />
                        <Route
                            path="/approvals"
                            element={
                                <ProtectedRoute>
                                    <MainLayout>
                                        <Approvals />
                                    </MainLayout>
                                </ProtectedRoute>
                            }
                        />

                        {/* Default Route */}
                        <Route path="/" element={<Navigate to="/dashboard" replace />} />
                    </Routes>
                </BrowserRouter>
            </ChatProvider>
        </AuthProvider>
    );
}

export default App;
