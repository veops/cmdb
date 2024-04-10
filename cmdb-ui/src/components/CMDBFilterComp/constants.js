import i18n from '@/lang'

export const ruleTypeList = () => {
    return [
        { value: 'and', label: i18n.t('cmdbFilterComp.and') },
        { value: 'or', label: i18n.t('cmdbFilterComp.or') },
        // { value: 'not', label: '非' },
    ]
}

export const expList = () => {
    return [
        { value: 'is', label: i18n.t('cmdbFilterComp.is') },
        { value: '~is', label: i18n.t('cmdbFilterComp.~is') },
        { value: 'contain', label: i18n.t('cmdbFilterComp.contain') },
        { value: '~contain', label: i18n.t('cmdbFilterComp.~contain') },
        { value: 'start_with', label: i18n.t('cmdbFilterComp.start_with') },
        { value: '~start_with', label: i18n.t('cmdbFilterComp.~start_with') },
        { value: 'end_with', label: i18n.t('cmdbFilterComp.end_with') },
        { value: '~end_with', label: i18n.t('cmdbFilterComp.~end_with') },
        { value: '~value', label: i18n.t('cmdbFilterComp.~value') }, // 为空的定义有点绕
        { value: 'value', label: i18n.t('cmdbFilterComp.value') },
    ]
}

export const advancedExpList = () => {
    return [
        { value: 'in', label: i18n.t('cmdbFilterComp.in') },
        { value: '~in', label: i18n.t('cmdbFilterComp.~in') },
        { value: 'range', label: i18n.t('cmdbFilterComp.range') },
        { value: '~range', label: i18n.t('cmdbFilterComp.~range') },
        { value: 'compare', label: i18n.t('cmdbFilterComp.compare') },
    ]
}

export const compareTypeList = [
    { value: '1', label: '>' },
    { value: '2', label: '>=' },
    { value: '3', label: '<' },
    { value: '4', label: '<=' },
]
