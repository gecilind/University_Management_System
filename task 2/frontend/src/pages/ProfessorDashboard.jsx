import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { dashboardService, authService, courseService } from '../services/api';
import '../styles/Dashboard.css';

function ProfessorDashboard() {
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
        const response = await dashboardService.getProfessorDashboard();
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
        const response = await courseService.getProfessorCourses();
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
      await courseService.enrollProfessorCourse(subjectId);
      // Refresh courses list to update enrollment status
      const response = await courseService.getProfessorCourses();
      setCourses(response.data.courses || []);
      // Also refresh dashboard to update teaching subjects count
      const dashboardResponse = await dashboardService.getProfessorDashboard();
      setDashboardData(dashboardResponse.data);
    } catch (err) {
      alert(err.response?.data?.error || err.response?.data?.message || 'Failed to enroll in course');
    } finally {
      setEnrollingId(null);
    }
  };

  if (loading) return <div className="loading">Loading...</div>;

  return (
    <div className="dashboard-container">
      <nav className="navbar">
        <h1>Professor Dashboard</h1>
        <button onClick={handleLogout} className="logout-btn">Logout</button>
      </nav>

      <div className="dashboard-content">
        {error && <div className="error-box">{error}</div>}

        {dashboardData?.professor && (
          <div className="profile-card">
            <h2>Welcome, {dashboardData.professor.user.first_name}!</h2>
            <div className="profile-details">
              <p><strong>Email:</strong> {dashboardData.professor.user.email}</p>
              <p><strong>Faculty:</strong> {dashboardData.professor.faculty_name}</p>
              <p><strong>Specialization:</strong> {dashboardData.professor.specialization}</p>
              <p><strong>Office Hours:</strong> {dashboardData.professor.office_hours}</p>
              <p><strong>Phone:</strong> {dashboardData.professor.phone}</p>
            </div>
          </div>
        )}

        <div className="stats-grid">
          <div className="stat-card">
            <h3>Teaching Subjects</h3>
            <p className="stat-number">{dashboardData?.subjects?.length || 0}</p>
          </div>
          <div className="stat-card">
            <h3>Total Students</h3>
            <p className="stat-number">{dashboardData?.students_count || 0}</p>
          </div>
        </div>

        <div className="content-section">
          <h2>Enrolled Courses (Teaching Subjects)</h2>
          {dashboardData?.subjects?.length > 0 ? (
            <table className="data-table">
              <thead>
                <tr>
                  <th>Subject Code</th>
                  <th>Subject Name</th>
                  <th>Faculty</th>
                  <th>Credits</th>
                  <th>Description</th>
                </tr>
              </thead>
              <tbody>
                {dashboardData.subjects.map((subject) => (
                  <tr key={subject.id}>
                    <td>{subject.code}</td>
                    <td>{subject.name}</td>
                    <td>{subject.faculty_name || 'N/A'}</td>
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

        <div className="content-section">
          <h2>My Students</h2>
          {dashboardData?.students?.length > 0 ? (
            <table className="data-table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Enrollment Number</th>
                  <th>Faculty</th>
                  <th>GPA</th>
                  <th>Phone</th>
                </tr>
              </thead>
              <tbody>
                {dashboardData.students.map((student) => (
                  <tr key={student.id}>
                    <td>
                      {student.user?.first_name || student.user?.last_name
                        ? `${student.user.first_name || ''} ${student.user.last_name || ''}`.trim()
                        : student.user?.username || 'N/A'}
                    </td>
                    <td>{student.user?.email || 'N/A'}</td>
                    <td>{student.enrollment_number}</td>
                    <td>{student.faculty_name || 'N/A'}</td>
                    <td>{student.gpa ? parseFloat(student.gpa).toFixed(2) : '0.00'}</td>
                    <td>{student.phone || 'N/A'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p>No students enrolled in your subjects</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default ProfessorDashboard;
