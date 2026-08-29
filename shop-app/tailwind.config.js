/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        ridge: { 50: '#eef1ec', 200: '#c3cec2', 700: '#2c4436', 800: '#21362b', 900: '#182720' },
        moss: { 400: '#7d9878', 600: '#4a6449', 700: '#3f5b41' },
        parchment: { 50: '#faf8f1', 100: '#efead9', 200: '#e3dcc4' },
        blaze: { amber: '#c98a2b', rust: '#a23e2b' },
      },
      fontFamily: {
        display: ['"Fraunces"', 'serif'],
        body: ['"Inter"', 'sans-serif'],
        stamp: ['"JetBrains Mono"', 'monospace'],
      },
    },
  },
  plugins: [],
}