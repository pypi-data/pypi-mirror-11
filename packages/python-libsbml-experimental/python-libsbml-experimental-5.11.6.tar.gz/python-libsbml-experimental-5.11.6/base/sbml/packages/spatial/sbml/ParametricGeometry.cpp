/**
 * @file:   ParametricGeometry.cpp
 * @brief:  Implementation of the ParametricGeometry class
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


#include <sbml/packages/spatial/sbml/ParametricGeometry.h>
#include <sbml/packages/spatial/validator/SpatialSBMLError.h>
#include <sbml/util/ElementFilter.h>


using namespace std;


LIBSBML_CPP_NAMESPACE_BEGIN


/*
 * Creates a new ParametricGeometry with the given level, version, and package version.
 */
ParametricGeometry::ParametricGeometry (unsigned int level, unsigned int version, unsigned int pkgVersion)
  : GeometryDefinition(level, version)
  , mSpatialPoints (NULL)
  , mParametricObjects (level, version, pkgVersion)
{
  // set an SBMLNamespaces derived object of this package
  setSBMLNamespacesAndOwn(new SpatialPkgNamespaces(level, version, pkgVersion));

  // connect to child objects
  connectToChild();
}


/*
 * Creates a new ParametricGeometry with the given SpatialPkgNamespaces object.
 */
ParametricGeometry::ParametricGeometry (SpatialPkgNamespaces* spatialns)
  : GeometryDefinition(spatialns)
  , mSpatialPoints (NULL)
  , mParametricObjects (spatialns)
{
  // set the element namespace of this object
  setElementNamespace(spatialns->getURI());

  // connect to child objects
  connectToChild();

  // load package extensions bound with this object (if any) 
  loadPlugins(spatialns);
}


/*
 * Copy constructor for ParametricGeometry.
 */
ParametricGeometry::ParametricGeometry (const ParametricGeometry& orig)
  : GeometryDefinition(orig)
  , mSpatialPoints ( NULL)
  , mParametricObjects  ( orig.mParametricObjects)

{
  if (orig.mSpatialPoints != NULL)
  {
    mSpatialPoints = orig.mSpatialPoints->clone();
  }

  // connect to child objects
  connectToChild();
}


/*
 * Assignment for ParametricGeometry.
 */
ParametricGeometry&
ParametricGeometry::operator=(const ParametricGeometry& rhs)
{
  if (&rhs != this)
  {
    GeometryDefinition::operator=(rhs);
    if (rhs.mSpatialPoints != NULL)
    {
      mSpatialPoints = rhs.mSpatialPoints->clone();
    }
    else
    {
      mSpatialPoints = NULL;
    }
    mParametricObjects  = rhs.mParametricObjects;

    // connect to child objects
    connectToChild();
  }
  return *this;
}


/*
 * Clone for ParametricGeometry.
 */
ParametricGeometry*
ParametricGeometry::clone () const
{
  return new ParametricGeometry(*this);
}


/*
 * Destructor for ParametricGeometry.
 */
ParametricGeometry::~ParametricGeometry ()
{
  delete mSpatialPoints;
  mSpatialPoints = NULL;
}


/*
 * Returns the value of the "spatialPoints" attribute of this ParametricGeometry.
 */
const SpatialPoints*
ParametricGeometry::getSpatialPoints() const
{
  return mSpatialPoints;
}


/*
 * Returns the value of the "spatialPoints" attribute of this ParametricGeometry.
 */
SpatialPoints*
ParametricGeometry::getSpatialPoints()
{
  return mSpatialPoints;
}


/*
 * Creates a new "spatialPoints" element of this ParametricGeometry and returns it.
 */
SpatialPoints*
ParametricGeometry::createSpatialPoints()
{
  if (mSpatialPoints != NULL) delete mSpatialPoints;
  SPATIAL_CREATE_NS(spatialns, getSBMLNamespaces());
  mSpatialPoints = new SpatialPoints(spatialns);
  delete spatialns;
  connectToChild();
  return mSpatialPoints;
}


