import i18n from '@/lang'

export const permMap = () => {
    return {
        read: i18n.t('view'),
        add: i18n.t('new'),
        create: i18n.t('new'),
        update: i18n.t('update'),
        delete: i18n.t('delete'),
        config: i18n.t('cmdb.components.config'),
        grant: i18n.t('grant'),
        'read_attr': i18n.t('cmdb.components.readAttribute'),
        'read_ci': i18n.t('cmdb.components.readCI')
    }
}
