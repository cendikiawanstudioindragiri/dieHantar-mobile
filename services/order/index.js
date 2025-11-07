const http = require('http');

const PORT = process.env.PORT || 3002;

let dbClient = null;
async function initDb() {
  const DATABASE_URL = process.env.DATABASE_URL;
  if (!DATABASE_URL) return null;
  try {
    const { Client } = require('pg');
    const client = new Client({ connectionString: DATABASE_URL });
    await client.connect();
    await client.query(`
      CREATE TABLE IF NOT EXISTS orders (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL,
        items JSONB NOT NULL,
        status TEXT NOT NULL DEFAULT 'created',
        created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
      )
    `);
    console.log('Order service connected to Postgres and ensured orders table exists');
    return client;
  } catch (err) {
    console.error('Order DB init failed:', err.message || err);
    return null;
  }
}

function sendJSON(res, status, obj) {
  res.writeHead(status, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify(obj));
}

async function handleRequest(req, res) {
  if (req.method === 'GET' && req.url === '/health') {
    return sendJSON(res, 200, { status: 'ok', service: 'order' });
  }

  if (req.method === 'POST' && req.url === '/orders') {
    let body = '';
    req.on('data', (chunk) => (body += chunk));
    req.on('end', async () => {
      try {
        const { userId, items } = JSON.parse(body || '{}');
        if (!userId || !items) return sendJSON(res, 400, { error: 'userId and items required' });
        if (dbClient) {
          try {
            const result = await dbClient.query('INSERT INTO orders(user_id, items) VALUES($1,$2) RETURNING id, status', [userId, items]);
            return sendJSON(res, 201, { orderId: result.rows[0].id, status: result.rows[0].status });
          } catch (dbErr) {
            return sendJSON(res, 500, { error: dbErr.message });
          }
        }
        // fallback
        return sendJSON(res, 201, { orderId: 1001, status: 'created' });
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
    console.error('Order request handler error', err);
    sendJSON(res, 500, { error: 'internal error' });
  });
});

(async () => {
  dbClient = await initDb();
  server.listen(PORT, () => console.log(`Order service listening on ${PORT}`));
})();