/*
 * Returns true/false if spatialPoints is set.
 */
bool
ParametricGeometry::isSetSpatialPoints() const
{
  return (mSpatialPoints != NULL);
}


/*
 * Sets spatialPoints and returns value indicating success.
 */
int
ParametricGeometry::setSpatialPoints(SpatialPoints* spatialPoints)
{
  if (mSpatialPoints == spatialPoints)
  {
    return LIBSBML_OPERATION_SUCCESS;
  }
  else if (spatialPoints == NULL)
  {
    delete mSpatialPoints;
    mSpatialPoints = NULL;
    return LIBSBML_OPERATION_SUCCESS;
  }
  else
  {
    delete mSpatialPoints;
    mSpatialPoints = (spatialPoints != NULL) ?
      static_cast<SpatialPoints*>(spatialPoints->clone()) : NULL;
    if (mSpatialPoints != NULL)
    {
      mSpatialPoints->connectToParent(this);
    }
    return LIBSBML_OPERATION_SUCCESS;
  }
}


/*
 * Unsets spatialPoints and returns value indicating success.
 */
int
ParametricGeometry::unsetSpatialPoints()
{
  delete mSpatialPoints;
  mSpatialPoints = NULL;
  return LIBSBML_OPERATION_SUCCESS;
}


/*
 * Returns the  "ListOfParametricObjects" in this ParametricGeometry object.
 */
const ListOfParametricObjects*
ParametricGeometry::getListOfParametricObjects() const
{
  return &mParametricObjects;
}


/*
 * Returns the  "ListOfParametricObjects" in this ParametricGeometry object.
 */
ListOfParametricObjects*
ParametricGeometry::getListOfParametricObjects()
{
  return &mParametricObjects;
}


/*
 * Removes the nth ParametricObject from the ListOfParametricObjects.
 */
ParametricObject*
ParametricGeometry::removeParametricObject(unsigned int n)
{
	return mParametricObjects.remove(n);
}


/*
 * Removes the a ParametricObject with given id from the ListOfParametricObjects.
 */
ParametricObject*
ParametricGeometry::removeParametricObject(const std::string& sid)
{
	return mParametricObjects.remove(sid);
}


/*
 * Return the nth ParametricObject in the ListOfParametricObjects within this ParametricGeometry.
 */
ParametricObject*
ParametricGeometry::getParametricObject(unsigned int n)
{
	return mParametricObjects.get(n);
}


/*
 * Return the nth ParametricObject in the ListOfParametricObjects within this ParametricGeometry.
 */
const ParametricObject*
ParametricGeometry::getParametricObject(unsigned int n) const
{
	return mParametricObjects.get(n);
}


/*
 * Return a ParametricObject from the ListOfParametricObjects by id.
 */
ParametricObject*
ParametricGeometry::getParametricObject(const std::string& sid)
{
	return mParametricObjects.get(sid);
}


/*
 * Return a ParametricObject from the ListOfParametricObjects by id.
 */
const ParametricObject*
ParametricGeometry::getParametricObject(const std::string& sid) const
{
	return mParametricObjects.get(sid);
}


/*
 * Adds a copy the given "ParametricObject" to this ParametricGeometry.
 *
 * @param po; the ParametricObject object to add
 *
 * @return integer value indicating success/failure of the
 * function.  @if clike The value is drawn from the
 * enumeration #OperationReturnValues_t. @endif The possible values
 * returned by this function are:
 * @li LIBSBML_OPERATION_SUCCESS
 * @li LIBSBML_INVALID_ATTRIBUTE_VALUE
 */
int
ParametricGeometry::addParametricObject(const ParametricObject* po)
{
  if (po == NULL)
  {
    return LIBSBML_OPERATION_FAILED;
  }
  else if (po->hasRequiredAttributes() == false)
  {
    return LIBSBML_INVALID_OBJECT;
  }
  else if (getLevel() != po->getLevel())
  {
    return LIBSBML_LEVEL_MISMATCH;
  }
  else if (getVersion() != po->getVersion())
  {
    return LIBSBML_VERSION_MISMATCH;
  }
  else if (matchesRequiredSBMLNamespacesForAddition(static_cast<const SBase *>(po)) == false)
  {
    return LIBSBML_NAMESPACES_MISMATCH;
  }
  else
  {
    mParametricObjects.append(po);
    return LIBSBML_OPERATION_SUCCESS;
  }
}


