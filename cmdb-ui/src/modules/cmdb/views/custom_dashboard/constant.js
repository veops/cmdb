import i18n from '@/lang'

export const dashboardCategory = () => {
    return {
        1: { label: i18n.t('cmdb.custom_dashboard.default') },
        2: { label: i18n.t('cmdb.custom_dashboard.relation') }
    }
}
