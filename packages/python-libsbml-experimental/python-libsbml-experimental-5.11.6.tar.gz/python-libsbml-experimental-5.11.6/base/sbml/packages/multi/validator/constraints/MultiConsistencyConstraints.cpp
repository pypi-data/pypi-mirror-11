  /** @cond doxygenLibsbmlInternal */

/**
 * @file:   MultiConsistencyConstraints.cpp
 * @brief:  Implementation of the MultiConsistencyConstraints class
 * @author: Fengkai Zhang
 *
 * <!--------------------------------------------------------------------------
 * This file is part of libSBML.  Please visit http://sbml.org for more
 * information about SBML, and the latest version of libSBML.
 *
 * Copyright (C) 2009-2013 jointly by the following organizations:
 *     1. California Institute of Technology, Pasadena, CA, USA
 *     2. EMBL European Bioinformatics Institute (EMBL-EBI), Hinxton, UK
 *
 * Copyright (C) 2006-2008 by the California Institute of Technology,
 *     Pasadena, CA, USA 
 *
 * Copyright (C) 2002-2005 jointly by the following organizations:
 *     1. California Institute of Technology, Pasadena, CA, USA
 *     2. Japan Science and Technology Agency, Japan
 *
 * This library is free software; you can redistribute it and/or modify it
 * under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation.  A copy of the license agreement is provided
 * in the file named "LICENSE.txt" included with this software distribution
 * and also available online as http://sbml.org/software/libsbml/license.html
 * ------------------------------------------------------------------------ -->
 */

#ifndef  AddingConstraintsToValidator

#include <sbml/validator/VConstraint.h>
#include <sbml/packages/multi/common/MultiExtensionTypes.h>


#endif  /* AddingConstrainstToValidator */

#include <sbml/validator/ConstraintMacros.h>
#include <sbml/packages/multi/validator/MultiSBMLError.h>

/** @cond doxygenIgnored */

using namespace std;
LIBSBML_CPP_NAMESPACE_USE


static bool __isSpeciesTypeComponent(const Model & model, const std::string & componentId)
{
  bool found = false;
  const MultiModelPlugin * mPlugin =
      static_cast<const MultiModelPlugin*>(model.getPlugin("multi"));
  if (mPlugin != 0) {
      for (unsigned int i = 0; !found && i < mPlugin->getNumMultiSpeciesTypes(); i++) {
          const MultiSpeciesType * speciesType = mPlugin->getMultiSpeciesType(i);
          if (speciesType) {
              if (speciesType->getId() == componentId) {
                  found = true;
              }

              // check instance
              for (unsigned int j = 0; !found && j < speciesType->getNumSpeciesTypeInstances(); j++) {
                  const SpeciesTypeInstance * speciesTypeInstance = speciesType->getSpeciesTypeInstance(j);
                  if (speciesTypeInstance && speciesTypeInstance->getId() ==  componentId) {
                      found = true;
                  }
              }

              // check index
              for (unsigned int j = 0; !found && j < speciesType->getNumSpeciesTypeComponentIndexes(); j++) {
                  const SpeciesTypeComponentIndex * speciesTypeComponentIndex = speciesType->getSpeciesTypeComponentIndex(j);
                  if (speciesTypeComponentIndex && speciesTypeComponentIndex->getId() ==  componentId) {
                      found = true;
                  }
              }
          }
      }
  }
  return found;
}

static bool __isSpeciesTypeIndexComponent(const Model & model, const std::string & componentId)
{
  bool found = false;
  const MultiModelPlugin * mPlugin =
      static_cast<const MultiModelPlugin*>(model.getPlugin("multi"));
  if (mPlugin != 0) {
      for (unsigned int i = 0; !found && i < mPlugin->getNumMultiSpeciesTypes(); i++) {
          const MultiSpeciesType * speciesType = mPlugin->getMultiSpeciesType(i);
          if (speciesType) {

              // check index
              for (unsigned int j = 0; !found && j < speciesType->getNumSpeciesTypeComponentIndexes(); j++) {
                  const SpeciesTypeComponentIndex * speciesTypeComponentIndex = speciesType->getSpeciesTypeComponentIndex(j);
                  if (speciesTypeComponentIndex && speciesTypeComponentIndex->getId() ==  componentId) {
                      found = true;
                  }
              }
          }
      }
  }
  return found;
}

static bool __isSpeciesTypeInstanceOrIndex(const Model & model, const std::string & componentId)
{
  bool found = false;
  const MultiModelPlugin * mPlugin =
      static_cast<const MultiModelPlugin*>(model.getPlugin("multi"));
  if (mPlugin != 0) {
      for (unsigned int i = 0; !found && i < mPlugin->getNumMultiSpeciesTypes(); i++) {
          const MultiSpeciesType * speciesType = mPlugin->getMultiSpeciesType(i);
          if (speciesType) {

              // check instance
              for (unsigned int j = 0; !found && j < speciesType->getNumSpeciesTypeInstances(); j++) {
                  const SpeciesTypeInstance * speciesTypeInstance = speciesType->getSpeciesTypeInstance(j);
                  if (speciesTypeInstance && speciesTypeInstance->getId() ==  componentId) {
                      found = true;
                  }
              }

              // check index
              for (unsigned int j = 0; !found && j < speciesType->getNumSpeciesTypeComponentIndexes(); j++) {
                  const SpeciesTypeComponentIndex * speciesTypeComponentIndex = speciesType->getSpeciesTypeComponentIndex(j);
                  if (speciesTypeComponentIndex && speciesTypeComponentIndex->getId() ==  componentId) {
                      found = true;
                  }
              }
          }
      }
  }
  return found;
}

static bool __isSpeciesTypeComponent(const Model & model, const std::string & speciesTypeId,const std::string & componentId)
{
        bool isComponent = false;
        bool good = true;

        const MultiModelPlugin * modelPlugin =
                        static_cast<const MultiModelPlugin*>(model.getPlugin("multi"));

        if (modelPlugin == 0) {
                good = false;
        }

        const MultiSpeciesType * speciesType = 0;
        if (good) {
                 speciesType = modelPlugin->getMultiSpeciesType(speciesTypeId);
        }

        if (speciesType == 0) {
                good = false;
        }

        if (good) {
                for(unsigned int i = 0; good && !isComponent && i < speciesType->getNumSpeciesTypeInstances(); i++) {
                        const SpeciesTypeInstance * speciesTypeInstance = speciesType->getSpeciesTypeInstance(i);
                        if (speciesTypeInstance->getId() == componentId) {
                                isComponent = true;
                        }
                        else {
                                std::string refSpeciesTypeId = speciesTypeInstance->getSpeciesType();
                                isComponent = __isSpeciesTypeComponent(model, refSpeciesTypeId, componentId);
                        }
                }

                for(unsigned int i = 0; good && !isComponent && i < speciesType->getNumSpeciesTypeComponentIndexes(); i++) {
                        const SpeciesTypeComponentIndex * speciesTypeComponentIndex = speciesType->getSpeciesTypeComponentIndex(i);
                        if (speciesTypeComponentIndex->getId() == componentId) {
                                isComponent = true;
                        }
                }
        }

        return isComponent;
}


