import React from 'react'
import ReactDOM from 'react-dom/client'
import './index.css'
import 'antd/dist/reset.css'
import { BrowserRouter as Router, useRoutes } from 'react-router-dom'
import { RecoilRoot } from 'recoil'

import Root from './Root'
import Dashboard from './pages/dashboard'
import Config from './pages/config'
import CustomTask from './pages/customtask'

import router from './router'

const App = () => {
    const element = useRoutes(router)
    return element
}

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
    // <React.StrictMode>
    <RecoilRoot>
        <Router basename={import.meta.env.PROD ? '/index.html' : '/'}>
            <App />
        </Router>
    </RecoilRoot>
    // </React.StrictMode>
)
