import { defineNuxtConfig } from 'nuxt/config';

export default defineNuxtConfig({
  devtools: { enabled: true },

  // Runtime config for environment variables
  runtimeConfig: {
    public: {
      apiBaseUrl: process.env.NUXT_PUBLIC_API_BASE_URL || 'https://ten-be.koyeb.app', // Added a fallback for development
      backendApiKey: process.env.NUXT_PUBLIC_BACKEND_API_KEY, // Keep backend API key if used by your composable
    }
  },

  // Modules: Tailwind CSS is already here.
  modules: [
    '@nuxtjs/tailwindcss'
  ],

  // Global CSS files. Font Awesome's styles are added here.
  css: [
    '@fortawesome/fontawesome-svg-core/styles.css', // Font Awesome's core CSS
    '~/assets/css/main.css', 
    'animate.css/animate.min.css',
// Your custom/Tailwind base CSS
  ],

  // Plugins to be loaded before the app mounts. Font Awesome plugin is added here.
  plugins: [
    '~/plugins/fontawesome.js', // Path to your Font Awesome plugin
  ],

  // Components auto-discovery setup
  components: {
    dirs: [
      '~/components', // Scan components in this directory
      // No need to explicitly add '~/assets/icons' here if Font Awesome is used.
      // If you still have non-Font Awesome SVG components there, you can keep it,
      // but if you're fully switching to FA, it's redundant.
    ]
  },

  // Nuxt App Head configuration
  app: {
    head: {
      charset: 'utf-8',
      viewport: 'width=device-width, initial-scale=1',
      title: 'TEN - Startup Growth Tools', // Add a default title
      htmlAttrs: {
        lang: 'en' // Specify language for accessibility
      },
      link: [
        { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
        { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: 'anonymous' },
        {
          rel: 'stylesheet',
          href: 'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap'
        },
        { rel: 'icon', type: 'image/png', href: '/favicon.png' } // Ensure favicon.png is in your `public` directory
      ]
    }
  },

  // Tailwind CSS configuration
  tailwindcss: {
    viewer: false, // Disables the Tailwind CSS viewer in development
    config: {
      // Ensure content paths are correct and comprehensive
      content: [
        './components/**/*.{js,vue,ts}',
        './layouts/**/*.vue',
        './pages/**/*.vue',
        './plugins/**/*.{js,ts}',
        './nuxt.config.{js,ts}',
        './app.vue',
        // If you remove `~/assets/icons` from `components.dirs`, this line can be removed too
        // './assets/icons/**/*.vue',
        './app.config.{js,ts}',
        './error.vue',
        './content/**/*.md', // Good to keep if you might use @nuxt/content
        // Add any other specific files or directories where Tailwind classes might be used
        // e.g., if you have utility files that generate HTML/classes
      ],
      theme: {
        extend: {
          colors: {
            // Your custom color palette
            'primary-dark': '#222222',
            'primary-green': '#328336',
            'accent-green': '#64cc4f',
            'light-green': '#b2e05b',
            'text-light': '#ffffff',
            'text-secondary': '#5a687a',
            'border-color': '#e5e7eb',
            'card-background': '#ffffff',
            'background': '#fbfbfd',
            // Added colors for consistency with the new components (optional, but good practice)
            'indigo-600': '#4f46e5', // For ExitStrategyExplorer
            'blue-600': '#2563eb',   // For RiskAssessment
            'purple-600': '#9333ea', // For ReputationAnalysis
            'orange-600': '#ea580c', // For InvestorMatch
            'emerald-600': '#059669',// For PitchFeedback
            'sky-600': '#0284c7',    // For CompetitorRadar
            'teal-600': '#0d9488',   // For TractionEstimator
            'rose-600': '#e11d48',   // For LegalAssistance
          }
        }
      }
    }
  },

  // Nitro server configuration
  nitro: {
    compatibility: {
      date: '2025-06-27'
    }
  }
})