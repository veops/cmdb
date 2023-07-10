export const ruleTypeList = [
    { value: '&', label: '与' },
    { value: '|', label: '或' },
    // { value: 'not', label: '非' },
]

export const expList = [
    { value: 1, label: '等于' },
    { value: 2, label: '不等于' },
    // { value: 'contain', label: '包含' },
    // { value: '~contain', label: '不包含' },
    // { value: 'start_with', label: '以...开始' },
    // { value: '~start_with', label: '不以...开始' },
    // { value: 'end_with', label: '以...结束' },
    // { value: '~end_with', label: '不以...结束' },
    { value: 7, label: '为空' }, // 为空的定义有点绕
    { value: 8, label: '不为空' },
]

export const advancedExpList = [
    // { value: 'in', label: 'in查询' },
    // { value: '~in', label: '非in查询' },
    // { value: 'range', label: '范围' },
    // { value: '~range', label: '范围外' },
    { value: 'compare', label: '比较' },
]

export const compareTypeList = [
    { value: 5, label: '大于' },
    // { value: '2', label: '>=' },
    { value: 6, label: '小于' },
    // { value: '4', label: '<=' },
]
