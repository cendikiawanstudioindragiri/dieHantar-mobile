const http = require('http');
const { URL } = require('url');

const PORT = process.env.PORT || 3001;

let dbClient = null;
async function initDb() {
  const DATABASE_URL = process.env.DATABASE_URL;
  if (!DATABASE_URL) return null;
  try {
    const { Client } = require('pg');
    const client = new Client({ connectionString: DATABASE_URL });
    await client.connect();
    // create users table if not exists (simple schema for demo)
    await client.query(`
      CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
      )
    `);
    console.log('Connected to Postgres and ensured users table exists');
    return client;
  } catch (err) {
    console.error('Failed to initialize DB:', err.message || err);
    return null;
  }
}

function sendJSON(res, status, obj) {
  res.writeHead(status, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify(obj));
}

async function handleRequest(req, res) {
  if (req.method === 'GET' && req.url === '/health') {
    return sendJSON(res, 200, { status: 'ok', service: 'auth' });
  }

  if (req.method === 'POST' && req.url === '/auth/register') {
    let body = '';
    req.on('data', (chunk) => (body += chunk));
    req.on('end', async () => {
      try {
        const { username, password } = JSON.parse(body || '{}');
        if (!username || !password) return sendJSON(res, 400, { error: 'username and password required' });
        if (dbClient) {
          try {
            const bcrypt = require('bcrypt');
            const hashed = await bcrypt.hash(password, 10);
            const result = await dbClient.query('INSERT INTO users(username,password) VALUES($1,$2) RETURNING id, username', [username, hashed]);
            return sendJSON(res, 201, { user: result.rows[0] });
          } catch (dbErr) {
            return sendJSON(res, 400, { error: dbErr.message });
          }
        }
        // fallback: return fake user (no DB)
        return sendJSON(res, 201, { user: { id: 1, username } });
      } catch (err) {
        return sendJSON(res, 400, { error: 'invalid json' });
      }
    });
    return;
  }

  if (req.method === 'POST' && req.url === '/auth/login') {
    let body = '';
    req.on('data', (chunk) => (body += chunk));
    req.on('end', async () => {
      try {
        const { username, password } = JSON.parse(body || '{}');
        if (!username || !password) return sendJSON(res, 400, { error: 'username and password required' });
        if (dbClient) {
          try {
            const result = await dbClient.query('SELECT id, username, password FROM users WHERE username=$1', [username]);
            const user = result.rows[0];
            if (!user) return sendJSON(res, 401, { error: 'invalid credentials' });
            // Compare hashed password
            const bcrypt = require('bcrypt');
            const ok = await bcrypt.compare(password, user.password);
            if (!ok) return sendJSON(res, 401, { error: 'invalid credentials' });
            return sendJSON(res, 200, { token: 'fake-jwt-token', user: { id: user.id, username: user.username } });
          } catch (dbErr) {
            return sendJSON(res, 500, { error: dbErr.message });
          }
        }
        // fallback: return fake token
        return sendJSON(res, 200, { token: 'fake-jwt-token', user: { id: 1, username } });
      } catch (err) {
        return sendJSON(res, 400, { error: 'invalid json' });
      }
    });
    return;
  }

  sendJSON(res, 404, { error: 'not found' });
}

const server = http.createServer((req, res) => {
  handleRequest(req, res).catch((err) => {
    console.error('Request handler error', err);
    sendJSON(res, 500, { error: 'internal error' });
  });
});

(async () => {
  dbClient = await initDb();
  server.listen(PORT, () => console.log(`Auth service listening on ${PORT}`));
})();
