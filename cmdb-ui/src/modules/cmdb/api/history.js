import { axios } from '@/utils/request'

export function getCIHistory(ciId) {
  return axios({
    url: `/v0.1/history/ci/${ciId}`,
    method: 'GET'
  })
}

export function getCIHistoryTable(params) {
  return axios({
    url: `/v0.1/history/records/attribute`,
    method: 'GET',
    params: params,
    timeout: 30 * 1000
  })
}

export function getRelationTable(params) {
  return axios({
    url: `/v0.1/history/records/relation`,
    method: 'GET',
    params: params,
    timeout: 30 * 1000
  })
}

export function getCITypesTable(params) {
  return axios({
    url: `/v0.1/history/ci_types`,
    method: 'GET',
    params: params,
    timeout: 30 * 1000
  })
}

export function getUsers(params) {
  return axios({
    url: `/v1/acl/users/employee`,
    method: 'GET',
    params: params
  })
}

export function getCiTriggers(params) {
  return axios({
    url: `/v0.1/history/ci_triggers`,
    method: 'GET',
    params: params
  })
}

export function getCiTriggersByCiId(ci_id, params) {
  return axios({
    url: `/v0.1/history/ci_triggers/${ci_id}`,
    method: 'GET',
    params
  })
}

export function getCiRelatedTickets(params) {
  return axios({
    url: `/itsm/v1/process_ticket/get_tickets_by`,
    method: 'POST',
    data: params,
    isShowMessage: false
  })
}

export function judgeItsmInstalled() {
  return axios({
    url: `/itsm/v1/process_ticket/itsm_existed`,
    method: 'GET',
    isShowMessage: false
  })
}

export function getCIsBaseline(params) {
  return axios({
    url: `/v0.1/ci/baseline`,
    method: 'GET',
    params
  })
}

export function CIBaselineRollback(ciId, params) {
  return axios({
    url: `/v0.1/ci/${ciId}/baseline/rollback`,
    method: 'POST',
    data: params
  })
}
