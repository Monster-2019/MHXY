import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { createHtmlPlugin } from 'vite-plugin-html'
import { visualizer } from 'rollup-plugin-visualizer'

// https://vitejs.dev/config/
export default defineConfig({
    base: './',
    // server: {
    //     host: '0.0.0.0',
    //     port: 6000
    // },
    build: {
        watch: {
            exclude: 'node_modules/**',
            include: 'src/**'
        }
    },
    plugins: [
        react(),
        createHtmlPlugin({
            minify: true,
            /**
             * 需要注入 index.html ejs 模版的数据
             */
            inject: {
                data: {
                    title: 'index',
                    injectScript:
                        process.env.NODE_ENV === 'production'
                            ? `<script src="/eel.js"></script>`
                            : `<script src="http://localhost:9000/eel.js"></script><script>eel.set_host('ws://localhost:9000')</script>`
                }
            }
        }),
        // visualizer()
    ]
})
