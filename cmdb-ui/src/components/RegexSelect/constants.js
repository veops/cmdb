/* eslint-disable no-useless-escape */

import i18n from '@/lang'
export const regList = () => {
    return [
        { id: 'letter', label: i18n.t('regexSelect.letter'), value: '^[A-Za-z]+$', message: '请输入字母' },
        { id: 'number', label: i18n.t('regexSelect.number'), value: '^-?(?!0\\d+)\\d+(\\.\\d+)?$', message: '请输入数字' },
        { id: 'letterAndNumber', label: i18n.t('regexSelect.letterAndNumber'), value: '^[A-Za-z0-9.]+$', message: '请输入字母和数字' },
        { id: 'phone', label: i18n.t('regexSelect.phone'), value: '^1[3-9]\\d{9}$', message: '请输入正确手机号码' },
        { id: 'landline', label: i18n.t('regexSelect.landline'), value: '^(?:(?:\\d{3}-)?\\d{8}|^(?:\\d{4}-)?\\d{7,8})(?:-\\d+)?$', message: '请输入正确座机' },
        { id: 'zipCode', label: i18n.t('regexSelect.zipCode'), value: '^(0[1-7]|1[0-356]|2[0-7]|3[0-6]|4[0-7]|5[1-7]|6[1-7]|7[0-5]|8[013-6])\\d{4}$', message: '请输入正确邮政编码' },
        { id: 'IDCard', label: i18n.t('regexSelect.IDCard'), value: '(^[1-9]\\d{5}(18|19|([23]\\d))\\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\\d{3}[0-9Xx]$)|(^[1-9]\\d{5}\\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\\d{3}$)', message: '请输入正确身份证号' },
        { id: 'ip', label: i18n.t('regexSelect.ip'), value: '^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', message: '请输入正确IP地址' },
        { id: 'email', label: i18n.t('regexSelect.email'), value: '^\\w+([-+.]\\w+)*@\\w+([-.]\\w+)*\.\\w+([-.]\\w+)*$', message: '请输入正确邮箱' },
        { id: 'link', label: i18n.t('regexSelect.link'), value: '^(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z0-9]{2,}(\.[a-zA-Z0-9]{2,})(\.[a-zA-Z0-9]{2,})?$', message: '请输入链接' },
        { id: 'monetaryAmount', label: i18n.t('regexSelect.monetaryAmount'), value: '^-?\\d+(,\\d{3})*(\.\\d{1,2})?$', message: '请输入货币金额' },
        { id: 'custom', label: i18n.t('regexSelect.custom'), value: '', message: '' }
    ]
}
