import { useEffect, useState } from 'react'
import { Row, Input, InputNumber } from 'antd'
import { useUpdateEffect } from 'ahooks'

const getConfig = async () => {
    let config = {}
    const public_config = await window.eel.get_public_config()()
    public_config.forEach(p => {
        const [key, val] = p
        config[key] = val
    })
    return config
}

export default function Log() {
    const [bp, setBp] = useState(0)
    const [gf, setGf] = useState(0)

    useEffect(() => {
        getConfig().then(config => {
            console.log(111, config)
            setBp(prev => Number(config['bp']))
            setGf(prev => Number(config['gf']))
        })
    }, [])

    useUpdateEffect(() => {
        updateConfig()
    }, [bp, gf])

    const updateConfig = () => {
        const config = {
            bp: String(bp),
            gf: String(gf)
        }
        window.eel.set_public_config(config)
    }

    const changeBp = val => {
        setBp(prev => val)
    }

    const changeGf = val => {
        setGf(prev => val)
    }

    return (
        <>
            <Row className="flex flex-row items-center mt-2">
                帮派设置：周{' '}
                <InputNumber className="mx-2" min={1} max={7} value={bp} onChange={changeBp} />{' '}
                做帮派任务
            </Row>
            <Row className="flex flex-row items-center mt-2">
                工坊设置：周{' '}
                <InputNumber className="mx-2" min={1} max={7} value={gf} onChange={changeGf} />{' '}
                做工坊任务
            </Row>
        </>
    )
}
