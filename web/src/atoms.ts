import { atom } from 'recoil'

interface DataType {
    key?: number
    hwnd: string
    name: string
    level: string
    gold: string
    silver: string
    status: string
    config: string
}

const emptyData: DataType = {
    key: 0,
    hwnd: '',
    name: '',
    level: '',
    gold: '',
    silver: '',
    status: '',
    config: '',
}

const getEmptyData = () => {
    return new Array(5).fill(0).map((_: any, index: number) => {
        return {
            ...emptyData,
            key: index,
            config: index === 0 ? 'daily_leader' : 'daily_user'
        }
    })
}

export const windowsState = atom({
    key: "windowsState",
    default: getEmptyData()
})