/*
 * Get the number of ParametricObject objects in this ParametricGeometry.
 *
 * @return the number of ParametricObject objects in this ParametricGeometry
 */
unsigned int
ParametricGeometry::getNumParametricObjects() const
{
  return mParametricObjects.size();
}


/*
 * Creates a new ParametricObject object, adds it to this ParametricGeometrys
 * ParametricGeometry and returns the ParametricObject object created. 
 *
 * @return a new ParametricObject object instance
 *
 * @see addParametricObject(const ParametricObject* po)
 */
ParametricObject*
ParametricGeometry::createParametricObject()
{
  ParametricObject* po = NULL;

  try
  {
    SPATIAL_CREATE_NS(spatialns, getSBMLNamespaces());
    po = new ParametricObject(spatialns);
    delete spatialns;
  }
  catch (...)
  {
    /* here we do not create a default object as the level/version must
     * match the parent object
     *
     * do nothing
     */
  }

  if(po != NULL)
  {
    mParametricObjects.appendAndOwn(po);
  }

  return po;
}


List*
ParametricGeometry::getAllElements(ElementFilter* filter)
{
  List* ret = new List();
  List* sublist = NULL;

  ADD_FILTERED_POINTER(ret, sublist, mSpatialPoints, filter);
  ADD_FILTERED_LIST(ret, sublist, mParametricObjects, filter);

  ADD_FILTERED_FROM_PLUGIN(ret, sublist, filter);

  return ret;
}


/*
 * Returns the XML element name of this object
 */
const std::string&
ParametricGeometry::getElementName () const
{
  static const string name = "parametricGeometry";
  return name;
}


/*
 * Returns the libSBML type code for this SBML object.
 */
int
ParametricGeometry::getTypeCode () const
{
  return SBML_SPATIAL_PARAMETRICGEOMETRY;
}


/*
 * check if all the required attributes are set
 */
bool
ParametricGeometry::hasRequiredAttributes () const
{
  bool allPresent = GeometryDefinition::hasRequiredAttributes();

  return allPresent;
}


/*
 * check if all the required elements are set
 */
bool
ParametricGeometry::hasRequiredElements () const
{
  bool allPresent = GeometryDefinition::hasRequiredElements();

  return allPresent;
}


  /** @cond doxygenLibsbmlInternal */

/*
 * write contained elements
 */
void
ParametricGeometry::writeElements (XMLOutputStream& stream) const
{
  GeometryDefinition::writeElements(stream);
  if (isSetSpatialPoints() == true)
  {
    mSpatialPoints->write(stream);
  }
  if (getNumParametricObjects() > 0)
  {
    mParametricObjects.write(stream);
  }

  SBase::writeExtensionElements(stream);
}


  /** @endcond doxygenLibsbmlInternal */


  /** @cond doxygenLibsbmlInternal */

/*
 * Accepts the given SBMLVisitor.
 */
bool
ParametricGeometry::accept (SBMLVisitor& v) const
{
  v.visit(*this);

/* VISIT CHILDREN */

  v.leave(*this);

  return true;
}


  /** @endcond doxygenLibsbmlInternal */


  /** @cond doxygenLibsbmlInternal */

/*
 * Sets the parent SBMLDocument.
 */
void
ParametricGeometry::setSBMLDocument (SBMLDocument* d)
{
  GeometryDefinition::setSBMLDocument(d);
  if (mSpatialPoints != NULL)
    mSpatialPoints->setSBMLDocument(d);
  mParametricObjects.setSBMLDocument(d);
}


  /** @endcond doxygenLibsbmlInternal */


  /** @cond doxygenLibsbmlInternal */

/*
   * Connects to child elements.
 */
