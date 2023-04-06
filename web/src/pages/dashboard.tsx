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

const configs = [
    { value: 'daily_single', label: '单人日常' },
    { value: 'daily_leader', label: '日常队长' },
    { value: 'daily_user', label: '日常队友' },
    { value: 'daily_custom', label: '自定义' }
]

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
                <Select defaultValue={record.config} style={{ width: 100 }} options={configs} />
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
        window.eel.expose(updateLog, 'updateLog')
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

    const updateLog = (hwnd, status) => {
        const finishUpdate = () => {
            setData(prevData => {
                const updateData = prevData.map(row => {
                    if (row.hwnd == hwnd) {
                        return {
                            ...row,
                            status
                        }
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

    const getGroupConfig = () => {
        let groupConfig = selectedRowKeys.map(i => hwnds[i])
        groupConfig = groupConfig.map(hwnd => {
            const { config } = data.find(item => item.hwnd === hwnd)
            return { hwnd, config }
        })
        return groupConfig
    }

    const handleSelected = (selectedRowKeys: React.Key[]) => {
        setSelectedRowKeys(selectedRowKeys)
    }

    const updateWindows = async (val: number[]) => {
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
        setData(prev => [...result])
        setSelectedRowKeys(prev => result.filter(item => item.hwnd).map((_, i) => i))
    }

    const handleConfig = (value, index) => {
        setData(prev => {
            const newData = prev.map((row, i) => {
                if (index === i) {
                    return {
                        ...row,
                        config: value
                    }
                }
                return row
            })
            return newData
        })
    }

    const start = () => {
        const groupConfig = getGroupConfig()
        window.eel.start(groupConfig)
    }

    const stop = () => {
        const selectHnwds = selectedRowKeys.map(i => hwnds[i])
        window.eel.stopAll(selectHnwds)
    }

    const stopAll = () => {
        window.eel.stopAll(hwnds)
    }

    const oneKey = () => {
        const groupConfig = data.map(row => {
            return row?.config
        })
        console.log(groupConfig);
        window.eel.onekey(groupConfig)
    }

    const rowSelection: any = {
        onChange: handleSelected,
        selectedRowKeys
    }

    return (
        <>
            <Table
                columns={columns.map(col => {
                    if (col.key == 'config') {
                        return {
                            ...col,
                            render: (_, record, index) => (
                                <>
                                    <Select
                                        defaultValue={record.config}
                                        style={{ width: 100 }}
                                        options={configs}
                                        onChange={value => handleConfig(value, index)}
                                    />
                                </>
                            )
                        }
                    }
                    return col
                })}
                // columns={columns}
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
                <Button className="mr-4" onClick={() => updateWindows()}>
                    刷新窗口
                </Button>
                <Button className="mr-4" onClick={oneKey}>
                    一键
                </Button>
                <Button className="mr-4" onClick={start}>
                    启动
                </Button>
                {/* <Button className="mr-4" onClick={stop}>
                    停止
                </Button> */}
                <Button className="mr-4" onClick={stopAll}>
                    终止
                </Button>
            </div>
        </>
    )
}

export default Dashboard
