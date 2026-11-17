// frontend/pages/index.tsx
import Head from 'next/head';

export default function Home() {
  return (
    <>
      <Head>
        <title>NIKITHA.AI</title>
      </Head>
      <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-gray-900 via-gray-800 to-black text-white">
        <div className="text-center max-w-2xl">
          <h1 className="text-5xl font-bold mb-4">NIKITHA.AI</h1>
          <p className="text-xl mb-8">Your Personal AI. Beyond Assistance.</p>
          <a
            href="/login"
            className="px-6 py-3 bg-indigo-600 hover:bg-indigo-500 rounded transition"
          >
            Get Started
          </a>
        </div>
      </div>
    </>
  );
}
