import React, { createContext, useContext, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axiosClient from '../api/axiosClient';
import toast from 'react-hot-toast';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  // Check if user is logged in on app start
  useEffect(() => {
    const token = localStorage.getItem('access_token');
    const userRole = localStorage.getItem('user_role');

    if (token && userRole) {
      // Validate token by making a request to get user info
      getCurrentUser();
    } else {
      setLoading(false);
    }
  }, []);

  const getCurrentUser = async () => {
    try {
      const response = await axiosClient.get('/auth/me');
      const userData = response.data;
      setUser(userData);
      localStorage.setItem('user_role', userData.role);
    } catch (error) {
      // Token is invalid, clear it
      localStorage.removeItem('access_token');
      localStorage.removeItem('user_role');
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  const login = async (email, password) => {
    try {
      const response = await axiosClient.post('/auth/login', {
        username: email,
        password: password
      });

      const { access_token, role, user_id } = response.data;

      // Store token and role
      localStorage.setItem('access_token', access_token);
      localStorage.setItem('user_role', role);

      // Set user data (basic info)
      setUser({
        id: user_id,
        email: email,
        role: role,
        _id: user_id // For MongoDB compatibility
      });

      toast.success('Login successful!');
      navigate(dashboardRoute(role));

    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  };

  const registerStudent = async (formData) => {
    try {
      const response = await axiosClient.post('/auth/student/signup', formData);
      toast.success('Registration successful! Please login.');
      navigate('/login');
    } catch (error) {
      console.error('Registration error:', error);
      throw error;
    }
  };

  const registerRecruiter = async (formData) => {
    try {
      const response = await axiosClient.post('/auth/recruiter/signup', formData);
      toast.success('Registration successful! Please login.');
      navigate('/login');
    } catch (error) {
      console.error('Recruiter registration error:', error);
      throw error;
    }
  };

  const registerMentor = async (formData) => {
    try {
      const response = await axiosClient.post('/auth/mentor/signup', formData);
      toast.success('Registration successful! Please login.');
      navigate('/login');
    } catch (error) {
      console.error('Mentor registration error:', error);
      throw error;
    }
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_role');
    setUser(null);
    navigate('/');
    toast.success('Logged out successfully!');
  };

  const dashboardRoute = (role) => {
    switch (role) {
      case 'student':
        return '/student-dashboard';
      case 'recruiter':
        return '/recruiter-dashboard';
      case 'mentor':
        return '/mentor-dashboard';
      default:
        return '/';
    }
  };

  const isAuthenticated = () => {
    return user !== null && localStorage.getItem('access_token') !== null;
  };

  const isStudent = () => user?.role === 'student';
  const isRecruiter = () => user?.role === 'recruiter';
  const isMentor = () => user?.role === 'mentor';

  const value = {
    user,
    loading,
    login,
    logout,
    registerStudent,
    registerRecruiter,
    registerMentor,
    isAuthenticated,
    isStudent,
    isRecruiter,
    isMentor,
    getCurrentUser
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
