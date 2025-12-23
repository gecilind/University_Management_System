import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { dashboardService, resourceService, authService } from '../services/api';
import '../styles/Dashboard.css';

function AdminDashboard() {
  const [dashboardData, setDashboardData] = useState(null);
  const [faculties, setFaculties] = useState([]);
  const [professors, setProfessors] = useState([]);
  const [students, setStudents] = useState([]);
  const [showProfessors, setShowProfessors] = useState(true);
  const [showStudents, setShowStudents] = useState(true);
  const [loadingProfessors, setLoadingProfessors] = useState(false);
  const [loadingStudents, setLoadingStudents] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [editingProfessor, setEditingProfessor] = useState(null);
  const [editingStudent, setEditingStudent] = useState(null);
  const [showProfessorForm, setShowProfessorForm] = useState(false);
  const [showStudentForm, setShowStudentForm] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const dashResponse = await dashboardService.getAdminDashboard();
        const facResponse = await resourceService.getFaculties();
        
        setDashboardData(dashResponse.data);
        setFaculties(facResponse.data);
        
        // Load professors and students by default
        await loadProfessors();
        await loadStudents();
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

  const loadProfessors = async () => {
    setLoadingProfessors(true);
    try {
      const response = await resourceService.getProfessors();
      setProfessors(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to fetch professors');
    } finally {
      setLoadingProfessors(false);
    }
  };

  const loadStudents = async () => {
    setLoadingStudents(true);
    try {
      const response = await resourceService.getStudents();
      setStudents(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to fetch students');
    } finally {
      setLoadingStudents(false);
    }
  };

  const handleLogout = async () => {
    try {
      await authService.logout();
    } finally {
      navigate('/login');
    }
  };

  const handleShowProfessors = () => {
    setShowProfessors(!showProfessors);
    if (!showProfessors && professors.length === 0) {
      loadProfessors();
    }
  };

  const handleShowStudents = () => {
    setShowStudents(!showStudents);
    if (!showStudents && students.length === 0) {
      loadStudents();
    }
  };

  const handleCreateProfessor = () => {
    setEditingProfessor(null);
    setShowProfessorForm(true);
  };

  const handleEditProfessor = (professor) => {
    setEditingProfessor(professor);
    setShowProfessorForm(true);
  };

  const handleDeleteProfessor = async (id) => {
    if (!window.confirm('Are you sure you want to delete this professor?')) {
      return;
    }
    try {
      await resourceService.deleteProfessor(id);
      await loadProfessors();
      alert('Professor deleted successfully');
    } catch (err) {
      alert(err.response?.data?.error || 'Failed to delete professor');
    }
  };

  const handleCreateStudent = () => {
    setEditingStudent(null);
    setShowStudentForm(true);
  };

  const handleEditStudent = (student) => {
    setEditingStudent(student);
    setShowStudentForm(true);
  };

  const handleDeleteStudent = async (id) => {
    if (!window.confirm('Are you sure you want to delete this student?')) {
      return;
    }
    try {
      await resourceService.deleteStudent(id);
      await loadStudents();
      alert('Student deleted successfully');
    } catch (err) {
      alert(err.response?.data?.error || 'Failed to delete student');
    }
  };

  if (loading) return <div className="loading">Loading...</div>;

  return (
    <div className="dashboard-container">
      <nav className="navbar">
        <h1>Admin Dashboard</h1>
        <button onClick={handleLogout} className="logout-btn">Logout</button>
      </nav>

      <div className="dashboard-content">
        {error && <div className="error-box">{error}</div>}

        <div className="stats-grid">
          <div className="stat-card">
            <h3>Total Students</h3>
            <p className="stat-number">{dashboardData?.total_students || 0}</p>
          </div>
          <div className="stat-card">
            <h3>Total Professors</h3>
            <p className="stat-number">{dashboardData?.total_professors || 0}</p>
          </div>
          <div className="stat-card">
            <h3>Total Subjects</h3>
            <p className="stat-number">{dashboardData?.total_subjects || 0}</p>
          </div>
          <div className="stat-card">
            <h3>Total Faculties</h3>
            <p className="stat-number">{dashboardData?.total_faculties || 0}</p>
          </div>
        </div>

        <div className="content-section">
          <h2>Faculty Overview</h2>
          <table className="data-table">
            <thead>
              <tr>
                <th>Faculty Name</th>
                <th>Department</th>
                <th>Description</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {faculties.map((faculty) => (
                <tr key={faculty.id}>
                  <td>{faculty.name}</td>
                  <td>{faculty.department}</td>
                  <td>{faculty.description || 'N/A'}</td>
                  <td>{faculty.is_active ? '✓ Active' : '✗ Inactive'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="content-section">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
            <h2>Professors</h2>
            <div style={{ display: 'flex', gap: '10px' }}>
              {/* <button 
                onClick={handleCreateProfessor}
                style={{ 
                  padding: '0.5rem 1rem', 
                  fontSize: '0.9rem',
                  backgroundColor: '#28a745',
                  color: 'white',
                  border: 'none',
                  borderRadius: '4px',
                  cursor: 'pointer'
                }}
              >
                + Add Professor
              </button> */}
              <button 
                onClick={handleShowProfessors} 
                className="logout-btn"
                disabled={loadingProfessors}
                style={{ padding: '0.5rem 1rem', fontSize: '0.9rem' }}
              >
                {loadingProfessors ? 'Loading...' : showProfessors ? 'Hide' : 'Show'}
              </button>
            </div>
          </div>
          {showProfessors && (
            loadingProfessors ? (
              <p>Loading professors...</p>
            ) : professors.length > 0 ? (
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Faculty</th>
                    <th>Specialization</th>
                    <th>Phone</th>
                    <th>Office Hours</th>
                    <th>Subjects Count</th>
                    <th>Status</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {professors.map((professor) => (
                    <tr key={professor.id}>
                      <td>{professor.user?.first_name || ''} {professor.user?.last_name || ''} ({professor.user?.username || ''})</td>
                      <td>{professor.user?.email || 'N/A'}</td>
                      <td>{professor.faculty_name || 'N/A'}</td>
                      <td>{professor.specialization || 'N/A'}</td>
                      <td>{professor.phone || 'N/A'}</td>
                      <td>{professor.office_hours || 'N/A'}</td>
                      <td>{professor.subjects?.length || 0}</td>
                      <td>{professor.is_active ? '✓ Active' : '✗ Inactive'}</td>
                      <td>
                        <button
                          onClick={() => handleEditProfessor(professor)}
                          style={{
                            padding: '5px 10px',
                            marginRight: '5px',
                            backgroundColor: '#007bff',
                            color: 'white',
                            border: 'none',
                            borderRadius: '4px',
                            cursor: 'pointer',
                            fontSize: '0.85rem'
                          }}
                        >
                          Edit
                        </button>
                        <button
                          onClick={() => handleDeleteProfessor(professor.id)}
                          style={{
                            padding: '5px 10px',
                            backgroundColor: '#dc3545',
                            color: 'white',
                            border: 'none',
                            borderRadius: '4px',
                            cursor: 'pointer',
                            fontSize: '0.85rem'
                          }}
                        >
                          Delete
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <p>No professors found</p>
            )
          )}
        </div>

        <div className="content-section">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
            <h2>Students</h2>
            <div style={{ display: 'flex', gap: '10px' }}>
              {/* <button 
                onClick={handleCreateStudent}
                style={{ 
                  padding: '0.5rem 1rem', 
                  fontSize: '0.9rem',
                  backgroundColor: '#28a745',
                  color: 'white',
                  border: 'none',
                  borderRadius: '4px',
                  cursor: 'pointer'
                }}
              >
                + Add Student
              </button> */}
              <button 
                onClick={handleShowStudents} 
                className="logout-btn"
                disabled={loadingStudents}
                style={{ padding: '0.5rem 1rem', fontSize: '0.9rem' }}
              >
                {loadingStudents ? 'Loading...' : showStudents ? 'Hide' : 'Show'}
              </button>
            </div>
          </div>
          {showStudents && (
            loadingStudents ? (
              <p>Loading students...</p>
            ) : students.length > 0 ? (
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Enrollment Number</th>
                    <th>Faculty</th>
                    <th>GPA</th>
                    <th>Phone</th>
                    <th>Subjects Count</th>
                    <th>Status</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {students.map((student) => {
                    const gpaValue = student.gpa != null ? Number(student.gpa) : 0;
                    const displayGPA = Number.isFinite(gpaValue) ? gpaValue.toFixed(2) : '0.00';
                    return (
                      <tr key={student.id}>
                        <td>{student.user?.first_name || ''} {student.user?.last_name || ''} ({student.user?.username || ''})</td>
                        <td>{student.user?.email || 'N/A'}</td>
                        <td>{student.enrollment_number}</td>
                        <td>{student.faculty_name || 'N/A'}</td>
                        <td>{displayGPA}</td>
                        <td>{student.phone || 'N/A'}</td>
                        <td>{student.subjects?.length || 0}</td>
                        <td>{student.is_active ? '✓ Active' : '✗ Inactive'}</td>
                        <td>
                          <button
                            onClick={() => handleEditStudent(student)}
                            style={{
                              padding: '5px 10px',
                              marginRight: '5px',
                              backgroundColor: '#007bff',
                              color: 'white',
                              border: 'none',
                              borderRadius: '4px',
                              cursor: 'pointer',
                              fontSize: '0.85rem'
                            }}
                          >
                            Edit
                          </button>
                          <button
                            onClick={() => handleDeleteStudent(student.id)}
                            style={{
                              padding: '5px 10px',
                              backgroundColor: '#dc3545',
                              color: 'white',
                              border: 'none',
                              borderRadius: '4px',
                              cursor: 'pointer',
                              fontSize: '0.85rem'
                            }}
                          >
                            Delete
                          </button>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            ) : (
              <p>No students found</p>
            )
          )}
        </div>

        {/* Professor Form Modal */}
        {showProfessorForm && (
          <ProfessorForm
            professor={editingProfessor}
            faculties={faculties}
            onClose={() => {
              setShowProfessorForm(false);
              setEditingProfessor(null);
            }}
            onSave={async (data) => {
              try {
                if (editingProfessor) {
                  await resourceService.updateProfessor(editingProfessor.id, data);
                  alert('Professor updated successfully');
                } else {
                  await resourceService.createProfessor(data);
                  alert('Professor created successfully');
                }
                await loadProfessors();
                setShowProfessorForm(false);
                setEditingProfessor(null);
              } catch (err) {
                alert(err.response?.data?.error || 'Failed to save professor');
              }
            }}
          />
        )}

        {/* Student Form Modal */}
        {showStudentForm && (
          <StudentForm
            student={editingStudent}
            faculties={faculties}
            onClose={() => {
              setShowStudentForm(false);
              setEditingStudent(null);
            }}
            onSave={async (data) => {
              try {
                if (editingStudent) {
                  await resourceService.updateStudent(editingStudent.id, data);
                  alert('Student updated successfully');
                } else {
                  await resourceService.createStudent(data);
                  alert('Student created successfully');
                }
                await loadStudents();
                setShowStudentForm(false);
                setEditingStudent(null);
              } catch (err) {
                alert(err.response?.data?.error || 'Failed to save student');
              }
            }}
          />
        )}
      </div>
    </div>
  );
}

// Professor Form Component
function ProfessorForm({ professor, faculties, onClose, onSave }) {
  const [formData, setFormData] = useState({
    username: professor?.user?.username || '',
    email: professor?.user?.email || '',
    first_name: professor?.user?.first_name || '',
    last_name: professor?.user?.last_name || '',
    password: '',
    faculty: professor?.faculty || '',
    specialization: professor?.specialization || '',
    phone: professor?.phone || '',
    office_hours: professor?.office_hours || '',
    is_active: professor?.is_active !== undefined ? professor.is_active : true,
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave(formData);
  };

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      backgroundColor: 'rgba(0,0,0,0.5)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 1000
    }}>
      <div style={{
        backgroundColor: 'white',
        padding: '30px',
        borderRadius: '8px',
        maxWidth: '600px',
        width: '90%',
        maxHeight: '90vh',
        overflowY: 'auto',
        boxShadow: '0 4px 6px rgba(0,0,0,0.1)'
      }}>
        <h3>{professor ? 'Edit Professor' : 'Create Professor'}</h3>
        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '5px' }}>Username *</label>
            <input
              type="text"
              required
              value={formData.username}
              onChange={(e) => setFormData({...formData, username: e.target.value})}
              style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }}
              disabled
            />
          </div>
          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '5px' }}>Email *</label>
            <input
              type="email"
              required
              value={formData.email}
              onChange={(e) => setFormData({...formData, email: e.target.value})}
              style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }}
              disabled
            />
          </div>
          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '5px' }}>First Name</label>
            <input
              type="text"
              value={formData.first_name}
              onChange={(e) => setFormData({...formData, first_name: e.target.value})}
              style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }}
              disabled
            />
          </div>
          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '5px' }}>Last Name</label>
            <input
              type="text"
              value={formData.last_name}
              onChange={(e) => setFormData({...formData, last_name: e.target.value})}
              style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }}
              disabled
            />
          </div>
          {!professor && (
            <div style={{ marginBottom: '15px' }}>
              <label style={{ display: 'block', marginBottom: '5px' }}>Password *</label>
              <input
                type="password"
                required={!professor}
                value={formData.password}
                onChange={(e) => setFormData({...formData, password: e.target.value})}
                style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }}
              />
            </div>
          )}
          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '5px' }}>Faculty</label>
            <select
              value={formData.faculty}
              onChange={(e) => setFormData({...formData, faculty: e.target.value})}
              style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }}
            >
              <option value="">Select Faculty</option>
              {faculties.map(f => (
                <option key={f.id} value={f.id}>{f.name}</option>
              ))}
            </select>
          </div>
          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '5px' }}>Specialization</label>
            <input
              type="text"
              value={formData.specialization}
              onChange={(e) => setFormData({...formData, specialization: e.target.value})}
              style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }}
            />
          </div>
          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '5px' }}>Phone</label>
            <input
              type="text"
              value={formData.phone}
              onChange={(e) => setFormData({...formData, phone: e.target.value})}
              style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }}
            />
          </div>
          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '5px' }}>Office Hours</label>
            <input
              type="text"
              value={formData.office_hours}
              onChange={(e) => setFormData({...formData, office_hours: e.target.value})}
              style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }}
            />
          </div>
          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <input
                type="checkbox"
                checked={formData.is_active}
                onChange={(e) => setFormData({...formData, is_active: e.target.checked})}
              />
              Active
            </label>
          </div>
          <div style={{ display: 'flex', gap: '10px', justifyContent: 'flex-end' }}>
            <button
              type="button"
              onClick={onClose}
              style={{
                padding: '10px 20px',
                backgroundColor: '#6c757d',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer'
              }}
            >
              Cancel
            </button>
            <button
              type="submit"
              style={{
                padding: '10px 20px',
                backgroundColor: '#007bff',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer'
              }}
            >
              {professor ? 'Update' : 'Create'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

// Student Form Component
function StudentForm({ student, faculties, onClose, onSave }) {
  const [formData, setFormData] = useState({
    username: student?.user?.username || '',
    email: student?.user?.email || '',
    first_name: student?.user?.first_name || '',
    last_name: student?.user?.last_name || '',
    password: '',
    enrollment_number: student?.enrollment_number || '',
    faculty: student?.faculty || '',
    phone: student?.phone || '',
    gpa: student?.gpa || '0.00',
    is_active: student?.is_active !== undefined ? student.is_active : true,
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave(formData);
  };

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      backgroundColor: 'rgba(0,0,0,0.5)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 1000
    }}>
      <div style={{
        backgroundColor: 'white',
        padding: '30px',
        borderRadius: '8px',
        maxWidth: '600px',
        width: '90%',
        maxHeight: '90vh',
        overflowY: 'auto',
        boxShadow: '0 4px 6px rgba(0,0,0,0.1)'
      }}>
        <h3>{student ? 'Edit Student' : 'Create Student'}</h3>
        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '5px' }}>Username *</label>
            <input
              type="text"
              required
              value={formData.username}
              onChange={(e) => setFormData({...formData, username: e.target.value})}
              style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }}
              disabled
            />
          </div>
          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '5px' }}>Email *</label>
            <input
              type="email"
              required
              value={formData.email}
              onChange={(e) => setFormData({...formData, email: e.target.value})}
              style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }}
              disabled
            />
          </div>
          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '5px' }}>First Name</label>
            <input
              type="text"
              value={formData.first_name}
              onChange={(e) => setFormData({...formData, first_name: e.target.value})}
              style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }}
              disabled
            />
          </div>
          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '5px' }}>Last Name</label>
            <input
              type="text"
              value={formData.last_name}
              onChange={(e) => setFormData({...formData, last_name: e.target.value})}
              style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }}
              disabled
            />
          </div>
          {!student && (
            <div style={{ marginBottom: '15px' }}>
              <label style={{ display: 'block', marginBottom: '5px' }}>Password *</label>
              <input
                type="password"
                required={!student}
                value={formData.password}
                onChange={(e) => setFormData({...formData, password: e.target.value})}
                style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }}
              />
            </div>
          )}
          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '5px' }}>Enrollment Number *</label>
            <input
              type="text"
              required
              value={formData.enrollment_number}
              onChange={(e) => setFormData({...formData, enrollment_number: e.target.value})}
              style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }}
            />
          </div>
          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '5px' }}>Faculty</label>
            <select
              value={formData.faculty}
              onChange={(e) => setFormData({...formData, faculty: e.target.value})}
              style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }}
            >
              <option value="">Select Faculty</option>
              {faculties.map(f => (
                <option key={f.id} value={f.id}>{f.name}</option>
              ))}
            </select>
          </div>
          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '5px' }}>Phone</label>
            <input
              type="text"
              value={formData.phone}
              onChange={(e) => setFormData({...formData, phone: e.target.value})}
              style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }}
            />
          </div>
          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '5px' }}>GPA</label>
            <input
              type="number"
              step="0.01"
              min="0"
              max="4"
              value={formData.gpa}
              onChange={(e) => setFormData({...formData, gpa: e.target.value})}
              style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }}
            />
          </div>
          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <input
                type="checkbox"
                checked={formData.is_active}
                onChange={(e) => setFormData({...formData, is_active: e.target.checked})}
              />
              Active
            </label>
          </div>
          <div style={{ display: 'flex', gap: '10px', justifyContent: 'flex-end' }}>
            <button
              type="button"
              onClick={onClose}
              style={{
                padding: '10px 20px',
                backgroundColor: '#6c757d',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer'
              }}
            >
              Cancel
            </button>
            <button
              type="submit"
              style={{
                padding: '10px 20px',
                backgroundColor: '#007bff',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer'
              }}
            >
              {student ? 'Update' : 'Create'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default AdminDashboard;