static bool __isSpeciesFeature(const Model & model, const std::string & speciesId,const std::string & speciesFeatureId)
{
        bool isSpeciesFeature = false;
        bool good = true;


        const Species * species = 0;
        if (good) {
                 species = model.getSpecies(speciesId);
        }

        if (species == 0) {
                good = false;
        }

        if (good) {
            const MultiSpeciesPlugin * speciesPlugin =
                static_cast<const MultiSpeciesPlugin*>(species->getPlugin("multi"));

            if (speciesPlugin == 0) {
                    good = false;
            }

            for(unsigned int i = 0; good && !isSpeciesFeature && i < speciesPlugin->getNumSpeciesFeatures(); i++) {
                const SpeciesFeature * speciesFeature = speciesPlugin->getSpeciesFeature(i);
                if (speciesFeature->getId() == speciesFeatureId) {
                        isSpeciesFeature = true;
                }
            }
        }

        return isSpeciesFeature;
}



/** @endcond */

/** PUT CONSTRAINTS HERE */

//************************************
// General rules about the Multi package

// MultiNSUndeclared                     = 7010101 - inexplicitly checked at read when creating plugin at 'SBMLDocument::readAttributes()'
// MultiElementNotInNs                   = 7010102 - inexplicitly checked at read when creating plugin at 'SBMLDocument::readAttributes()'
// MultiSBML_RequiredAttMissing          = 7010103 - caught at read at 'MultiSBMLDocumentPlugin::readAttributes()'
// MultiSBML_RequiredAttMustBeBoolean    = 7010104 - caught at read at 'MultiSBMLDocumentPlugin::readAttributes()'
// MultiSBML_RequiredAttMustBeTrue       = 7010105 - caught at read at 'MultiSBMLDocumentPlugin::readAttributes()'

//************************************
// Rules for extended Model objects

// MultiLofStps_OnlyOne                  = 7020101 - caught at read at 'MultiModelPlugin::createObject()'
// MultiLofStps_NoEmpty                  = 7020102 - caught at read at 'SBase::checkListOfPopulated()', TODO: need update if core is revised.
// MultiLofStps_AllowedAtts              = 7020103 - caught at read at 'MultiSpeciesType::readAttributes()'
// MultiLofStps_AllowedElts              = 7020104 - caught at read at 'SBase::logUnknownElement()'

//************************************
// Rules for extended Compartment objects

// MultiExCpa_AllowedMultiAtts           = 7020201 - caught at read at 'MultiCompartmentPlugin::readAttributes()'
// MultiExCpa_IsTypeAtt_Invalid          = 7020202 - caught at read at 'MultiCompartmentPlugin::readAttributes()'
// MultiExCpa_IsTypeAtt_Required         = 7020203 - caught at read at 'MultiCompartmentPlugin::readAttributes()'

// MultiExCpa_IsTypeAtt_SameAsParent     = 7020204
/* !< Extended Compartment: 'isType' attribute, if referenced, must be same as that of the containing compartment */

START_CONSTRAINT (MultiExCpa_IsTypeAtt_SameAsParent, Compartment, compartment)
{
  const MultiCompartmentPlugin * compPlug =
    static_cast<const MultiCompartmentPlugin*>(compartment.getPlugin("multi"));

  pre (compPlug != 0);

  std::string parentCompartmentId = compartment.getId();
  bool parentCompartmentIsType = compPlug->isSetIsType() && compPlug->getIsType();

  for (unsigned int i = 0; i < compPlug->getNumCompartmentReferences(); i++) {
      const CompartmentReference * cRef = compPlug->getCompartmentReference(i);
      std::string referencedCompartmentId = cRef->getCompartment();
      const Compartment * referencedCompartment = m.getCompartment(referencedCompartmentId);

      const MultiCompartmentPlugin * referencedCompPlug =
        static_cast<const MultiCompartmentPlugin*>(referencedCompartment->getPlugin("multi"));
      bool referencedCompartmentIsType = referencedCompPlug->isSetIsType() && referencedCompPlug->getIsType();

      inv(parentCompartmentIsType == referencedCompartmentIsType);
  }
}
END_CONSTRAINT

// MultiExCpa_CpaTypAtt_Restrict         = 7020205
/*!< Extended Compartment: Compartment type can not reference another compartment type */

START_CONSTRAINT (MultiExCpa_CpaTypAtt_Restrict, Compartment, compartment)
{
  const MultiCompartmentPlugin * compPlug =
    static_cast<const MultiCompartmentPlugin*>(compartment.getPlugin("multi"));

  pre (compPlug != 0);

  const bool isType = compPlug->isSetIsType() && compPlug->getIsType();
  if (isType) {
      inv(compPlug->isSetCompartmentType() == false);
  }
}
END_CONSTRAINT

// MultiLofCpaRefs_OnlyOne               = 7020206 - caught at read at 'MultiCompartmentPlugin::createObject()'
// MultiLofCpaRefs_NoEmpty               = 7020207 - caught at read at 'SBase::checkListOfPopulated()', TODO: need update if core is revised.
// MultiLofCpaRefs_AllowedAtts           = 7020208 - caught at read at 'CompartmentReference::readAttributes()'
// MultiLofCpaRefs_AllowedElts           = 7020209 - caught at read at 'SBase::logUnknownElement()'

//************************************
// Rules for CompartmentReference objects

// MultiCpaRef_AllowedCoreAtts           = 7020301 - caught at read at 'CompartmentReference::readAttributes()'
// MultiCpaRef_AllowedCoreElts           = 7020302 - caught at read at 'SBase::logUnknownElement()'
// MultiCpaRef_AllowedMultiAtts          = 7020303 - caught at read at 'CompartmentReference::readAttributes()'

// MultiCpaRef_CompartmentAtt_Ref        = 7020304
/*!< CompartmentReference: 'compartment' must be the 'id' of a compartment */

START_CONSTRAINT (MultiCpaRef_CompartmentAtt_Ref, CompartmentReference, compartmentReference)
{
  std::string compartmentId = compartmentReference.getCompartment();
  inv(m.getCompartment(compartmentId) != 0);
}
END_CONSTRAINT

// MultiCpaRef_IdRequiredOrOptional      = 7020305
/*!< CompartmentReference: 'multi:id' is required when referencing the same compartment */

START_CONSTRAINT (MultiCpaRef_IdRequiredOrOptional, ListOfCompartmentReferences, listOfCompartmentReferences)
{
  for (unsigned int i = 0; i < listOfCompartmentReferences.size(); i++) {
      const CompartmentReference * compartmentReference = listOfCompartmentReferences.get(i);
      for (unsigned int j = i + 1; j < listOfCompartmentReferences.size(); j++) {
          const CompartmentReference * anotherCompartmentReference = listOfCompartmentReferences.get(j);
          if (compartmentReference->getCompartment() == anotherCompartmentReference->getCompartment()) {
              inv(compartmentReference->isSetId() == true);
              inv(anotherCompartmentReference->isSetId() == true);
          }
      }
  }
}
END_CONSTRAINT

//************************************
// Rules for SpeciesType objects

// MultiSpt_AllowedCoreAtts              = 7020401 - caught at read at 'MultiSpeciesType::readAttributes()'
// MultiSpt_AllowedCoreElts              = 7020402 - caught at read at 'SBase::logUnknownElement()'
// MultiSpt_AllowedMultiAtts             = 7020403 - caught at read at 'MultiSpeciesType::readAttributes()'

