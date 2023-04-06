import { useEffect, useState } from 'react'

export default function Log() {
    const [log, setLog] = useState('')

    const initLog = async () => {
        const logs = await window.eel.get_all_log()()
        updateAllLog(logs)
    }
    const updateAllLog = fileLog => {
        console.log(typeof fileLog, fileLog)
        const newLog = fileLog.replace(/\n/g, '<br />')
        setLog(prev => `<p className='leading-4'>${newLog}</p>`)
        const el = document.querySelector('.container')
        el.scrollTop = el.scrollHeight
    }

    useEffect(() => {
        initLog()
        window.eel.expose(updateAllLog, 'updateAllLog')
    }, [])

    return (
        <>
            <div
                dangerouslySetInnerHTML={{ __html: log }}
                className="container border-2 overflow-y-auto h-full max-h-full p-2"
            />
        </>
    )
}
