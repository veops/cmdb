/* eslint-disable */
import _ from 'lodash'
export function sum(arr) {
    if (!arr.length) {
        return 0
    }
    return arr.reduce(function (prev, curr, idx, arr) {
        return prev + curr
    })
}

const strLength = (fData) => {

    if (!fData) {
        return 0
    }
    if (fData.length && typeof fData === 'object') {
        fData = fData.join(' ')
    }
    let intLength = 0
    for (let i = 0; i < fData.length; i++) {
        if ((fData.charCodeAt(i) < 0) || (fData.charCodeAt(i) > 255)) {
            intLength = intLength + 2
        }
        else {
            intLength = intLength + 1
        }

    }
    return Math.floor(intLength * 7)
}

String.prototype.pxWidth = function (font) {
    // re-use canvas object for better performance
    const canvas = String.prototype.pxWidth.canvas || (String.prototype.pxWidth.canvas = document.createElement("canvas")),
        context = canvas.getContext("2d");

    font && (context.font = font);
    const metrics = context.measureText(this);

    return metrics.width;
}

export function getCITableColumns(data, attrList, width = 1600, height) {
    // 计算出来 主table的列表 布局属性

    const _attrList = _.orderBy(attrList, ['is_fixed'], ['desc'])
    const columns = []
    for (let attr of _attrList) {

        const editRender = { name: 'input' }
        switch (attr.value_type) {
            case '0':
                editRender['props'] = { 'type': 'float' }
                break
            case '1':
                editRender['props'] = { 'type': 'float' }
                break
            case '2':
                editRender['attrs'] = { 'type': 'text' }
                break
            case '3':
                editRender['props'] = { 'type': 'datetime' }
                break
            case "4":
                editRender['props'] = { 'type': 'date' }
                break
            case '5':
                editRender['props'] = { 'type': 'time' }
                break
            case '6':
                editRender['props'] = { 'type': 'text' }
                break
            default:
                editRender['props'] = { 'type': 'text' }
                break
        }

        if (attr.is_choice) {
            editRender.name = '$select'
            editRender.options = attr.choice_value ? attr.choice_value.map(item => { return { label: item, value: item } }) : []
            delete editRender.props

        }
        columns.push({
            editRender,
            title: attr.alias || attr.name,
            field: attr.name,
            value_type: attr.value_type,
            sortable: !!attr.is_sortable,
            filters: attr.is_choice ? attr.choice_value : null,
            width: Math.min(Math.max(100, ...data.map(item => strLength(item[attr.name]))), 350),
            is_link: attr.is_link,
            is_password: attr.is_password,
            is_list: attr.is_list,
            is_choice: attr.is_choice,
            is_fixed: attr.is_fixed,
        })
    }

    const totalWidth = sum(columns.map(col => col.width))
    if (totalWidth < width) {
        columns.map(item => {
            // if (item.width === 100) {
            delete item.width
            // }
        })
    }
    return columns
}

export const getPropertyStyle = (attr) => {
    switch (attr.value_type) {
        case '0':
            return { color: '#cf1322', backgroundColor: '#fff1f0' }
        case '1':
            return { color: '#d4b106', backgroundColor: '#feffe6' }
        case '2':
            return { color: '#d46b08', backgroundColor: '#fff7e6' }
        case '3':
            return { color: '#531dab', backgroundColor: '#f9f0ff' }
        case '4':
            return { color: '#389e0d', backgroundColor: '#f6ffed' }
        case '5':
            return { color: '#08979c', backgroundColor: '#e6fffb' }
        case '6':
            return { color: '#c41d7f', backgroundColor: '#fff0f6' }
    }
}

export const getLastLayout = (data, x1 = 0, y1 = 0, w1 = 0) => {
    const _tempData = _.orderBy(data, ['y', 'x'], ['asc', 'asc'])
    if (!_tempData.length) {
        return { xLast: 0, yLast: 0, wLast: 0 }
    }
    const { x, y, w } = _tempData[_tempData.length - 1]
    if (y < y1) {
        return { xLast: x1, yLast: y1, wLast: w1 }
    } else if (y > y1) {
        return { xLast: x, yLast: y, wLast: w }
    } else {
        const xLast = _.max([x, x1])
        return { xLast, yLast: y, wLast: xLast === x ? w : w1 }
    }
}

// 数字加逗号
export const toThousands = (num = 0) => {
    return num.toString().replace(/\d+/, function (n) {
        return n.replace(/(\d)(?=(?:\d{3})+$)/g, '$1,')
    })
}