// MultiSpt_CompartmentAtt_Ref           = 7020404
/*!< SpeciesType: 'compartment' must be the 'id' of a compartment */

START_CONSTRAINT (MultiSpt_CompartmentAtt_Ref, MultiSpeciesType, speciesType)
{
  if (!speciesType.isSetCompartment()) return;

  std::string compartmentId = speciesType.getCompartment();
  inv(m.getCompartment(compartmentId) != 0);
}
END_CONSTRAINT

// MultiSpt_ListOfDefs_NoEmpty           = 7020405 - caught at read at 'SBase::checkListOfPopulated()', TODO: need update if core is revised.
// MultiLofSpeFtrTyps_onlyOne            = 7020406 - caught at read at 'MultiSpeciesType::createObject()'
// MultiLofSpeFtrTyps_Elts               = 7020407 - caught at read at 'SBase::logUnknownElement()'
// MultiLofSpeFtrTyps_AllowedAtts        = 7020408 - caught at read at 'SpeciesFeatureType::readAttributes()'
// MultiLofSptInss_onlyOne               = 7020409 - caught at read at 'MultiSpeciesType::createObject()'
// MultiLofSptInss_Elts                  = 7020410 - caught at read at 'SBase::logUnknownElement()'
// MultiLofSptInss_AllowedAtts           = 7020411 - caught at read at 'SpeciesTypeInstance::readAttributes()'
// MultiLofSptCpoInds_onlyOne            = 7020412 - caught at read at 'MultiSpeciesType::createObject()'
// MultiLofSptCpoInds_Elts               = 7020413 - caught at read at 'SBase::logUnknownElement()'
// MultiLofSptCpoInds_AllowedAtts        = 7020414 - caught at read at 'SpeciesTypeComponentIndex::readAttributes()'
// MultiLofInSptBnds_onlyOne             = 7020415 - caught at read at 'MultiSpeciesType::createObject()'
// MultiLofInSptBnds_Elts                = 7020416 - caught at read at 'SBase::logUnknownElement()'
// MultiLofInSptBnds_AllowedAtts         = 7020417 - caught at read at 'InSpeciesTypeBond::readAttributes()'

//************************************
// Rules for BindingSiteSpeciesType objects

// MultiBstSpt_Restrict                  = 7020501
/*!< BindingSiteSpeciesType: Not permitted to have listOfSpeciesTypeInstances */

START_CONSTRAINT (MultiBstSpt_Restrict, BindingSiteSpeciesType, bindingSiteSpeciesType)
{
  inv(bindingSiteSpeciesType.getNumSpeciesTypeInstances() == 0);
}
END_CONSTRAINT

//************************************
// Rules for SpeciesFeatureType objects

// MultiSpeFtrTyp_AllowedCoreAtts        = 7020601 - caught at read at 'MultiSpeciesFeatureType::readAttributes()'
// MultiSpeFtrTyp_AllowedCoreElts        = 7020602 - caught at read at 'SBase::logUnknownElement()'
// MultiSpeFtrTyp_AllowedMultiAtts       = 7020603 - caught at read at 'MultiSpeciesFeatureType::readAttributes()'
// MultiSpeFtrTyp_OccAtt_Ref             = 7020604 - caught at read at 'MultiSpeciesFeatureType::readAttributes()'

// MultiSpeFtrTyp_RestrictElt            = 7020605
/*!< SpeciesFeatureType: Required to have one listOfPossibleSpeciesFeatureValues */

START_CONSTRAINT (MultiSpeFtrTyp_RestrictElt, SpeciesFeatureType, speciesFeatureType)
{
  inv(speciesFeatureType.getNumPossibleSpeciesFeatureValues() > 0);
}
END_CONSTRAINT

// MultiLofPsbSpeFtrVals_AllowedAtts     = 7020606 - caught at read at 'PossibleSpeciesFeatureValue::readAttributes()'
// MultiLofPsbSpeFtrVals_Elts            = 7020607 - caught at read at 'SBase::logUnknownElement()'
// MultiLofPsbSpeFtrVals_NoEmpty         = 7020608 - caught at read at 'SBase::checkListOfPopulated()', TODO: need update if core is revised.

//************************************
// Rules for PossibleSpeciesFeatureValue objects

// MultiPsbSpeFtrVal_AllowedCoreAtts     = 7020701 - caught at read at 'PossibleSpeciesFeatureValue::readAttributes()'
// MultiPsbSpeFtrVal_AllowedCoreElts     = 7020702 - caught at read at 'SBase::logUnknownElement()'
// MultiPsbSpeFtrVal_AllowedMultiAtts    = 7020703 - caught at read at 'PossibleSpeciesFeatureValue::readAttributes()'

// MultiPsbSpeFtrVal_NumAtt_Ref          = 7020704
/*!< PossibleSpeciesFeatureValue: 'numbericValue' must be the 'id' of a parameter */

START_CONSTRAINT (MultiPsbSpeFtrVal_NumAtt_Ref, PossibleSpeciesFeatureValue, possibleSpeciesFeatureValue)
{
  std::string numericValueId = possibleSpeciesFeatureValue.getNumericValue();
  inv(m.getParameter(numericValueId) != 0);
}
END_CONSTRAINT

//************************************
// Rules for SpeciesTypeInstance objects

// MultiSptIns_AllowedCoreAtts           = 7020801 - caught at read at 'SpeciesTypeInstance::readAttributes()'
// MultiSptIns_AllowedCoreElts           = 7020802 - caught at read at 'SBase::logUnknownElement()'
// MultiSptIns_AllowedMultiAtts          = 7020803 - caught at read at 'SpeciesTypeInstance::readAttributes()'
// MultiSptIns_OccAtt_Ref                = 7020804 - caught at read at 'SpeciesTypeInstance::readAttributes()'

// MultiSptIns_SptAtt_Ref                = 7020805
/*!< SpeciesTypeInstance: 'speciesType' must be the 'id' of a speciesType */

START_CONSTRAINT (MultiSptIns_SptAtt_Ref, SpeciesTypeInstance, speciesTypeInstance)
{
  std::string speciesTypeId = speciesTypeInstance.getSpeciesType();
  const MultiModelPlugin * mPlugin =
      static_cast<const MultiModelPlugin*>(m.getPlugin("multi"));

  pre (mPlugin != 0);

  inv(mPlugin->getMultiSpeciesType(speciesTypeId) != 0);
}
END_CONSTRAINT

// MultiSptIns_CpaRefAtt_Ref             = 7020806
/*!< SpeciesTypeInstance: 'compartmentReference' must be the 'id' of a compartmentReference */

START_CONSTRAINT (MultiSptIns_CpaRefAtt_Ref, SpeciesTypeInstance, speciesTypeInstance)
{

  bool found = !speciesTypeInstance.isSetCompartmentReference();

  if (!found) {
      std::string compartmentReferenceId = speciesTypeInstance.getCompartmentReference();

      for (unsigned int i = 0; !found && i < m.getNumCompartments(); i++) {

        const MultiCompartmentPlugin * compartmentPlugin =
            static_cast<const MultiCompartmentPlugin*>(m.getCompartment(i)->getPlugin("multi"));

        if (compartmentPlugin != 0) {
            if (compartmentPlugin->getCompartmentReference(compartmentReferenceId)) {
                found = true;
            }
        }
      }
  }

  inv(found == true);
}
END_CONSTRAINT


