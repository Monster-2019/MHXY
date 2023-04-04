import { useEffect, useState } from 'react'
import { Input, Space, Button } from 'antd'
import { useUpdateEffect } from 'ahooks'
import { useRecoilValue } from 'recoil'
import { windowsState } from '../atoms'

const getPath = async () => {
    let softwarePath = {}
    const path = await window.eel.get_software_path()()
    path.forEach(p => {
        const [key, val] = p
        softwarePath[key] = val
    })
    return softwarePath
}

export default function Config() {
    const [tesseract_ocr, set_tesseract_ocr] = useState('')
    const [ssk, set_ssk] = useState('')

    const windows = useRecoilValue(windowsState)

    useEffect(() => {
        getPath().then(path => {
            if (path.tesseract_ocr) set_tesseract_ocr(path.tesseract_ocr)
            if (path.ssk) set_ssk(path.ssk)
        })
    }, [])

    const selectFile = async func => {
        const res = await window.eel.set_software_file()()
        func(res)
    }

    const updatePath = () => {
        const path = {
            tesseract_ocr,
            ssk
        }
        eel.set_software_path(path)
    }

    useUpdateEffect(() => {
        updatePath()
    }, [tesseract_ocr, ssk])

    return (
        <>
            <div className="mb-4">
                <label>Tesseract目录</label>
                <Space.Compact className="w-1/2 mx-2">
                    <Input value={tesseract_ocr} />
                </Space.Compact>
                <Button onClick={e => selectFile(set_tesseract_ocr)}>选择目录</Button>
            </div>
            <div className="mb-4">
                <label>SSK目录</label>
                <Space.Compact className="w-1/2 mx-2">
                    <Input value={ssk} />
                </Space.Compact>
                <Button onClick={e => selectFile(set_ssk)}>选择目录</Button>
            </div>
        </>
    )
}
