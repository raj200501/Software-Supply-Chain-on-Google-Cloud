const http = require('http');

function createApp() {
  const routes = new Map();

  function handler(req, res) {
    const key = `${req.method} ${req.url.split('?')[0]}`;
    if (routes.has(key)) {
      routes.get(key)(req, res);
      return;
    }
    res.statusCode = 404;
    res.end('not found');
  }

  handler.post = (path, fn) => {
    routes.set(`POST ${path}`, fn);
  };
  handler.get = (path, fn) => {
    routes.set(`GET ${path}`, fn);
  };

  return handler;
}

const app = createApp();

app.get('/healthz', (_req, res) => {
  res.setHeader('Content-Type', 'application/json');
  res.end(JSON.stringify({ status: 'ok' }));
});

app.post('/payments/capture', async (req, res) => {
  let body = '';
  req.on('data', (chunk) => {
    body += chunk;
  });
  req.on('end', async () => {
    try {
      const payload = JSON.parse(body || '{}');
      if (!payload.orderId || typeof payload.amount !== 'number') {
        res.statusCode = 400;
        res.end(JSON.stringify({ error: 'orderId and amount are required' }));
        return;
      }
      if (process.env.NOTIFICATIONS_URL) {
        try {
          await fetch(`${process.env.NOTIFICATIONS_URL}/notifications`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              orderId: payload.orderId,
              amount: payload.amount,
            }),
          });
        } catch (err) {
          console.error('failed to call notifications service', err);
        }
      }
      res.statusCode = 201;
      res.setHeader('Content-Type', 'application/json');
      res.end(
        JSON.stringify({
          id: `pay-${Date.now()}`,
          orderId: payload.orderId,
          amount: payload.amount,
          status: 'captured',
        }),
      );
    } catch (err) {
      res.statusCode = 400;
      res.end(JSON.stringify({ error: err.message }));
    }
  });
});

function listen(port, cb) {
  const server = http.createServer((req, res) => app(req, res));
  server.listen(port, cb);
  return server;
}

if (require.main === module) {
  const port = Number(process.env.PORT || 8083);
  listen(port, () => {
    console.log(`payments service listening on :${port}`);
  });
}

module.exports = { app, listen };