//************************************
// Rules for SpeciesTypeComponentIndex objects

// MultiSptCpoInd_AllowedCoreAtts        = 7020901 - caught at read at 'SpeciesTypeComponentIndex::readAttributes()'
// MultiSptCpoInd_AllowedCoreElts        = 7020902 - caught at read at 'SBase::logUnknownElement()'
// MultiSptCpoInd_AllowedMultiAtts       = 7020903 - caught at read at 'SpeciesTypeComponentIndex::readAttributes()'

// MultiSptCpoInd_CpoAtt_Ref             = 7020904
/*!< SpeciesTypeComponentIndex: 'component' must be the 'id' of a component */

START_CONSTRAINT (MultiSptCpoInd_CpoAtt_Ref, SpeciesTypeComponentIndex, speciesTypeComponentIndex)
{
  std::string componentId = speciesTypeComponentIndex.getComponent();
  bool found = __isSpeciesTypeComponent(m, componentId);
  inv (found == true);
}
END_CONSTRAINT

// MultiSptCpoInd_RestrictElts           = 7020905
/*!< SpeciesTypeComponentIndex: Can not have a listOfDenotedSpeciesTypeComponentIndexes if component references an index  */

START_CONSTRAINT (MultiSptCpoInd_RestrictElts, SpeciesTypeComponentIndex, speciesTypeComponentIndex)
{
  const std::string componentId = speciesTypeComponentIndex.getComponent();
  if( __isSpeciesTypeIndexComponent(m, componentId)) {
      inv (speciesTypeComponentIndex.getNumDenotedSpeciesTypeComponentIndexes() == 0);
  }
}
END_CONSTRAINT

// MultiSptCpoInd_SameOccurAsRefIndex    = 7020906
/*!< SpeciesTypeComponentIndex: 'occur' attribute must have the same value as that of the referenced index */

START_CONSTRAINT (MultiSptCpoInd_SameOccurAsRefIndex, SpeciesTypeComponentIndex, speciesTypeComponentIndex)
{
  const MultiModelPlugin * mPlugin =
      static_cast<const MultiModelPlugin*>(m.getPlugin("multi"));

  pre (mPlugin != 0);

  const std::string componentId = speciesTypeComponentIndex.getComponent();
  unsigned int indexOccur = speciesTypeComponentIndex.getOccur();

  bool found = false;
  for (unsigned int i = 0; !found && i < mPlugin->getNumMultiSpeciesTypes(); i++) {
      const MultiSpeciesType * multiSpeciesType = mPlugin->getMultiSpeciesType(i);

      for (unsigned j = 0; !found && j < multiSpeciesType->getNumSpeciesTypeComponentIndexes(); j++) {
          const SpeciesTypeComponentIndex * index = multiSpeciesType->getSpeciesTypeComponentIndex(j);
          if (componentId == index->getId()) {
              found = true;
              inv (indexOccur == index->getOccur());
          }
      }
  }
}
END_CONSTRAINT

// MultiSptCpoInd_IdParAtt_Ref           = 7020907
/*!< SpeciesTypeComponentIndex: 'identifyingParent' must be the 'id' of a component */

START_CONSTRAINT (MultiSptCpoInd_IdParAtt_Ref, SpeciesTypeComponentIndex, speciesTypeComponentIndex)
{
  if (speciesTypeComponentIndex.isSetIdentifyingParent()) {
      std::string identifyingParentId = speciesTypeComponentIndex.getIdentifyingParent();
      bool found = __isSpeciesTypeComponent(m, identifyingParentId);
      inv (found == true);
  }
}
END_CONSTRAINT

// MultiSptCpoInd_OccAtt_Ref             = 7020908 - caught at read at 'SpeciesTypeComponentIndex::readAttributes()'
// MultiLofDenSptCpoInds_NoEmpty         = 7020909 - caught at read at 'SBase::checkListOfPopulated()', TODO: need update if core is revised.
// MultiLofDenSptCpoInds_AllowedAtts     = 7020910 - caught at read at 'DenotedSpeciesTypeComponentIndex::readAttributes()'
// MultiLofDenSptCpoInds_Elts            = 7020911 - caught at read at 'SBase::logUnknownElement()'

//************************************
// Rules for DenotedSpeciesTypeComponentIndex objects

// MultiDenSptCpoInd_AllowedCoreAtts     = 7021001 - caught at read at 'DenotedSpeciesTypeComponentIndex::readAttributes()'
// MultiDenSptCpoInd_AllowedCoreElts     = 7021002 - caught at read at 'SBase::logUnknownElement()'
// MultiDenSptCpoInd_AllowedMultiAtts    = 7021003 - caught at read at 'DenotedSpeciesTypeComponentIndex::readAttributes()'

// MultiDenSptCpoInd_SpTypeCpoIndAtt_Ref = 7021004
/*!< DenotedSpeciesTypeComponentIndex: 'speciesTypeComponentIndex' must the 'id' of a speciesTypeComponentIndex */

START_CONSTRAINT (MultiDenSptCpoInd_SpTypeCpoIndAtt_Ref, DenotedSpeciesTypeComponentIndex, denotedSpeciesTypeComponentIndex)
{
  std::string speciesTypeComponentIndexId = denotedSpeciesTypeComponentIndex.getSpeciesTypeComponentIndex();
  inv( __isSpeciesTypeIndexComponent(m, speciesTypeComponentIndexId) == true);
}
END_CONSTRAINT

//************************************
// Rules for InSpeciesTypeBond objects

// MultiInSptBnd_AllowedCoreAtts         = 7021101 - caught at read at 'InSpeciesTypeBond::readAttributes()'
// MultiInSptBnd_AllowedCoreElts         = 7021102 - caught at read at 'SBase::logUnknownElement()'
// MultiInSptBnd_AllowedMultiAtts        = 7021103 - caught at read at 'InSpeciesTypeBond::readAttributes()'

// MultiInSptBnd_Bst1Att_Ref             = 7021104
/*!< InSpeciesTypeBond: 'bindingSite1' must be the 'id' of a speciesTypeInstance or speciesTypeComponentIndex */

START_CONSTRAINT (MultiInSptBnd_Bst1Att_Ref, InSpeciesTypeBond, inSpeciesTypeBond)
{
  std::string bindingSite1Id = inSpeciesTypeBond.getBindingSite1();
  inv( __isSpeciesTypeInstanceOrIndex(m, bindingSite1Id) == true);
}
END_CONSTRAINT

// MultiInSptBnd_Bst2Att_Ref             = 7021105
/*!< InSpeciesTypeBond: 'bindingSite2' must be the 'id' of a speciesTypeInstance or speciesTypeComponentIndex */

START_CONSTRAINT (MultiInSptBnd_Bst2Att_Ref, InSpeciesTypeBond, inSpeciesTypeBond)
{
  std::string bindingSite2Id = inSpeciesTypeBond.getBindingSite2();
  inv( __isSpeciesTypeInstanceOrIndex(m, bindingSite2Id) == true);
}
END_CONSTRAINT

// MultiInSptBnd_TwoBstAtts_NotSame      = 7021106
/*!< InSpeciesTypeBond: 'bindingSite1' and 'bindingSite2' can not reference the same binding site */

