import sys
import os
import csv
import re
import datetime

import lxml.etree as etree
from lxml.etree import Element, SubElement, QName, tostring

# Declaring namespaces
ms = 'http://www.meta-share.org/OMTD-SHARE_XMLSchema'
xsi = 'http://www.w3.org/2001/XMLSchema-instance'
# Set omtd-share version on 3.0.2
omtd_share_version = "v302"

# Read tsv file with rest metadata info
with open("./InputTSVs/TestLanguageContentResources.csv") as tsv:
    reader = csv.reader(tsv, dialect="excel-tab")
    data = list(reader)

# for resource in data:
# for j in range(2, len(data)):
print len(data)
for j in range(5, len(data)):  # len(data)):
    # Set working data
    resource = data[j]

    # Root element
    root = Element(QName(ms, "lcrMetadataRecord"),
                   nsmap={'ms': ms, 'xsi': xsi})
    root.attrib[QName(xsi, "schemaLocation")
                ] = ms + " " + ms + "/" + omtd_share_version + "/OMTD-SHARE-LexicalConceptualResource.xsd"

    #########################################
    # metadataHeaderInfo [m]
    metadataHeaderInfo = SubElement(
        root, QName(ms, "metadataHeaderInfo"))
    mdh_metadataRecordId = SubElement(
        metadataHeaderInfo, QName(ms, "metadataRecordIdentifier"))
    mdh_metadataRecordId.text = "omtd_id"
    mdh_metadataRecordId.attrib[
        "metadataIdentifierSchemeName"] = "OMTD"
    mdh_metadataCreationDate = SubElement(
        metadataHeaderInfo, QName(ms, "metadataCreationDate"))
    mdh_metadataCreationDate.text = str(datetime.datetime.now().date())

    
    # metadataCreators [m]
    mdh_metadataCreators = SubElement(
        metadataHeaderInfo, QName(ms, "metadataCreators"))
    creatorsName = resource[43].split(";")  
    creatorsEmail = resource[44].split(";")
    assert(len(creatorsName) == len(creatorsEmail))

    # metadataCreator
    for i in range(0, len(creatorsName)):
        mdh_metadataCreator = SubElement(
            mdh_metadataCreators, QName(ms, "metadataCreator"))

        name = creatorsName[i].split(",")
        # surname [m]
        mdh_creatorSurname = SubElement(
            mdh_metadataCreator, QName(ms, "surname"))
        mdh_creatorSurname.text = name[0].strip()
        # Given name [o]
        mdh_creatorName = SubElement(
            mdh_metadataCreator, QName(ms, "givenName"))
        mdh_creatorName.text = name[1].strip()

    #     # Id
    #     mdh_creatorIdentifiers = SubElement(
    #         mdh_metadataCreator, QName(ms, "personIdentifiers"))
    #     mdh_creatorId = SubElement(
    #         mdh_creatorIdentifiers, QName(ms, "personIdentifier"))
    #     mdh_creatorId.text = creatorsId[i].strip()
    #     mdh_creatorId.attrib[
    #         "personIdentifierSchemeName"] = creatorsIdSchema[i].strip()

        # communicationInfo [o]
        mdh_creatorCommunication = SubElement(
            mdh_metadataCreator, QName(ms, "communicationInfo"))
        mdh_creatorEmails = SubElement(
            mdh_creatorCommunication, QName(ms, "emails"))
        mdh_creatorEmail = SubElement(
            mdh_creatorEmails, QName(ms, "email"))
        mdh_creatorEmail.text = creatorsEmail[i].strip()

    #     # affliation info
    #     mdh_creatorAffiliationsInfo = SubElement(
    #         mdh_metadataCreator, QName(ms, "affiliations"))
    #     mdh_creatorAffiliation = SubElement(
    #         mdh_creatorAffiliationsInfo, QName(ms, "affiliation"))
    #     mdh_creatorPosition = SubElement(
    #         mdh_creatorAffiliation, QName(ms, "position"))
    #     mdh_creatorPosition.text = creatorsPosition[i].strip()
    #     mdh_creatorOrganization = SubElement(
    #         mdh_creatorAffiliation, QName(ms, "affiliatedOrganization"))

    #     # Organization
    #     mdh_creatorOrganizationNames = SubElement(
    #         mdh_creatorOrganization, QName(ms, "organizationNames"))
    #     mdh_creatorOrganizationName = SubElement(
    #         mdh_creatorOrganizationNames, QName(ms, "organizationName"))
    #     mdh_creatorOrganizationName.text = creatorsOrganization[i].strip()
    #     mdh_creatorOrganizationName.attrib["lang"] = "en"

    #     # Department
    #     mdh_creatorDepartmentNames = SubElement(
    #         mdh_creatorOrganization, QName(ms, "departmentNames"))
    #     mdh_creatorDepartmentName = SubElement(
    #         mdh_creatorDepartmentNames, QName(ms, "departmentName"))
    #     mdh_creatorDepartmentName.text = creatorsDepartment[i].strip()
    #     mdh_creatorDepartmentName.attrib["lang"] = "en"

    #########################################
    # lexicalConceptualResourceInfo [m]
    lexicalConceptualResourceInfo = SubElement(
        root, QName(ms, "lexicalConceptualResourceInfo"))
    resourceType = SubElement(
        lexicalConceptualResourceInfo, QName(ms, "resourceType"))
    resourceType.text = "lexicalConceptualResource"

    #########################################
    # identificationInfo [m]
    identificationInfo = SubElement(
        lexicalConceptualResourceInfo, QName(ms, "identificationInfo"))

    # identificationInfo - resourceName [m]
    print "Working on resource " + resource[1]
    id_resourceNames = SubElement(
        identificationInfo, QName(ms, "resourceNames"))
    id_name = SubElement(id_resourceNames, QName(ms, "resourceName"))
    id_name.text = resource[1].strip()
    id_name.attrib["lang"] = "en"

    # identificationInfo - description [m]
    print "Working on description " + resource[1]
    id_descriptions = SubElement(identificationInfo, QName(ms, "descriptions"))
    id_descr = SubElement(id_descriptions, QName(ms, "description"))
    id_descr.text = resource[2].strip()
    id_descr.attrib["lang"] = "en"

    # identificationInfo  - resourceShortNames [o]
    if resource[3] != '':
        print "Working on resource short name " + resource[3]
        id_resourceShortName = SubElement(
            identificationInfo, QName(ms, "resourceShortName"))
        id_resourceShortName.text = resource[3].strip()

    # identificationInfo - resourceIdentifier [m+]
    id_resourceIdentifiers = SubElement(
        identificationInfo, QName(ms, "resourceIdentifiers"))
    print "Working on resource ids: " + resource[4] + " with schemas: " + resource[5]
    resourceId = resource[4].split(";")
    resourceIdSchema = resource[5].split(";")
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
    # versionInfo [m]
    versionInfo = SubElement(
        lexicalConceptualResourceInfo, QName(ms, "versionInfo"))

    # versionInfo - version [m]
    print "Working on version " + resource[6]
    versionInfo_version = SubElement(versionInfo, QName(ms, "version"))
    versionInfo_version.text = resource[6].strip()

    # versionInfo - version date [o]
    if resource[7] != '':
        print "Working on version date " + resource[7]
        versionInfo_versionDate = SubElement(
            versionInfo, QName(ms, "versionDate"))
        versionInfo_versionDate.text = resource[7].strip()

    ###########################
    # contactInfo [m]
    contactInfo = SubElement(
        lexicalConceptualResourceInfo, QName(ms, "contactInfo"))

    # [m : (G or H or (I and J))]
    # contactInfo - generic contact email
    if resource[8] != '':
        print "Working on generic contact email " + resource[8]
        contact_point = SubElement(
            contactInfo, QName(ms, "contactPoint"))
        contact_point.text = resource[8].strip()
        contact_type = SubElement(
            contactInfo, QName(ms, "contactType"))
        contact_type.text = "contactEmail"

    # contactInfo - landing page
    if resource[9] != '':
        print "Working on landing page " + resource[9]
        contact_point = SubElement(
            contactInfo, QName(ms, "contactPoint"))
        contact_point.text = resource[9].strip()
        contact_type = SubElement(
            contactInfo, QName(ms, "contactType"))
        contact_type.text = "landingPage"

    # contactInfo - contact person name [+]
    # contactInfo - contact person email [+]
    if resource[10] != '' and resource[11] != '':
        print "Working on contact persons' name " + resource[10]
        print "Working on contact persons' email " + resource[11]
        personName = resource[10].split(";")
        personEmail = resource[11].split(";")
        assert(len(personName) == len(personEmail))
        contact_persons = SubElement(contactInfo, QName(ms, "contactPersons"))
        for i in range(0, len(personName)):
            contact_person = SubElement(
                contact_persons, QName(ms, "contactPerson"))
            names = personName[i].split(',')
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
    # datasetDistributionInfo - 1[m]
    datasetDistributionInfo1 = SubElement(
        distributionInfos, QName(ms, "datasetDistributionInfo"))

    # datasetDistributionInfo [m] - distribution medium [m]
    print "Working on distribution medium " + resource[12]
    distr1_distributionMedium = SubElement(
        datasetDistributionInfo1, QName(ms, "distributionMedium"))
    distr1_distributionMedium.text = resource[12].strip()

    # datasetDistributionInfo [m] - distribution medium [o]
    if resource[13].strip() != '':
        print "Working on distribution location " + resource[13]
        distr1_distributionLocation = SubElement(
            datasetDistributionInfo1, QName(ms, "distributionLocation"))
        distr1_distributionLocation.text = resource[13].strip()

    #  datasetDistributionInfo [m] - sizes [m]
    lrc_textSizes = SubElement(
        datasetDistributionInfo1, QName(ms, "sizes"))
    sizes = resource[14].split(";")
    sizeUnits = resource[15].split(";")
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

    # datasetDistributionInfo [m] - text formats [m+]
    print "Working on text formats " + resource[16]
    distr1_textFormats = SubElement(
        datasetDistributionInfo1, QName(ms, "textFormats"))
    textFormat_list = resource[16].split(";")
    for textFormat in textFormat_list:
        distr1_textFormatInfo = SubElement(
            distr1_textFormats, QName(ms, "textFormatInfo"))
        distr1_dataFormatInfo = SubElement(
            distr1_textFormatInfo, QName(ms, "dataFormatInfo"))
        distr1_dataFormat = SubElement(
            distr1_dataFormatInfo, QName(ms, "dataFormat"))
        distr1_dataFormat.text = textFormat.strip()


    #########################
    # datasetDistributionInfo - 2 [o]
    if resource[17] != '':
        datasetDistributionInfo1 = SubElement(
            distributionInfos, QName(ms, "datasetDistributionInfo"))

        # datasetDistributionInfo [o] - distribution medium [m]
        print "Working on distribution medium " + resource[17]
        distr1_distributionMedium = SubElement(
            datasetDistributionInfo1, QName(ms, "distributionMedium"))
        distr1_distributionMedium.text = resource[17].strip()

        # datasetDistributionInfo [o] - distribution medium [o]
        if resource[13].strip() != '':
            print "Working on distribution location " + resource[18]
            distr1_distributionLocation = SubElement(
                datasetDistributionInfo1, QName(ms, "distributionLocation"))
            distr1_distributionLocation.text = resource[18].strip()

            #  datasetDistributionInfo [o] - sizes [m]
            lrc_textSizes = SubElement(
                datasetDistributionInfo1, QName(ms, "sizes"))
            sizes = resource[19].split(";")
            sizeUnits = resource[20].split(";")
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

            # datasetDistributionInfo [o] - text formats [m+]
            print "Working on text formats " + resource[21]
            distr1_textFormats = SubElement(
                datasetDistributionInfo1, QName(ms, "textFormats"))
            textFormat_list = resource[21].split(";")
            for textFormat in textFormat_list:
                distr1_textFormatInfo = SubElement(
                    distr1_textFormats, QName(ms, "textFormatInfo"))
                distr1_dataFormatInfo = SubElement(
                    distr1_textFormatInfo, QName(ms, "dataFormatInfo"))
                distr1_dataFormat = SubElement(
                    distr1_dataFormatInfo, QName(ms, "dataFormat"))
                distr1_dataFormat.text = textFormat.strip()

    #########################
    # datasetDistributionInfo - 3 [o]
    if resource[22] != '':
        datasetDistributionInfo1 = SubElement(
            distributionInfos, QName(ms, "datasetDistributionInfo"))

        # datasetDistributionInfo [o] - distribution medium [m]
        print "Working on distribution medium " + resource[22]
        distr1_distributionMedium = SubElement(
            datasetDistributionInfo1, QName(ms, "distributionMedium"))
        distr1_distributionMedium.text = resource[22].strip()

        # datasetDistributionInfo [o] - distribution medium [o]
        if resource[23].strip() != '':
            print "Working on distribution location " + resource[23]
            distr1_distributionLocation = SubElement(
                datasetDistributionInfo1, QName(ms, "distributionLocation"))
            distr1_distributionLocation.text = resource[23].strip()

            #  datasetDistributionInfo [o] - sizes [m]
            lrc_textSizes = SubElement(
                datasetDistributionInfo1, QName(ms, "sizes"))
            sizes = resource[24].split(";")
            sizeUnits = resource[25].split(";")
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

            # datasetDistributionInfo [o] - text formats [m+]
            print "Working on text formats " + resource[26]
            distr1_textFormats = SubElement(
                datasetDistributionInfo1, QName(ms, "textFormats"))
            textFormat_list = resource[26].split(";")
            for textFormat in textFormat_list:
                distr1_textFormatInfo = SubElement(
                    distr1_textFormats, QName(ms, "textFormatInfo"))
                distr1_dataFormatInfo = SubElement(
                    distr1_textFormatInfo, QName(ms, "dataFormatInfo"))
                distr1_dataFormat = SubElement(
                    distr1_dataFormatInfo, QName(ms, "dataFormat"))
                distr1_dataFormat.text = textFormat.strip()

    ####################################
    # rightsInfo [m]
    rightsInfo = SubElement(
        lexicalConceptualResourceInfo, QName(ms, "rightsInfo"))
    licenceInfos = SubElement(
        rightsInfo, QName(ms, "licenceInfos"))
    
    # rightsInfo [m] - licenceInfo 1 [m]
    distr1_licenceInfo = SubElement(
        licenceInfos, QName(ms, "licenceInfo"))
    print "Working on licence " + resource[27]
    distr1_licence = SubElement(distr1_licenceInfo, QName(ms, "licence"))
    distr1_licence.text = resource[27].strip()
    if distr1_licence.text == "nonStandardLicenceTerms":
        assert(resource[28].strip() != "")
        print "Working on nonStandardLicenceName " + resource[28]
        distr1_nonStandardLicenceName = SubElement(
        distr1_licenceInfo, QName(ms, "nonStandardLicenceName"))
        distr1_nonStandardLicenceName.text = resource[28].strip()
        assert (resource[29].strip() != "" or resource[30].strip() != "")
        if resource[29].strip() != "" and resource[30].strip() == "":
            print "Working on nonStandardLicenceTermsURL" + resource[29]
            distr1_nonStandardLicenceTermsURL = SubElement(
                distr1_licenceInfo, QName(ms, "nonStandardLicenceTermsURL"))
            distr1_nonStandardLicenceTermsURL.text = resource[29].strip()
        elif resource[30].strip() != "" and resource[29].strip() == "":
            print "Working on nonStandardLicenceTermsText " + resource[30]
            distr1_nonStandardLicenceTermsText = SubElement(
                distr1_licenceInfo, QName(ms, "nonStandaradLicenceTermsText"))
            distr1_nonStandardLicenceTermsText.text = resource[30].strip()
        else:
            print "Both  resource[29] and resource[30] were not empty"
            assert(0)

    # rightsInfo [m] - licenceInfo 2 [o]
    if resource[31] != "":
        distr2_licenceInfo = SubElement(
            licenceInfos, QName(ms, "licenceInfo"))
        print "Working on licence " + resource[31]
        distr2_licence = SubElement(distr1_licenceInfo, QName(ms, "licence"))
        distr2_licence.text = resource[31].strip()
        if distr2_licence.text == "nonStandardLicenceTerms":
            assert(resource[32].strip() != "")
            print "Working on nonStandardLicenceName " + resource[32]
            distr2_nonStandardLicenceName = SubElement(
                distr1_licenceInfo, QName(ms, "nonStandardLicenceName"))
            distr2_nonStandardLicenceName.text = resource[32].strip()        
            assert (resource[33].strip() != "" or resource[34].strip() != "")
            if resource[33].strip() != "" and resource[34].strip() == "":
                print "Working on nonStandardLicenceTermsURL" + resource[33]
                distr2_nonStandardLicenceTermsURL = SubElement(
                    distr1_licenceInfo, QName(ms, "nonStandardLicenceTermsURL"))
                distr2_nonStandardLicenceTermsURL.text = resource[33].strip()
            elif resource[34].strip() != "" and resource[33].strip() == "":
                print "Working on nonStandardLicenceTermsText " + resource[34]
                distr2_nonStandardLicenceTermsText = SubElement(
                    distr1_licenceInfo, QName(ms, "nonStandaradLicenceTermsText"))
                distr2_nonStandardLicenceTermsText.text = resource[34].strip()
            else:
                print "Both resource[33] and resource[34] were not empty"
                assert(0)

    ###########
    # TODO Add rightsStatement rule based on info
    rightsStatement = SubElement(
        rightsInfo, QName(ms, "rightsStatement"))
    rightsStatement.text = "openAccess"
   
    
    ###################################
    # resource documentation info
    if resource[35].strip() != "":        
        resourceDocumentations = SubElement(
            lexicalConceptualResourceInfo, QName(ms, "resourceDocumentations"))
        resourceDocumentationInfo = SubElement(
            lexicalConceptualResourceInfo, QName(ms, "resourceDocumentationInfo"))       
        doc_description = SubElement(
            resourceDocumentationInfo, QName(ms, "documentationDescription"))
        doc_description.text = resource[35].strip()
        doc_documentationType = SubElement(
            resourceDocumentationInfo, QName(ms, "documentationType"))
        doc_documentationType.text = "publicationForCitation"

        doc_publicationIdentifiers = SubElement(
            resourceDocumentationInfo, QName(ms, "publicationIdentifiers"))
        publId = resource[36].split(";")
        publIdSchema = resource[37].split(";")
        assert(len(publId) == len(publIdSchema))
        for i in range(0, len(publId)):
            doc_publicationId = SubElement(
                doc_publicationIdentifiers, QName(ms, "publicationIdentifier"))
            doc_publicationId.text = publId[i].strip()
            doc_publicationId.attrib[
                "publicationIdentifierSchemeName"] = publIdSchema[i].strip()

    ##################################
    # lexicalConceptualResourceType
    assert(resource[38].strip() != "")
    resourceType = SubElement(
        lexicalConceptualResourceInfo, QName(ms, "lexicalConceptualResourceType"))
    resourceType.text = resource[38].strip()

    #################################
    # lexicalConceptualResourceEncodingInfo
    if resource[39].strip() != "":
        resourceEncodingInfo = SubElement(
            lexicalConceptualResourceInfo, QName(ms, "lexicalConceptualResourceEncodingInfo"))
        contentTypes = resource[39].split(";")
        for content in contentTypes:
            encoding_contentTypes = SubElement(
                resourceEncodingInfo, QName(ms, "contentTypes"))
            encoding_contentTypes.text = content.strip()

    ###########################################
    # lexicalConceptualResourceMediaType
  
    lrc_textInfo = SubElement(
        lexicalConceptualResourceInfo, QName(ms, "lexicalConceptualResourceTextInfo"))

    # mediaType
    lrc_textMediaType = SubElement(
        lrc_textInfo, QName(ms, "mediaType"))
    lrc_textMediaType.text = "text"

    # lingualityInfo
    assert(resource[40].strip() != "")
    lrc_textLingualityInfo = SubElement(        
        lrc_textInfo, QName(ms, "lingualityInfo"))
    lrc_textLingualityType = SubElement(
        lrc_textLingualityInfo, QName(ms, "lingualityType"))
    lrc_textLingualityType.text = resource[40].strip()

    # language tag
    assert(resource[41].strip() != "")
    lrc_textLanguages = SubElement(
        lrc_textInfo, QName(ms, "languages"))
    languages = resource[41].split(";")
    for lang in languages:
        lrc_textLanguageInfo = SubElement(
            lrc_textLanguages, QName(ms, "languageInfo"))
        lrc_textLanguage = SubElement(
            lrc_textLanguageInfo, QName(ms, "language"))
        lrc_textLanguage.text = lang.strip()
       

    # meta-language tag
    assert(resource[42].strip() != "")
    lrc_textMetaLanguages = SubElement(
        lrc_textInfo, QName(ms, "metalanguages"))
    metalanguages = resource[42].split(";")
    for metalang in metalanguages:
        lrc_textMetaLanguageInfo = SubElement(
            lrc_textMetaLanguages, QName(ms, "metalanguageInfo"))
        lrc_textMetaLanguage = SubElement(
            lrc_textMetaLanguageInfo, QName(ms, "language"))
        lrc_textMetaLanguage.text = metalang.strip()

    # Print xml
    fileXML = open("GeneratedXMLs/" +
                   resource[1].replace(" ", "") + ".xml", 'w')
    fileXML.write(tostring(root, pretty_print=True))
    fileXML.close()
#    print etree.tostring(root, pretty_print=True)
