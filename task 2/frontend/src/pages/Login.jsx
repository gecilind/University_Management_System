import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { authService } from '../services/api';
import '../styles/Auth.css';

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      console.log('Attempting login with:', { username, password });
      const response = await authService.login(username, password);
      console.log('Login response:', response);
      console.log('Response data:', response.data);
      const { role, access_token } = response.data;
      console.log('User role:', role);

      // Store access token in localStorage for cross-origin support
      if (access_token) {
        localStorage.setItem('accessToken', access_token);
      }

      // Redirect based on role
      if (role === 'admin') {
        console.log('Redirecting to admin dashboard');
        navigate('/admin-dashboard', { replace: true });
      } else if (role === 'professor') {
        console.log('Redirecting to professor dashboard');
        navigate('/professor-dashboard', { replace: true });
      } else if (role === 'student') {
        console.log('Redirecting to student dashboard');
        navigate('/student-dashboard', { replace: true });
      } else {
        console.warn('Unknown role:', role);
        setError(`Unknown role: ${role}. Please contact administrator.`);
      }
    } catch (err) {
      console.error('Login error:', err);
      console.error('Error response:', err.response);
      setError(err.response?.data?.error || 'Login failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h1>University Management System</h1>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter username"
              required
            />
          </div>
          <div className="form-group">
            <label>Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter password"
              required
            />
          </div>
          {error && <div className="error-message">{error}</div>}
          <button type="submit" disabled={loading}>
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>
        {/* <div className="demo-credentials">
          <h3>Demo Credentials:</h3>
          <p><strong>Admin:</strong> admin / admin123</p>
          <p><strong>Professor:</strong> professor1 / prof123</p>
          <p><strong>Student:</strong> student1 / student123</p>
        </div> */}
      </div>
    </div>
  );
}

export default Login;