START_CONSTRAINT (MultiInSptBnd_TwoBstAtts_NotSame, InSpeciesTypeBond, inSpeciesTypeBond)
{
  std::string bindingSite1Id = inSpeciesTypeBond.getBindingSite1();
  std::string bindingSite2Id = inSpeciesTypeBond.getBindingSite2();
  inv( bindingSite1Id != bindingSite2Id);
}
END_CONSTRAINT

//************************************
// Rules for extended Species objects

// MultiExSpe_AllowedMultiAtts           = 7021201 - caught at read at 'MultiSpeciesPlugin::readAttributes()'

// MultiExSpe_RestrictSpeciesTypeAtt     = 7021202
/*!< Extended Species: SpeciesType attribute must have value of the id of a speciesType */

START_CONSTRAINT (MultiExSpe_RestrictSpeciesTypeAtt, Species, species)
{
  const MultiSpeciesPlugin * speciesPlugin =
      static_cast<const MultiSpeciesPlugin*>(species.getPlugin("multi"));

  pre (speciesPlugin != 0);

  if (speciesPlugin->isSetSpeciesType()) {
      std::string speciesTypeId = speciesPlugin->getSpeciesType();

      const MultiModelPlugin * mPlugin =
          static_cast<const MultiModelPlugin*>(m.getPlugin("multi"));

      pre (mPlugin != 0);

      inv (mPlugin->getMultiSpeciesType(speciesTypeId) != 0);
  }
}
END_CONSTRAINT

// MultiExSpe_NoEmptyListOfDefs          = 7021203 - caught at read at 'SBase::checkListOfPopulated()', TODO: need update if core is revised.
// MultiLofOutBsts_AllowedAtts           = 7021204 - caught at read at 'OutwardBindingSite::readAttributes()'
// MultiLofOutBsts_AllowedElts           = 7021205 - caught at read at 'SBase::logUnknownElement()'
// MultiLofSpeFtrs_AllowedCoreAtts       = 7021206 - caught at read at 'SpeciesFeature::readAttributes()'
// MultiLofSpeFtrs_AllowedMultiAtts      = 7021207 - caught at read at 'SpeciesFeature::readAttributes()'
// MultiLofSpeFtrs_RelationAtt_Ref       = 7021208 - caught at read at 'ListOfSpeciesFeatures::readAttributes()'
// MultiLofSpeFtrs_AllowedElts           = 7021209 - caught at read at 'SBase::logUnknownElement()'

//************************************
// Rules for OutwardBindingSite objects

// MultiOutBst_AllowedCoreAtts           = 7021301 - caught at read at 'OutwardBindingSite::readAttributes()'
// MultiOutBst_AllowedCoreElts           = 7021302 - caught at read at 'SBase::logUnknownElement()'
// MultiOutBst_AllowedMultiAtts          = 7021303 - caught at read at 'OutwardBindingSite::readAttributes()'
// MultiOutBst_BdgStaAtt_Ref             = 7021304 - caught at read at 'OutwardBindingSite::readAttributes()'

// MultiOutBst_CpoAtt_Ref                = 7021305
/*!< OutwardBindingSite: 'component' must be the 'id' of a 'BindingSiteSpeciesType' component */

START_CONSTRAINT (MultiOutBst_CpoAtt_Ref, OutwardBindingSite, outwardBindingSite)
{
  const MultiModelPlugin * mPlugin =
      static_cast<const MultiModelPlugin*>(m.getPlugin("multi"));

  pre (mPlugin != 0);

  std::string bindingSiteSpeciesTypeId = outwardBindingSite.getComponent();

  const MultiSpeciesType * speciesType = mPlugin->getMultiSpeciesType(bindingSiteSpeciesTypeId);
  const BindingSiteSpeciesType * bSpeciesType = static_cast<const BindingSiteSpeciesType *> (speciesType);

  inv(bSpeciesType != 0);
}
END_CONSTRAINT

//************************************
// Rules for SpeciesFeature objects

// MultiSpeFtr_AllowedCoreAtts           = 7021401 - caught at read at 'SpeciesFeature::readAttributes()'
// MultiSpeFtr_AllowedCoreElts           = 7021402 - caught at read at 'SBase::logUnknownElement()'
// MultiSpeFtr_AllowedMultiAtts          = 7021403 - caught at read at 'SpeciesFeature::readAttributes()'

// MultiSpeFtr_SpeFtrTypAtt_Ref          = 7021404
/*!< SpeciesFeature: 'speciesFeatureType' must be the 'id' of a speciesFeatureType */

START_CONSTRAINT (MultiSpeFtr_SpeFtrTypAtt_Ref, SpeciesFeature, speciesFeature)
{
  const MultiModelPlugin * mPlugin =
      static_cast<const MultiModelPlugin*>(m.getPlugin("multi"));

  pre (mPlugin != 0);

  std::string speciesFeatureTypeId = speciesFeature.getSpeciesFeatureType();

  bool found = false;

  for (unsigned int i = 0; !found && i < mPlugin->getNumMultiSpeciesTypes(); i++ ) {
      const MultiSpeciesType * speciesType = mPlugin->getMultiSpeciesType(i);
      for (unsigned int j = 0; !found && j < speciesType->getNumSpeciesFeatureTypes(); j++) {
          const SpeciesFeatureType * speciesFeatureType = speciesType->getSpeciesFeatureType(j);
          if (speciesFeatureType->getId() == speciesFeatureTypeId) {
              found = true;
          }
      }
  }

  inv(found == true);
}
END_CONSTRAINT

// MultiSpeFtr_OccAtt_Ref                = 7021405
/*!< SpeciesFeature: 'occur' must be a positiveInteger with restriction */

START_CONSTRAINT (MultiSpeFtr_OccAtt_Ref, SpeciesFeature, speciesFeature)
{
  const MultiModelPlugin * mPlugin =
      static_cast<const MultiModelPlugin*>(m.getPlugin("multi"));

  pre (mPlugin != 0);

  std::string sftId = speciesFeature.getSpeciesFeatureType();
  unsigned int sfOccur = speciesFeature.getOccur();
  unsigned int sftOccur = 0;

  const SBase * sbaseListOfSpeciesFeatures = speciesFeature.getParentSBMLObject();
  pre (sbaseListOfSpeciesFeatures != 0);

  const SBase * sbaseSpecies = sbaseListOfSpeciesFeatures->getParentSBMLObject();
  pre (sbaseSpecies != 0);

  const Species * species = static_cast<const Species *> (sbaseSpecies);
  pre (species != 0);

  const MultiSpeciesPlugin * spPlugin =
      static_cast<const MultiSpeciesPlugin*>(species->getPlugin("multi"));
  pre (spPlugin !=0);

  std::string sptId = spPlugin->getSpeciesType();

  bool found = false;
  for (unsigned int i = 0; !found && i < mPlugin->getNumMultiSpeciesTypes(); i++) {
      const MultiSpeciesType * spt = mPlugin->getMultiSpeciesType(i);
      if (sptId == spt->getId()) {
          for (unsigned int j = 0; !found && j < spt->getNumSpeciesFeatureTypes(); j++) {
              const SpeciesFeatureType * sft = spt->getSpeciesFeatureType(j);
              if (sftId == sft->getId()) {
                  found = true;
                  sftOccur = sft->getOccur();
              }
          }
      }
  }

  pre (found == true);

  inv (sftOccur >= sfOccur);
}
END_CONSTRAINT

