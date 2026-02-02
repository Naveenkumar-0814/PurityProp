import React, { createContext, useState, useContext, useEffect } from "react";
import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL; // 👈 REQUIRED

const AuthContext = createContext(null);

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error("useAuth must be used within AuthProvider");
    }
    return context;
};

// ✅ Single axios instance (BEST PRACTICE)
const api = axios.create({
    baseURL: API_URL,
    headers: {
        "Content-Type": "application/json",
    },
});

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [token, setToken] = useState(localStorage.getItem("token"));
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (token) {
            fetchCurrentUser();
        } else {
            setLoading(false);
        }

        // ✅ Token refresh interceptor
        const interceptor = api.interceptors.response.use(
            (response) => response,
            async (error) => {
                const originalRequest = error.config;

                if (error.response?.status === 401 && !originalRequest._retry) {
                    originalRequest._retry = true;
                    try {
                        const refreshToken = localStorage.getItem("refresh_token");
                        if (!refreshToken) throw new Error("No refresh token");

                        const res = await api.post("/api/auth/refresh", {
                            refresh_token: refreshToken,
                        });

                        const { access_token } = res.data;

                        localStorage.setItem("token", access_token);
                        setToken(access_token);

                        originalRequest.headers.Authorization = `Bearer ${access_token}`;
                        return api(originalRequest);
                    } catch (err) {
                        logout();
                        return Promise.reject(err);
                    }
                }
                return Promise.reject(error);
            }
        );

        return () => {
            api.interceptors.response.eject(interceptor);
        };
    }, []);

    const fetchCurrentUser = async () => {
        try {
            const response = await api.get("/api/auth/me", {
                headers: { Authorization: `Bearer ${token}` },
            });
            setUser(response.data);
        } catch {
            logout();
        } finally {
            setLoading(false);
        }
    };

    const login = async (email, password) => {
        const response = await api.post("/api/auth/login", { email, password });

        const { access_token, refresh_token, user: userData } = response.data;

        localStorage.setItem("token", access_token);
        localStorage.setItem("refresh_token", refresh_token);
        setToken(access_token);
        setUser(userData);

        return userData;
    };

    const register = async (name, email, password) => {
        const response = await api.post("/api/auth/register", {
            name,
            email,
            password,
        });

        const { access_token, refresh_token, user: userData } = response.data;

        localStorage.setItem("token", access_token);
        localStorage.setItem("refresh_token", refresh_token);
        setToken(access_token);
        setUser(userData);

        return userData;
    };

    const logout = () => {
        localStorage.removeItem("token");
        localStorage.removeItem("refresh_token");
        setToken(null);
        setUser(null);
    };

    return (
        <AuthContext.Provider
            value={{
                user,
                token,
                loading,
                login,
                register,
                logout,
                isAuthenticated: !!user,
            }}
        >
            {children}
        </AuthContext.Provider>
    );
};
