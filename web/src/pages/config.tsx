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
    const [leidian, set_leidian] = useState('')
    const [shared_folder, set_shared_folder] = useState('')
    const [tesseract_ocr, set_tesseract_ocr] = useState('')
    const [ssk, set_ssk] = useState('')

    const windows = useRecoilValue(windowsState)

    useEffect(() => {
        getPath().then(path => {
            if (path.leidian) set_leidian(path.leidian)
            if (path.shared_folder) set_shared_folder(path.shared_folder)
            if (path.tesseract_ocr) set_tesseract_ocr(path.tesseract_ocr)
            if (path.ssk) set_ssk(path.ssk)
        })
    }, [])

    const selectFolder = async func => {
        const res = await window.eel.set_software_dir()()
        func(res)
    }

    const selectFile = async func => {
        const res = await window.eel.set_software_file()()
        func(res)
    }

    const updatePath = () => {
        const path = {
            leidian,
            shared_folder,
            tesseract_ocr,
            ssk
        }
        console.log(path)
        eel.set_software_path(path)
    }

    useUpdateEffect(() => {
        updatePath()
    }, [leidian, shared_folder, tesseract_ocr, ssk])

    return (
        <>
            <div className="mb-4">
                <label>雷电模拟器</label>
                <Space.Compact className="w-1/2 mx-2">
                    <Input value={leidian} />
                </Space.Compact>
                <Button onClick={e => selectFile(set_leidian)}>选择目录</Button>
            </div>
            <div className="mb-4">
                <label>模拟器共享目录</label>
                <Space.Compact className="w-1/2 mx-2">
                    <Input value={shared_folder} />
                </Space.Compact>
                <Button onClick={e => selectFolder(set_shared_folder)}>选择目录</Button>
            </div>
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
