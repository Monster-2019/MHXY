import { useState } from 'react'
import { Outlet } from 'react-router-dom'

import Slider from './components/Slider'

export default function Root() {
    const [count, setCount] = useState(0)
    const list = [
        { label: '仪表盘', path: '/' },
        { label: '自动登录配置', path: '/autologin' },
        { label: '自定义任务', path: '/custom_task' },
        { label: '通用配置', path: '/public' },
        { label: '其他配置', path: '/config' },
        { label: '日志', path: '/log' }
    ]

    return (
        <div className="flex flex-row h-screen w-full box-border">
            <Slider className="w-40 w-fi box-border flex-shrink-0" list={list} />
            <div className="p-6 flex-1 box-border">
                <Outlet />
            </div>
        </div>
    )
}
