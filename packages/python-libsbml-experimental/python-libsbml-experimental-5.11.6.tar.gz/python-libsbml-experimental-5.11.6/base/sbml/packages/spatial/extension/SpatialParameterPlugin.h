/**
 * @file:   SpatialParameterPlugin.h
 * @brief:  Implementation of the SpatialParameterPlugin class
 * @author: SBMLTeam
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


#ifndef SpatialParameterPlugin_H__
#define SpatialParameterPlugin_H__


#include <sbml/common/extern.h>


#ifdef __cplusplus


#include <sbml/extension/SBasePlugin.h>
#include <sbml/packages/spatial/sbml/SpatialSymbolReference.h>
#include <sbml/packages/spatial/sbml/AdvectionCoefficient.h>
#include <sbml/packages/spatial/sbml/BoundaryCondition.h>
#include <sbml/packages/spatial/sbml/DiffusionCoefficient.h>


LIBSBML_CPP_NAMESPACE_BEGIN


class LIBSBML_EXTERN SpatialParameterPlugin : public SBasePlugin
{
public:

  /**
   * Creates a new SpatialParameterPlugin
   */
  SpatialParameterPlugin(const std::string& uri, const std::string& prefix, 
                                 SpatialPkgNamespaces* spatialns);


  /**
   * Copy constructor for SpatialParameterPlugin.
   *
   * @param orig; the SpatialParameterPlugin instance to copy.
   */
  SpatialParameterPlugin(const SpatialParameterPlugin& orig);


   /**
   * Assignment operator for SpatialParameterPlugin.
   *
   * @param rhs; the object whose values are used as the basis
   * of the assignment
   */
  SpatialParameterPlugin& operator=(const SpatialParameterPlugin& rhs);


   /**
   * Creates and returns a deep copy of this SpatialParameterPlugin object.
   *
   * @return a (deep) copy of this SpatialParameterPlugin object.
   */
  virtual SpatialParameterPlugin* clone () const;


   /**
   * Destructor for SpatialParameterPlugin.
   */
  virtual ~SpatialParameterPlugin();


   //---------------------------------------------------------------
  //
  // overridden virtual functions for read/write/check
  //
  //---------------------------------------------------------------

  /** @cond doxygenLibsbmlInternal */

  /**
   * Subclasses must override this method to create, store, and then
   * return an SBML object corresponding to the next XMLToken in the
   * XMLInputStream if they have their specific elements.
   *
   * @return the SBML object corresponding to next XMLToken in the
   * XMLInputStream or NULL if the token was not recognized.
   */
  virtual SBase* createObject (XMLInputStream& stream);


  /** @endcond doxygenLibsbmlInternal */


  /** @cond doxygenLibsbmlInternal */

  /**
   * Subclasses must override this method to write out their contained
   * SBML objects as XML elements if they have their specific elements.
   */
  virtual void writeElements (XMLOutputStream& stream) const;


  /** @endcond doxygenLibsbmlInternal */


  /**
   * Checks if this plugin object has all the required elements.
   *
   * Subclasses must override this method 
   * if they have their specific elements.
   *
   * @return true if this plugin object has all the required elements
   * otherwise false will be returned.
   */
  virtual bool hasRequiredElements () const;


  //---------------------------------------------------------------


  /** @cond doxygenLibsbmlInternal */

  /**
   * Get the list of expected attributes for this element.
   */
  virtual void addExpectedAttributes(ExpectedAttributes& attributes);


  /** @endcond doxygenLibsbmlInternal */


  /** @cond doxygenLibsbmlInternal */

  /**
   * Read values from the given XMLAttributes set into their specific fields.
   */
  virtual void readAttributes (const XMLAttributes& attributes,
                               const ExpectedAttributes& expectedAttributes);


  /** @endcond doxygenLibsbmlInternal */


  /** @cond doxygenLibsbmlInternal */

  /**
   * Write values of XMLAttributes to the output stream.
   */
  virtual void writeAttributes (XMLOutputStream& stream) const;


  /** @endcond doxygenLibsbmlInternal */


  //---------------------------------------------------------------
  //
  // Functions for interacting with the members of the plugin
  //
  //---------------------------------------------------------------

  /**
   * Returns a List of all child SBase objects, including those nested to an
   * arbitrary depth.
   *
   * @return a List* of pointers to all child objects.
   */
   virtual List* getAllElements(ElementFilter * filter = NULL);


  /**
   * Returns the SpatialSymbolReference from this SpatialParameterPlugin object.
   *
   * @return the SpatialSymbolReference from object in this SpatialParameterPlugin object.
   */
  const SpatialSymbolReference* getSpatialSymbolReference () const;


  /**
   * Returns the SpatialSymbolReference from this SpatialParameterPlugin object.
   *
   * @return the SpatialSymbolReference from object in this SpatialParameterPlugin object.
   */
  SpatialSymbolReference* getSpatialSymbolReference ();


  /**
   * Predicate returning @c true or @c false depending on whether the
    "SpatialSymbolReference" element has been set.
   *
   * @return @c true if the "SpatialSymbolReference" element has been set,
   * otherwise @c false is returned.
   */
  bool isSetSpatialSymbolReference() const;


  /**
   * Sets the SpatialSymbolReference element in this SpatialParameterPlugin object.
   *
   * @param spatialSymbolReference the spatialSymbolReference* to be set.
   *
   * @return integer value indicating success/failure of the
   * function.  @if clike The value is drawn from the
   * enumeration #OperationReturnValues_t. @endif The possible values
   * returned by this function are:
   * @li LIBSBML_OPERATION_SUCCESS
   */
  int setSpatialSymbolReference (const SpatialSymbolReference* spatialSymbolReference);


  /**
   * Creates a new SpatialSymbolReference object and adds it to the SpatialParameterPlugin object.
   *
   * @return the newly created SpatialSymbolReference object.
   */
  SpatialSymbolReference* createSpatialSymbolReference ();


  /**
   * Returns the AdvectionCoefficient from this SpatialParameterPlugin object.
   *
   * @return the AdvectionCoefficient from object in this SpatialParameterPlugin object.
   */
  const AdvectionCoefficient* getAdvectionCoefficient () const;


  /**
   * Returns the AdvectionCoefficient from this SpatialParameterPlugin object.
   *
   * @return the AdvectionCoefficient from object in this SpatialParameterPlugin object.
   */
  AdvectionCoefficient* getAdvectionCoefficient ();


  /**
   * Predicate returning @c true or @c false depending on whether the
    "AdvectionCoefficient" element has been set.
   *
   * @return @c true if the "AdvectionCoefficient" element has been set,
   * otherwise @c false is returned.
   */
  bool isSetAdvectionCoefficient() const;


  /**
   * Sets the AdvectionCoefficient element in this SpatialParameterPlugin object.
   *
   * @param advectionCoefficient the advectionCoefficient* to be set.
   *
   * @return integer value indicating success/failure of the
   * function.  @if clike The value is drawn from the
   * enumeration #OperationReturnValues_t. @endif The possible values
   * returned by this function are:
   * @li LIBSBML_OPERATION_SUCCESS
   */
  int setAdvectionCoefficient (const AdvectionCoefficient* advectionCoefficient);


  /**
   * Creates a new AdvectionCoefficient object and adds it to the SpatialParameterPlugin object.
   *
   * @return the newly created AdvectionCoefficient object.
   */
  AdvectionCoefficient* createAdvectionCoefficient ();


  /**
   * Returns the BoundaryCondition from this SpatialParameterPlugin object.
   *
   * @return the BoundaryCondition from object in this SpatialParameterPlugin object.
   */
  const BoundaryCondition* getBoundaryCondition () const;


  /**
   * Returns the BoundaryCondition from this SpatialParameterPlugin object.
   *
   * @return the BoundaryCondition from object in this SpatialParameterPlugin object.
   */
  BoundaryCondition* getBoundaryCondition ();


  /**
   * Predicate returning @c true or @c false depending on whether the
    "BoundaryCondition" element has been set.
   *
   * @return @c true if the "BoundaryCondition" element has been set,
   * otherwise @c false is returned.
   */
  bool isSetBoundaryCondition() const;


  /**
   * Sets the BoundaryCondition element in this SpatialParameterPlugin object.
   *
   * @param boundaryCondition the boundaryCondition* to be set.
   *
   * @return integer value indicating success/failure of the
   * function.  @if clike The value is drawn from the
   * enumeration #OperationReturnValues_t. @endif The possible values
   * returned by this function are:
   * @li LIBSBML_OPERATION_SUCCESS
   */
  int setBoundaryCondition (const BoundaryCondition* boundaryCondition);


  /**
   * Creates a new BoundaryCondition object and adds it to the SpatialParameterPlugin object.
   *
   * @return the newly created BoundaryCondition object.
   */
  BoundaryCondition* createBoundaryCondition ();


  /**
   * Returns the DiffusionCoefficient from this SpatialParameterPlugin object.
   *
   * @return the DiffusionCoefficient from object in this SpatialParameterPlugin object.
   */
  const DiffusionCoefficient* getDiffusionCoefficient () const;


  /**
   * Returns the DiffusionCoefficient from this SpatialParameterPlugin object.
   *
   * @return the DiffusionCoefficient from object in this SpatialParameterPlugin object.
   */
  DiffusionCoefficient* getDiffusionCoefficient ();


  /**
   * Predicate returning @c true or @c false depending on whether the
    "DiffusionCoefficient" element has been set.
   *
   * @return @c true if the "DiffusionCoefficient" element has been set,
   * otherwise @c false is returned.
   */
  bool isSetDiffusionCoefficient() const;


  /**
   * Sets the DiffusionCoefficient element in this SpatialParameterPlugin object.
   *
   * @param diffusionCoefficient the diffusionCoefficient* to be set.
   *
   * @return integer value indicating success/failure of the
   * function.  @if clike The value is drawn from the
   * enumeration #OperationReturnValues_t. @endif The possible values
   * returned by this function are:
   * @li LIBSBML_OPERATION_SUCCESS
   */
  int setDiffusionCoefficient (const DiffusionCoefficient* diffusionCoefficient);


  /**
   * Creates a new DiffusionCoefficient object and adds it to the SpatialParameterPlugin object.
   *
   * @return the newly created DiffusionCoefficient object.
   */
  DiffusionCoefficient* createDiffusionCoefficient ();


  /** @cond doxygenLibsbmlInternal */

  /**
   * Sets the parent SBMLDocument.
   */
  virtual void setSBMLDocument (SBMLDocument* d);


  /** @endcond doxygenLibsbmlInternal */


  /** @cond doxygenLibsbmlInternal */

  virtual void connectToParent (SBase* sbase);


  /** @endcond doxygenLibsbmlInternal */


  /** @cond doxygenLibsbmlInternal */

  virtual void enablePackageInternal(const std::string& pkgURI,
                                     const std::string& pkgPrefix, bool flag);


  /** @endcond doxygenLibsbmlInternal */


  /** @cond doxygenLibsbmlInternal */

  virtual bool accept (SBMLVisitor& v) const;

  /** @endcond doxygenLibsbmlInternal */


protected:

  /** @cond doxygenLibsbmlInternal */

  SpatialSymbolReference* mSpatialSymbolReference;
  AdvectionCoefficient* mAdvectionCoefficient;
  BoundaryCondition* mBoundaryCondition;
  DiffusionCoefficient* mDiffusionCoefficient;

  /** @endcond doxygenLibsbmlInternal */


public:
   /** 
   * @return true, if either the spatial symbol reference, diffusion coefficient, 
   *   advection coefficient or boundary is set. Otherwise the return value is false.
   */ 
  bool isSpatialParameter() const;

  /** 
   * Determines the type of the spatial parameter, that is one of: 
   * 
   * SBML_SPATIAL_SPATIALSYMBOLREFERENCE
   * SBML_SPATIAL_DIFFUSIONCOEFFICIENT
   * SBML_SPATIAL_ADVECTIONCOEFFICIENT
   * SBML_SPATIAL_BOUNDARYCONDITION
   * 
   * or -1 in case no other is defined.
   */
  int getType() const;};




LIBSBML_CPP_NAMESPACE_END


#endif /* __cplusplus */
#endif /* SpatialParameterPlugin_H__ */


