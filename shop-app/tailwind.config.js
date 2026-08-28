/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        moss: {
          50: '#f2f5f1', 100: '#e1e8dd', 200: '#c4d3bc',
          400: '#7d9c6c', 700: '#3b5330', 800: '#2c4a3e',
        },
        clay: { 500: '#b06f2c', 600: '#93591f' },
        sand: { 50: '#f9f7f2' },
      },
    },
  },
  plugins: [],
}