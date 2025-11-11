// Placeholder client-side auth service (calls backend endpoints)
export async function login(username: string, password: string) {
  const resp = await fetch('/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  });
  return resp.json();
}
