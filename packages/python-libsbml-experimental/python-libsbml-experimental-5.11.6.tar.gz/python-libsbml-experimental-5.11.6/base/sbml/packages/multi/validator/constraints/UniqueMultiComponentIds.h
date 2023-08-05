/**
 * @cond doxygenLibsbmlInternal
 *
 * @file    UniqueMultiComponentIds.h
 * @brief   Ensures the appropriate ids within a Model are unique
 * @author  Fengkai Zhang
 * @author  Sarah Keating
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

#ifndef UniqueMultiComponentIds_h
#define UniqueMultiComponentIds_h


#ifdef __cplusplus

#include <string>

#include "UniqueMultiIdBase.h"

LIBSBML_CPP_NAMESPACE_BEGIN

class UniqueMultiComponentIds: public UniqueMultiIdBase
{
public:

  /**
   * Creates a new Constraint with the given constraint id.
   */
  UniqueMultiComponentIds (unsigned int id, MultiValidator& v);

  /**
   * Destroys this Constraint.
   */
  virtual ~UniqueMultiComponentIds ();


protected:

  /**
   * Checks that all ids on the following Model objects are unique:
   * FunctionDefinitions, Species, Compartments, global Parameters,
   * Reactions, and Events.
   */
  virtual void doCheck (const Model& m);
};

LIBSBML_CPP_NAMESPACE_END

#endif  /* __cplusplus */
#endif  /* UniqueMultiComponentIds_h */

/** @endcond */