void
ParametricGeometry::connectToChild()
{
  GeometryDefinition::connectToChild();

  if (mSpatialPoints != NULL)
    mSpatialPoints->connectToParent(this);
  mParametricObjects.connectToParent(this);
}


  /** @endcond doxygenLibsbmlInternal */


  /** @cond doxygenLibsbmlInternal */

/*
 * Enables/Disables the given package with this element.
 */
void
ParametricGeometry::enablePackageInternal(const std::string& pkgURI,
             const std::string& pkgPrefix, bool flag)
{
  GeometryDefinition::enablePackageInternal(pkgURI, pkgPrefix, flag);
  mParametricObjects.enablePackageInternal(pkgURI, pkgPrefix, flag);
}


  /** @endcond doxygenLibsbmlInternal */


  /** @cond doxygenLibsbmlInternal */

/*
 * creates object.
 */
SBase*
ParametricGeometry::createObject(XMLInputStream& stream)
{
  SBase* object = GeometryDefinition::createObject(stream);

  const string& name = stream.peek().getName();

  SPATIAL_CREATE_NS(spatialns, getSBMLNamespaces());

  if (name == "spatialPoints")
  {
    mSpatialPoints = new SpatialPoints(spatialns);
    object = mSpatialPoints;
  }
  else if (name == "listOfParametricObjects")
  {
    object = &mParametricObjects;
  }

  delete spatialns;

  connectToChild();


  return object;
}


  /** @endcond doxygenLibsbmlInternal */


  /** @cond doxygenLibsbmlInternal */

/*
 * Get the list of expected attributes for this element.
 */
void
ParametricGeometry::addExpectedAttributes(ExpectedAttributes& attributes)
{
  GeometryDefinition::addExpectedAttributes(attributes);

}


  /** @endcond doxygenLibsbmlInternal */


  /** @cond doxygenLibsbmlInternal */

/*
 * Read values from the given XMLAttributes set into their specific fields.
 */
void
ParametricGeometry::readAttributes (const XMLAttributes& attributes,
                             const ExpectedAttributes& expectedAttributes)
{
  const unsigned int sbmlLevel   = getLevel  ();
  const unsigned int sbmlVersion = getVersion();

  unsigned int numErrs;

  GeometryDefinition::readAttributes(attributes, expectedAttributes);

  // look to see whether an unknown attribute error was logged
  if (getErrorLog() != NULL)
  {
    numErrs = getErrorLog()->getNumErrors();
    for (int n = numErrs-1; n >= 0; n--)
    {
      if (getErrorLog()->getError(n)->getErrorId() == UnknownPackageAttribute)
      {
        const std::string details =
                          getErrorLog()->getError(n)->getMessage();
        getErrorLog()->remove(UnknownPackageAttribute);
        getErrorLog()->logPackageError("spatial", SpatialUnknownError,
                       getPackageVersion(), sbmlLevel, sbmlVersion, details, getLine(), getColumn());
      }
      else if (getErrorLog()->getError(n)->getErrorId() == UnknownCoreAttribute)
      {
        const std::string details =
                          getErrorLog()->getError(n)->getMessage();
        getErrorLog()->remove(UnknownCoreAttribute);
        getErrorLog()->logPackageError("spatial", SpatialUnknownError,
                       getPackageVersion(), sbmlLevel, sbmlVersion, details, getLine(), getColumn());
      }
    }
  }

}


  /** @endcond doxygenLibsbmlInternal */


  /** @cond doxygenLibsbmlInternal */

/*
 * Write values of XMLAttributes to the output stream.
 */
  void
ParametricGeometry::writeAttributes (XMLOutputStream& stream) const
{
  GeometryDefinition::writeAttributes(stream);

}


  /** @endcond doxygenLibsbmlInternal */


LIBSBML_EXTERN
ParametricGeometry_t *
ParametricGeometry_create(unsigned int level, unsigned int version,
                          unsigned int pkgVersion)
{
  return new ParametricGeometry(level, version, pkgVersion);
}