// MultiSpeFtr_CpoAtt_Ref                = 7021406
/*< SpeciesFeature: 'component' must be the 'id' of a component */

START_CONSTRAINT (MultiSpeFtr_CpoAtt_Ref, SpeciesFeature, speciesFeature)
{
  if (speciesFeature.isSetComponent()) {
      std::string componentId = speciesFeature.getComponent();
      bool found = __isSpeciesTypeComponent(m, componentId);
      inv (found == true);
  }
}
END_CONSTRAINT

// MultiSpeFtr_RestrictElts              = 7021407
/*!< SpeciesFeature: Required one listOfSpeciesFeatureValues  */

START_CONSTRAINT (MultiSpeFtr_RestrictElts, SpeciesFeature, speciesFeature)
{
  inv (speciesFeature.getNumSpeciesFeatureValues() > 0);
}
END_CONSTRAINT

// MultiLofSpeFtrVals_NoEmpty            = 7021408 - caught at read at 'SBase::checkListOfPopulated()', TODO: need update if core is revised.
// MultiLofSpeFtrVals_AllowedAtts        = 7021409 - caught at read at 'SpeciesFeatureValue::readAttributes()'
// MultiLofSpeFtrVals_AllowedElts        = 7021410 - caught at read at 'SBase::logUnknownElement()'

//************************************
// Rules for SpeciesFeatureValue objects

// MultiSpeFtrVal_AllowedCoreAtts        = 7021501 - caught at read at 'SpeciesFeatureValue::readAttributes()'
// MultiSpeFtrVal_AllowedCoreElts        = 7021502 - caught at read at 'SBase::logUnknownElement()'
// MultiSpeFtrVal_AllowedMultiAtts       = 7021503 - caught at read at 'SpeciesFeatureValue::readAttributes()'

// MultiSpeFtrVal_ValAtt_Ref             = 7021504
/*!< SpeciesFeatureValue: 'value' must be the 'id' of a possibleSpeciesFeatureValue */

START_CONSTRAINT (MultiSpeFtrVal_ValAtt_Ref, SpeciesFeatureValue, speciesFeatureValue)
{
  const MultiModelPlugin * mPlugin =
      static_cast<const MultiModelPlugin*>(m.getPlugin("multi"));

  pre (mPlugin != 0);

  std::string sfv_value = speciesFeatureValue.getValue();

  const SBase * sbaseListOfSpeciesFeatureValues = speciesFeatureValue.getParentSBMLObject();
  pre(sbaseListOfSpeciesFeatureValues != 0);

  const SBase * sbaseSpeciesFeature = sbaseListOfSpeciesFeatureValues->getParentSBMLObject();
  pre (sbaseSpeciesFeature != 0);

  const SpeciesFeature * speciesFeature = static_cast<const SpeciesFeature *> (sbaseSpeciesFeature);
  pre (speciesFeature != 0);

  std::string sftId = speciesFeature->getSpeciesFeatureType();

  const SBase * sbaseListOfSpeciesFeatures = sbaseSpeciesFeature->getParentSBMLObject();
  pre (sbaseListOfSpeciesFeatures != 0);

  const SBase * sbaseSpecies = sbaseListOfSpeciesFeatures->getParentSBMLObject();
  pre (sbaseSpecies != 0);

  const Species * species = static_cast<const Species *> (sbaseSpecies);
  pre (species != 0);

  const MultiSpeciesPlugin * spPlugin =
      static_cast<const MultiSpeciesPlugin*>(species->getPlugin("multi"));
  pre (spPlugin !=0);

  std::string sptId = spPlugin->getSpeciesType();

  bool found = false;
  for (unsigned int i = 0; !found && i < mPlugin->getNumMultiSpeciesTypes(); i++) {
      const MultiSpeciesType * spt = mPlugin->getMultiSpeciesType(i);
      if (sptId == spt->getId()) {
          for (unsigned int j = 0; !found && j < spt->getNumSpeciesFeatureTypes(); j++) {
              const SpeciesFeatureType * sft = spt->getSpeciesFeatureType(j);
              if (sftId == sft->getId()) {
                  for (unsigned int m = 0; !found && m < sft->getNumPossibleSpeciesFeatureValues(); m++) {
                      const PossibleSpeciesFeatureValue * pValue = sft->getPossibleSpeciesFeatureValue(m);
                      if (sfv_value == pValue->getId()) {
                          found = true;
                      }
                  }
                  pre (found == true);
              }
          }
      }
  }

  inv (found == true);
}
END_CONSTRAINT

//************************************
// Rules for IntraSpeciesReaction objects

// MultiIntSpeRec_AllowedAtts            = 7021601 - caught at read at 'IntraSpeciesReaction::readAttributes()'
// MultiIntSpeRec_AllowedCoreElts        = 7021602 - caught at read at 'SBase::logUnknownElement()'

//************************************
// Rules for extended SimpleSpeciesReference objects

// MultiExSplSpeRef_AllowedMultiAtts     = 7021701 - caught at read at 'MultiSimpleSpeciesReferencePlugin::readAttributes()'

// MultiExSplSpeRef_CpaRefAtt_Ref        = 7021702
/* !< Extended SimpleSpeciesReference: 'compartmentReference' must be the 'id' of a compartmentReference */

START_CONSTRAINT (MultiExSplSpeRef_CpaRefAtt_Ref, SimpleSpeciesReference, simpleSpeciesReference)
{

  const MultiSimpleSpeciesReferencePlugin * simpleSpeciesRefPlugin =
      static_cast<const MultiSimpleSpeciesReferencePlugin*>(m.getPlugin("multi"));

  pre (simpleSpeciesRefPlugin != 0);

  if (simpleSpeciesRefPlugin->isSetCompartmentReference()) {
      std::string compRefId = simpleSpeciesRefPlugin->getCompartmentReference();

      bool found = false;
      for (unsigned int i = 0; !found && i < m.getNumCompartments(); i++) {
          const Compartment * compartment = m.getCompartment(i);
          const MultiCompartmentPlugin * compartmentPlugin =
              static_cast<const MultiCompartmentPlugin*>(compartment->getPlugin("multi"));
          if (compartmentPlugin != 0) {
              for (unsigned int j = 0; !found && j < compartmentPlugin->getNumCompartmentReferences(); j++) {
                  const CompartmentReference * compartmentRef = compartmentPlugin->getCompartmentReference(j);
                  if (compartmentRef->isSetId() && compartmentRef->getId() == compRefId) {
                      found = true;
                  }
              }
          }
      }

      inv (found == true);
  }
}
END_CONSTRAINT

//************************************
// Rules for extended SpeciesReference objects

// MultiLofSptCpoMapsInPro_NoEmpty       = 7021801 - caught at read at 'SBase::checkListOfPopulated()', TODO: need update if core is revised.
// MultiLofSptCpoMapsInPro_AllowedAtts   = 7021802 - caught at read at 'SpeciesTypeComponentMapInProduct::readAttributes()'
// MultiLofSptCpoMapsInPro_AllowedElts   = 7021803 - caught at read at 'SBase::logUnknownElement()'

//************************************
// Rules for SpeciesTypeComponentMapInProduct objects

