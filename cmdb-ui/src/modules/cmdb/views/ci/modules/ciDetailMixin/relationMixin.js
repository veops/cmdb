import { getCITypeChildren, getCITypeParent } from '@/modules/cmdb/api/CITypeRelation'
import { searchCIRelation } from '@/modules/cmdb/api/CIRelation'

const RelationMixin = {
  data() {
    return {
      relationData: {
        parentCITypeList: [],
        childCITypeList: [],
        parentCIList: [],
        childCIList: []
      }
    }
  },

  methods: {
    async initRelationData(typeId, ciId) {
      const {
        parentCITypeList,
        childCITypeList
      } = await this.getRelationCITypeList(typeId)
      const {
        parentCIList,
        childCIList
      } = await this.getRelationCIList(ciId)
      this.relationData = {
        parentCITypeList,
        childCITypeList,
        parentCIList,
        childCIList
      }
    },

    async getRelationCITypeList(typeId) {
      let parentCITypeList = []
      let childCITypeList = []

      if (typeId) {
        parentCITypeList = await this.getParentCITypeList(typeId)
        childCITypeList = await this.getChildCITypeList(typeId)
      }

      return {
        parentCITypeList,
        childCITypeList
      }
    },

    async getRelationCIList(ciId) {
      let parentCIList = []
      let childCIList = []

      if (ciId) {
        parentCIList = await this.getParentCIList(ciId)
        childCIList = await this.getChildCIList(ciId)
      }

      return {
        parentCIList,
        childCIList
      }
    },

    async refreshRelationCI(ciId) {
      const {
        parentCIList,
        childCIList
      } = await this.getRelationCIList(ciId)
      this.relationData.parentCIList = parentCIList
      this.relationData.childCIList = childCIList
    },

    async getParentCITypeList(typeId) {
      const res = await getCITypeParent(typeId)
      return res?.parents || []
    },

    async getChildCITypeList(typeId) {
      const res = await getCITypeChildren(typeId)
      return res.children || []
    },

    async getParentCIList(ciId) {
      const res = await searchCIRelation(`root_id=${ciId}&level=1&reverse=1&count=10000`)
      return res?.result || []
    },

    async getChildCIList(ciId) {
      const res = await searchCIRelation(`root_id=${ciId}&level=1&reverse=0&count=10000`)
      return res?.result || []
    }
  }
}

export default RelationMixin
