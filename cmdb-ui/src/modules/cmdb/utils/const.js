import i18n from '@/lang'

export const valueTypeMap = () => {
  return {
    '0': i18n.t('cmdb.ciType.int'),
    '1': i18n.t('cmdb.ciType.float'),
    '2': i18n.t('cmdb.ciType.text'),
    '3': i18n.t('cmdb.ciType.datetime'),
    '4': i18n.t('cmdb.ciType.date'),
    '5': i18n.t('cmdb.ciType.time'),
    '6': 'JSON',
    '7': i18n.t('cmdb.ciType.password'),
    '8': i18n.t('cmdb.ciType.link')
  }
}

export const defautValueColor = [
  { value: '#d9d9d9' },
  { value: '#ffccc7' },
  { value: '#ffd8bf' },
  { value: '#ffe7ba' },
  { value: '#fff1b8' },
  { value: '#f4ffb8' },
  { value: '#d9f7be' },
  { value: '#b5f5ec' },
  { value: '#bae7ff' },
  { value: '#d6e4ff' },
  { value: '#efdbff' },
  { value: '#ffd6e7' },
]

export const defaultBGColors = ['#ffccc7', '#ffd8bf', '#ffe7ba', '#fff1b8', '#d9f7be', '#b5f5ec', '#bae7ff', '#d6e4ff', '#efdbff', '#ffd6e7']
