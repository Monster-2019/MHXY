import { lazy } from 'react'

const Root = lazy(() => import('./Root'))
const Dashboard = lazy(() => import('./pages/dashboard'))
const Config = lazy(() => import('./pages/config'))
const CustomTask = lazy(() => import('./pages/customtask'))
const AutoLogin = lazy(() => import('./pages/autologin'))
const Log = lazy(() => import('./pages/log'))

const router = [
    {
        path: '/',
        element: <Root />,
        children: [
            {
                index: true,
                element: <Dashboard />
            },
            {
                path: '/autologin',
                element: <AutoLogin />
            },
            {
                path: '/config',
                element: <Config />
            },
            {
                path: '/custom_task',
                element: <CustomTask />
            },
            {
                path: '/log',
                element: <Log />
            }
        ]
    }
]

export default router
