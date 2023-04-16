import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/api/game": {
        target: "ws://127.0.0.1:8000",
        rewrite: () => "/game",
        ws: true,
      },

      "/api": {
        target: "http://127.0.0.1:8000",
        rewrite: (path) => path.substring(4),
      },
    },
  },
})
