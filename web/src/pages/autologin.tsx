import React, { useEffect, useState } from 'react'
import { Collapse, Button, Input, Row, Col, Form, App } from 'antd'
import { DeleteOutlined, EditOutlined } from '@ant-design/icons'

const { Panel } = Collapse

const getAutoLoginJson = async () => {
    const json = await window.eel.get_auto_login_json()()
    return json
}

const generateGroup = () => {
    return new Array(5).fill({ account: '', server: '' })
}

export default function AutoLogin() {
    const [json, setJson] = useState([])
    const { message } = App.useApp()

    useEffect(() => {
        getAutoLoginJson().then(autoLoginJson => {
            autoLoginJson = JSON.parse(autoLoginJson)
            const { accounts } = autoLoginJson
            if (accounts.length === 0) {
                accounts.push(generateGroup())
            }
            setJson(accounts)
            // handleSaveJson(accounts)
        })
    }, [])

    const handleSaveJson = async val => {
        const data = {
            accounts: val || json
        }
        await window.eel.set_auto_login_json(data)
        message.success("账号配置已保存")
    }

    const handleResetJson = () => {
        const newData = [generateGroup()]
        setJson(newData)
        message.success("账号配置已重置")
        handleSaveJson(newData)
    }

    const handleChange = (e, group, i, field) => {
        const value = e.target.value
        setJson(prevJson => {
            const newJson = prevJson.map((groupData, groupIndex) => {
                if (groupIndex == group) {
                    const newGroup = groupData.map((row, index) => {
                        if (index == i) {
                            return { ...row, [`${field}`]: value }
                        }
                        return row
                    })
                    return newGroup
                }
                return groupData
            })
            return newJson
        })
    }

    const handleAdd = () => {
        setJson(prev => [...prev, generateGroup()])
    }

    const autoGroup = (groupIndex: number, e: Event) => {
        e.stopPropagation()
        const { account, server } = json[groupIndex][0]
        const reg = /^\w*(\d{1,2})\w*$/
        if (!account || !server) {
            message.error('账号1未填写完整')
            return
        }
        if (!reg.test(account)) {
            message.error('账号1中没有数字，无法自动填充')
            return
        }
        const index = Number(reg.exec(account)[1])
        const newJson = new Array(5).fill({ account, server }).map((row, i) => {
            const { account, server } = row
            console.log(index, i)
            return {
                account: account.replace(index, index + i),
                server: server.replace(index, index + i)
            }
        })
        setJson(prev => {
            const nextJson = prev.map((group, index) => {
                if (index == groupIndex) {
                    return newJson
                }
                return group
            })
            return nextJson
        })
    }

    const delGroup = (groupIndex: number, e: Event) => {
        e.stopPropagation()
        setJson(prevJson => {
            const newJson = prevJson.filter((_, i) => {
                return !(i === groupIndex)
            })
            return newJson
        })
    }

    const genExtra = (groupIndex: number) => (
        <div className="flex flex-row items-center">
            <EditOutlined
                className="mr-2"
                style={{ fontSize: '16px' }}
                onClick={e => autoGroup(groupIndex, e)}
            />
            <DeleteOutlined style={{ fontSize: '16px' }} onClick={e => delGroup(groupIndex, e)} />
        </div>
    )

    return (
        <>
            <Collapse size="small" className="mb-4" accordion>
                {json.map((group, groupIndex) => {
                    return (
                        <Panel
                            header={`第${groupIndex + 1}组`}
                            key={'group' + groupIndex}
                            extra={genExtra(groupIndex)}
                        >
                            {group.map((user, i) => {
                                return (
                                    <Row gutter={16} key={'row' + i}>
                                        <Col span={12} className="mb-2">
                                            <Input
                                                value={json[groupIndex][i].account}
                                                placeholder="账号"
                                                onChange={e =>
                                                    handleChange(e, groupIndex, i, 'account')
                                                }
                                            />
                                        </Col>
                                        <Col span={12} className="mb-2">
                                            <Input
                                                value={json[groupIndex][i].server}
                                                placeholder="服务器"
                                                onChange={e =>
                                                    handleChange(e, groupIndex, i, 'server')
                                                }
                                            />
                                        </Col>
                                    </Row>
                                )
                            })}
                        </Panel>
                    )
                })}
            </Collapse>
            <Button onClick={e => handleSaveJson()} className="mr-2">
                保存
            </Button>
            <Button onClick={handleResetJson} className="mr-2">
                重置
            </Button>
            <Button onClick={handleAdd}>添加一组</Button>
        </>
    )
}
