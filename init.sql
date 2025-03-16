ALTER SYSTEM SET listen_addresses = '*';
ALTER SYSTEM SET password_encryption = 'scram-sha-256';
CREATE USER admin WITH PASSWORD '00000000';
ALTER USER admin WITH SUPERUSER;
