import i18n from '@/lang'

export const ruleTypeList = [
    { value: '&', label: i18n.t('cs.components.and') },
    { value: '|', label: i18n.t('cs.components.or') },
    // { value: 'not', label: '非' },
]

export const expList = [
    { value: 1, label: i18n.t('cs.components.equal') },
    { value: 2, label: i18n.t('cs.components.notEqual') },
    // { value: 'contain', label: '包含' },
    // { value: '~contain', label: '不包含' },
    // { value: 'start_with', label: '以...开始' },
    // { value: '~start_with', label: '不以...开始' },
    // { value: 'end_with', label: '以...结束' },
    // { value: '~end_with', label: '不以...结束' },
    { value: 7, label: i18n.t('cs.components.isEmpty') }, // 为空的定义有点绕
    { value: 8, label: i18n.t('cs.components.isNotEmpty') },
]

export const advancedExpList = [
    // { value: 'in', label: 'in查询' },
    // { value: '~in', label: '非in查询' },
    // { value: 'range', label: '范围' },
    // { value: '~range', label: '范围外' },
    { value: 'compare', label: i18n.t('cs.components.compare') },
]

export const compareTypeList = [
    { value: 5, label: i18n.t('cs.components.moreThan') },
    // { value: '2', label: '>=' },
    { value: 6, label: i18n.t('cs.components.lessThan') },
    // { value: '4', label: '<=' },
]
