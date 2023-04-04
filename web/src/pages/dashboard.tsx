import React, { useEffect, useState, useMemo, useRef } from 'react'
import { Space, Table, Tag, Button, Select } from 'antd'
import type { ColumnsType } from 'antd/es/table'
import { useRecoilState } from 'recoil'
import { windowsState } from '../atoms'

interface DataType {
    key: number
    hwnd: string
    name: string
    level: string
    gold: string
    silver: string
    status: string
    config: string
    action?: any
}

const handleChange = (value: string, index: number) => {
    console.log(value, index)
}

const columns: ColumnsType<DataType> = [
    {
        title: '句柄',
        dataIndex: 'hwnd',
        key: 'hwnd',
        width: 80
    },
    {
        title: '名称',
        dataIndex: 'name',
        key: 'name',
        width: 120
    },
    {
        title: '等级',
        dataIndex: 'level',
        key: 'level',
        width: 50
    },
    {
        title: '金币',
        dataIndex: 'gold',
        key: 'gold',
        width: 100
    },
    {
        title: '银币',
        dataIndex: 'silver',
        key: 'silver',
        width: 100
    },
    {
        title: '状态',
        dataIndex: 'status',
        key: 'status'
    },
    {
        title: '配置',
        dataIndex: 'config',
        key: 'config',
        width: 100,
        render: (_, record, index) => (
            <>
                <Select
                    defaultValue={record.config}
                    style={{ width: 100 }}
                    onChange={value => handleChange(value, index)}
                    options={[
                        { value: 'single_daily', label: '单人日常' },
                        { value: 'daily_leader', label: '日常队长' },
                        { value: 'daily_user', label: '日常队友' },
                        { value: 'custom', label: '自定义' }
                    ]}
                />
            </>
        )
    },
    {
        title: '操作',
        dataIndex: 'tags',
        key: 'tags',
        width: 100,
        render: () => (
            <>
                <Button size="small">置顶</Button>
            </>
        )
    }
]

// {
//     key: 3,
//     hwnd: 1231313,
//     name: 'Monster1',
//     level: 69,
//     gold: '10000',
//     silver: '10000',
//     status: '宝图任务中',
//     config: 'test',
//     group: '1'
// }

let isUpdating = false

const Dashboard: React.FC = () => {
    const [data, setData] = useRecoilState(windowsState)
    const [selectedRowKeys, setSelectedRowKeys] = useState<React.Key[]>(
        data.filter((t: any) => t.hwnd).map((_, i) => i)
    )
    const [hwnds, setHwnds] = useState<string[]>([])
    const dataRef = useRef(null)

    useEffect(() => {
        window.eel.expose(updateInfo, 'updateInfo')
        window.eel.expose(updateState, 'updateState')
        window.eel.expose(updateWindows, 'updateWindows')
    }, [])

    useEffect(() => {
        dataRef.current = data
        setHwnds(data.map(t => t.hwnd).filter(t => t))
        setData(data)
    }, [data])

    const updateInfo = val => {
        setData(prevData => {
            const updateData = prevData.map(row => {
                if (row.hwnd == val.hwnd) {
                    return { ...row, ...val }
                }
                return row
            })
            return updateData
        })
    }

    const updateState = val => {
        // console.log(hwnd, status)
        const finishUpdate = () => {
            setData(prevData => {
                const updateData = prevData.map(row => {
                    if (row.hwnd == val.hwnd) {
                        return { ...row, ...val }
                    }
                    return row
                })
                return updateData
            })
            isUpdating = false
        }

        if (isUpdating) {
            setTimeout(() => {
                updateState(val)
            }, 0)
        } else {
            isUpdating = true
            finishUpdate()
        }
    }

    const updateWindows = val => {
        handleUpdateWindow(val)
    }

    const handleSelected = (selectedRowKeys: React.Key[]) => {
        setSelectedRowKeys(selectedRowKeys)
    }

    const rowSelection: any = {
        onChange: handleSelected,
        selectedRowKeys
    }

    const handleUpdateWindow = async (val: number[]) => {
        let res
        if (!val) {
            res = await window.eel.get_hwnd_list()()
        } else {
            res = val
        }
        const result = data.map((item, index) => {
            if (res[index]) {
                return {
                    ...item,
                    hwnd: res[index]
                }
            } else {
                return item
            }
        })
        setData(list => [...result])
        setSelectedRowKeys(result.filter(item => item.hwnd).map((_, i) => i))
    }

    const handleStart = () => {
        const selectHnwds = selectedRowKeys.map(i => hwnds[i])
        window.eel.start(selectHnwds)
    }

    const handleStop = () => {
        const selectHnwds = selectedRowKeys.map(i => hwnds[i])
        window.eel.stopAll(selectHnwds)
    }

    const handleStopAll = () => {
        window.eel.stopAll(hwnds)
    }

    const handleOnekey = () => {
        window.eel.onekey()
    }

    return (
        <>
            <Table
                columns={columns}
                rowSelection={{
                    type: 'checkbox',
                    ...rowSelection
                }}
                pagination={false}
                bordered={true}
                dataSource={data}
                size={'small'}
            />
            <div className="my-4">
                <Button className="mr-4" onClick={() => handleUpdateWindow()}>
                    刷新窗口
                </Button>
                <Button className="mr-4" onClick={handleOnekey}>
                    一键
                </Button>
                <Button className="mr-4" onClick={handleStart}>
                    启动
                </Button>
                <Button className="mr-4" onClick={handleStop}>
                    停止
                </Button>
                <Button className="mr-4" onClick={handleStopAll}>
                    终止
                </Button>
            </div>
        </>
    )
}

export default Dashboard
