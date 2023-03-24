import React, { useState } from 'react'
import { Checkbox, Divider, Button } from 'antd'
import type { CheckboxChangeEvent } from 'antd/es/checkbox'
import type { CheckboxValueType } from 'antd/es/checkbox/Group'

const CheckboxGroup = Checkbox.Group

interface Option {
    label: string
    value: string
}

const plainOptions: option[] = [
    { label: '捉鬼', value: 'zg' },
    { label: '二本', value: 'fb' },
    { label: '师门', value: 'sm' },
    { label: '宝图', value: 'bt' },
    { label: '秘境', value: 'mj' },
    { label: '三界', value: 'sj' },
    { label: '科举', value: 'kj' },
    { label: '运镖', value: 'yb' }
]
const defaultCheckedList = []

export default function CustomTask() {
    const [checkedList, setCheckedList] = useState<CheckboxValueType[]>(defaultCheckedList)
    const [indeterminate, setIndeterminate] = useState(!!defaultCheckedList.length)
    const [checkAll, setCheckAll] = useState(false)

    const onChange = (list: CheckboxValueType[]) => {
        setCheckedList(list)
        setIndeterminate(!!list.length && list.length < plainOptions.length)
        setCheckAll(list.length === plainOptions.length)
    }

    const onCheckAllChange = (e: CheckboxChangeEvent) => {
        setCheckedList(e.target.checked ? plainOptions.map((t: option) => t.value) : [])
        setIndeterminate(false)
        setCheckAll(e.target.checked)
    }

    const saveConfig = () => {
        console.log(checkedList)
    }

    const resetConfig = () => {
        setCheckedList([])
        setIndeterminate(false)
        setCheckAll(false)
    }

    return (
        <>
            <Checkbox indeterminate={indeterminate} onChange={onCheckAllChange} checked={checkAll}>
                全选
            </Checkbox>
            <Divider />
            <CheckboxGroup options={plainOptions} value={checkedList} onChange={onChange} />
            <Divider />
            <Button onClick={saveConfig}>保存</Button>
            <Button className="ml-4" onClick={resetConfig}>
                重置
            </Button>
        </>
    )
}
