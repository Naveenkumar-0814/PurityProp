import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { UserPlus, Mail, Lock, User, AlertCircle, Loader2, CheckCircle, Eye, EyeOff } from 'lucide-react';
import logoImage from '../assets/logo.png';
import '../styles/auth.css';

const Register = () => {
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        password: '',
        confirmPassword: ''
    });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const [passwordStrength, setPasswordStrength] = useState(0);
    const [showPassword, setShowPassword] = useState(false);
    const [showConfirmPassword, setShowConfirmPassword] = useState(false);

    const { register } = useAuth();
    const navigate = useNavigate();

    const calculatePasswordStrength = (password) => {
        let strength = 0;
        if (password.length >= 8) strength += 25;
        if (password.length >= 12) strength += 25;
        if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength += 25;
        if (/\d/.test(password)) strength += 25;
        return strength;
    };

    const getStrengthClass = () => {
        if (passwordStrength < 50) return 'weak';
        if (passwordStrength < 75) return 'medium';
        return 'strong';
    };

    const getStrengthText = () => {
        if (passwordStrength < 50) return 'Weak password';
        if (passwordStrength < 75) return 'Medium password';
        return 'Strong password';
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));

        if (name === 'password') {
            setPasswordStrength(calculatePasswordStrength(value));
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        // Validation
        if (!formData.name.trim()) {
            setError('Please enter your full name');
            return;
        }

        if (formData.name.trim().length < 2) {
            setError('Name must be at least 2 characters long');
            return;
        }

        if (!formData.email) {
            setError('Please enter your email address');
            return;
        }

        if (formData.password.length < 8) {
            setError('Password must be at least 8 characters long');
            return;
        }

        if (formData.password !== formData.confirmPassword) {
            setError('Passwords do not match');
            return;
        }

        setLoading(true);

        try {
            await register(formData.name, formData.email, formData.password);
            navigate('/dashboard');
        } catch (err) {
            // Specific error messages
            if (err.response?.status === 400) {
                const detail = err.response?.data?.detail;
                if (detail?.includes('already registered') || detail?.includes('already exists')) {
                    setError('This email is already registered. Please login instead.');
                } else {
                    setError(detail || 'Registration failed. Please check your information.');
                }
            } else if (err.message === 'Network Error') {
                setError('Cannot connect to server. Please try again later.');
            } else {
                setError(err.response?.data?.detail || 'Registration failed. Please try again.');
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="auth-container">
            <div className="auth-card">
                {/* Logo */}
                <div className="auth-logo">
                    <img src={logoImage} alt="Purity Prop AI" className="auth-logo-image" />
                    <span className="auth-logo-text">Purity Prop AI</span>
                </div>

                {/* Header */}
                <div className="auth-header">
                    <h1 className="auth-title">Create your account</h1>
                    <p className="auth-subtitle">Join Purity Prop AI</p>
                </div>

                {/* Form */}
                <form className="auth-form" onSubmit={handleSubmit}>
                    {error && (
                        <div className="error-message">
                            <AlertCircle size={18} />
                            <span>{error}</span>
                        </div>
                    )}

                    {/* Full Name */}
                    <div className="form-group">
                        <label htmlFor="name" className="form-label">
                            <User size={18} />
                            Full Name
                        </label>
                        <input
                            id="name"
                            name="name"
                            type="text"
                            value={formData.name}
                            onChange={handleChange}
                            placeholder="Enter your full name"
                            className="form-input"
                            required
                            disabled={loading}
                            autoComplete="name"
                        />
                    </div>

                    {/* Email */}
                    <div className="form-group">
                        <label htmlFor="email" className="form-label">
                            <Mail size={18} />
                            Email Address
                        </label>
                        <input
                            id="email"
                            name="email"
                            type="email"
                            value={formData.email}
                            onChange={handleChange}
                            placeholder="your.email@example.com"
                            className="form-input"
                            required
                            disabled={loading}
                            autoComplete="email"
                        />
                    </div>

                    {/* Password */}
                    <div className="form-group">
                        <label htmlFor="password" className="form-label">
                            <Lock size={18} />
                            Password
                        </label>
                        <div className="input-wrapper">
                            <input
                                id="password"
                                name="password"
                                type={showPassword ? 'text' : 'password'}
                                value={formData.password}
                                onChange={handleChange}
                                placeholder="Create a strong password"
                                className="form-input"
                                required
                                disabled={loading}
                                autoComplete="new-password"
                            />
                            <button
                                type="button"
                                className="password-toggle"
                                onClick={() => setShowPassword(!showPassword)}
                                tabIndex={-1}
                            >
                                {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                            </button>
                        </div>
                        {formData.password && (
                            <div className="password-strength">
                                <div className="strength-bar">
                                    <div className={`strength-fill ${getStrengthClass()}`} />
                                </div>
                                <span className={`strength-text ${getStrengthClass()}`}>
                                    {getStrengthText()}
                                </span>
                            </div>
                        )}
                    </div>

                    {/* Confirm Password */}
                    <div className="form-group">
                        <label htmlFor="confirmPassword" className="form-label">
                            <CheckCircle size={18} />
                            Confirm Password
                        </label>
                        <div className="input-wrapper">
                            <input
                                id="confirmPassword"
                                name="confirmPassword"
                                type={showConfirmPassword ? 'text' : 'password'}
                                value={formData.confirmPassword}
                                onChange={handleChange}
                                placeholder="Re-enter your password"
                                className="form-input"
                                required
                                disabled={loading}
                                autoComplete="new-password"
                            />
                            <button
                                type="button"
                                className="password-toggle"
                                onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                                tabIndex={-1}
                            >
                                {showConfirmPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                            </button>
                        </div>
                    </div>

                    {/* Submit Button */}
                    <button type="submit" className="auth-button" disabled={loading}>
                        {loading ? (
                            <>
                                <Loader2 size={20} className="spinner" />
                                Creating account...
                            </>
                        ) : (
                            <>
                                <UserPlus size={20} />
                                Create Account
                            </>
                        )}
                    </button>
                </form>

                {/* Footer */}
                <div className="auth-footer">
                    <p className="auth-footer-text">
                        Already have an account?{' '}
                        <Link to="/login" className="auth-link">
                            Sign in here
                        </Link>
                    </p>
                </div>
            </div>
        </div>
    );
};

export default Register;
