const test = require('node:test');
const assert = require('node:assert');
const { listen } = require('../src/server');

async function withServer(t) {
  return new Promise((resolve) => {
    const server = listen(0, () => {
      const address = server.address();
      const url = `http://127.0.0.1:${address.port}`;
      t.after(() => server.close());
      resolve({ server, url });
    });
  });
}

test('health endpoint returns ok', async (t) => {
  const { url } = await withServer(t);
  const res = await fetch(`${url}/healthz`);
  assert.strictEqual(res.status, 200);
  const data = await res.json();
  assert.strictEqual(data.status, 'ok');
});

test('capture payment returns created', async (t) => {
  const { url } = await withServer(t);
  const res = await fetch(`${url}/payments/capture`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ orderId: 'order-1', amount: 42.5 }),
  });

  assert.strictEqual(res.status, 201);
  const payload = await res.json();
  assert.strictEqual(payload.orderId, 'order-1');
  assert.strictEqual(payload.status, 'captured');
});
