# API Endpoints Documentation

## Authentication & Authorization

All endpoints use JWT authentication via `Authorization: Bearer <token>` header, except for login/logout/renew endpoints.

---

## Public Endpoints (AllowAny - No Authentication Required)

### 1. Login
- **Endpoint:** `POST /api/login/`
- **Protection:** ✅ Public (AllowAny)
- **Description:** Login and receive JWT token
- **Request Body:**
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```

### 2. Logout
- **Endpoint:** `POST /api/logout/`
- **Protection:** ✅ Public (AllowAny)
- **Description:** Logout and clear refresh token

### 3. Renew Token
- **Endpoint:** `POST /api/renew/`
- **Protection:** ✅ Public (AllowAny)
- **Description:** Renew access token using refresh token from cookie

---

## Protected Endpoints (Require Authentication)

### Dashboard Endpoints

#### 4. Admin Dashboard
- **Endpoint:** `GET /api/admin-dashboard/`
- **Protection:** 🔒 Protected (IsAuthenticated + IsAdmin)
- **Description:** Get admin dashboard statistics

#### 5. Professor Dashboard
- **Endpoint:** `GET /api/professor-dashboard/`
- **Protection:** 🔒 Protected (IsAuthenticated + IsProfessor)
- **Description:** Get professor dashboard with subjects and students

#### 6. Student Dashboard
- **Endpoint:** `GET /api/student-dashboard/`
- **Protection:** 🔒 Protected (IsAuthenticated + IsStudent)
- **Description:** Get student dashboard with enrolled subjects and GPA

---

## Student Endpoints

#### 7. Get Available Courses
- **Endpoint:** `GET /api/courses/`
- **Protection:** 🔒 Protected (IsAuthenticated + IsStudent)
- **Description:** Get all available courses with enrollment status

#### 8. Enroll in Course
- **Endpoint:** `POST /api/enroll/<subject_id>/`
- **Protection:** 🔒 Protected (IsAuthenticated + IsStudent)
- **Description:** Enroll student in a course
- **Example:** `POST /api/enroll/1/`

---

## Professor Grading Endpoints

#### 9. Get Student Grades
- **Endpoint:** `GET /api/grades/<student_id>/`
- **Protection:** 🔒 Protected (IsAuthenticated + IsProfessor)
- **Description:** Get all grades for a student in professor's subjects
- **Example:** `GET /api/grades/1/`

#### 10. Get Student Grade for Specific Subject
- **Endpoint:** `GET /api/grades/<student_id>/<subject_id>/`
- **Protection:** 🔒 Protected (IsAuthenticated + IsProfessor)
- **Description:** Get grade for a specific student-subject combination
- **Example:** `GET /api/grades/1/2/`

#### 11. Grade Student (Create/Update)
- **Endpoint:** `POST /api/grade/<student_id>/<subject_id>/`
- **Protection:** 🔒 Protected (IsAuthenticated + IsProfessor)
- **Description:** Create or update a grade for a student in a subject
- **Example:** `POST /api/grade/1/2/`
- **Request Body:**
  ```json
  {
    "grade": 85.5,
    "notes": "Excellent work"
  }
  ```

#### 12. Update Grade
- **Endpoint:** `PUT /api/grade/<student_id>/<subject_id>/`
- **Protection:** 🔒 Protected (IsAuthenticated + IsProfessor)
- **Description:** Update an existing grade
- **Example:** `PUT /api/grade/1/2/`
- **Request Body:**
  ```json
  {
    "grade": 90.0,
    "notes": "Updated notes"
  }
  ```

---

## CRUD Endpoints (ViewSets)

All ViewSet endpoints require **IsAuthenticated** at minimum. Some have additional role-based restrictions.

### 13. Faculties
- **Endpoints:**
  - `GET /api/faculties/` - List all faculties
  - `POST /api/faculties/` - Create faculty
  - `GET /api/faculties/<id>/` - Get faculty details
  - `PUT /api/faculties/<id>/` - Update faculty
  - `PATCH /api/faculties/<id>/` - Partial update
  - `DELETE /api/faculties/<id>/` - Delete faculty
- **Protection:** 🔒 Protected (IsAuthenticated)

### 14. Subjects
- **Endpoints:**
  - `GET /api/subjects/` - List all subjects
  - `POST /api/subjects/` - Create subject
  - `GET /api/subjects/<id>/` - Get subject details
  - `PUT /api/subjects/<id>/` - Update subject
  - `PATCH /api/subjects/<id>/` - Partial update
  - `DELETE /api/subjects/<id>/` - Delete subject
- **Protection:** 🔒 Protected (IsAuthenticated)

### 15. Administrators
- **Endpoints:**
  - `GET /api/administrators/` - List all administrators
  - `POST /api/administrators/` - Create administrator
  - `GET /api/administrators/<id>/` - Get administrator details
  - `PUT /api/administrators/<id>/` - Update administrator
  - `PATCH /api/administrators/<id>/` - Partial update
  - `DELETE /api/administrators/<id>/` - Delete administrator
- **Protection:** 🔒 Protected (IsAuthenticated + IsAdmin)

### 16. Professors
- **Endpoints:**
  - `GET /api/professors/` - List all professors
  - `POST /api/professors/` - Create professor
  - `GET /api/professors/<id>/` - Get professor details
  - `PUT /api/professors/<id>/` - Update professor
  - `PATCH /api/professors/<id>/` - Partial update
  - `DELETE /api/professors/<id>/` - Delete professor
- **Protection:** 🔒 Protected (IsAuthenticated + IsAdmin)

### 17. Students
- **Endpoints:**
  - `GET /api/students/` - List all students
  - `POST /api/students/` - Create student
  - `GET /api/students/<id>/` - Get student details
  - `PUT /api/students/<id>/` - Update student
  - `PATCH /api/students/<id>/` - Partial update
  - `DELETE /api/students/<id>/` - Delete student
- **Protection:** 🔒 Protected (IsAuthenticated)

---

## Debug Endpoint

#### 18. Get All Users (Debug)
- **Endpoint:** `GET /api/users/`
- **Protection:** ✅ Public (AllowAny)
- **Description:** Debug endpoint to list all users (for development only)

---

## Summary

### Public Endpoints (3):
- ✅ `POST /api/login/`
- ✅ `POST /api/logout/`
- ✅ `POST /api/renew/`
- ✅ `GET /api/users/` (debug)

### Protected Endpoints (15+):
- 🔒 All dashboard endpoints (Admin, Professor, Student)
- 🔒 All student course endpoints
- 🔒 All professor grading endpoints
- 🔒 All CRUD ViewSet endpoints

### Authentication:
- All protected endpoints require JWT token in `Authorization: Bearer <token>` header
- Missing or invalid token returns **401 Unauthorized**
- Insufficient permissions return **403 Forbidden**

### Error Responses:
- **401 Unauthorized:** Missing or invalid authentication token
- **403 Forbidden:** Authenticated but insufficient permissions
- **404 Not Found:** Resource not found
- **400 Bad Request:** Invalid request data

