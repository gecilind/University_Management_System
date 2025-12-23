import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://lindgeci.pythonanywhere.com/api';

// Helper function to get cookie value by name
const getCookie = (name) => {
  const nameEQ = name + '=';
  const decodedCookie = decodeURIComponent(document.cookie);
  const ca = decodedCookie.split(';');
  for (let i = 0; i < ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) === ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(nameEQ) === 0) {
      return c.substring(nameEQ.length, c.length);
    }
  }
  return null;
};

// Get JWT from localStorage (for cross-origin support)
const getAccessToken = () => {
  // Try localStorage first (for cross-origin), then fallback to cookies
  return localStorage.getItem('accessToken') || getCookie('accessToken');
};

const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,  // Enable to send cookies (for refresh token)
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor: Add JWT to Authorization header (except for login/logout)
api.interceptors.request.use(
  (config) => {
    // Don't add Authorization header for login/logout endpoints
    const url = config.url || '';
    if (url.includes('/login/') || url.includes('/logout/')) {
      return config;
    }
    
    const token = getAccessToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor: Handle 401/403 by attempting to renew using refresh cookie and retrying
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    // Handle both 401 (Unauthorized) and 403 (Forbidden) - both indicate auth issues
    if ((error.response?.status === 401) && !originalRequest._retry) {
      // Skip retry for login/logout endpoints
      const url = originalRequest.url || '';
      if (url.includes('/login/') || url.includes('/logout/')) {
        return Promise.reject(error);
      }
      
      originalRequest._retry = true;
      try {
        // Call renew which sets new JWT in cookie and returns it in response body
        const renewResponse = await axios.post('/renew/', {}, { 
          baseURL: API_BASE_URL,
          withCredentials: true
        });
        const newAccessToken = renewResponse.data.access_token;
        
        // Store in localStorage for cross-origin support
        if (newAccessToken) {
          localStorage.setItem('accessToken', newAccessToken);
        }
        
        // Update the original request with new token
        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
        
        // Retry original request
        return api(originalRequest);
      } catch (err) {
        // Redirect to login on failure (cookies will be cleared by backend)
        window.location.href = '/login';
        return Promise.reject(err);
      }
    }
    return Promise.reject(error);
  }
);

export const authService = {
  login: async (username, password) => {
    console.log('Making login request...');
    // Token will be stored in cookie by backend
    const response = await api.post('/login/', { username, password });
    
    // console.log('JWT stored in cookie successfully');
    return response;
  },
  
  logout: async () => {
    try {
      await api.post('/logout/');
    } finally {
      // Clear localStorage on logout
      localStorage.removeItem('accessToken');
    }
  },
};

export const dashboardService = {
  getAdminDashboard: () => api.get('/admin-dashboard/'),
  getProfessorDashboard: () => api.get('/professor-dashboard/'),
  getStudentDashboard: () => api.get('/student-dashboard/'),
};

export const resourceService = {
  getFaculties: () => api.get('/faculties/'),
  getSubjects: () => api.get('/subjects/'),
  getProfessors: () => api.get('/professors/'),
  getStudents: () => api.get('/students/'),
  getAdministrators: () => api.get('/administrators/'),
  // Professor CRUD
  createProfessor: (data) => api.post('/professors/', data),
  updateProfessor: (id, data) => api.put(`/professors/${id}/`, data),
  deleteProfessor: (id) => api.delete(`/professors/${id}/`),
  // Student CRUD
  createStudent: (data) => api.post('/students/', data),
  updateStudent: (id, data) => api.put(`/students/${id}/`, data),
  deleteStudent: (id) => api.delete(`/students/${id}/`),
};

export const courseService = {
  getCourses: () => api.get('/courses/'),
  enrollCourse: (subjectId) => api.post(`/enroll/${subjectId}/`),
  getProfessorCourses: () => api.get('/professor-courses/'),
  enrollProfessorCourse: (subjectId) => api.post(`/enroll-professor/${subjectId}/`),
};

export const gradeService = {
  getStudentGrades: (studentId, subjectId = null) => {
    if (subjectId) {
      return api.get(`/grades/${studentId}/${subjectId}/`);
    }
    return api.get(`/grades/${studentId}/`);
  },
  gradeStudent: (studentId, subjectId, grade, notes = '') => {
    return api.post(`/grade/${studentId}/${subjectId}/`, { grade, notes });
  },
  updateGrade: (studentId, subjectId, grade, notes = '') => {
    return api.put(`/grade/${studentId}/${subjectId}/`, { grade, notes });
  },
  enrollStudent: (studentId, subjectId) => {
    return api.post(`/enroll-student/${studentId}/${subjectId}/`);
  },
};

export default api;
