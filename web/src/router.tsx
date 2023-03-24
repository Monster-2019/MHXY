import Root from './Root'
import Dashboard from './pages/dashboard'
import Config from './pages/config'
import CustomTask from './pages/customtask'

const router = [
    {
        path: '/',
        element: <Root />,
        children: [
            {
                index: true,
                path: '/',
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