// MultiSptCpoMapInPro_AllowedCoreAtts   = 7021901 - caught at read at 'SpeciesTypeComponentMapInProduct::readAttributes()'
// MultiSptCpoMapInPro_AllowedCoreElts   = 7021902 - caught at read at 'SBase::logUnknownElement()'
// MultiSptCpoMapInPro_AllowedMultiAtts  = 7021903 - caught at read at 'SpeciesTypeComponentMapInProduct::readAttributes()'

// MultiSptCpoMapInPro_RctAtt_Ref        = 7021904
/*!< SpeciesTypeComponentMapInProduct: 'reactant' must be the 'id' of a reactant speciesReference */

START_CONSTRAINT (MultiSptCpoMapInPro_RctAtt_Ref, SpeciesTypeComponentMapInProduct, speciesTypeComponentMapInProduct)
{
	std::string reactantId = speciesTypeComponentMapInProduct.getReactant();
	bool good = true;

	const SBase * sbaseListOfSpeciesTypeComponentMapsInProduct = speciesTypeComponentMapInProduct.getParentSBMLObject();
	if (sbaseListOfSpeciesTypeComponentMapsInProduct == 0) {
		good = false;
	}

	const SBase * sbaseSpeciesReference = 0;
	if (good) {
		sbaseSpeciesReference = sbaseListOfSpeciesTypeComponentMapsInProduct->getParentSBMLObject();
		if (sbaseSpeciesReference == 0) {
			good = false;
		}
	}

	const SBase * sbaseListOfSpeciesReferences = 0;
	if (good) {
		sbaseListOfSpeciesReferences = sbaseSpeciesReference->getParentSBMLObject();
		if (sbaseListOfSpeciesReferences == 0) {
			good = false;
		}
	}

	const Reaction * reaction = 0;
	if (good) {
		const SBase * sbaseReaction = sbaseListOfSpeciesReferences->getParentSBMLObject();
		reaction = static_cast<const Reaction *> (sbaseReaction);
		if (reaction == 0) {
			good = false;
		}
	}

	if (good) {
		bool found = false;
		for (unsigned int i = 0; !found && i < reaction->getNumReactants(); i++) {
			const SpeciesReference * sRef = reaction->getReactant(i);
			if (sRef != 0 && sRef->isSetId() && sRef->getId() == reactantId) {
				found = true;
			}
		}
		good = found;
	}
	inv(good == true);
}
END_CONSTRAINT

// MultiSptCpoMapInPro_RctCpoAtt_Ref     = 7021905
/*!< SpeciesTypeComponentMapInProduct: 'reactantComponent' must be the 'id' of a reactant component */

START_CONSTRAINT (MultiSptCpoMapInPro_RctCpoAtt_Ref, SpeciesTypeComponentMapInProduct, speciesTypeComponentMapInProduct)
{
	std::string reactantId = speciesTypeComponentMapInProduct.getReactant();
	std::string reactantComponentId = speciesTypeComponentMapInProduct.getReactantComponent();

	bool good = true;

	// parent of map -- list
	const SBase * sbaseListOfSpeciesTypeComponentMapsInProduct = 0;
	if (good) {
		sbaseListOfSpeciesTypeComponentMapsInProduct = speciesTypeComponentMapInProduct.getParentSBMLObject();
		if (sbaseListOfSpeciesTypeComponentMapsInProduct == 0) {
			good = false;
		}
	}

	// parent of map list -- speciesReference
	const SBase * sbaseSpeciesReference = 0;
	if (good) {
		sbaseSpeciesReference = sbaseListOfSpeciesTypeComponentMapsInProduct->getParentSBMLObject();
		if (sbaseSpeciesReference == 0) {
			good = false;
		}
	}

	// parent of speciesReference -- list
	const SBase * sbaseListOfSpeciesReferences = 0;
	if (good) {
		sbaseListOfSpeciesReferences = sbaseSpeciesReference->getParentSBMLObject();
		if (sbaseListOfSpeciesReferences == 0) {
			good = false;
		}
	}

	// parent of speciesReference list -- reaction
	const Reaction * reaction = 0;
	if (good) {
		const SBase * sbaseReaction = sbaseListOfSpeciesReferences->getParentSBMLObject();
		reaction = static_cast<const Reaction *> (sbaseReaction);
		if (reaction == 0) {
			good = false;
		}
	}

	// do real work here
	if (good) {
		bool found = false;

		// scan reactants
		for (unsigned int i = 0; !found && good && i < reaction->getNumReactants(); i++) {
			const SpeciesReference * sRef = reaction->getReactant(i);

			// reactant found
			if (sRef != 0 && sRef->isSetId() && sRef->getId() == reactantId) {
				// species
				const std::string speciesId = sRef->getSpecies();
				const Species * species = m.getSpecies(speciesId);
				if (species == 0) {
					good = false;
				}
				else {
					const MultiSpeciesPlugin * speciesPlugin =
							static_cast<const MultiSpeciesPlugin*>(species->getPlugin("multi"));
					if (speciesPlugin == 0) {
						good = false;
					}
					else {
						// speciesType
						std::string speciesTypeId = speciesPlugin->getSpeciesType();
						found = __isSpeciesTypeComponent(m, speciesTypeId, reactantComponentId);
					}
				}
			}
		}
		good = found;
	}
	inv(good == true);
}
END_CONSTRAINT

// MultiSptCpoMapInPro_ProCpoAtt_Ref     = 7021906
/*!< SpeciesTypeComponentMapInProduct: 'productComponent' must be the 'id' of a product component */

START_CONSTRAINT (MultiSptCpoMapInPro_ProCpoAtt_Ref, SpeciesTypeComponentMapInProduct, speciesTypeComponentMapInProduct)
{
	std::string productComponentId = speciesTypeComponentMapInProduct.getProductComponent();

	bool good = true;

	// must have model extended
	const MultiModelPlugin * modelPlugin =
			static_cast<const MultiModelPlugin*>(m.getPlugin("multi"));
	if (modelPlugin == 0) {
		good = false;
	}

	// parent of map -- list
	const SBase * sbaseListOfSpeciesTypeComponentMapsInProduct = 0;
	if (good) {
		sbaseListOfSpeciesTypeComponentMapsInProduct = speciesTypeComponentMapInProduct.getParentSBMLObject();
		if (sbaseListOfSpeciesTypeComponentMapsInProduct == 0) {
			good = false;
		}
	}

	// parent of map list -- speciesReference
	const SBase * sbaseSpeciesReference = 0;
	if (good) {
		sbaseSpeciesReference = sbaseListOfSpeciesTypeComponentMapsInProduct->getParentSBMLObject();
		const SpeciesReference * speciesReference =
				static_cast<const SpeciesReference*> (sbaseSpeciesReference);
		if (speciesReference == 0) {
			good = false;
		}
		else {
			std::string speciesId = speciesReference->getSpecies();
			const Species * species = m.getSpecies(speciesId);
			if (species == 0) {
				good = false;
			}
			else {
				const MultiSpeciesPlugin * speciesPlugin =
						static_cast<const MultiSpeciesPlugin*>(species->getPlugin("multi"));
				if (speciesPlugin == 0) {
					good = false;
				}
				else {
					std::string speciesTypeId = speciesPlugin->getSpeciesType();
					good = __isSpeciesTypeComponent(m, speciesId, productComponentId);
				}
			}
		}
	}
	inv(good == true);
}
END_CONSTRAINT

