import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { dashboardService, authService, courseService } from '../services/api';
import '../styles/Dashboard.css';

function StudentDashboard() {
  const [dashboardData, setDashboardData] = useState(null);
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [coursesLoading, setCoursesLoading] = useState(false);
  const [error, setError] = useState('');
  const [enrollingId, setEnrollingId] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await dashboardService.getStudentDashboard();
        setDashboardData(response.data);
      } catch (err) {
        setError(err.response?.data?.error || 'Failed to fetch data');
        if (err.response?.status === 403 || err.response?.status === 401) {
          navigate('/login');
        }
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [navigate]);

  useEffect(() => {
    const fetchCourses = async () => {
      setCoursesLoading(true);
      try {
        const response = await courseService.getCourses();
        setCourses(response.data.courses || []);
      } catch (err) {
        console.error('Failed to fetch courses:', err);
      } finally {
        setCoursesLoading(false);
      }
    };

    fetchCourses();
  }, []);

  const handleLogout = async () => {
    try {
      await authService.logout();
    } finally {
      navigate('/login');
    }
  };

  const handleEnroll = async (subjectId) => {
    setEnrollingId(subjectId);
    try {
      await courseService.enrollCourse(subjectId);
      // Refresh courses list to update enrollment status
      const response = await courseService.getCourses();
      setCourses(response.data.courses || []);
      // Also refresh dashboard to update enrolled subjects count
      const dashboardResponse = await dashboardService.getStudentDashboard();
      setDashboardData(dashboardResponse.data);
    } catch (err) {
      alert(err.response?.data?.error || err.response?.data?.message || 'Failed to enroll in course');
    } finally {
      setEnrollingId(null);
    }
  };

  // Ensure GPA is a number before calling toFixed
  const gpaValue = (() => {
    const raw = dashboardData?.gpa;
    if (raw === null || raw === undefined) return null;
    const n = Number(raw);
    return Number.isFinite(n) ? n : null;
  })();

  if (loading) return <div className="loading">Loading...</div>;

  return (
    <div className="dashboard-container">
      <nav className="navbar">
        <h1>Student Dashboard</h1>
        <button onClick={handleLogout} className="logout-btn">Logout</button>
      </nav>

      <div className="dashboard-content">
        {error && <div className="error-box">{error}</div>}

        {dashboardData?.student && (
          <div className="profile-card">
            <h2>Welcome, {dashboardData.student.user.first_name}!</h2>
            <div className="profile-details">
              <p><strong>Email:</strong> {dashboardData.student.user.email}</p>
              <p><strong>Enrollment Number:</strong> {dashboardData.student.enrollment_number}</p>
              <p><strong>Faculty:</strong> {dashboardData.student.faculty_name}</p>
              <p><strong>Phone:</strong> {dashboardData.student.phone}</p>
            </div>
          </div>
        )}

        <div className="stats-grid">
          <div className="stat-card">
            <h3>Current GPA</h3>
            <p className="stat-number">{gpaValue !== null ? gpaValue.toFixed(2) : '0.00'}</p>
          </div>
          <div className="stat-card">
            <h3>Enrolled Subjects</h3>
            <p className="stat-number">{dashboardData?.enrolled_subjects?.length || 0}</p>
          </div>
        </div>

        <div className="content-section">
          <h2>Enrolled Subjects</h2>
          {dashboardData?.enrolled_subjects?.length > 0 ? (
            <table className="data-table">
              <thead>
                <tr>
                  <th>Subject Code</th>
                  <th>Subject Name</th>
                  <th>Credits</th>
                  <th>Description</th>
                </tr>
              </thead>
              <tbody>
                {dashboardData.enrolled_subjects.map((subject) => (
                  <tr key={subject.id}>
                    <td>{subject.code}</td>
                    <td>{subject.name}</td>
                    <td>{subject.credits}</td>
                    <td>{subject.description || 'N/A'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p>No subjects enrolled</p>
          )}
        </div>

        <div className="content-section">
          <h2>Available Courses</h2>
          {coursesLoading ? (
            <p>Loading courses...</p>
          ) : courses.length > 0 ? (
            <table className="data-table">
              <thead>
                <tr>
                  <th>Subject Code</th>
                  <th>Subject Name</th>
                  <th>Faculty</th>
                  <th>Credits</th>
                  <th>Description</th>
                  <th>Status</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {courses.map((course) => (
                  <tr key={course.id}>
                    <td>{course.code}</td>
                    <td>{course.name}</td>
                    <td>{course.faculty_name || 'N/A'}</td>
                    <td>{course.credits}</td>
                    <td>{course.description || 'N/A'}</td>
                    <td>
                      {course.is_enrolled ? (
                        <span style={{ color: 'green', fontWeight: 'bold' }}>Enrolled</span>
                      ) : (
                        <span style={{ color: 'gray' }}>Not Enrolled</span>
                      )}
                    </td>
                    <td>
                      {course.is_enrolled ? (
                        <span style={{ color: 'gray' }}>Already Enrolled</span>
                      ) : (
                        <button
                          onClick={() => handleEnroll(course.id)}
                          disabled={enrollingId === course.id}
                          style={{
                            padding: '5px 15px',
                            backgroundColor: '#007bff',
                            color: 'white',
                            border: 'none',
                            borderRadius: '4px',
                            cursor: enrollingId === course.id ? 'not-allowed' : 'pointer',
                            opacity: enrollingId === course.id ? 0.6 : 1
                          }}
                        >
                          {enrollingId === course.id ? 'Enrolling...' : 'Enroll'}
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p>No courses available</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default StudentDashboard;
