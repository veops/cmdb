const notice = {
    state: {
        totalUnreadNum: 0,
        appUnreadNum: []
    },
    mutations: {
        SET_TOTAL_UNREAD_NUM: (state, totalUnreadNum) => {
            state.totalUnreadNum = totalUnreadNum
        },
        SET_APP_UNREAD_NUM: (state, appUnreadNum) => {
            state.appUnreadNum = appUnreadNum
        },
    },
    actions: {
    }
}
export default notice
