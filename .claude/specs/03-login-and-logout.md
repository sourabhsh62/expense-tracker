# Spec: Login and Logout

## Overview
Implement user authentication so registered users can sign in to their Spendly account and sign out securely. This step adds session-based login/logout functionality using Flask's built-in session support. The login route validates credentials against the `users` table, establishes a session on success, and redirects to a profile or dashboard page. Logout destroys the session and redirects to the landing page. This is a prerequisite for all authenticated expense management features.

## Depends on
- Step 01 — Database setup (`users` table, `get_db()`)
- Step 02 — Registration (user creation, password hashing)

## Routes
- `GET /login` — render login form — public (already exists as stub, upgrade it)
- `POST /login` — validate credentials, create session, redirect — public
- `GET /logout` — destroy session, redirect to landing — logged-in users

## Database changes
No new tables or columns. A new DB helper must be added to `database/db.py`:
- `get_user_by_email(email)` — returns the user row if found, `None` otherwise
- `get_user_by_id(user_id)` — returns the user row if found, `None` otherwise

## Templates
- **Modify**: `templates/login.html`
  - Change the form `action` to `url_for('login')` with `method="post"`
  - Add `name` attributes to inputs: `email`, `password` (verify existing)
  - Add a block to display flash error messages (e.g. "Invalid email or password")
  - Add flash success message display for logout confirmation
  - Keep all existing visual design

## Files to change
- `app.py` — upgrade `login()` to handle GET/POST with session logic; upgrade `logout()` to destroy session
- `database/db.py` — add `get_user_by_email()` and `get_user_by_id()` helpers
- `templates/login.html` — wire up form and flash message display
- `templates/base.html` — add logout link visible only when logged in (optional navigation enhancement)

## Files to create
None.

## New dependencies
No new dependencies. Uses Flask's built-in `session`, `flash`, `redirect`, `url_for`, and `abort`.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — never use f-strings in SQL
- Passwords verified with `werkzeug.security.check_password_hash` — never compare plaintext
- `app.secret_key` must be set in `app.py` for `session` and `flash` to work (use a hardcoded dev string)
- Server-side validation must check:
  1. All fields are non-empty
  2. Email exists in database
  3. Password hash matches stored hash
- On login failure, re-render the form with a flashed error message — do not redirect
- On login success, `flash` a welcome message and `redirect` to `url_for('profile')` or landing
- On logout, `flash` a goodbye message and `redirect` to `url_for('landing')`
- Use `abort(405)` if an unsupported HTTP method reaches the route
- All templates extend `base.html`
- Use CSS variables — never hardcode hex values
- Use `url_for()` for every internal link — never hardcode URLs
- Session key should be `user_id` — store only the integer ID, not the full user object

## Definition of done
- [ ] `GET /login` renders the login form without errors
- [ ] Submitting with valid email/password creates a session and redirects to profile or landing
- [ ] Submitting with invalid email re-renders form with "Invalid email or password" error
- [ ] Submitting with valid email but wrong password re-renders form with error
- [ ] Submitting with empty fields re-renders form with validation error
- [ ] `GET /logout` destroys the session and redirects to landing with goodbye message
- [ ] After logout, accessing a protected route (if any) does not crash — session is gone
- [ ] `user_id` stored in session is verifiable by inspecting Flask session after login
- [ ] No plaintext password comparison — only `check_password_hash` is used
