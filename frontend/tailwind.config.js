/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        surface: "var(--surface)",
        "surface-secondary": "var(--surface-secondary)",
        foreground: "var(--foreground)",
        muted: "var(--foreground-muted)",
        subtle: "var(--foreground-subtle)",
        border: "var(--border)",
        "border-strong": "var(--border-strong)",
        nav: "var(--nav)",
        "nav-hover": "var(--nav-hover)",
        primary: "var(--primary)",
        "primary-hover": "var(--primary-hover)",
        "primary-soft": "var(--primary-soft)",
        "primary-border": "var(--primary-border)",
        warning: "var(--warning)",
        "warning-soft": "var(--warning-soft)",
        danger: "var(--danger)",
        "danger-soft": "var(--danger-soft)",
        info: "var(--info)",
        "info-soft": "var(--info-soft)",
      },
      fontFamily: {
        sans: ["Geist", "Inter", "system-ui", "sans-serif"],
      },
      boxShadow: {
        card: "0 1px 2px rgba(16, 24, 40, 0.03), 0 1px 3px rgba(16, 24, 40, 0.04)",
        "card-hover": "0 8px 24px rgba(16, 24, 40, 0.07)",
      },
      borderRadius: {
        card: "14px",
        btn: "9px",
        input: "10px",
      },
    },
  },
  plugins: [],
};
