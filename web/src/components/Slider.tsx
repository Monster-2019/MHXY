import { useState } from 'react'
import { Link, NavLink } from 'react-router-dom'
import PropTypes from 'prop-types'

export default function Slider({ list, className }: any) {
    const [tab, setTabs] = useState('dashboard')

    return (
        <ul className={`bg-gray-200 mb-0 ${className}`}>
            {list.map((item: { label: string; path: string }) => {
                return (
                    <li className="w-full text-center rounded text-black" key={item.path}>
                        <NavLink
                            to={item.path}
                            className={({ isActive, isPending }) =>
                                `block w-100 h-100 py-3 bg-gray-200 ${
                                    isActive ? 'active bg-white' : ''
                                }`
                            }
                        >
                            {item.label}
                        </NavLink>
                    </li>
                )
            })}
        </ul>
    )
}

Slider.prototype = {
    list: PropTypes.array,
    className: PropTypes.string
}
