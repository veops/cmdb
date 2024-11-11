export const OPERATE_TYPE = {
  ADD_SCOPE: '0',
  UPDATE_SCOPE: '1',
  DELETE_SCOPE: '2',
  ADD_SUBNET: '3',
  UPDATE_SUBNET: '4',
  DELETE_SUBNET: '5',
  ASSIGN_ADDRESS: '6',
  REVOKE_ADDRESS: '7',
}

export const OPERATE_TYPE_TEXT = {
  [OPERATE_TYPE.ADD_SCOPE]: 'cmdb.ipam.addCatalog',
  [OPERATE_TYPE.UPDATE_SCOPE]: 'cmdb.ipam.updateCatalog',
  [OPERATE_TYPE.DELETE_SCOPE]: 'cmdb.ipam.deleteCatalog',
  [OPERATE_TYPE.ADD_SUBNET]: 'cmdb.ipam.addSubnet',
  [OPERATE_TYPE.UPDATE_SUBNET]: 'cmdb.ipam.updateSubnet',
  [OPERATE_TYPE.DELETE_SUBNET]: 'cmdb.ipam.deleteSubnet',
  [OPERATE_TYPE.ASSIGN_ADDRESS]: 'cmdb.ipam.addressAssign',
  [OPERATE_TYPE.REVOKE_ADDRESS]: 'cmdb.ipam.revokeAddress',
}

export const OPERATE_TYPE_COLOR = {
  [OPERATE_TYPE.ADD_SCOPE]: {
    color: '#2F54EB',
    backgroundColor: '#DCF5FF'
  },
  [OPERATE_TYPE.UPDATE_SCOPE]: {
    color: '#FF7D00',
    backgroundColor: '#FFECCF'
  },
  [OPERATE_TYPE.DELETE_SCOPE]: {
    color: '#FD4C6A',
    backgroundColor: '#FFECE8'
  },
  [OPERATE_TYPE.ADD_SUBNET]: {
    color: '#2F54EB',
    backgroundColor: '#DCF5FF'
  },
  [OPERATE_TYPE.UPDATE_SUBNET]: {
    color: '#FF7D00',
    backgroundColor: '#FFECCF'
  },
  [OPERATE_TYPE.DELETE_SUBNET]: {
    color: '#FD4C6A',
    backgroundColor: '#FFECE8'
  },
  [OPERATE_TYPE.ASSIGN_ADDRESS]: {
    color: '#00B42A',
    backgroundColor: '#F6FFED'
  },
  [OPERATE_TYPE.REVOKE_ADDRESS]: {
    color: '#0AA5A8',
    backgroundColor: '#E8FFFB'
  },
}
