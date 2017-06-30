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

# for resource in data:
#    print resource

resource = data[1]

# Root element
root = Element(QName(ms, "lcrMetadataRecord"), nsmap={'ms': ms, 'xsi': xsi})
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
id_resourceNames = SubElement(identificationInfo, QName(ms, "resourceNames"))
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
        identificationInfo, QName(ms, "resouceShortNames"))
    id_shortName = SubElement(id_resourceShortNames,
                              QName(ms, "resourceShortName"))
    id_shortName.text = resource[2].strip()
    id_shortName.attrib["lang"] = "en"

# identificationInfo - resourceIdentifier [m+]
id_resourceIdentifiers = SubElement(
    identificationInfo, QName(ms, "resourcesIdentifiers"))
resourceId = resource[3].split(";")
resourceIdSchema = resource[4].split(";")
assert(len(resourceId) == len(resourceIdSchema))
for i in range(0, len(resourceId)):
    id_resourceId = SubElement(
        id_resourceIdentifiers, QName(ms, "resourcesIdentifier"))
    id_resourceId.text = resourceId[i].strip()
    id_resourceId.attrib[
        "resourceIdentifierSchemeName"] = resourceIdSchema[i].strip()

###########################
# contactInfo
contactInfo = SubElement(
    lexicalConceptualResourceInfo, QName(ms, "contactInfo"))

# [m : (G or H or (I and J))]

# contactInfo - generic contact email
if resource[5] != '':
    contact_genericEmail = SubElement(contactInfo, QName(ms, "contactEmail"))
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
        contact_personNames = SubElement(contact_person, QName(ms, "names"))
        contact_personName = SubElement(contact_personNames, QName(ms, "name"))
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
distributionInfo = SubElement(
    lexicalConceptualResourceInfo, QName(ms, "distributionInfo"))

#########################
# datasetDistributionInfo [m]
datasetDistributionInfo1 = SubElement(
    distributionInfo, QName(ms, "datasetDistributionInfo"))

# datasetDistributionInfo - distribution location [m]
distr1_distributionLocationExternal = SubElement(
    datasetDistributionInfo1, QName(ms, "distributionLoc"))

distr1_distributionMedium = SubElement(
    distr1_distributionLocationExternal, QName(ms, "distributionMedium"))
distr1_distributionMedium.text = resource[11].strip()

if resource[12] != '':
    distr1_distributionLocation = SubElement(
        distr1_distributionLocationExternal, QName(ms, "distributionLocation"))
    distr1_distributionLocation.text = resource[12].strip()


# datasetDistributionInfo - text formats [o+]
if resource[13] != '':
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
distr1_licencesInfo = SubElement(distr1_rightsInfo, QName(ms, "licencesInfo"))
license_list = resource[14].split(";")
for license in license_list:
    distr1_licence = SubElement(distr1_licencesInfo, QName(ms, "licence"))
    distr1_licence.text = license

# Print xml
print tostring(root, pretty_print=True)
