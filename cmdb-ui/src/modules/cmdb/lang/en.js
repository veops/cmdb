const cmdb_en = {
    relation: 'Relation',
    attribute: 'Attributes',
    configTable: 'Config Table',
    enterpriseVersionFlag: 'Pro',
    enterpriseVersionTip: 'Enterprise version only',
    menu: {
        views: 'Views',
        topologyView: 'Topology Views',
        resources: 'Resources',
        config: 'Configuration',
        backend: 'Management',
        ciTable: 'Resource Views',
        ciTree: 'Tree Views',
        ciSearch: 'Search',
        adCIs: 'AutoDiscovery Pool',
        preference: 'Preference',
        batchUpload: 'Batch Import',
        citypeManage: 'Modeling',
        backendManage: 'Backend',
        customDashboard: 'Custom Dashboard',
        serviceTreeDefine: 'Service Tree',
        citypeRelation: 'CIType Relation',
        operationHistory: 'Operation Audit',
        relationType: 'Relation Type',
        ad: 'AutoDiscovery',
        cidetail: 'CI Detail'
    },
    ciType: {
        ciType: 'CIType',
        attributes: 'Attributes',
        relation: 'Relation',
        trigger: 'Triggers',
        autoDiscoveryTab: 'AutoDiscovery',
        attributeAD: 'Attributes AutoDiscovery',
        relationAD: 'Relation AutoDiscovery',
        grant: 'Grant',
        addGroup: 'New Group',
        editGroup: 'Edit Group',
        group: 'Group',
        attributeLibray: 'Attribute Library',
        viewAttributeLibray: 'Attribute Library',
        addGroup2: 'Add Group',
        modelExport: 'Model Export',
        filename: 'Filename',
        filenameInputTips: 'Please enter filename',
        selectModel: 'Select Model',
        unselectModel: 'Unselected',
        selectedModel: 'Selected',
        addCITypeInGroup: 'Add a new CIType to the group',
        addCIType: 'Add CIType',
        editGroupName: 'Edit group name',
        deleteGroup: 'Delete this group',
        CITypeName: 'Name(English)',
        English: 'English',
        inputAttributeName: 'Please enter the attribute name',
        attributeNameTips: 'It cannot start with a number, it can be English numbers and underscores (_)',
        editCIType: 'Edit CIType',
        defaultSort: 'Default sort',
        selectDefaultOrderAttr: 'Select default sorting attributes',
        asec: 'Forward order',
        desc: 'Reverse order',
        uniqueKey: 'Unique Identifies',
        uniqueKeySelect: 'Please select a unique identifier',
        uniqueKeyTips: 'json/password/computed/choice can not be unique identifies',
        notfound: 'Can\'t find what you want?',
        cannotDeleteGroupTips: 'There is data under this group and cannot be deleted!',
        confirmDeleteGroup: 'Are you sure you want to delete group [{groupName}]?',
        confirmDeleteCIType: 'Are you sure you want to delete model [{typeName}]?',
        uploading: 'Uploading',
        uploadFailed: 'Upload failed, please try again later',
        addPlugin: 'New plugin',
        deletePlugin: 'Delete plugin',
        confirmDeleteADT: 'Do you confirm to delete [{pluginName}]',
        attributeMap: 'Attribute mapping',
        nodeConfig: 'Node Configuration',
        autoDiscovery: 'AutoDiscovery',
        node: 'Node',
        adExecConfig: 'Execute configuration',
        adExecTarget: 'Execute targets',
        oneagentIdTips: 'Please enter the hexadecimal OneAgent ID starting with 0x',
        selectFromCMDBTips: 'Select from CMDB ',
        adAutoInLib: 'Save as CI auto',
        adAutoInLibTip: 'Discovered instances are directly warehoused into CI',
        adInterval: 'Collection frequency',
        byInterval: 'by interval',
        allNodes: 'All machines',
        specifyNodes: 'Specify machine',
        masterNode: 'Master machine',
        masterNodeTip: 'The machine where OneMaster is installed',
        specifyNodesTips: 'Please fill in the specify machine!',
        username: 'Username',
        password: 'Password',
        link: 'Link',
        list: 'List',
        listTips: 'The value of the field is one or more, and the type of the value returned by the interface is list.',
        computeForAllCITips: 'All CI trigger computes',
        confirmcomputeForAllCITips: 'Confirm triggering computes for all CIs?',
        isUnique: 'Is it unique',
        unique: 'Unique',
        isChoice: 'Choiced',
        defaultShow: 'Default Display',
        defaultShowTips: 'The CI instance table displays this field by default',
        isSortable: 'Sortable',
        isIndex: 'Indexed',
        index: 'Index',
        indexTips: 'Fields can be used for retrieval to speed up queries',
        confirmDelete: 'Confirm to delete [{name}]?',
        confirmDelete2: 'Confirm to delete?',
        computeSuccess: 'Triggered successfully!',
        basicConfig: 'Basic Settings',
        AttributeName: 'Name(English)',
        DataType: 'Data Type',
        defaultValue: 'Default value',
        autoIncID: 'Auto-increment ID',
        customTime: 'Custom time',
        advancedSettings: 'Advanced Settings',
        font: 'Font',
        color: 'Color',
        choiceValue: 'Predefined value',
        computedAttribute: 'Computed Attribute',
        computedAttributeTips: 'The value of this attribute is calculated through an expression constructed from other attributes of the CIType or by executing a piece of code. The reference method of the attribute is: {{ attribute name }}',
        addAttribute: 'New attribute',
        existedAttributes: 'Already have attributes',
        editAttribute: 'Edit attribute',
        addAttributeTips1: 'If sorting is selected, it must also be selected!',
        uniqueConstraint: 'Unique Constraint',
        up: 'Move up',
        down: 'Move down',
        selectAttribute: 'Select Attribute',
        groupExisted: 'Group name already exists',
        attributeSortedTips: 'Attributes in other groups cannot be sorted. If you need to sort, please drag them to a custom group first!',
        buildinAttribute: 'built-in attributes',
        expr: 'Expression',
        code: 'Code',
        apply: 'apply',
        continueAdd: 'Keep adding',
        filter: 'Filter',
        choiceOther: 'Other CIType Attributes',
        choiceWebhookTips: 'The returned results are filtered by fields, and the hierarchical nesting is separated by ##, such as k1##k2. The web request returns {k1: [{k2: 1}, {k2: 2}]}, and the parsing result is [1, 2 ]',
        selectCIType: 'Please select a CMDB CIType',
        selectCITypeAttributes: 'Please select CIType attributes',
        selectAttributes: 'Please select attributes',
        choiceScriptDemo: 'class ChoiceValue(object):\n    @staticmethod\n    def values():\n        """\n        Execution entry, returns predefined value\n        :return: Returns a list, the type of the value is the same as the type of the attribute\n        For example:\n        return ["online", "offline"]\n        """\n        return []',
        valueExisted: 'The current value already exists!',
        addRelation: 'Add Relation',
        sourceCIType: 'Source CIType',
        sourceCITypeTips: 'Please select Source CIType',
        dstCIType: 'Target CIType',
        dstCITypeTips: 'Please select target CIType',
        relationType: 'Relation Type',
        relationTypeTips: 'Please select relation type',
        isParent: 'is parent',
        relationConstraint: 'Constraints',
        relationConstraintTips: 'please select a relationship constraint',
        one2Many: 'One to Many',
        one2One: 'One to One',
        many2Many: 'Many to Many',
        basicInfo: 'Basic Information',
        nameInputTips: 'Please enter name',
        triggerDataChange: 'Data changes',
        triggerDate: 'Date attribute',
        triggerEnable: 'Turn on',
        descInput: 'Please enter descriptions',
        triggerCondition: 'Triggering conditions',
        addInstance: 'Add new instance',
        deleteInstance: 'Delete instance',
        changeInstance: 'Instance changes',
        selectMutipleAttributes: 'Please select attributes (multiple selections)',
        selectSingleAttribute: 'Please select an attribute (single choice)',
        beforeDays: 'ahead of time',
        days: 'Days',
        notifyAt: 'Send time',
        notify: 'Notify',
        triggerAction: 'Trigger action',
        receivers: 'Recipients',
        emailTips: 'Please enter your email address, separate multiple email addresses with ;',
        customEmail: 'Custom recipients',
        notifySubject: 'Notification title',
        notifySubjectTips: 'Please enter notification title',
        notifyContent: 'Content',
        notifyMethod: 'Notify methods',
        botSelect: 'Please select a robot',
        refAttributeTips: 'The title and content can reference the attribute value of the CIType. The reference method is: {{ attr_name }}',
        webhookRefAttributeTips: 'Request parameters can reference the attribute value of the model. The reference method is: {{ attr_name }}',
        newTrigger: 'Add trigger',
        editTriggerTitle: 'Edit trigger {name}',
        newTriggerTitle: 'Add trigger {name}',
        confirmDeleteTrigger: 'Are you sure to delete this trigger?',
        int: 'Integer',
        float: 'Float',
        longText: 'Long Text',
        shortText: 'Short Text',
        shortTextTip: 'Text length <= 128',
        referenceModel: 'Reference Model',
        referenceModelTip: 'Please select reference model',
        referenceModelTip1: 'For quick view of referenced model instances',
        bool: 'Bool',
        reference: 'Reference',
        text: 'Text',
        datetime: 'DateTime',
        date: 'Date',
        time: 'Time',
        json: 'JSON',
        event: 'Event',
        reg: 'Regex',
        isInherit: 'Inherit',
        inheritType: 'Inherit Type',
        inheritTypePlaceholder: 'Please select inherit types',
        inheritFrom: 'inherit from {name}',
        groupInheritFrom: 'Please go to the {name} for modification',
        downloadType: 'Download CIType',
        deleteCIType: 'Delete CIType',
        otherGroupTips: 'Non sortable within the other group',
        filterTips: 'click to show {name}',
        attributeAssociation: 'Attribute Association',
        attributeAssociationTip1: 'Automatically establish relationships through attribute values (except password, json, multi-value, long text, boolean, reference) of two models',
        attributeAssociationTip2: 'Double click to edit',
        attributeAssociationTip3: 'Two Attributes must be selected',
        attributeAssociationTip4: 'Please select a attribute from Source CIType',
        attributeAssociationTip5: 'Please select a attribute from Target CIType',
        attributeAssociationTip6: 'Cannot be deleted again.',
        show: 'show attribute',
        setAsShow: 'Set as show attribute',
        cancelSetAsShow: 'Cancel show attribute',
        showTips: 'The names of nodes in the service tree and topology view',
        isDynamic: 'Dynamic',
        dynamicTips: 'For example, for monitoring data and frequently updated data, it is recommended to set it as a dynamic attribute, so that the change history of the attribute will not be recorded.',
        cloudAccessKey: 'Public Cloud AccessKey',
        cloudAccessKeyTip: 'For the system to synchronize public cloud information without installing Agent',
        configCheckTitle: 'Configuration check',
        checkTestTip: 'Save configuration before checking',
        checkTestBtn: 'Perform machine synchronization rule checking',
        checkTestTip2: 'Click to view the synchronization status of the discovery rule on the executing machine, the system synchronizes every 5 minutes, if the status is abnormal, you can view the possible problems',
        checkTestBtn1: 'Automated discovery testing',
        checkTestTip3: 'At the click of a button, the system will execute the autodiscovery rules on one machine',
        checkModalTitle: 'Perform machine synchronization rule checking',
        checkModalTip: 'If the status is down, check the Agent as follows',
        checkModalTip1: '1. Check if OneAgent process is alive',
        checkModalTip2: '2. View OneAgent logs with autodiscovery rule synchronisation every 5 minutes',
        checkModalColumn1: 'Executing machine',
        checkModalColumn2: 'AgentID',
        checkModalColumn3: 'Status',
        checkModalColumnStatus1: 'online',
        checkModalColumnStatus2: 'offline',
        checkModalColumn4: 'Last checkup time',
        testModalTitle: 'Automated discovery testing',
        attrMapTableAttrPlaceholder: 'Please edit the name',
        nodeSettingIp: 'Network device IP address',
        nodeSettingIpTip: 'Please enter the ip address',
        nodeSettingIpTip1: 'ip address format error',
        nodeSettingCommunity: 'Community',
        nodeSettingCommunityTip: 'Please enter community',
        nodeSettingVersion: 'Version',
        nodeSettingVersionTip: 'Please select version',
        cronRequiredTip: 'Acquisition frequency cannot be null',
        relationADTip: 'Relationship autodiscovery assumes that there is attribute autodiscovery configured',
        relationADHeader1: 'AutoDiscovery Attributes',
        relationADHeader2: 'Associative Model Attributes',
        relationADSelectAttr: 'Please select auto-discovered attributes',
        relationADSelectCIType: 'Please select the model associated with this model',
        relationADSelectModelAttr: 'Please select the associated model attribute',
        relationADTip2: 'When an auto-discovered attribute matches an associated model attribute, the two instance models are automatically associated',
        relationADTip3: 'If the value of the auto-discovered attribute is a list, multiple relationships are established with the association model',
        deleteRelationAdTip: 'Cannot be deleted again',
        cronTips: 'The format is the same as crontab, for example: 0 15 * * 1-5',
        privateCloud: 'vSphere API Configuration',
        host: 'Host',
        account: 'Account',
        insecure: 'Certificate Validation',
        vcenterName: 'Platform Name',
        resourceSearchTip1: 'Please use conditional filtering for CI filtering and copy and paste the filter expression into the fill-in box in the previous step.',
        resourceSearchTip2: 'Note 1: Please use the green button to the right of the expression to copy it',
        resourceSearchTip3: 'Note 2: If you do not need to filter, please click the grey button to copy and paste directly to configure for all nodes',
        enable: 'Enable',
        enableTip: 'Confirm switching on?',
        portScanConfig: 'Port Scan Config',
        portScanLabel1: 'CIDR',
        portScanLabel2: 'Port Range',
        portScanLabel3: 'AgentID',
        viewAllAttr: 'View All Prop',
        attrGroup: 'Attr Group',
        attrName: 'Attr Name',
        attrAlias: 'Attr Alias',
        attrCode: 'Attr Code',
        computedAttrTip1: 'Reference attributes follow jinja2 syntax',
        computedAttrTip2: `Multi-valued attributes (lists) are rendered with [ ] included by default, if you want to remove it, the reference method is: """{{ attr_name | join(',') }}""" where commas are separators`,
        example: 'Example',
        attrFilterTip: `The third column of values allows you to select attributes of this model to cascade attributes`,
        rule: 'Rule',
        cascadeAttr: 'Cascade',
        cascadeAttrTip: 'Cascading attributes note the order',
        enumValue: 'Value',
        label: 'Label',
        valueInputTip: 'Please input value'
    },
    components: {
        unselectAttributes: 'Unselected',
        selectAttributes: 'Selected',
        downloadCI: 'Export data',
        filename: 'Filename',
        filenameInputTips: 'Please enter filename',
        saveType: 'Save type',
        saveTypeTips: 'Please select save type',
        xlsx: 'Excel workbook (*.xlsx)',
        csv: 'CSV (comma separated) (*.csv)',
        html: 'Web page (*.html)',
        xml: 'XML data (*.xml)',
        txt: 'Text file (tab delimited) (*.txt)',
        grantUser: 'Grant User/Department',
        grantRole: 'Grant Role',
        confirmRevoke: 'Confirm to delete the [Authorization] permission of [{name}]?',
        readAttribute: 'View Attributes',
        readCI: 'View CIs',
        config: 'Configuration',
        ciTypeGrant: 'Grant CIType',
        ciGrant: 'Grant CI',
        attributeGrant: 'Grant Attribute',
        relationGrant: 'Grant Relation',
        perm: 'Permissions',
        all: 'All',
        customize: 'Customize',
        none: 'None',
        customizeFilterName: 'Please enter a custom filter name',
        colorPickerError: 'Initialization color format error, use #fff or rgb format',
        example: 'Example value',
        aliyun: 'aliyun',
        tencentcloud: 'Tencent Cloud',
        huaweicloud: 'Huawei Cloud',
        beforeChange: 'Before change',
        afterChange: 'After change',
        noticeContentTips: 'Please enter notification content',
        saveQuery: 'Save Filters',
        pleaseSearch: 'Please search',
        conditionFilter: 'Conditional filtering',
        attributeDesc: 'Attribute Description',
        ciSearchTips: '1. JSON/password/link/longText/reference attributes cannot be searched\n2. If the search content includes commas, they need to be escaped\n3. Only index attributes are searched, non-index attributes use conditional filtering',
        ciSearchTips2: 'For example: q=hostname:*0.0.0.0*',
        subCIType: 'Subscription CIType',
        already: 'already',
        not: 'not',
        sub: 'subscription',
        selectBelow: 'Please select below',
        subSuccess: 'Subscription successful',
        subFailed: 'Subscription failed, please try again later',
        selectMethods: 'Please select a method',
        noAuthRequest: 'No certification requested yet',
        noParamRequest: 'No parameter certification yet',
        requestParam: 'Request parameters',
        param: 'Parameter{param}',
        value: 'Value{value}',
        clear: 'Clear',
    },
    batch: {
        downloadFailed: 'Download failed',
        unselectCIType: 'No CIType selected yet',
        pleaseUploadFile: 'Please upload files',
        batchUploadCanceled: 'Batch upload canceled',
        selectCIType: 'Select CIType',
        selectCITypeTips: 'Please select a CIType and then download',
        downloadTemplate: 'Download Template',
        clickDownload: 'Click to Download',
        drawTips: 'Click or drag files here to upload!',
        supportFileTypes: 'Supported file types: xls, xlsx',
        uploadResult: 'Upload results',
        total: 'total',
        successItems: 'items, succeeded',
        failedItems: 'items, failed',
        items: 'items',
        errorTips: 'Error message',
        requestFailedTips: 'An error occurred with the request, please try again later',
        requestSuccessTips: 'Upload completed',
        uploadFile: 'Upload File',
        drawTips1: 'Please <span class="cmdb-batch-upload-tips">select a CIType</span>, and then <span class="cmdb-batch-upload-tips">download</span> ,',
        drawTips2: '<span class="cmdb-batch-upload-tips">click or drag file</span> to upload',
        dataPreview: 'Preview data and upload',
        tips1: 'Kind Reminder :',
        tips2: '1. Click to download the template, and users can customize the header of the template file, including model properties and model associations',
        // eslint-disable-next-line no-template-curly-in-string
        tips3: '2. The red color in the template file represents the model relationship, such as the $Product. Product Name (${Model Name}. {Attribute Name}) column, which establishes the relationship with the product.',
        tips4: '3. In the download template Excel file, the predefined values of attributes will be set as dropdown options. Please note that due to the limitations of Excel itself, a single dropdown box is limited to a maximum of 255 characters. If it exceeds 255 characters, we will not set the dropdown options for this attribute',
        tips5: '4. When using Excel templates, please ensure that a single file does not exceed 5000 lines.',
    },
    preference: {
        mySub: 'My Subscription',
        sub: 'Subscribe',
        cancelSub: 'Unsubscribe',
        editSub: 'Edit subscription',
        peopleSub: ' people subscribed',
        noSub: 'No subscribed',
        cancelSubSuccess: 'Unsubscribe successfully',
        confirmcancelSub: 'Are you sure to cancel your subscription?',
        confirmcancelSub2: 'Are you sure you want to unsubscribe {name}?',
        of: 'of',
        hoursAgo: 'hours ago',
        daysAgo: 'days ago',
        monthsAgo: 'month ago',
        yearsAgo: 'years ago',
        just: 'just now',
        searchPlaceholder: 'Please search CIType',
        subCITable: 'Data',
        subCITree: 'Tree',
    },
    custom_dashboard: {
        charts: 'Chart',
        newChart: 'Add Chart',
        editChart: 'Edit Chart',
        title: 'Title',
        titleTips: 'Please enter a chart title',
        calcIndicators: 'Counter',
        dimensions: 'Dimensions',
        selectDimensions: 'Please select a dimension',
        quantity: 'Quantity',
        childCIType: 'Relational CIType',
        level: 'Level',
        levelTips: 'Please enter the relationship level',
        preview: 'Preview',
        showIcon: 'Display icon',
        chartType: 'Chart Type',
        dataFilter: 'Data Filtering',
        format: 'Formats',
        fontColor: 'Font Color',
        backgroundColor: 'Background',
        chartColor: 'Chart Color',
        chartLength: 'Length',
        barType: 'Bar Type',
        stackedBar: 'Stacked Bar',
        multipleSeriesBar: 'Multiple Series Bar ',
        axis: 'Axis',
        direction: 'Direction',
        lowerShadow: 'Lower Shadow',
        count: 'Indicator',
        bar: 'Bar',
        line: 'Line',
        pie: 'Pie',
        table: 'Table',
        default: 'default',
        relation: 'Relation',
        noCustomDashboard: 'The administrator has not customized the dashboard yet',
    },
    preference_relation: {
        newServiceTree: 'Add Service Tree',
        editServiceTree: 'Edit Service Tree',
        serviceTreeName: 'Name',
        serviceTreeNamePlaceholder: 'Please enter the service tree name',
        public: 'Public',
        saveLayout: 'Save Layout',
        childNodesNotFound: 'There are no child nodes and no business relationship can be formed. Please select again!',
        tips1: 'Cannot form a view with the currently selected node, please select again!',
        tips2: 'Please enter the new serviceTree name!',
        tips3: 'Please select at least two nodes!',
        tips4: 'Leaf node must be selected',
        tips5: 'Select the tree directory node and display the service tree sub nodes as a Table',
        showLeafNode: 'Show Leaf Node',
        showTreeNode: 'Show Tree Node',
        sort: 'Sort',
        sort1: 'Leaf node information comes first',
        sort2: 'Tree node information comes first'
    },
    history: {
        ciChange: 'CI',
        relationChange: 'Relation',
        ciTypeChange: 'CIType',
        triggerHistory: 'Triggers',
        opreateTime: 'Operate Time',
        user: 'User',
        userTips: 'Enter filter username',
        filter: 'Search',
        filterOperate: 'fitler operation',
        attribute: 'Attribute',
        old: 'Old',
        new: 'New',
        noUpdate: 'No update',
        itemsPerPage: '/page',
        triggerName: 'Name',
        event: 'Event',
        action: 'Actoin',
        status: 'Status',
        done: 'Done',
        undone: 'Undone',
        triggerTime: 'Trigger Time',
        totalItems: '{total} records in total',
        pleaseSelect: 'Please select',
        startTime: 'Start Time',
        endTime: 'End Time',
        deleteCIType: 'Delete CIType',
        addCIType: 'Add CIType',
        updateCIType: 'Update CIType',
        addAttribute: 'Add Attribute',
        updateAttribute: 'Update Attribute',
        deleteAttribute: 'Delete Attribute',
        addTrigger: 'Add Trigger',
        updateTrigger: 'Update Trigger',
        deleteTrigger: 'Delete Trigger',
        addUniqueConstraint: 'Add Unique Constraint',
        updateUniqueConstraint: 'Update Unique Constraint',
        deleteUniqueConstraint: 'Delete Unique Constraint',
        addRelation: 'Add Relation',
        deleteRelation: 'Delete Relation',
        noModifications: 'No Modifications',
        attr: 'attribute',
        attrId: 'attribute id',
        changeDescription: 'attribute id: {attr_id}, {before_days} day(s) in advance, Subject: {subject}\nContent: {body}\nNotify At: {notify_at}',
        ticketStartTime: 'Start Time',
        ticketCreator: 'Creator',
        ticketTitle: 'Title',
        ticketFinishTime: 'Finish Time',
        ticketNodeName: 'Node Name',
        itsmUninstalled: 'Please use it in combination with VE ITSM',
        applyItsm: 'Free Apply ITSM',
        ticketId: 'Ticket ID',
        addReconciliation: 'Add Reconciliation',
        updateReconciliation: 'Update Reconciliation',
        deleteReconciliation: 'Delete Reconciliation',
    },
    relation_type: {
        addRelationType: 'New',
        nameTips: 'Please enter a type name',
    },
    ad: {
        upload: 'Import',
        download: 'Export',
        accept: 'Accept',
        acceptBy: 'Accept By',
        acceptTime: 'Accept Time',
        confirmAccept: 'Confirm Accept?',
        acceptSuccess: 'Accept successfully',
        isAccept: 'Accept',
        deleteADC: 'Confirm to delete this data?',
        batchDelete: 'Confirm to delete this data?',
        agent: 'Server',
        snmp: 'Network Devices',
        http: 'Public Clouds',
        plugin: 'Plugin',
        component: 'Databases & Middleware',
        privateCloud: 'Private Clouds',
        rule: 'AutoDiscovery Rules',
        timeout: 'Timeout error',
        mode: 'Mode',
        collectSettings: 'Collection Settings',
        updateFields: 'Update Field',
        pluginScript: `# -*- coding:utf-8 -*-

import json
        
        
class AutoDiscovery(object):
        
    @property
    def unique_key(self):
        """
        
        :return: Returns the name of a unique attribute
        """
        return
        
    @staticmethod
    def attributes():
        """
        Define attribute fields
        :return: Returns a list of attribute fields. The list items are (name, type, description). The name must be in English.
        type: String Integer Float Date DateTime Time JSON Bool Reference
        For example:
        return [
            ("ci_type", "String", "CIType name"),
            ("private_ip", "String", "Internal IP, multiple values separated by commas")
        ]
        """
        return []
        
    @staticmethod
    def run():
        """
        Execution entry, returns collected attribute values
        :return: 
        Returns a list, the list item is a dictionary, the dictionary key is the attribute name, and the value is the attribute value
        For example:
        return [dict(ci_type="server", private_ip="192.168.1.1")]
        """
        return []
        
        
if __name__ == "__main__":
    result = AutoDiscovery().run()
    if isinstance(result, list):
        print("AutoDiscovery::Result::{}".format(json.dumps(result)))
    else:
        print("ERROR: The collection return must be a list")
        `,
        server: 'Server',
        vserver: 'VServer',
        nic: 'NIC',
        disk: 'harddisk',
        httpSearchPlaceHolder: 'Please enter keywords',
        corporateTip: 'More types are available in the corporate version, please contact us if you need ',
        ruleCount: 'Rule count',
        execMachine: 'Exec. machine count',
        resource: 'Auto-discovered resources count',
        autoInventory: 'Inclusions count',
        newThisWeek: 'New this week',
        newThisMonth: 'New this month',
        log: 'Log',
        discoveryCardResoureTip: 'Number of resource types automatically discovered',
        addPlugin: 'Add plugin',
        pluginSearchTip: 'Please search the rules',
        innerFlag: 'Inner',
        defaultName: 'Default Name',
        deleteTip: 'Cannot be deleted again.',
        tabCustom: 'Custom',
        tabConfig: 'Configured',
        addConfig: 'Add Config',
        configErrTip: 'Please select config'
    },
    ci: {
        attributeDesc: 'Attribute Description',
        selectRows: 'Select: {rows} items',
        addRelation: 'Add Relation',
        all: 'All',
        batchUpdate: 'Batch Update',
        batchUpdateConfirm: 'Are you sure you want to make batch updates?',
        batchUpdateInProgress: 'Currently being updated in batches',
        batchUpdateInProgress2: 'Updating in batches, {total} in total, {successNum} successful, {errorNum} failed',
        batchDeleting: 'Deleting...',
        batchDeleting2: 'Deleting {total} items in total, {successNum} items successful, {errorNum} items failed',
        copyFailed: 'Copy failed',
        noLevel: 'No hierarchical relationship!',
        batchAddRelation: 'Batch Add Relation',
        history: 'Change Logs',
        relITSM: 'Related Tickets',
        topo: 'Topology',
        table: 'Table',
        m2mTips: 'The current CIType relationship is many-to-many, please go to the SerivceTree(relation view) to add or delete',
        confirmDeleteRelation: 'Confirm to delete the relationship?',
        tips1: 'Use commas to separate multiple values',
        tips2: 'The field can be modified as needed. When the value is empty, the field will be left empty.',
        tips3: 'Please select the fields that need to be modified',
        tips4: 'At least one field must be selected',
        tips5: 'Search name | alias',
        tips6: 'Speed ​​up retrieval, full-text search possible, no need to use conditional filtering\n\n json/link/password currently does not support indexing \n\nText characters longer than 190 cannot be indexed',
        tips7: 'The form of expression is a drop-down box, and the value must be in the predefined value',
        tips8: 'Multiple values, such as intranet IP',
        tips9: 'For front-end only',
        tips10: 'Other attributes of the CIType are computed using expressions\n\nA code snippet computes the returned value.',
        newUpdateField: 'Add a Attribute',
        attributeSettings: 'Attribute Settings',
        share: 'Share',
        noPermission: 'No Permission',
        rollback: 'Rollback',
        rollbackHeader: 'Instance Rollback',
        rollbackTo: 'Rollback to',
        rollbackToTips: 'Please select rollback time',
        baselineDiff: 'Difference from baseline',
        instance: 'Instance',
        rollbackBefore: 'Current value',
        rollbackAfter: 'After rollback',
        noDiff: 'CI data has not changed after {baseline}',
        rollbackConfirm: 'Are you sure you want to rollback?',
        rollbackSuccess: 'Rollback successfully',
        rollbackingTips: 'Rollbacking',
        batchRollbacking: 'Deleting {total} items in total, {successNum} items successful, {errorNum} items failed',
        baselineTips: 'Changes at this point in time will also be rollbacked, Unique ID, password and dynamic attributes do not support',
        cover: 'Cover',
    },
    serviceTree: {
        remove: 'Remove',
        deleteNode: 'Delete {name}',
        tips1: 'For example: q=os_version:centos&sort=os_version',
        tips2: 'Expression search',
        alert1: 'The administrator has not configured the ServiceTree(relation view), or you do not have permission to access it!',
        copyFailed: 'Copy failed',
        deleteRelationConfirm: 'Confirm to remove selected {name} from current relationship?',
        batch: 'Batch',
        editNode: 'Edit Node',
        editNodeName: 'Edit Node Name',
        grantTitle: 'Grant(read)',
        userPlaceholder: 'Please select users',
        rolePlaceholder: 'Please select roles',
        grantedByServiceTree: 'Granted By Service Tree:',
        grantedByServiceTreeTips: 'Please delete id_filter in Servive Tree',
        peopleHasRead: 'Personnel authorized to read:',
        authorizationPolicy: 'CI Authorization Policy:',
        idAuthorizationPolicy: 'Authorized by node:',
        view: 'View permissions',
        searchTips: 'Search in service tree'
    },
    tree: {
        tips1: 'Please go to Preference page first to complete your subscription!',
        subSettings: 'Settings',
    },
    topo: {
        addTopoView: 'Add Topology View',
        editTopoView: 'Edit Topology View',
        addTopoViewInGroup: 'Define topology view under grouping',
        groupRequired: 'Please select a group first or create a group',
        viewName: 'Title',
        viewNamePlaceholder: 'Please enter a title for the topology view',
        inputNameTips: 'Title is required',
        centralNodeType: 'Central Node Model',
        filterInstances: 'Central Node Instances',
        typeRequired: 'Central Node Model is required',
        instancesRequired: 'instances are required',
        path: 'Path',
        aggregationCount: 'Aggregation Count',
        aggreationCountTip: 'When the number of child nodes > the number of aggregations, paging display',
        preview: 'Preivew',
        noData: 'No data',
        edit: 'Edit',
        delete: 'Delete',
        searchPlaceholder: 'Search topology view',
        confirmDeleteView: 'Are you sure you want to delete this view ?',
        noInstancePerm: 'You do not have read permissions for this instance',
        noPreferenceAttributes: 'This instance has no subscription attributes or no default displayed attributes',
        topoViewSearchPlaceholder: 'Please enter the node name.',
        moreBtn: 'Show more({count})'
    },
}
export default cmdb_en
