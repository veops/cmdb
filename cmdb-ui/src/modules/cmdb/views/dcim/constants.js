export const DCIM_TYPE = {
  REGION: 'region',
  IDC: 'idc',
  SERVER_ROOM: 'server_room',
  RACK: 'rack'
}

export const DCIM_CITYPE_NAME = {
  REGION: 'dcim_region',
  IDC: 'dcim_idc',
  SERVER_ROOM: 'dcim_server_room',
  RACK: 'dcim_rack'
}

export const DEVICE_CITYPE_NAME = {
  SWITCH: 'switch',
  FC_SWITCH: 'fc_switch',
  F5: 'bigip',
  ROUTER: 'router',
  FIRE_WALL: 'firewall',
  SERVER: 'server',
  RAID: 'raid'
}

const createTypeNameMap = (typeObj, typeNameObj) => {
  const map = {}

  Object.keys(typeObj).forEach(key => {
    map[typeObj[key]] = typeNameObj[key]
    map[typeNameObj[key]] = typeObj[key]
  })

  return map
}

export const DCIM_TYPE_NAME_MAP = createTypeNameMap(DCIM_TYPE, DCIM_CITYPE_NAME)
