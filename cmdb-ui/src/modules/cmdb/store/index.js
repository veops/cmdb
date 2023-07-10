const cmdbStore = {
    namespaced: true,
    name: 'cmdbStore',
    state: {
        isTableLoading: false,
    },
    actions: {
    },
    mutations: {
        SET_IS_TABLE_LOADING(state, payload) {
            state.isTableLoading = payload
        },
    },
}

export default cmdbStore
