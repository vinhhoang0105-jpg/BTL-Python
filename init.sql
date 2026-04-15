-- Bootstrap script executed by PostgreSQL container on first start.
-- Tables are managed by Alembic migrations, this only ensures the DB exists.

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
