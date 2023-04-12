import React, { Suspense } from 'react'
import ReactDOM from 'react-dom/client'
import './index.css'
import 'antd/dist/reset.css'
import { BrowserRouter as Router, useRoutes } from 'react-router-dom'
import { RecoilRoot } from 'recoil'

import router from './router'

const App = () => {
    const element = useRoutes(router)
    return element
}

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
    // <React.StrictMode>
    <RecoilRoot>
        <Suspense>
            <Router basename={import.meta.env.PROD ? '/index.html' : '/'}>
                <App />
            </Router>
        </Suspense>
    </RecoilRoot>
    // </React.StrictMode>
)
