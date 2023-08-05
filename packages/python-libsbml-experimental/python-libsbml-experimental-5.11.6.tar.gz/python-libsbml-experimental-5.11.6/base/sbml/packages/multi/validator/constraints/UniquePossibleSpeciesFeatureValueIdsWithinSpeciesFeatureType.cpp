/**
 * @cond doxygenLibsbmlInternal
 *
 * @file    UniquePossibleSpeciesFeatureValueIdsWithinSpeciesFeatureType.cpp
 * @brief   Ensures the PossibleSpeciesFeatureValue ids within a SpeciesFeatureType are unique
 * @author  Fengkai Zhang
 * 
 * <!--------------------------------------------------------------------------
 * This file is part of libSBML.  Please visit http://sbml.org for more
 * information about SBML, and the latest version of libSBML.
 *
 * Copyright (C) 2013-2015 jointly by the following organizations:
 *     1. California Institute of Technology, Pasadena, CA, USA
 *     2. EMBL European Bioinformatics Institute (EMBL-EBI), Hinxton, UK
 *     3. University of Heidelberg, Heidelberg, Germany
 * 
 * Copyright 2011-2012 jointly by the following organizations:
 *     1. California Institute of Technology, Pasadena, CA, USA
 *     2. EMBL European Bioinformatics Institute (EMBL-EBI), Hinxton, UK
 *
 * This library is free software; you can redistribute it and/or modify it
 * under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation.  A copy of the license agreement is provided
 * in the file named "LICENSE.txt" included with this software distribution
 * and also available online as http://sbml.org/software/libsbml/license.html
 * ---------------------------------------------------------------------- -->*/

#include <sbml/Model.h>
#include "UniquePossibleSpeciesFeatureValueIdsWithinSpeciesFeatureType.h"

/** @cond doxygenIgnored */

using namespace std;

/** @endcond */

LIBSBML_CPP_NAMESPACE_BEGIN
#ifdef __cplusplus

/*
 * Creates a new Constraint with the given constraint id.
 */
UniquePossibleSpeciesFeatureValueIdsWithinSpeciesFeatureType::UniquePossibleSpeciesFeatureValueIdsWithinSpeciesFeatureType (unsigned int id, MultiValidator& v) :
  UniqueMultiIdBase(id, v)
{
}


/*
 * Destroys this Constraint.
 */
UniquePossibleSpeciesFeatureValueIdsWithinSpeciesFeatureType::~UniquePossibleSpeciesFeatureValueIdsWithinSpeciesFeatureType ()
{
}


/*
 * Checks that all the PossibleSpeciesFeatureValue ids under the direct parent SpeciesFeatureType objects are unique.
 */
void
UniquePossibleSpeciesFeatureValueIdsWithinSpeciesFeatureType::doCheck (const Model& m)
{
  const MultiModelPlugin * plug =
    static_cast <const MultiModelPlugin*>(m.getPlugin("multi"));
  if (plug == NULL)
  {
    return;
  }

  for (unsigned int n = 0; n < plug->getNumMultiSpeciesTypes(); n++)
  {
    const MultiSpeciesType* spt = plug->getMultiSpeciesType(n);
    if (spt == NULL) continue;

    for (unsigned int i = 0; i < spt->getNumSpeciesFeatureTypes(); i++)
    {
        const SpeciesFeatureType * sft = spt->getSpeciesFeatureType(i);

        if (sft == NULL) continue;

        for (unsigned int j = 0; j < sft->getNumPossibleSpeciesFeatureValues(); j++) {

            const PossibleSpeciesFeatureValue * psv = sft->getPossibleSpeciesFeatureValue(j);
            checkId( *psv );
        }

        reset();
   }

  }

}

#endif /* __cplusplus */

LIBSBML_CPP_NAMESPACE_END

/** @endcond */