LIBSBML_EXTERN
void
ParametricGeometry_free(ParametricGeometry_t * pg)
{
  if (pg != NULL)
    delete pg;
}


LIBSBML_EXTERN
ParametricGeometry_t *
ParametricGeometry_clone(ParametricGeometry_t * pg)
{
  if (pg != NULL)
  {
    return static_cast<ParametricGeometry_t*>(pg->clone());
  }
  else
  {
    return NULL;
  }
}


LIBSBML_EXTERN
SpatialPoints_t*
ParametricGeometry_getSpatialPoints(ParametricGeometry_t * pg)
{
	if (pg == NULL)
		return NULL;

	return (SpatialPoints_t*)pg->getSpatialPoints();
}


LIBSBML_EXTERN
SpatialPoints_t*
ParametricGeometry_createSpatialPoints(ParametricGeometry_t * pg)
{
	if (pg == NULL)
		return NULL;

	return (SpatialPoints_t*)pg->createSpatialPoints();
}


LIBSBML_EXTERN
int
ParametricGeometry_isSetSpatialPoints(const ParametricGeometry_t * pg)
{
  return (pg != NULL) ? static_cast<int>(pg->isSetSpatialPoints()) : 0;
}


LIBSBML_EXTERN
int
ParametricGeometry_setSpatialPoints(ParametricGeometry_t * pg, SpatialPoints_t* spatialPoints)
{
	return (pg != NULL) ? pg->setSpatialPoints(spatialPoints) : LIBSBML_INVALID_OBJECT;
}


LIBSBML_EXTERN
int
ParametricGeometry_addParametricObject(ParametricGeometry_t * pg, ParametricObject_t * po)
{
	return  (pg != NULL) ? pg->addParametricObject(po) : LIBSBML_INVALID_OBJECT;
}

LIBSBML_EXTERN
ParametricObject_t *
ParametricGeometry_createParametricObject(ParametricGeometry_t * pg)
{
	return  (pg != NULL) ? pg->createParametricObject() : NULL;
}

LIBSBML_EXTERN
ListOf_t *
ParametricGeometry_getListOfParametricObjects(ParametricGeometry_t * pg)
{
	return  (pg != NULL) ? (ListOf_t *)pg->getListOfParametricObjects() : NULL;
}

LIBSBML_EXTERN
ParametricObject_t *
ParametricGeometry_getParametricObject(ParametricGeometry_t * pg, unsigned int n)
{
	return  (pg != NULL) ? pg->getParametricObject(n) : NULL;
}

LIBSBML_EXTERN
ParametricObject_t *
ParametricGeometry_getParametricObjectById(ParametricGeometry_t * pg, const char * sid)
{
	return  (pg != NULL) ? pg->getParametricObject(sid) : NULL;
}

LIBSBML_EXTERN
unsigned int
ParametricGeometry_getNumParametricObjects(ParametricGeometry_t * pg)
{
	return  (pg != NULL) ? pg->getNumParametricObjects() : SBML_INT_MAX;
}

LIBSBML_EXTERN
ParametricObject_t *
ParametricGeometry_removeParametricObject(ParametricGeometry_t * pg, unsigned int n)
{
	return  (pg != NULL) ? pg->removeParametricObject(n) : NULL;
}

LIBSBML_EXTERN
ParametricObject_t *
ParametricGeometry_removeParametricObjectById(ParametricGeometry_t * pg, const char * sid)
{
	return  (pg != NULL) ? pg->removeParametricObject(sid) : NULL;
}

LIBSBML_EXTERN
int
ParametricGeometry_hasRequiredAttributes(const ParametricGeometry_t * pg)
{
  return (pg != NULL) ? static_cast<int>(pg->hasRequiredAttributes()) : 0;
}


LIBSBML_EXTERN
int
ParametricGeometry_hasRequiredElements(const ParametricGeometry_t * pg)
{
	return (pg != NULL) ? static_cast<int>(pg->hasRequiredElements()) : 0;
}




LIBSBML_CPP_NAMESPACE_END


