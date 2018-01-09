import sys
import os
import csv
import re
import lxml.etree as etree
from lxml.etree import Element, SubElement, QName, tostring

# Declaring namespaces
ms = 'http://www.meta-share.org/OMTD-SHARE_XMLSchema'
xsi = 'http://www.w3.org/2001/XMLSchema-instance'
# Set omtd-share version on 3.0.2
omtd_share_version = "v302"

# Read tsv file with creation metadata info
with open("./InputTSVs/metadataCreationInfo.csv") as tsv:
    reader = csv.reader(tsv, dialect="excel-tab")
    creation_data = list(reader)
    print creation_data

# Read tsv file with rest metadata info
with open("./InputTSVs/TestLanguageContentResources.csv") as tsv:
    reader = csv.reader(tsv, dialect="excel-tab")
    data = list(reader)

# for resource in data:
# for j in range(2, len(data)):
for j in range(1, 2):  # len(data)):
    # Set working data
    resource = data[j]
    creation_resource = creation_data[j]
    # Root element
    root = Element(QName(ms, "lcrMetadataRecord"),
                   nsmap={'ms': ms, 'xsi': xsi})
    root.attrib[QName(xsi, "schemaLocation")
                ] = ms + " " + ms + "/" + omtd_share_version + "/OMTD-SHARE-LexicalConceptualResource.xsd"

    #########################################
    # metadataHeaderInfo
    metadataHeaderInfo = SubElement(
        root, QName(ms, "metadataHeaderInfo"))
    mdh_metadataRecordId = SubElement(
        metadataHeaderInfo, QName(ms, "metadataRecordIdentifier"))
    mdh_metadataRecordId.text = creation_resource[0].strip()
    mdh_metadataRecordId.attrib[
        "metadataIdentifierSchemeName"] = creation_resource[1].strip()
    mdh_metadataCreationDate = SubElement(
        metadataHeaderInfo, QName(ms, "metadataCreationDate"))
    mdh_metadataCreationDate.text = creation_resource[2].strip()

    ###############################
    # metadataCreators
    mdh_metadataCreators = SubElement(
        metadataHeaderInfo, QName(ms, "metadataCreators"))
    creatorsName = creation_resource[3].split(";")
    creatorsId = creation_resource[4].split(";")
    creatorsIdSchema = creation_resource[5].split(";")
    creatorsSex = creation_resource[6].split(";")
    creatorsEmail = creation_resource[7].split(";")
    creatorsPosition = creation_resource[8].split(";")
    creatorsOrganization = creation_resource[9].split(";")
    creatorsDepartment = creation_resource[10].split(";")
    assert(len(creatorsName) == len(creatorsId))
    assert(len(creatorsName) == len(creatorsIdSchema))
    assert(len(creatorsName) == len(creatorsSex))
    assert(len(creatorsName) == len(creatorsEmail))
    assert(len(creatorsName) == len(creatorsPosition))
    assert(len(creatorsName) == len(creatorsOrganization))
    assert(len(creatorsName) == len(creatorsDepartment))

    # metadataCreator
    for i in range(0, len(creatorsName)):
        mdh_metadataCreator = SubElement(
            mdh_metadataCreators, QName(ms, "metadataCreator"))

        name = creatorsName[i].split(" ")
        # surname
        mdh_creatorSurname = SubElement(
            mdh_metadataCreator, QName(ms, "surname"))
        mdh_creatorSurname.text = name[1].strip()

        mdh_creatorName = SubElement(
            mdh_metadataCreator, QName(ms, "givenName"))
        mdh_creatorName.text = name[0].strip()

        # Id
        mdh_creatorIdentifiers = SubElement(
            mdh_metadataCreator, QName(ms, "personIdentifiers"))
        mdh_creatorId = SubElement(
            mdh_creatorIdentifiers, QName(ms, "personIdentifier"))
        mdh_creatorId.text = creatorsId[i].strip()
        mdh_creatorId.attrib[
            "personIdentifierSchemeName"] = creatorsIdSchema[i].strip()

        # communicationInfo
        mdh_creatorCommunication = SubElement(
            mdh_metadataCreator, QName(ms, "communicationInfo"))
        mdh_creatorEmails = SubElement(
            mdh_creatorCommunication, QName(ms, "emails"))
        mdh_creatorEmail = SubElement(
            mdh_creatorEmails, QName(ms, "email"))
        mdh_creatorEmail.text = creatorsEmail[i].strip()

        # affliation info
        mdh_creatorAffiliationsInfo = SubElement(
            mdh_metadataCreator, QName(ms, "affiliations"))
        mdh_creatorAffiliation = SubElement(
            mdh_creatorAffiliationsInfo, QName(ms, "affiliation"))
        mdh_creatorPosition = SubElement(
            mdh_creatorAffiliation, QName(ms, "position"))
        mdh_creatorPosition.text = creatorsPosition[i].strip()
        mdh_creatorOrganization = SubElement(
            mdh_creatorAffiliation, QName(ms, "affiliatedOrganization"))

        # Organization
        mdh_creatorOrganizationNames = SubElement(
            mdh_creatorOrganization, QName(ms, "organizationNames"))
        mdh_creatorOrganizationName = SubElement(
            mdh_creatorOrganizationNames, QName(ms, "organizationName"))
        mdh_creatorOrganizationName.text = creatorsOrganization[i].strip()
        mdh_creatorOrganizationName.attrib["lang"] = "en"

        # Department
        mdh_creatorDepartmentNames = SubElement(
            mdh_creatorOrganization, QName(ms, "departmentNames"))
        mdh_creatorDepartmentName = SubElement(
            mdh_creatorDepartmentNames, QName(ms, "departmentName"))
        mdh_creatorDepartmentName.text = creatorsDepartment[i].strip()
        mdh_creatorDepartmentName.attrib["lang"] = "en"

    #########################################
    # lexicalConceptualResourceInfo
    lexicalConceptualResourceInfo = SubElement(
        root, QName(ms, "lexicalConceptualResourceInfo"))
    resourceType = SubElement(
        lexicalConceptualResourceInfo, QName(ms, "resourceType"))
    resourceType.text = "lexicalConceptualResource"

    #########################################
    # identificationInfo
    identificationInfo = SubElement(
        lexicalConceptualResourceInfo, QName(ms, "identificationInfo"))

    # identificationInfo - resourceName [m]
    print "Working on resource " + resource[0]
    id_resourceNames = SubElement(
        identificationInfo, QName(ms, "resourceNames"))
    id_name = SubElement(id_resourceNames, QName(ms, "resourceName"))
    id_name.text = resource[0].strip()
    id_name.attrib["lang"] = "en"

    # identificationInfo - description [m]
    print "Working on description " + resource[1]
    id_descriptions = SubElement(identificationInfo, QName(ms, "descriptions"))
    id_descr = SubElement(id_descriptions, QName(ms, "description"))
    id_descr.text = resource[1].strip()
    id_descr.attrib["lang"] = "en"

    # identificationInfo  - resourceShortNames [o]
    if resource[2] != '':
        print "Working on resource short name " + resource[2]
        id_resourceShortNames = SubElement(
            identificationInfo, QName(ms, "resourceShortNames"))
        id_shortName = SubElement(id_resourceShortNames,
                                  QName(ms, "resourceShortName"))
        id_shortName.text = resource[2].strip()
        id_shortName.attrib["lang"] = "en"

    # identificationInfo - resourceIdentifier [m+]
    id_resourceIdentifiers = SubElement(
        identificationInfo, QName(ms, "resourceIdentifiers"))
    print "Working on resource id " + resource[3] + " with schemas " + resource[4]
    resourceId = resource[3].split(";")
    resourceIdSchema = resource[4].split(";")
    assert(len(resourceId) == len(resourceIdSchema))
    for i in range(0, len(resourceId)):
        id_resourceId = SubElement(
            id_resourceIdentifiers, QName(ms, "resourceIdentifier"))
        id_resourceId.text = resourceId[i].strip()
        id_resourceId.attrib[
            "resourceIdentifierSchemeName"] = resourceIdSchema[i].strip()

    id_public = SubElement(
        identificationInfo, QName(ms, "public"))
    id_public.text = "true"

    ###########################
    # versionInfo
    versionInfo = SubElement(
        lexicalConceptualResourceInfo, QName(ms, "versionInfo"))

    # versionInfo - version
    print "Working on version " + resource[9]
    versionInfo_version = SubElement(versionInfo, QName(ms, "version"))
    versionInfo_version.text = resource[9].strip()

    # versionInfo - version date
    if resource[10] != '':
        print "Working on version date " + resource[10]
        versionInfo_versionDate = SubElement(
            versionInfo, QName(ms, "versionDate"))
        versionInfo_versionDate.text = resource[10].strip()

    ###########################
    # contactInfo
    contactInfo = SubElement(
        lexicalConceptualResourceInfo, QName(ms, "contactInfo"))

    # [m : (G or H or (I and J))]

    # contactInfo - generic contact email
    if resource[5] != '':
        print "Working on generic contact email " + resource[5]
        contact_point = SubElement(
            contactInfo, QName(ms, "contactPoint"))
        contact_point.text = resource[5].strip()
        contact_type = SubElement(
            contactInfo, QName(ms, "contactType"))
        contact_type.text = "contactEmail"

    # contactInfo - landing page
    if resource[6] != '':
        print "Working on landing page " + resource[6]
        contact_point = SubElement(
            contactInfo, QName(ms, "contactPoint"))
        contact_point.text = resource[6].strip()
        contact_type = SubElement(
            contactInfo, QName(ms, "contactType"))
        contact_type.text = "landingPage"

    # contactInfo - contact person name [+]
    # contactInfo - contact person email [+]
    if resource[7] != '' and resource[8] != '':
        print "Working on contact person name " + resource[7]
        print "Working on contact person email " + resource[8]
        personName = resource[7].split(";")
        personEmail = resource[8].split(";")
        assert(len(personName) == len(personEmail))
        contact_persons = SubElement(contactInfo, QName(ms, "contactPersons"))
        for i in range(0, len(personName)):
            contact_person = SubElement(
                contact_persons, QName(ms, "contactPerson"))
            names = personName[i].split(' ')
            # Contact Person Surname
            contact_personSurname = SubElement(
                contact_person, QName(ms, "surname"))
            contact_personSurname.text = names[0].strip()
            # Contact Person given name
            contact_personGivenName = SubElement(
                contact_person, QName(ms, "givenName"))
            contact_personGivenName.text = names[1].strip()
            # Contact Person Email
            contact_communication = SubElement(
                contact_person, QName(ms, "communicationInfo"))
            contact_communicationEmails = SubElement(
                contact_communication, QName(ms, "emails"))
            contact_communicationEmail = SubElement(
                contact_communicationEmails, QName(ms, "email"))
            contact_communicationEmail.text = personEmail[i].strip()

    ##########################
    # distributionInfo
    distributionInfos = SubElement(
        lexicalConceptualResourceInfo, QName(ms, "distributionInfos"))

    #########################
    # datasetDistributionInfo [m]
    datasetDistributionInfo1 = SubElement(
        distributionInfos, QName(ms, "datasetDistributionInfo"))

    # datasetDistributionInfo - distribution location [m]
    distr1_distributionLocationExternal = SubElement(
        datasetDistributionInfo1, QName(ms, "distributionLoc"))

    distr1_distributionMedium = SubElement(
        distr1_distributionLocationExternal, QName(ms, "distributionMedium"))
    print "Working on distribution medium " + resource[11]
    distr1_distributionMedium.text = resource[11].strip()

    if resource[12].strip() != '':
        print "Working on distributio location " + resource[12]
        distr1_distributionLocation = SubElement(
            distr1_distributionLocationExternal, QName(ms, "distributionLocation"))
        distr1_distributionLocation.text = resource[12].strip()

    # datasetDistributionInfo - text formats [o+]
    if resource[13].strip() != '':
        print "Working on text formats " + resource[13]
        distr1_textFormats = SubElement(
            datasetDistributionInfo1, QName(ms, "textFormats"))
        textFormat_list = resource[13].split(";")
        for textFormat in textFormat_list:
            distr1_textFormatInfo = SubElement(
                distr1_textFormats, QName(ms, "textFormatInfo"))
            distr1_dataFormatInfo = SubElement(
                distr1_textFormatInfo, QName(ms, "dataFormatInfo"))
            distr1_dataFormat = SubElement(
                distr1_dataFormatInfo, QName(ms, "dataFormat"))
            distr1_dataFormat.text = textFormat.strip()

    # datasetDistributionInfo - licence info [m+]
    distr1_rightsInfo = SubElement(
        datasetDistributionInfo1, QName(ms, "rightsInfo"))
    distr1_licenceInfos = SubElement(
        distr1_rightsInfo, QName(ms, "licenceInfos"))

    print "Working on licence " + resource[14]
    license_list = resource[14].split(";")
    for license in license_list:
        distr1_licenceInfo = SubElement(
            distr1_licenceInfos, QName(ms, "licenceInfo"))
        distr1_licence = SubElement(distr1_licenceInfo, QName(ms, "licence"))
        distr1_licence.text = license.strip()
        if distr1_licence.text == "nonStandardLicenceTerms":
            assert(resource[15].strip() != "")
            print "Working on nonStandardLicenceName " + resource[15]
            distr1_nonStandardLicenceName = SubElement(
                distr1_licenceInfo, QName(ms, "nonStandardLicenceName"))
            distr1_nonStandardLicenceName.text = resource[15].strip()
            distr1_nonStandardLicenceName.attrib["lang"] = "en"
            assert (resource[16].strip() != "" or resource[17].strip() != "")
            if resource[16].strip() != "":
                print "Working on nonStandardLicenceTermsURL" + resource[16]
                distr1_nonStandardLicenceTermsURL = SubElement(
                    distr1_licenceInfo, QName(ms, "nonStandardLicenceTermsURL"))
                distr1_nonStandardLicenceTermsURL.text = resource[16].strip()
            if resource[17].strip() != "":
                print "Working on nonStandardLicenceTermsText " + resource[17]
                distr1_nonStandardLicenceTermsText = SubElement(
                    distr1_licenceInfo, QName(ms, "nonStandaradLicenceTermsText"))
                distr1_nonStandardLicenceTermsText.text = resource[17].strip()

    #########################
    # datasetDistributionInfo [o]
    if resource[18].strip() != "":
        print "Working on distribution medium " + resource[18]
        datasetDistributionInfo2 = SubElement(
            distributionInfos, QName(ms, "datasetDistributionInfo"))

    # datasetDistributionInfo - distribution location [m]
        distr2_distributionLocationExternal = SubElement(
            datasetDistributionInfo2, QName(ms, "distributionLoc"))

        distr2_distributionMedium = SubElement(
            distr2_distributionLocationExternal, QName(ms, "distributionMedium"))
        distr2_distributionMedium.text = resource[18].strip()

        if resource[19].strip() != '':
            print "Working on distr location " + resource[19]
            distr2_distributionLocation = SubElement(
                distr2_distributionLocationExternal, QName(ms, "distributionLocation"))
            distr2_distributionLocation.text = resource[19].strip()

        # datasetDistributionInfo - text formats [o+]
        if resource[20].strip() != '':
            print "Working on text formats " + resource[20]
            distr2_textFormats = SubElement(
                datasetDistributionInfo2, QName(ms, "textFormats"))
            textFormat_list = resource[20].split(";")
            for textFormat in textFormat_list:
                distr2_textFormatInfo = SubElement(
                    distr2_textFormats, QName(ms, "textFormatInfo"))
                distr2_dataFormatInfo = SubElement(
                    distr2_textFormatInfo, QName(ms, "dataFormatInfo"))
                distr2_dataFormat = SubElement(
                    distr2_dataFormatInfo, QName(ms, "dataFormat"))
                distr2_dataFormat.text = textFormat.strip()

        # datasetDistributionInfo - licence info [m+]
        distr2_rightsInfo = SubElement(
            datasetDistributionInfo2, QName(ms, "rightsInfo"))
        distr2_licenceInfos = SubElement(
            distr2_rightsInfo, QName(ms, "licenceInfos"))
        print "Working on licence " + resource[21]
        license_list = resource[21].split(";")
        for license in license_list:
            distr2_licenceInfo = SubElement(
                distr2_licenceInfos, QName(ms, "licenceInfo"))
            distr2_licence = SubElement(
                distr2_licenceInfo, QName(ms, "licence"))
            distr2_licence.text = license.strip()
            if distr2_licence.text == "nonStandardLicenceTerms":
                assert(resource[22].strip() != "")
                print "Working on nonStandardLicenceName " + resource[22]
                distr2_nonStandardLicenceName = SubElement(
                    distr2_licenceInfo, QName(ms, "nonStandardLicenceName"))
                distr2_nonStandardLicenceName.text = resource[22].strip()
                distr2_nonStandardLicenceName.attrib["lang"] = "en"
                assert (resource[23].strip() !=
                        "" or resource[24].strip() != "")
                if resource[23].strip() != "":
                    print "Working on nonStandardLicenceURL " + resource[23]
                    distr2_nonStandardLicenceTermsURL = SubElement(
                        distr2_licenceInfo, QName(ms, "nonStandardLicenceTermsURL"))
                    distr2_nonStandardLicenceTermsURL.text = resource[
                        23].strip()
                if resource[24].strip() != "":
                    print "Working on nonStandardLicenceText " + resource[24]
                    distr2_nonStandardLicenceTermsText = SubElement(
                        distr2_licenceInfo, QName(ms, "nonStandaradLicenceTermsText"))
                    distr2_nonStandardLicenceTermsText.text = resource[
                        24].strip()

    #########################
    # datasetDistributionInfo [o]
    if resource[25].strip() != "":
        datasetDistributionInfo3 = SubElement(
            distributionInfos, QName(ms, "datasetDistributionInfo"))

    # datasetDistributionInfo - distribution location [m]
        distr3_distributionLocationExternal = SubElement(
            datasetDistributionInfo3, QName(ms, "distributionLoc"))
        distr3_distributionMedium = SubElement(
            distr3_distributionLocationExternal, QName(ms, "distributionMedium"))
        print "Working on distributio medium " + resource[25]
        distr3_distributionMedium.text = resource[25].strip()

        if resource[26].strip() != '':
            distr3_distributionLocation = SubElement(
                distr3_distributionLocationExternal, QName(ms, "distributionLocation"))
            print "Working on distributio location " + resource[26]
            distr3_distributionLocation.text = resource[26].strip()

        # datasetDistributionInfo - text formats [o+]
        if resource[27].strip() != '':
            distr3_textFormats = SubElement(
                datasetDistributionInfo3, QName(ms, "textFormats"))
            print "Working on text formats" + resource[27]
            textFormat_list = resource[27].split(";")
            for textFormat in textFormat_list:
                distr3_textFormatInfo = SubElement(
                    distr3_textFormats, QName(ms, "textFormatInfo"))
                distr3_dataFormatInfo = SubElement(
                    distr3_textFormatInfo, QName(ms, "dataFormatInfo"))
                distr3_dataFormat = SubElement(
                    distr3_dataFormatInfo, QName(ms, "dataFormat"))
                distr3_dataFormat.text = textFormat.strip()

        # datasetDistributionInfo - licence info [m+]
        distr3_rightsInfo = SubElement(
            datasetDistributionInfo3, QName(ms, "rightsInfo"))
        distr3_licenceInfos = SubElement(
            distr3_rightsInfo, QName(ms, "licenceInfos"))

        print "Working on licence " + resource[28]
        license_list = resource[28].split(";")
        for license in license_list:
            distr3_licenceInfo = SubElement(
                distr3_licenceInfos, QName(ms, "licenceInfo"))
            distr3_licence = SubElement(
                distr3_licenceInfo, QName(ms, "licence"))
            distr3_licence.text = license.strip()
            if distr3_licence.text == "nonStandardLicenceTerms":
                assert(resource[29].strip() != "")
                print "Working on nonStandardLicenceName " + resource[29]
                distr3_nonStandardLicenceName = SubElement(
                    distr3_licenceInfo, QName(ms, "nonStandardLicenceName"))
                distr3_nonStandardLicenceName.text = resource[29].strip()
                distr3_nonStandardLicenceName.attrib["lang"] = "en"
                assert (resource[30].strip() !=
                        "" or resource[31].strip() != "")
                if resource[30].strip() != "":
                    print "Working on nonStandardLicenceURL " + resource[30]
                    distr3_nonStandardLicenceTermsURL = SubElement(
                        distr3_licenceInfo, QName(ms, "nonStandardLicenceTermsURL"))
                    distr3_nonStandardLicenceTermsURL.text = resource[
                        30].strip()
                if resource[31].strip() != "":
                    distr3_nonStandardLicenceTermsText = SubElement(
                        distr3_licenceInfo, QName(ms, "nonStandaradLicenceTermsText"))
                    print "Working on nonStandardLicenceText " + resource[31]
                    distr3_nonStandardLicenceTermsText.text = resource[
                        31].strip()

    ###################################
    # resource documentation info
    if resource[32].strip() != "":
        assert(resource[33].strip() != "")
        documentationInfo = SubElement(
            lexicalConceptualResourceInfo, QName(ms, "resourceDocumentationInfo"))
        doc_citations = SubElement(
            documentationInfo, QName(ms, "citations"))
        doc_mustBeCitedWith = SubElement(
            doc_citations, QName(ms, "mustBeCitedWith"))
        doc_publicationIdentifiers = SubElement(
            doc_mustBeCitedWith, QName(ms, "publicationIdentifiers"))
        publId = resource[32].split(";")
        publIdSchema = resource[33].split(";")
        assert(len(publId) == len(publIdSchema))
        for i in range(0, len(publId)):
            doc_publicationId = SubElement(
                doc_publicationIdentifiers, QName(ms, "publicationIdentifier"))
            #doc_publicationId.text = publId[i].strip()
            doc_publicationId.attrib[
                "publicationIdentifierSchemeName"] = publIdSchema[i].strip()

    ##################################
    # lexicalConceptualResourceType
    assert(resource[34].strip() != "")
    resourceType = SubElement(
        lexicalConceptualResourceInfo, QName(ms, "lexicalConceptualResourceType"))
    resourceType.text = resource[34].strip()

    #################################
    # lexicalConceptualResourceEncodingInfo
    if resource[35].strip() != "":
        resourceEncodingInfo = SubElement(
            lexicalConceptualResourceInfo, QName(ms, "lexicalConceptualResourceEncodingInfo"))
        contentTypes = resource[35].split(";")
        for content in contentTypes:
            encoding_contentTypes = SubElement(
                resourceEncodingInfo, QName(ms, "contentTypes"))
            encoding_contentTypes.text = content.strip()

    ###########################################
    # lexicalConceptualResourceMediaType
    assert(resource[36].strip() != "")
    lcr_mediaType = SubElement(
        lexicalConceptualResourceInfo, QName(ms, "lexicalConceptualResourceMediaType"))
    lrc_textInfo = SubElement(
        lcr_mediaType, QName(ms, "lexicalConceptualResourceTextInfo"))

    # mediaType
    lrc_textMediaType = SubElement(
        lrc_textInfo, QName(ms, "mediaType"))
    lrc_textMediaType.text = "text"

    # lingualityInfo
    lrc_textLingualityInfo = SubElement(
        lrc_textInfo, QName(ms, "lingualityInfo"))
    lrc_textLingualityType = SubElement(
        lrc_textLingualityInfo, QName(ms, "lingualityType"))
    lrc_textLingualityType.text = resource[36].strip()

    # language tag
    assert(resource[37].strip() != "")
    lrc_textLanguages = SubElement(
        lrc_textInfo, QName(ms, "languages"))
    languageTags = resource[37].split(";")
    for langTag in languageTags:
        lrc_textLanguageInfo = SubElement(
            lrc_textLanguages, QName(ms, "languageInfo"))
        lrc_textLanguage = SubElement(
            lrc_textLanguageInfo, QName(ms, "language"))
        lrc_textLanguageTag = SubElement(
            lrc_textLanguage, QName(ms, "languageTag"))
        lrc_textLanguageTag.text = langTag.strip()
        lrc_textLanguageId = SubElement(
            lrc_textLanguage, QName(ms, "languageId"))
        lrc_textLanguageId.text = langTag.strip()

    # meta-language tag
    assert(resource[38].strip() != "")
    lrc_textMetaLanguages = SubElement(
        lrc_textInfo, QName(ms, "metalanguages"))
    metalanguageTags = resource[38].split(";")
    for metalangTag in metalanguageTags:
        lrc_textMetaLanguageInfo = SubElement(
            lrc_textMetaLanguages, QName(ms, "metalanguageInfo"))
        lrc_textMetaLanguage = SubElement(
            lrc_textMetaLanguageInfo, QName(ms, "language"))
        lrc_textMetaLanguageTag = SubElement(
            lrc_textMetaLanguage, QName(ms, "languageTag"))
        lrc_textMetaLanguageTag.text = metalangTag.strip()
        lrc_textMetaLanguageId = SubElement(
            lrc_textMetaLanguage, QName(ms, "languageId"))
        lrc_textMetaLanguageId.text = metalangTag.strip()

    # sizes
    lrc_textSizes = SubElement(
        lrc_textInfo, QName(ms, "sizes"))
    sizes = resource[39].split(";")
    sizeUnits = resource[40].split(";")
    assert(len(sizes) == len(sizeUnits))
    for i in range(0, len(sizes)):
        lrc_textSizeInfo = SubElement(
            lrc_textSizes, QName(ms, "sizeInfo"))
        lrc_texiSizeSize = SubElement(
            lrc_textSizeInfo, QName(ms, "size"))
        lrc_texiSizeSize.text = sizes[i].strip()
        lrc_texiSizeSizeUnit = SubElement(
            lrc_textSizeInfo, QName(ms, "sizeUnit"))
        lrc_texiSizeSizeUnit.text = sizeUnits[i].strip()

    # Print xml
    # fileXML = open("GeneratedXMLs/" +
    #               resource[0].replace(" ", "") + ".xml", 'w')
    # fileXML.write(tostring(root, pretty_print=True))
    # fileXML.close()
    print etree.tostring(root, pretty_print=True)
#    print(tostring(root, pretty_print=True))
