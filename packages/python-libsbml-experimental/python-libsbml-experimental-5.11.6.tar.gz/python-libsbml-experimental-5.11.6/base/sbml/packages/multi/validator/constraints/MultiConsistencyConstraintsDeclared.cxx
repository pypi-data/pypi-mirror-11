/**
 * @cond doxygenLibsbmlInternal
 *
 * @file    MultiConsistencyConstraintsDeclared.cxx
 * @brief   Declarations of constraints
 * @author  Fengkai Zhang
 * @author  SBML Team
 * 
 * <!--------------------------------------------------------------------------
 * This file is part of libSBML.  Please visit http://sbml.org for more
 * information about SBML, and the latest version of libSBML.
 *
 * Copyright (C) 2013-2014 jointly by the following organizations:
 *     1. California Institute of Technology, Pasadena, CA, USA
 *     2. EMBL European Bioinformatics Institute (EMBL-EBI), Hinxton, UK
 *     3. University of Heidelberg, Heidelberg, Germany
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
 * ---------------------------------------------------------------------- -->*/

// MultiExCpa_IsTypeAtt_SameAsParent     = 7020204
addConstraint(new VConstraintCompartmentMultiExCpa_IsTypeAtt_SameAsParent(*this));

// MultiExCpa_CpaTypAtt_Restrict         = 7020205
addConstraint(new VConstraintCompartmentMultiExCpa_CpaTypAtt_Restrict(*this));

// MultiCpaRef_CompartmentAtt_Ref        = 7020304
addConstraint(new VConstraintCompartmentReferenceMultiCpaRef_CompartmentAtt_Ref(*this));

// MultiCpaRef_IdRequiredOrOptional      = 7020305
addConstraint(new VConstraintListOfCompartmentReferencesMultiCpaRef_IdRequiredOrOptional(*this));

// MultiSpt_CompartmentAtt_Ref           = 7020404
addConstraint(new VConstraintMultiSpeciesTypeMultiSpt_CompartmentAtt_Ref(*this));

// MultiBstSpt_Restrict                  = 7020501
addConstraint(new VConstraintBindingSiteSpeciesTypeMultiBstSpt_Restrict(*this));

// MultiSpeFtrTyp_RestrictElt            = 7020605
addConstraint(new VConstraintSpeciesFeatureTypeMultiSpeFtrTyp_RestrictElt(*this));

// MultiPsbSpeFtrVal_NumAtt_Ref          = 7020704
addConstraint(new VConstraintPossibleSpeciesFeatureValueMultiPsbSpeFtrVal_NumAtt_Ref(*this));

// MultiSptIns_SptAtt_Ref                = 7020805
addConstraint(new VConstraintSpeciesTypeInstanceMultiSptIns_SptAtt_Ref(*this));

// MultiSptIns_CpaRefAtt_Ref             = 7020806
addConstraint(new VConstraintSpeciesTypeInstanceMultiSptIns_CpaRefAtt_Ref(*this));

// MultiSptCpoInd_CpoAtt_Ref             = 7020904
addConstraint(new VConstraintSpeciesTypeComponentIndexMultiSptCpoInd_CpoAtt_Ref(*this));

// MultiSptCpoInd_RestrictElts           = 7020905
addConstraint(new VConstraintSpeciesTypeComponentIndexMultiSptCpoInd_RestrictElts(*this));

// MultiSptCpoInd_SameOccurAsRefIndex    = 7020906
addConstraint(new VConstraintSpeciesTypeComponentIndexMultiSptCpoInd_SameOccurAsRefIndex(*this));

// MultiSptCpoInd_IdParAtt_Ref           = 7020907
addConstraint(new VConstraintSpeciesTypeComponentIndexMultiSptCpoInd_IdParAtt_Ref(*this));

// MultiDenSptCpoInd_SpTypeCpoIndAtt_Ref = 7021004
addConstraint(new VConstraintDenotedSpeciesTypeComponentIndexMultiDenSptCpoInd_SpTypeCpoIndAtt_Ref(*this));

// MultiInSptBnd_Bst1Att_Ref             = 7021104
addConstraint(new VConstraintInSpeciesTypeBondMultiInSptBnd_Bst1Att_Ref(*this));

// MultiInSptBnd_Bst2Att_Ref             = 7021105
addConstraint(new VConstraintInSpeciesTypeBondMultiInSptBnd_Bst2Att_Ref(*this));

// MultiInSptBnd_TwoBstAtts_NotSame      = 7021106
addConstraint(new VConstraintInSpeciesTypeBondMultiInSptBnd_TwoBstAtts_NotSame(*this));

// MultiExSpe_RestrictSpeciesTypeAtt     = 7021202
addConstraint(new VConstraintSpeciesMultiExSpe_RestrictSpeciesTypeAtt(*this));

// MultiOutBst_CpoAtt_Ref                = 7021305
addConstraint(new VConstraintOutwardBindingSiteMultiOutBst_CpoAtt_Ref(*this));

// MultiSpeFtr_SpeFtrTypAtt_Ref          = 7021404
addConstraint(new VConstraintSpeciesFeatureMultiSpeFtr_SpeFtrTypAtt_Ref(*this));

// MultiSpeFtr_OccAtt_Ref                = 7021405
addConstraint(new VConstraintSpeciesFeatureMultiSpeFtr_OccAtt_Ref(*this));

// MultiSpeFtr_CpoAtt_Ref                = 7021406
addConstraint(new VConstraintSpeciesFeatureMultiSpeFtr_CpoAtt_Ref(*this));

// MultiSpeFtr_RestrictElts              = 7021407
addConstraint(new VConstraintSpeciesFeatureMultiSpeFtr_RestrictElts(*this));

// MultiSpeFtrVal_ValAtt_Ref             = 7021504
addConstraint(new VConstraintSpeciesFeatureValueMultiSpeFtrVal_ValAtt_Ref(*this));

// MultiExSplSpeRef_CpaRefAtt_Ref        = 7021702
addConstraint(new VConstraintSimpleSpeciesReferenceMultiExSplSpeRef_CpaRefAtt_Ref(*this));

// MultiSptCpoMapInPro_RctAtt_Ref        = 7021904
addConstraint(new VConstraintSpeciesTypeComponentMapInProductMultiSptCpoMapInPro_RctAtt_Ref(*this));

// MultiSptCpoMapInPro_RctCpoAtt_Ref     = 7021905
addConstraint(new VConstraintSpeciesTypeComponentMapInProductMultiSptCpoMapInPro_RctCpoAtt_Ref(*this));

// MultiSptCpoMapInPro_ProCpoAtt_Ref     = 7021906
addConstraint(new VConstraintSpeciesTypeComponentMapInProductMultiSptCpoMapInPro_ProCpoAtt_Ref(*this));

// MultiSpeFtrChg_RctSpeFtrAtt_Ref       = 7022004
addConstraint(new VConstraintSpeciesFeatureChangeMultiSpeFtrChg_RctSpeFtrAtt_Ref(*this));

// MultiSpeFtrChg_ProSpeFtrAtt_Ref       = 7022005
addConstraint(new VConstraintSpeciesFeatureChangeMultiSpeFtrChg_ProSpeFtrAtt_Ref(*this));

// MultiMathCi_SpeRefAtt_Ref             = 7022102
addConstraint(new VConstraintASTNodeMultiMathCi_SpeRefAtt_Ref(*this));



/** @endcond */

