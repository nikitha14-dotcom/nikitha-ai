// frontend/pages/_app.tsx
import '../styles/globals.css';
import type { AppProps } from 'next/app';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';

function MyApp({ Component, pageProps }: AppProps) {
  const router = useRouter();
  const [token, setToken] = useState<string | null>(null);

  useEffect(() => {
    const stored = typeof window !== 'undefined' ? localStorage.getItem('nikitha_token') : null;
    setToken(stored);
  }, []);

  // protect routes that start with /dashboard, /chat, /tasks, /memory, /settings
  const protectedRoutes = ['/dashboard', '/chat', '/tasks', '/memory', '/settings'];
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const path = router.pathname;
      if (protectedRoutes.includes(path) && !token) {
        router.replace('/login');
      }
    }
  }, [router, token]);

  return <Component {...pageProps} />;
}

export default MyApp;
