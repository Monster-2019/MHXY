import { useEffect, useState } from 'react'
import { Collapse, Button, Input, Row, Col, Form } from 'antd'
import { DeleteOutlined } from '@ant-design/icons'

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

    useEffect(() => {
        getAutoLoginJson().then(autoLoginJson => {
            autoLoginJson = JSON.parse(autoLoginJson)
            const { accounts } = autoLoginJson
            if (accounts.length === 0) {
                accounts.push(generateGroup())
            }
            setJson(accounts)
            handleSaveJson(accounts)
        })
    }, [])

    const handleSaveJson = async val => {
        const data = {
            accounts: val || json
        }
        await window.eel.set_auto_login_json(data)
    }

    const handleResetJson = () => {
        const newData = [generateGroup()]
        setJson(newData)
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

    const genExtra = groupIndex => (
        <DeleteOutlined
            onClick={event => {
                alert(groupIndex)
                setJson(prevJson => {
                    const newJson = prevJson.filter((_, i) => {
                        return !(i === groupIndex)
                    })
                    return newJson
                })
            }}
        />
    )

    return (
        <>
            <Collapse size="small" className="mb-4" accordion>
                {json.map((group, groupIndex) => {
                    return (
                        <Panel
                            header={`第${groupIndex + 1}组`}
                            key={"group" + groupIndex}
                            extra={genExtra(groupIndex)}
                        >
                            <Row gutter={16} key={'group' + group}>
                                {group.map((user, i) => {
                                    return (
                                        <>
                                            <Col span={12} className="mb-2" key={'a' + i}>
                                                <Input
                                                    value={json[groupIndex][i].account}
                                                    placeholder="账号"
                                                    onChange={e =>
                                                        handleChange(e, groupIndex, i, 'account')
                                                    }
                                                />
                                            </Col>
                                            <Col span={12} className="mb-2" key={'s' + i}>
                                                <Input
                                                    value={json[groupIndex][i].server}
                                                    placeholder="服务器"
                                                    onChange={e =>
                                                        handleChange(e, groupIndex, i, 'server')
                                                    }
                                                />
                                            </Col>
                                        </>
                                    )
                                })}
                            </Row>
                        </Panel>
                    )
                })}
            </Collapse>
            <Button onClick={e => handleSaveJson()} className="mr-2">
                保存
            </Button>
            <Button onClick={handleResetJson} className="mr-2">重置</Button>
            <Button onClick={handleAdd}>添加一组</Button>
        </>
    )
}
