import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#07080e",
        surface: {
          DEFAULT: "#0d111d",
          elevated: "#13192b",
          border: "#1e2843",
          hover: "#1a233c"
        },
        primary: {
          DEFAULT: "#8b5cf6",
          dark: "#7c3aed",
          light: "#a78bfa",
          glow: "rgba(139, 92, 246, 0.35)"
        },
        cyan: {
          DEFAULT: "#06b6d4",
          light: "#38bdf8",
          glow: "rgba(6, 182, 212, 0.35)"
        },
        accent: {
          blue: "#3b82f6",
          purple: "#9333ea",
          pink: "#ec4899",
          emerald: "#10b981",
          amber: "#f59e0b",
          rose: "#f43f5e"
        }
      },
      backgroundImage: {
        "gradient-radial": "radial-gradient(var(--tw-gradient-stops))",
        "jarvis-grid": "linear-gradient(to right, rgba(139, 92, 246, 0.05) 1px, transparent 1px), linear-gradient(to bottom, rgba(139, 92, 246, 0.05) 1px, transparent 1px)",
      },
      animation: {
        "pulse-slow": "pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite",
        "spin-slow": "spin 12s linear infinite",
        "glow": "glow 2.5s ease-in-out infinite alternate",
      },
      keyframes: {
        glow: {
          "0%": { boxShadow: "0 0 15px rgba(139, 92, 246, 0.3)" },
          "100%": { boxShadow: "0 0 30px rgba(6, 182, 212, 0.6), 0 0 45px rgba(139, 92, 246, 0.4)" }
        }
      }
    },
  },
  plugins: [],
};
export default config;
