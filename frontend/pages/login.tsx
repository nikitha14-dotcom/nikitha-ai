// frontend/pages/login.tsx
import { useState } from 'react';
import { useRouter } from 'next/router';
import { fetchJson } from '../lib/api';

export default function Login() {
  const router = useRouter();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const data = await fetchJson('/api/v1/auth/login', {
        method: 'POST',
        body: JSON.stringify({ username, password }),
        headers: { 'Content-Type': 'application/json' },
      });
      localStorage.setItem('nikitha_token', data.access_token);
      router.replace('/dashboard');
    } catch (err: any) {
      setError(err?.detail || 'Login failed');
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-900 text-white">
      <form onSubmit={handleSubmit} className="bg-gray-800 p-6 rounded shadow-md w-80">
        <h2 className="text-xl mb-4 text-center">Login</h2>
        {error && <p className="text-red-400 mb-2">{error}</p>}
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={e => setUsername(e.target.value)}
          className="w-full p-2 mb-2 bg-gray-700 rounded text-white"
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={e => setPassword(e.target.value)}
          className="w-full p-2 mb-4 bg-gray-700 rounded text-white"
          required
        />
        <button type="submit" className="w-full bg-blue-600 hover:bg-blue-500 p-2 rounded">
          Login
        </button>
      </form>
    </div>
  );
}