// MultiLofSpeFtrChgs_NoEmpty            = 7021907 - caught at read at 'SBase::checkListOfPopulated()', TODO: need update if core is revised.
// MultiLofSpeFtrChgs_AllowedAtts        = 7021908 - caught at read at 'SpeciesFeatureChange::readAttributes()'
// MultiLofSpeFtrChgs_AllowedElts        = 7021909 - caught at read at 'SBase::logUnknownElement()'

//************************************
// Rules for SpeciesFeatureChange objects

// MultiSpeFtrChg_AllowedCoreAtts        = 7022001 - caught at read at 'SpeciesFeatureChange::readAttributes()'
// MultiSpeFtrChg_AllowedCoreElts        = 7022002 - caught at read at 'SBase::logUnknownElement()'
// MultiSpeFtrChg_AllowedMultiAtts       = 7022003 - caught at read at 'SpeciesFeatureChange::readAttributes()'

// MultiSpeFtrChg_RctSpeFtrAtt_Ref       = 7022004
/*!< SpeciesFeatureChange: 'reactantSpeciesFeature' must be the 'id' of a speciesFeature */

START_CONSTRAINT (MultiSpeFtrChg_RctSpeFtrAtt_Ref, SpeciesFeatureChange, speciesFeatureChange)
{
    std::string reactantSpeciesFeatureId =
        speciesFeatureChange.getReactantSpeciesFeature();

    bool good = true;

    // must have model extended
    const MultiModelPlugin * modelPlugin =
        static_cast<const MultiModelPlugin*>(m.getPlugin("multi"));
    if (modelPlugin == 0)
      {
        good = false;
      }

    // parent of map -- list
    const SBase * sbaseListOfSpeciesFeatureChanges = 0;
    if (good)
      {
        sbaseListOfSpeciesFeatureChanges =
            speciesFeatureChange.getParentSBMLObject();
        if (sbaseListOfSpeciesFeatureChanges == 0)
          {
            good = false;
          }
      }

    // parent of map list -- speciesReference
    const SBase * sbaseSpeciesTypeComponentMapInProduct = 0;
    if (good)
      {
        sbaseSpeciesTypeComponentMapInProduct =
            sbaseListOfSpeciesFeatureChanges->getParentSBMLObject();

        if (sbaseSpeciesTypeComponentMapInProduct == 0)
          {
            good = false;
          }
        else
          {
            const SBase * sbaseSpeciesReference =
                sbaseSpeciesTypeComponentMapInProduct->getParentSBMLObject();

            if (sbaseSpeciesReference == 0)
              {
                good = false;
              }
            else
              {
                const SpeciesReference * speciesReference =
                    static_cast<const SpeciesReference*>(sbaseSpeciesReference);
                if (speciesReference == 0)
                  {
                    good = false;
                  }
                else
                  {
                    std::string speciesId = speciesReference->getSpecies();
                    good = __isSpeciesFeature(m, speciesId,
                        reactantSpeciesFeatureId);
                  }
              }
          }
      }
    inv(good == true);
  }
END_CONSTRAINT

// MultiSpeFtrChg_ProSpeFtrAtt_Ref       = 7022005
/*!< SpeciesFeatureChange: 'productSpeciesFeature' must be the 'id' of a speciesFeature */

START_CONSTRAINT (MultiSpeFtrChg_ProSpeFtrAtt_Ref, SpeciesFeatureChange, speciesFeatureChange)
{
    std::string productSpeciesFeatureId =
        speciesFeatureChange.getReactantSpeciesFeature();

    bool good = true;

    // must have model extended
    const MultiModelPlugin * modelPlugin =
        static_cast<const MultiModelPlugin*>(m.getPlugin("multi"));
    if (modelPlugin == 0)
      {
        good = false;
      }

    // parent of map -- list
    const SBase * sbaseListOfSpeciesFeatureChanges = 0;
    if (good)
      {
        sbaseListOfSpeciesFeatureChanges =
            speciesFeatureChange.getParentSBMLObject();
        if (sbaseListOfSpeciesFeatureChanges == 0)
          {
            good = false;
          }
      }

    // parent of map list -- speciesReference
    const SBase * sbaseSpeciesTypeComponentMapInProduct = 0;
    if (good)
      {
        sbaseSpeciesTypeComponentMapInProduct =
            sbaseListOfSpeciesFeatureChanges->getParentSBMLObject();

        if (sbaseSpeciesTypeComponentMapInProduct == 0)
          {
            good = false;
          }
        else
          {
            const SBase * sbaseSpeciesReference =
                sbaseSpeciesTypeComponentMapInProduct->getParentSBMLObject();

            if (sbaseSpeciesReference == 0)
              {
                good = false;
              }
            else
              {
                const SpeciesReference * speciesReference =
                    static_cast<const SpeciesReference*>(sbaseSpeciesReference);
                if (speciesReference == 0)
                  {
                    good = false;
                  }
                else
                  {
                    std::string speciesId = speciesReference->getSpecies();
                    good = __isSpeciesFeature(m, speciesId,
                        productSpeciesFeatureId);
                  }
              }
          }
      }
    inv(good == true);
  }
END_CONSTRAINT

//************************************
// Rules for extended ci elements in Math objects

// MultiMathCi_AllowedMultiAtts          = 7022101 /*!< Math ci element: Allowed Multi attributes */

// MultiMathCi_SpeRefAtt_Ref             = 7022102
/*!< Math ci element: 'speciesReference' must be the 'id' of a speciesReference */

START_CONSTRAINT (MultiMathCi_SpeRefAtt_Ref, ASTNode, astNode)
{
  bool isSpeciesReference = true;
  const MultiASTPlugin * astPlugin = static_cast<const MultiASTPlugin*>(astNode.getPlugin("multi"));

  if (astPlugin == 0) {
      isSpeciesReference = false;
  }
  else {
      std::string speciesReferenceId = astPlugin->getSpeciesReference();

      const SBase * sbaseKineticLaw = astNode.getParentSBMLObject();
      if (sbaseKineticLaw == 0) {
          isSpeciesReference = false;
      }
      else {
          const SBase * sbaseReaction = sbaseKineticLaw->getParentSBMLObject();
          if (sbaseReaction == 0) {
              isSpeciesReference = false;
          }
          else {
              const Reaction * reaction = static_cast<const Reaction*> (sbaseReaction);
              isSpeciesReference = false;

              if (reaction != 0) {
                  for (unsigned int i = 0; !isSpeciesReference && i < reaction->getNumReactants(); i++) {
                      const SpeciesReference * reactant = reaction->getReactant(i);
                      if (reactant != 0 && reactant->isSetId()) {
                          std::string reactantId = reactant->getId();
                          if (speciesReferenceId == reactantId) {
                              isSpeciesReference = true;
                          }
                      }
                  }

                  for (unsigned int i = 0; !isSpeciesReference && i < reaction->getNumProducts(); i++) {
                      const SpeciesReference * product = reaction->getProduct(i);
                      if (product != 0 && product->isSetId()) {
                          std::string productId = product->getId();
                          if (speciesReferenceId == productId) {
                              isSpeciesReference = true;
                          }
                      }
                  }
              }

          }
      }
  }

  inv(isSpeciesReference == true);
}
END_CONSTRAINT

// MultiMathCi_RepTypAtt_Ref             = 7022102 /*!< Math ci element: 'representationType' must be a value of the Multi data type 'RepresentationType' */

  /** @endcond doxygenLibsbmlInternal */


