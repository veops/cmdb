// Import các module ngôn ngữ tiếng Việt
let acl_vi = {}
let chartDemo_vi = {}
let cmdb_vi = {}
let cs_vi = {}

// Thử import các module, nếu không có thì sử dụng object rỗng
try {
  acl_vi = require('@/modules/acl/lang/vi.js').default || {}
} catch (e) {
  console.warn('Module ACL tiếng Việt chưa được tạo đầy đủ')
}

try {
  chartDemo_vi = require('@/modules/chart-demo/lang/vi.js').default || {}
} catch (e) {
  console.warn('Module Chart Demo tiếng Việt chưa được tạo đầy đủ')
}

try {
  cmdb_vi = require('@/modules/cmdb/lang/vi.js').default || {}
} catch (e) {
  console.warn('Module CMDB tiếng Việt chưa được tạo đầy đủ')
}

try {
  cs_vi = require('../views/setting/lang/vi.js').default || {}
} catch (e) {
  console.warn('Module Settings tiếng Việt chưa được tạo đầy đủ')
}

export default {
    commonMenu: {
        permission: 'Quản lý quyền',
        role: 'Quản lý vai trò',
        resource: 'Quản lý tài nguyên',
        resourceType: 'Loại tài nguyên',
        trigger: 'Trình kích hoạt',
    },
    settings: 'Cài đặt chung',
    screen: 'Màn hình lớn',
    dashboard: 'Bảng điều khiển',
    admin: 'Quản trị viên',
    user: 'Người dùng',
    role: 'Vai trò',
    operation: 'Thao tác',
    login: 'Đăng nhập',
    refresh: 'Làm mới',
    cancel: 'Hủy bỏ',
    confirm: 'Xác nhận',
    create: 'Tạo mới',
    edit: 'Chỉnh sửa',
    deleting: 'Đang xóa',
    deletingTip: 'Đang xóa, tổng cộng {total} mục, thành công {successNum} mục, thất bại {errorNum} mục',
    grant: 'Cấp quyền',
    revoke: 'Thu hồi',
    login_at: 'Thời gian đăng nhập',
    logout_at: 'Thời gian đăng xuất',
    createSuccess: 'Tạo thành công',
    editSuccess: 'Chỉnh sửa thành công',
    warning: 'Cảnh báo',
    export: 'Xuất',
    placeholderSearch: 'Vui lòng tìm kiếm',
    success: 'Thành công',
    fail: 'Thất bại',
    browser: 'Trình duyệt',
    status: 'Trạng thái',
    type: 'Loại',
    description: 'Mô tả',
    new: 'Mới',
    add: 'Thêm',
    define: 'Định nghĩa',
    update: 'Cập nhật',
    clear: 'Xóa',
    delete: 'Xóa',
    copy: 'Sao chép',
    created_at: 'Ngày tạo',
    updated_at: 'Ngày cập nhật',
    placeholder1: 'Vui lòng nhập',
    placeholder2: 'Vui lòng chọn',
    confirmDelete: 'Xác nhận xóa?',
    confirmDelete2: 'Xác nhận xóa [{name}]?',
    query: 'Truy vấn',
    search: 'Tìm kiếm',
    hide: 'Ẩn',
    expand: 'Mở rộng',
    save: 'Lưu',
    submit: 'Gửi',
    upload: 'Nhập',
    download: 'Xuất',
    name: 'Tên',
    alias: 'Bí danh',
    desc: 'Mô tả',
    other: 'Khác',
    icon: 'Biểu tượng',
    addSuccess: 'Thêm thành công',
    uploadSuccess: 'Nhập thành công',
    saveSuccess: 'Lưu thành công',
    copySuccess: 'Sao chép thành công',
    updateSuccess: 'Cập nhật thành công',
    deleteSuccess: 'Xóa thành công',
    operateSuccess: 'Thao tác thành công',
    noPermission: 'Không có quyền',
    noData: 'Không có dữ liệu',
    seconds: 'giây',
    createdAt: 'Thời gian tạo',
    updatedAt: 'Thời gian cập nhật',
    deletedAt: 'Thời gian xóa',
    required: 'Bắt buộc',
    email: 'Email',
    wechat: 'WeChat',
    dingding: 'DingTalk',
    feishu: 'Feishu',
    bot: 'Bot',
    checkAll: 'Chọn tất cả',
    loading: 'Đang tải...',
    view: 'Xem',
    reset: 'Đặt lại',
    yes: 'Có',
    no: 'Không',
    all: 'Tất cả',
    selectRows: 'Đã chọn: {rows} mục',
    itemsPerPage: '/trang',
    '星期一': 'Thứ Hai',
    '星期二': 'Thứ Ba',
    '星期三': 'Thứ Tư',
    '星期四': 'Thứ Năm',
    '星期五': 'Thứ Sáu',
    '星期六': 'Thứ Bảy',
    '星期日': 'Chủ Nhật',
    '一月': 'Tháng 1',
    '二月': 'Tháng 2',
    '三月': 'Tháng 3',
    '四月': 'Tháng 4',
    '五月': 'Tháng 5',
    '六月': 'Tháng 6',
    '七月': 'Tháng 7',
    '八月': 'Tháng 8',
    '九月': 'Tháng 9',
    '十月': 'Tháng 10',
    '十一月': 'Tháng 11',
    '十二月': 'Tháng 12',
    tip: 'Thông báo',
    topMenu: {
        personalCenter: 'Hồ sơ cá nhân',
        logout: 'Đăng xuất',
        confirmLogout: 'Bạn có chắc chắn muốn đăng xuất?',
        profile: 'Hồ sơ cá nhân',
        settings: 'Cài đặt',
        language: 'Ngôn ngữ'
    },
    userPanel: {
      myProfile: 'Hồ sơ cá nhân',
      accountPassword: 'Mật khẩu tài khoản',
      notice: 'Thông báo',
      switchLanguage: 'Chuyển đổi ngôn ngữ',
      bindAccount: 'Liên kết tài khoản',
      switchAccount: 'Chuyển đổi tài khoản',
      logout: 'Đăng xuất'
    },
    cs: {
      person: {
        confirmUnbind: 'Bạn có chắc chắn muốn hủy liên kết?',
        unbindSuccess: 'Hủy liên kết thành công',
        bindSuccess: 'Liên kết thành công'
      }
    },
    ...acl_vi,
    ...chartDemo_vi,
    ...cmdb_vi,
    ...cs_vi
}
