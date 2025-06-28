// nuxt.config.ts
import { defineNuxtConfig } from 'nuxt/config';

export default defineNuxtConfig({
  devtools: { enabled: true },

  runtimeConfig: {
    public: {
      apiBaseUrl: process.env.NUXT_PUBLIC_API_BASE_URL || 'https://ten-be.koyeb.app',
      backendApiKey: process.env.NUXT_PUBLIC_BACKEND_API_KEY,
    }
  },

  modules: [
    '@nuxtjs/tailwindcss',
    '@vite-pwa/nuxt',
  ],

  css: [
    '@fortawesome/fontawesome-svg-core/styles.css',
    '~/assets/css/main.css',
  ],

  plugins: [
    '~/plugins/fontawesome.js',
  ],

  components: {
    dirs: [
      '~/components',
    ]
  },

  app: {
    head: {
      charset: 'utf-8',
      viewport: 'width=device-width, initial-scale=1',
      title: 'TEN - Startup Growth Tools',
      htmlAttrs: {
        lang: 'en'
      },
      link: [
        { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
        { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: 'anonymous' },
        {
          rel: 'stylesheet',
          href: 'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap'
        },
        { rel: 'icon', type: 'image/png', href: '/favicon.png' }
      ]
    }
  },

  pwa: {
    // MOVE THIS LINE HERE:
    strategy: 'generateSW', // <--- MOVED THIS LINE HERE

    manifest: {
      name: 'TEN - Startup Growth Tools',
      short_name: 'TEN',
      description: 'Your platform for startup growth and success tools.',
      theme_color: '#328336',
      background_color: '#ffffff',
      display: 'standalone',
      scope: '/',
      start_url: '/',
      icons: [
        {
          src: 'pwa-192x192.png',
          sizes: '192x192',
          type: 'image/png',
        },
        {
          src: 'pwa-512x512.png',
          sizes: '512x512',
          type: 'image/png',
        },
        {
          src: 'pwa-512x512.png',
          sizes: '512x512',
          type: 'image/png',
          purpose: 'any maskable',
        },
      ],
    },

    workbox: {
      // REMOVE THIS LINE: strategy: 'generateSW', // <--- REMOVED FROM HERE
      globPatterns: ['**/*.{js,css,html,png,svg,ico,json}'],

      runtimeCaching: [
        {
          urlPattern: /^https:\/\/fonts\.googleapis\.com\/.*/i,
          handler: 'CacheFirst',
          options: {
            cacheName: 'google-fonts-cache',
            expiration: {
              maxEntries: 10,
              maxAgeSeconds: 60 * 60 * 24 * 365,
            },
            cacheableResponse: {
              statuses: [0, 200],
            },
          },
        },
        {
          urlPattern: /^https:\/\/fonts\.gstatic\.com\/.*/i,
          handler: 'CacheFirst',
          options: {
            cacheName: 'gstatic-fonts-cache',
            expiration: {
              maxEntries: 10,
              maxAgeSeconds: 60 * 60 * 24 * 365,
            },
            cacheableResponse: {
              statuses: [0, 200],
            },
          },
        },
        {
          urlPattern: /^https:\/\/ten-be\.koyeb\.app\/.*/i,
          handler: 'NetworkFirst',
          options: {
            cacheName: 'api-cache',
            expiration: {
              maxEntries: 50,
              maxAgeSeconds: 60 * 60 * 24,
            },
            cacheableResponse: {
              statuses: [0, 200],
            },
          },
        },
      ],
    },

    client: {
      installPrompt: true,
      registerPlugin: true,
    },

    devOptions: {
      enabled: true,
      type: 'module',
    },
  },

  tailwindcss: {
    viewer: false,
    config: {
      content: [
        './components/**/*.{js,vue,ts}',
        './layouts/**/*.vue',
        './pages/**/*.vue',
        './plugins/**/*.{js,ts}',
        './nuxt.config.{js,ts}',
        './app.vue',
        './app.config.{js,ts}',
        './error.vue',
        './content/**/*.md',
      ],
      theme: {
        extend: {
          colors: {
            'primary-dark': '#222222',
            'primary-green': '#328336',
            'accent-green': '#64cc4f',
            'light-green': '#b2e05b',
            'text-light': '#ffffff',
            'text-secondary': '#5a687a',
            'border-color': '#e5e7eb',
            'card-background': '#ffffff',
            'background': '#fbfbfd',
            'indigo-600': '#4f46e5',
            'blue-600': '#2563eb',
            'purple-600': '#9333ea',
            'orange-600': '#ea580c',
            'emerald-600': '#059669',
            'sky-600': '#0284c7',
            'teal-600': '#0d9488',
            'rose-600': '#e11d48',
          }
        }
      }
    }
  },

  nitro: {
    compatibility: {
      date: '2025-06-27'
    }
  }
})
