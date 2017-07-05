import sys
import os
import csv
import re
from lxml.etree import Element, SubElement, QName, tostring

# Declaring namespaces
ms = 'http://www.meta-share.org/OMTD-SHARE_XMLSchema'
xsi = 'http://www.w3.org/2001/XMLSchema-instance'

# Read tsv file
with open("testData.tsv") as tsv:
    reader = csv.reader(tsv, dialect="excel-tab")
    data = list(reader)
    # print data[1]

for resource in data:
    print "Working on resource " + resource[0]
    # Root element
    root = Element(QName(ms, "lcrMetadataRecord"),
                   nsmap={'ms': ms, 'xsi': xsi})
    root.attrib[QName(xsi, "schemaLocation")
                ] = "http://www.meta-share.org/OMTD-SHARE_XMLSchema http://www.meta-share.org/OMTD-SHARE_XMLSchema/v200/OMTD-SHARE-LexicalConceptualResource.xsd"

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
    id_resourceNames = SubElement(
        identificationInfo, QName(ms, "resourceNames"))
    id_name = SubElement(id_resourceNames, QName(ms, "resourceName"))
    id_name.text = resource[0].strip()
    id_name.attrib["lang"] = "en"

    # identificationInfo - description [m]
    id_descriptions = SubElement(identificationInfo, QName(ms, "descriptions"))
    id_descr = SubElement(id_descriptions, QName(ms, "description"))
    id_descr.text = resource[1].strip()
    id_descr.attrib["lang"] = "en"

    # identificationInfo  - resourceShortNames [o]
    if resource[2] != '':
        id_resourceShortNames = SubElement(
            identificationInfo, QName(ms, "resourceShortNames"))
        id_shortName = SubElement(id_resourceShortNames,
                                  QName(ms, "resourceShortName"))
        id_shortName.text = resource[2].strip()
        id_shortName.attrib["lang"] = "en"

    # identificationInfo - resourceIdentifier [m+]
    id_resourceIdentifiers = SubElement(
        identificationInfo, QName(ms, "resourceIdentifiers"))
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
    # contactInfo
    contactInfo = SubElement(
        lexicalConceptualResourceInfo, QName(ms, "contactInfo"))

    # [m : (G or H or (I and J))]

    # contactInfo - generic contact email
    if resource[5] != '':
        contact_genericEmail = SubElement(
            contactInfo, QName(ms, "contactEmail"))
        contact_genericEmail.text = resource[5].strip()

    # contactInfo - landing page
    if resource[6] != '':
        contact_landingPage = SubElement(contactInfo, QName(ms, "landingPage"))
        contact_landingPage.text = resource[6].strip()

    # contactInfo - contact person name [+]
    # contactInfo - contact person email [+]
    if resource[7] != '' and resource[8] != '':
        personName = resource[7].split(";")
        personEmail = resource[8].split(";")
        assert(len(personName) == len(personEmail))
        contact_persons = SubElement(contactInfo, QName(ms, "contactPersons"))
        for i in range(0, len(personName)):
            contact_person = SubElement(
                contact_persons, QName(ms, "contactPerson"))
            # Contact Person Name
            contact_personNames = SubElement(
                contact_person, QName(ms, "names"))
            contact_personName = SubElement(
                contact_personNames, QName(ms, "name"))
            contact_personName.text = personName[i].strip()
            # Contact Person Email
            contact_communication = SubElement(
                contact_person, QName(ms, "communicationInfo"))
            contact_communicationEmails = SubElement(
                contact_communication, QName(ms, "emails"))
            contact_communicationEmail = SubElement(
                contact_communicationEmails, QName(ms, "email"))
            contact_communicationEmail.text = personEmail[i].strip()

    ###########################
    # versionInfo
    versionInfo = SubElement(
        lexicalConceptualResourceInfo, QName(ms, "versionInfo"))

    # [m: (K or L)]

    # versionInfo - version
    if resource[9] != '':
        versionInfo_version = SubElement(versionInfo, QName(ms, "version"))
        versionInfo_version.text = resource[9].strip()

    # versionInfo - version date
    if resource[10] != '':
        versionInfo_versionDate = SubElement(
            versionInfo, QName(ms, "versionDate"))
        versionInfo_versionDate.text = resource[10].strip()

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
    distr1_distributionMedium.text = resource[11].strip()

    if resource[12].strip() != '':
        distr1_distributionLocation = SubElement(
            distr1_distributionLocationExternal, QName(ms, "distributionLocation"))
        distr1_distributionLocation.text = resource[12].strip()

    # datasetDistributionInfo - text formats [o+]
    if resource[13].strip() != '':
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

    license_list = resource[14].split(";")
    for license in license_list:
        distr1_licenceInfo = SubElement(
            distr1_licenceInfos, QName(ms, "licenceInfo"))
        distr1_licence = SubElement(distr1_licenceInfo, QName(ms, "licence"))
        distr1_licence.text = license.strip()
        if distr1_licence.text == "nonStandardLicenceTerms":
            assert(resource[15].strip() != "")
            distr1_nonStandardLicenceName = SubElement(
                distr1_licenceInfo, QName(ms, "nonStandardLicenceName"))
            distr1_nonStandardLicenceName.text = resource[15].strip()
            distr1_nonStandardLicenceName.attrib["lang"] = "en"
            assert (resource[16].strip() != "" or resource[17].strip() != "")
            if resource[16].strip() != "":
                distr1_nonStandardLicenceTermsURL = SubElement(
                    distr1_licenceInfo, QName(ms, "nonStandardLicenceTermsURL"))
                distr1_nonStandardLicenceTermsURL.text = resource[16].strip()
            if resource[17].strip() != "":
                distr1_nonStandardLicenceTermsText = SubElement(
                    distr1_licenceInfo, QName(ms, "nonStandardLicenceTermsText"))
                distr1_nonStandardLicenceTermsText.text = resource[17].strip()

    #########################
    # datasetDistributionInfo [o]
    if resource[18].strip() != "":
        datasetDistributionInfo2 = SubElement(
            distributionInfos, QName(ms, "datasetDistributionInfo"))

    # datasetDistributionInfo - distribution location [m]
        distr2_distributionLocationExternal = SubElement(
            datasetDistributionInfo2, QName(ms, "distributionLoc"))

        distr2_distributionMedium = SubElement(
            distr2_distributionLocationExternal, QName(ms, "distributionMedium"))
        distr2_distributionMedium.text = resource[18].strip()

        if resource[19].strip() != '':
            distr2_distributionLocation = SubElement(
                distr2_distributionLocationExternal, QName(ms, "distributionLocation"))
            distr2_distributionLocation.text = resource[19].strip()

        # datasetDistributionInfo - text formats [o+]
        if resource[20].strip() != '':
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

        license_list = resource[21].split(";")
        for license in license_list:
            distr2_licenceInfo = SubElement(
                distr2_licenceInfos, QName(ms, "licenceInfo"))
            distr2_licence = SubElement(
                distr2_licenceInfo, QName(ms, "licence"))
            distr2_licence.text = license.strip()
            if distr2_licence.text == "nonStandardLicenceTerms":
                assert(resource[22].strip() != "")
                distr2_nonStandardLicenceName = SubElement(
                    distr2_licenceInfo, QName(ms, "nonStandardLicenceName"))
                distr2_nonStandardLicenceName.text = resource[22].strip()
                distr2_nonStandardLicenceName.attrib["lang"] = "en"
                assert (resource[23].strip() !=
                        "" or resource[24].strip() != "")
                if resource[23].strip() != "":
                    distr2_nonStandardLicenceTermsURL = SubElement(
                        distr2_licenceInfo, QName(ms, "nonStandardLicenceTermsURL"))
                    distr2_nonStandardLicenceTermsURL.text = resource[
                        23].strip()
                if resource[24].strip() != "":
                    distr2_nonStandardLicenceTermsText = SubElement(
                        distr2_licenceInfo, QName(ms, "nonStandardLicenceTermsText"))
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
        distr3_distributionMedium.text = resource[25].strip()

        if resource[26].strip() != '':
            distr3_distributionLocation = SubElement(
                distr3_distributionLocationExternal, QName(ms, "distributionLocation"))
            distr3_distributionLocation.text = resource[26].strip()

        # datasetDistributionInfo - text formats [o+]
        if resource[27].strip() != '':
            distr3_textFormats = SubElement(
                datasetDistributionInfo3, QName(ms, "textFormats"))
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

        license_list = resource[28].split(";")
        for license in license_list:
            distr3_licenceInfo = SubElement(
                distr3_licenceInfos, QName(ms, "licenceInfo"))
            distr3_licence = SubElement(
                distr3_licenceInfo, QName(ms, "licence"))
            distr3_licence.text = license.strip()
            if distr3_licence.text == "nonStandardLicenceTerms":
                assert(resource[29].strip() != "")
                distr3_nonStandardLicenceName = SubElement(
                    distr3_licenceInfo, QName(ms, "nonStandardLicenceName"))
                distr3_nonStandardLicenceName.text = resource[29].strip()
                distr3_nonStandardLicenceName.attrib["lang"] = "en"
                assert (resource[30].strip() !=
                        "" or resource[31].strip() != "")
                if resource[30].strip() != "":
                    distr3_nonStandardLicenceTermsURL = SubElement(
                        distr3_licenceInfo, QName(ms, "nonStandardLicenceTermsURL"))
                    distr3_nonStandardLicenceTermsURL.text = resource[
                        30].strip()
                if resource[31].strip() != "":
                    distr3_nonStandardLicenceTermsText = SubElement(
                        distr3_licenceInfo, QName(ms, "nonStandardLicenceTermsText"))
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
            doc_publicationId.text = publId[i].strip()
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

    #################
    # Print xml
    fileXML = open("GeneratedXMLs/" +
                   resource[0].replace(" ", "") + ".xml", 'w')
    fileXML.write(tostring(root, pretty_print=True))
    fileXML.close()
