// tailwind.config.js
module.exports = {
  content: [
    './components/**/*.{js,vue,ts}',
    './layouts/**/*.vue',
    './pages/**/*.vue',
    './plugins/**/*.{js,ts}',
    './nuxt.config.{js,ts}',
    './app.vue',
    './assets/icons/**/*.vue' // Add this line for icon components
  ],
  theme: {
    extend: {
      colors: {
        // Your custom colors
        'primary-dark': '#222222',
        'primary-green': '#328336',
        'accent-green': '#64cc4f',
        'light-green': '#b2e05b',
        'text-light': '#ffffff',
        'text-secondary': '#5a687a',
        'border-color': '#e5e7eb',
        'card-background': '#ffffff'
      }
    }
  },
  plugins: [],
}