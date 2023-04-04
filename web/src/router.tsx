import { lazy } from 'react'

const Root = lazy(() => import('./Root'))
const Dashboard = lazy(() => import('./pages/dashboard'))
const Config = lazy(() => import('./pages/config'))
const CustomTask = lazy(() => import('./pages/customtask'))

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
                path: '/config',
                element: <Config />
            },
            {
                path: '/custom_task',
                element: <CustomTask />
            }
        ]
    }
]

export default router
