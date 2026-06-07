## User Routes (/api/user)

### GET /api/user
- Purpose: Get current authenticated user profile
- Auth: JWT required
- Body: none
- Success:
  - `200 OK`
  - User DTO

### PUT /api/user
- Purpose: Update current user profile
- Auth: JWT required
- Body (any of):
  - `name` (string, optional)
  - `email` (string, optional)
- Success:
  - `200 OK`
  - Updated user DTO

### PUT /api/user/name
- Purpose: Update current user's display name
- Auth: JWT required
- Body:
  - `name` (string, required)
- Success:
  - `200 OK`
  - Updated user DTO
- Errors:
  - `400 Bad Request` when name is missing or empty

### PUT /api/user/email
- Purpose: Update current user's email address
- Auth: JWT required
- Body:
  - `email` (string, required)
- Success:
  - `200 OK`
  - Updated user DTO
- Errors:
  - `400 Bad Request` when email is missing, empty, or already in use

### PUT /api/user/password
- Purpose: Change current user password
- Auth: JWT required
- Body:
  - `password` (string, required)
  - `new_password` (string, required)
- Success:
  - `200 OK`
  - `{ "success": true, "message": "Password updated" }`
- Error:
  - `400 Bad Request` when current password is incorrect

### POST user image 
- Purpose: Upload and replace the current user's profile image
- Auth: JWT required
- Content-Type: `multipart/form-data`
- Body:
  - `profile_image` (file, required)
- Success:
  - `200 OK`
  - `{ "success": true, "message": "Profile image uploaded successfully", "profileImage": "..." }`
- Errors:
  - `400 Bad Request` when the request is not multipart/form-data
  - `400 Bad Request` when no file is uploaded
  - `400 Bad Request` when the image is invalid, empty, or larger than 2MB

### DELETE /api/user/image
- Purpose: Delete the current user's profile image
- Auth: JWT required
- Success:
  - `200 OK`
  - `{ "success": true, "message": "Profile image deleted successfully" }`
- Errors:
  - `400 Bad Request` when no profile image exists for the user
