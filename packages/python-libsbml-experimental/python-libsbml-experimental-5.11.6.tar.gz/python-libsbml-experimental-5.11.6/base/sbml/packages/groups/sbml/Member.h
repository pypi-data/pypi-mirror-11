/**
 * @file:   Member.h
 * @brief:  Implementation of the Member class
 * @author: Generated by autocreate code
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


#ifndef Member_H__
#define Member_H__


#include <sbml/common/extern.h>
#include <sbml/common/sbmlfwd.h>
#include <sbml/packages/groups/common/groupsfwd.h>


#ifdef __cplusplus


#include <string>


#include <sbml/SBase.h>
#include <sbml/ListOf.h>
#include <sbml/packages/groups/extension/GroupsExtension.h>


LIBSBML_CPP_NAMESPACE_BEGIN


class LIBSBML_EXTERN Member : public SBase
{

protected:

  std::string   mId;
  std::string   mName;
  std::string   mIdRef;
  std::string   mMetaIdRef;


public:

  /**
   * Creates a new Member with the given level, version, and package version.
   *
   * @param level an unsigned int, the SBML Level to assign to this Member
   *
   * @param version an unsigned int, the SBML Version to assign to this Member
   *
   * @param pkgVersion an unsigned int, the SBML Groups Version to assign to this Member
   */
  Member(unsigned int level      = GroupsExtension::getDefaultLevel(),
         unsigned int version    = GroupsExtension::getDefaultVersion(),
         unsigned int pkgVersion = GroupsExtension::getDefaultPackageVersion());


  /**
   * Creates a new Member with the given GroupsPkgNamespaces object.
   *
   * @param groupsns the GroupsPkgNamespaces object
   */
  Member(GroupsPkgNamespaces* groupsns);


  /**
   * Copy constructor for Member.
   *
   * @param orig; the Member instance to copy.
   */
  Member(const Member& orig);


  /**
   * Assignment operator for Member.
   *
   * @param rhs; the object whose values are used as the basis
   * of the assignment
   */
  Member& operator=(const Member& rhs);


  /**
   * Creates and returns a deep copy of this Member object.
   *
   * @return a (deep) copy of this Member object.
   */
  virtual Member* clone () const;


  /**
   * Destructor for Member.
   */
  virtual ~Member();


  /**
   * Returns the value of the "id" attribute of this Member.
   *
   * @return the value of the "id" attribute of this Member as a string.
   */
  virtual const std::string& getId() const;


  /**
   * Predicate returning @c true or @c false depending on whether this
   * Member's "id" attribute has been set.
   *
   * @return @c true if this Member's "id" attribute has been set,
   * otherwise @c false is returned.
   */
  virtual bool isSetId() const;


  /**
   * Sets the value of the "id" attribute of this Member.
   *
   * @param id; const std::string& value of the "id" attribute to be set
   *
   * @return integer value indicating success/failure of the
   * function.  @if clike The value is drawn from the
   * enumeration #OperationReturnValues_t. @endif The possible values
   * returned by this function are:
   * @li LIBSBML_OPERATION_SUCCESS
   * @li LIBSBML_INVALID_ATTRIBUTE_VALUE
   */
  virtual int setId(const std::string& id);


  /**
   * Unsets the value of the "id" attribute of this Member.
   *
   * @return integer value indicating success/failure of the
   * function.  @if clike The value is drawn from the
   * enumeration #OperationReturnValues_t. @endif The possible values
   * returned by this function are:
   * @li LIBSBML_OPERATION_SUCCESS
   * @li LIBSBML_OPERATION_FAILED
   */
  virtual int unsetId();


  /**
   * Returns the value of the "name" attribute of this Member.
   *
   * @return the value of the "name" attribute of this Member as a string.
   */
  virtual const std::string& getName() const;


  /**
   * Predicate returning @c true or @c false depending on whether this
   * Member's "name" attribute has been set.
   *
   * @return @c true if this Member's "name" attribute has been set,
   * otherwise @c false is returned.
   */
  virtual bool isSetName() const;


  /**
   * Sets the value of the "name" attribute of this Member.
   *
   * @param name; const std::string& value of the "name" attribute to be set
   *
   * @return integer value indicating success/failure of the
   * function.  @if clike The value is drawn from the
   * enumeration #OperationReturnValues_t. @endif The possible values
   * returned by this function are:
   * @li LIBSBML_OPERATION_SUCCESS
   * @li LIBSBML_INVALID_ATTRIBUTE_VALUE
   */
  virtual int setName(const std::string& name);


  /**
   * Unsets the value of the "name" attribute of this Member.
   *
   * @return integer value indicating success/failure of the
   * function.  @if clike The value is drawn from the
   * enumeration #OperationReturnValues_t. @endif The possible values
   * returned by this function are:
   * @li LIBSBML_OPERATION_SUCCESS
   * @li LIBSBML_OPERATION_FAILED
   */
  virtual int unsetName();


  /**
   * Returns the value of the "idRef" attribute of this Member.
   *
   * @return the value of the "idRef" attribute of this Member as a string.
   */
  virtual const std::string& getIdRef() const;


  /**
   * Predicate returning @c true or @c false depending on whether this
   * Member's "idRef" attribute has been set.
   *
   * @return @c true if this Member's "idRef" attribute has been set,
   * otherwise @c false is returned.
   */
  virtual bool isSetIdRef() const;


  /**
   * Sets the value of the "idRef" attribute of this Member.
   *
   * @param idRef; const std::string& value of the "idRef" attribute to be set
   *
   * @return integer value indicating success/failure of the
   * function.  @if clike The value is drawn from the
   * enumeration #OperationReturnValues_t. @endif The possible values
   * returned by this function are:
   * @li LIBSBML_OPERATION_SUCCESS
   * @li LIBSBML_INVALID_ATTRIBUTE_VALUE
   */
  virtual int setIdRef(const std::string& idRef);


  /**
   * Unsets the value of the "idRef" attribute of this Member.
   *
   * @return integer value indicating success/failure of the
   * function.  @if clike The value is drawn from the
   * enumeration #OperationReturnValues_t. @endif The possible values
   * returned by this function are:
   * @li LIBSBML_OPERATION_SUCCESS
   * @li LIBSBML_OPERATION_FAILED
   */
  virtual int unsetIdRef();


  /**
   * Returns the value of the "metaIdRef" attribute of this Member.
   *
   * @return the value of the "metaIdRef" attribute of this Member as a string.
   */
  virtual const std::string& getMetaIdRef() const;


  /**
   * Predicate returning @c true or @c false depending on whether this
   * Member's "metaIdRef" attribute has been set.
   *
   * @return @c true if this Member's "metaIdRef" attribute has been set,
   * otherwise @c false is returned.
   */
  virtual bool isSetMetaIdRef() const;


  /**
   * Sets the value of the "metaIdRef" attribute of this Member.
   *
   * @param metaIdRef; const std::string& value of the "metaIdRef" attribute to be set
   *
   * @return integer value indicating success/failure of the
   * function.  @if clike The value is drawn from the
   * enumeration #OperationReturnValues_t. @endif The possible values
   * returned by this function are:
   * @li LIBSBML_OPERATION_SUCCESS
   * @li LIBSBML_INVALID_ATTRIBUTE_VALUE
   */
  virtual int setMetaIdRef(const std::string& metaIdRef);


  /**
   * Unsets the value of the "metaIdRef" attribute of this Member.
   *
   * @return integer value indicating success/failure of the
   * function.  @if clike The value is drawn from the
   * enumeration #OperationReturnValues_t. @endif The possible values
   * returned by this function are:
   * @li LIBSBML_OPERATION_SUCCESS
   * @li LIBSBML_OPERATION_FAILED
   */
  virtual int unsetMetaIdRef();


  /**
   * Returns the XML element name of this object, which for Member, is
   * always @c "member".
   *
   * @return the name of this element, i.e. @c "member".
   */
  virtual const std::string& getElementName () const;


  /**
   * Returns the libSBML type code for this SBML object.
   * 
   * @if clike LibSBML attaches an identifying code to every kind of SBML
   * object.  These are known as <em>SBML type codes</em>.  The set of
   * possible type codes is defined in the enumeration #SBMLTypeCode_t.
   * The names of the type codes all begin with the characters @c
   * SBML_. @endif@if java LibSBML attaches an identifying code to every
   * kind of SBML object.  These are known as <em>SBML type codes</em>.  In
   * other languages, the set of type codes is stored in an enumeration; in
   * the Java language interface for libSBML, the type codes are defined as
   * static integer constants in the interface class {@link
   * libsbmlConstants}.  The names of the type codes all begin with the
   * characters @c SBML_. @endif@if python LibSBML attaches an identifying
   * code to every kind of SBML object.  These are known as <em>SBML type
   * codes</em>.  In the Python language interface for libSBML, the type
   * codes are defined as static integer constants in the interface class
   * @link libsbml@endlink.  The names of the type codes all begin with the
   * characters @c SBML_. @endif@if csharp LibSBML attaches an identifying
   * code to every kind of SBML object.  These are known as <em>SBML type
   * codes</em>.  In the C# language interface for libSBML, the type codes
   * are defined as static integer constants in the interface class @link
   * libsbmlcs.libsbml@endlink.  The names of the type codes all begin with
   * the characters @c SBML_. @endif
   *
   * @return the SBML type code for this object, or
   * @link SBMLTypeCode_t#SBML_UNKNOWN SBML_UNKNOWN@endlink (default).
   *
   * @see getElementName()
   */
  virtual int getTypeCode () const;


  /**
   * Predicate returning @c true if all the required attributes
   * for this Member object have been set.
   *
   * @note The required attributes for a Member object are:
   *
   * @return a boolean value indicating whether all the required
   * attributes for this object have been defined.
   */
  virtual bool hasRequiredAttributes() const;


  /** @cond doxygenLibsbmlInternal */

  /**
   * Subclasses should override this method to write out their contained
   * SBML objects as XML elements.  Be sure to call your parents
   * implementation of this method as well.
   */
  virtual void writeElements (XMLOutputStream& stream) const;


  /** @endcond doxygenLibsbmlInternal */


  /** @cond doxygenLibsbmlInternal */

  /**
   * Accepts the given SBMLVisitor.
   */
  virtual bool accept (SBMLVisitor& v) const;


  /** @endcond doxygenLibsbmlInternal */


  /** @cond doxygenLibsbmlInternal */

  /**
   * Sets the parent SBMLDocument.
   */
  virtual void setSBMLDocument (SBMLDocument* d);


  /** @endcond doxygenLibsbmlInternal */


  /** @cond doxygenLibsbmlInternal */

  /**
   * Enables/Disables the given package with this element.
   */
  virtual void enablePackageInternal(const std::string& pkgURI,
               const std::string& pkgPrefix, bool flag);


  /** @endcond doxygenLibsbmlInternal */


protected:

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



};

class LIBSBML_EXTERN ListOfMembers : public ListOf
{

public:

  /**
   * Creates a new ListOfMembers with the given level, version, and package version.
   *
   * @param level an unsigned int, the SBML Level to assign to this ListOfMembers
   *
   * @param version an unsigned int, the SBML Version to assign to this ListOfMembers
   *
   * @param pkgVersion an unsigned int, the SBML Groups Version to assign to this ListOfMembers
   */
  ListOfMembers(unsigned int level      = GroupsExtension::getDefaultLevel(),
                unsigned int version    = GroupsExtension::getDefaultVersion(),
                unsigned int pkgVersion = GroupsExtension::getDefaultPackageVersion());


  /**
   * Creates a new ListOfMembers with the given GroupsPkgNamespaces object.
   *
   * @param groupsns the GroupsPkgNamespaces object
   */
  ListOfMembers(GroupsPkgNamespaces* groupsns);


  /**
   * Creates and returns a deep copy of this ListOfMembers object.
   *
   * @return a (deep) copy of this ListOfMembers object.
   */
  virtual ListOfMembers* clone () const;


  /**
   * Get a Member from the ListOfMembers.
   *
   * @param n the index number of the Member to get.
   *
   * @return the nth Member in this ListOfMembers.
   *
   * @see size()
   */
  virtual Member* get(unsigned int n);


  /**
   * Get a Member from the ListOfMembers.
   *
   * @param n the index number of the Member to get.
   *
   * @return the nth Member in this ListOfMembers.
   *
   * @see size()
   */
  virtual const Member* get(unsigned int n) const;


  /**
   * Get a Member from the ListOfMembers
   * based on its identifier.
   *
   * @param sid a string representing the identifier
   * of the Member to get.
   *
   * @return Member in this ListOfMembers
   * with the given id or NULL if no such
   * Member exists.
   *
   * @see get(unsigned int n)   *
   * @see size()
   */
  virtual Member* get(const std::string& sid);


  /**
   * Get a Member from the ListOfMembers
   * based on its identifier.
   *
   * @param sid a string representing the identifier
   * of the Member to get.
   *
   * @return Member in this ListOfMembers
   * with the given id or NULL if no such
   * Member exists.
   *
   * @see get(unsigned int n)   *
   * @see size()
   */
  virtual const Member* get(const std::string& sid) const;


  /**
   * Removes the nth Member from this ListOfMembers
   * and returns a pointer to it.
   *
   * The caller owns the returned item and is responsible for deleting it.
   *
   * @param n the index of the Member to remove.
   *
   * @see size()
   */
  virtual Member* remove(unsigned int n);


  /**
   * Removes the Member from this ListOfMembers with the given identifier
   * and returns a pointer to it.
   *
   * The caller owns the returned item and is responsible for deleting it.
   * If none of the items in this list have the identifier @p sid, then
   * @c NULL is returned.
   *
   * @param sid the identifier of the Member to remove.
   *
   * @return the Member removed. As mentioned above, the caller owns the
   * returned item.
   */
  virtual Member* remove(const std::string& sid);


  /**
   * Returns the XML element name of this object, which for ListOfMembers, is
   * always @c "listOfMembers".
   *
   * @return the name of this element, i.e. @c "listOfMembers".
   */
  virtual const std::string& getElementName () const;


  /**
   * Returns the libSBML type code for this SBML object.
   * 
   * @if clike LibSBML attaches an identifying code to every kind of SBML
   * object.  These are known as <em>SBML type codes</em>.  The set of
   * possible type codes is defined in the enumeration #SBMLTypeCode_t.
   * The names of the type codes all begin with the characters @c
   * SBML_. @endif@if java LibSBML attaches an identifying code to every
   * kind of SBML object.  These are known as <em>SBML type codes</em>.  In
   * other languages, the set of type codes is stored in an enumeration; in
   * the Java language interface for libSBML, the type codes are defined as
   * static integer constants in the interface class {@link
   * libsbmlConstants}.  The names of the type codes all begin with the
   * characters @c SBML_. @endif@if python LibSBML attaches an identifying
   * code to every kind of SBML object.  These are known as <em>SBML type
   * codes</em>.  In the Python language interface for libSBML, the type
   * codes are defined as static integer constants in the interface class
   * @link libsbml@endlink.  The names of the type codes all begin with the
   * characters @c SBML_. @endif@if csharp LibSBML attaches an identifying
   * code to every kind of SBML object.  These are known as <em>SBML type
   * codes</em>.  In the C# language interface for libSBML, the type codes
   * are defined as static integer constants in the interface class @link
   * libsbmlcs.libsbml@endlink.  The names of the type codes all begin with
   * the characters @c SBML_. @endif
   *
   * @return the SBML type code for this object, or
   * @link SBMLTypeCode_t#SBML_UNKNOWN SBML_UNKNOWN@endlink (default).
   *
   * @see getElementName()
   */
  virtual int getTypeCode () const;


  /**
   * Returns the libSBML type code for the SBML objects
   * contained in this ListOf object
   * 
   * @if clike LibSBML attaches an identifying code to every kind of SBML
   * object.  These are known as <em>SBML type codes</em>.  The set of
   * possible type codes is defined in the enumeration #SBMLTypeCode_t.
   * The names of the type codes all begin with the characters @c
   * SBML_. @endif@if java LibSBML attaches an identifying code to every
   * kind of SBML object.  These are known as <em>SBML type codes</em>.  In
   * other languages, the set of type codes is stored in an enumeration; in
   * the Java language interface for libSBML, the type codes are defined as
   * static integer constants in the interface class {@link
   * libsbmlConstants}.  The names of the type codes all begin with the
   * characters @c SBML_. @endif@if python LibSBML attaches an identifying
   * code to every kind of SBML object.  These are known as <em>SBML type
   * codes</em>.  In the Python language interface for libSBML, the type
   * codes are defined as static integer constants in the interface class
   * @link libsbml@endlink.  The names of the type codes all begin with the
   * characters @c SBML_. @endif@if csharp LibSBML attaches an identifying
   * code to every kind of SBML object.  These are known as <em>SBML type
   * codes</em>.  In the C# language interface for libSBML, the type codes
   * are defined as static integer constants in the interface class @link
   * libsbmlcs.libsbml@endlink.  The names of the type codes all begin with
   * the characters @c SBML_. @endif
   *
   * @return the SBML type code for the objects in this ListOf instance, or
   * @link SBMLTypeCode_t#SBML_UNKNOWN SBML_UNKNOWN@endlink (default).
   *
   * @see getElementName()
   */
  virtual int getItemTypeCode () const;


protected:

  /** @cond doxygenLibsbmlInternal */

  /**
   * Creates a new Member in this ListOfMembers
   */
  virtual SBase* createObject(XMLInputStream& stream);


  /** @endcond doxygenLibsbmlInternal */


  /** @cond doxygenLibsbmlInternal */

  /**
   * Write the namespace for the Groups package.
   */
  virtual void writeXMLNS(XMLOutputStream& stream) const;


  /** @endcond doxygenLibsbmlInternal */



};



LIBSBML_CPP_NAMESPACE_END

#endif  /*  __cplusplus  */

#ifndef SWIG

LIBSBML_CPP_NAMESPACE_BEGIN
BEGIN_C_DECLS

LIBSBML_EXTERN
Member_t *
Member_create(unsigned int level, unsigned int version,
              unsigned int pkgVersion);


LIBSBML_EXTERN
void
Member_free(Member_t * m);


LIBSBML_EXTERN
Member_t *
Member_clone(Member_t * m);


LIBSBML_EXTERN
char *
Member_getId(Member_t * m);


LIBSBML_EXTERN
char *
Member_getName(Member_t * m);


LIBSBML_EXTERN
char *
Member_getIdRef(Member_t * m);


LIBSBML_EXTERN
char *
Member_getMetaIdRef(Member_t * m);


LIBSBML_EXTERN
int
Member_isSetId(Member_t * m);


LIBSBML_EXTERN
int
Member_isSetName(Member_t * m);


LIBSBML_EXTERN
int
Member_isSetIdRef(Member_t * m);


LIBSBML_EXTERN
int
Member_isSetMetaIdRef(Member_t * m);


LIBSBML_EXTERN
int
Member_setId(Member_t * m, const char * id);


LIBSBML_EXTERN
int
Member_setName(Member_t * m, const char * name);


LIBSBML_EXTERN
int
Member_setIdRef(Member_t * m, const char * idRef);


LIBSBML_EXTERN
int
Member_setMetaIdRef(Member_t * m, const char * metaIdRef);


LIBSBML_EXTERN
int
Member_unsetId(Member_t * m);


LIBSBML_EXTERN
int
Member_unsetName(Member_t * m);


LIBSBML_EXTERN
int
Member_unsetIdRef(Member_t * m);


LIBSBML_EXTERN
int
Member_unsetMetaIdRef(Member_t * m);


LIBSBML_EXTERN
int
Member_hasRequiredAttributes(Member_t * m);


LIBSBML_EXTERN
Member_t *
ListOfMembers_getById(ListOf_t * lo, const char * sid);


LIBSBML_EXTERN
Member_t *
ListOfMembers_removeById(ListOf_t * lo, const char * sid);




END_C_DECLS
LIBSBML_CPP_NAMESPACE_END

#endif  /*  !SWIG  */

#endif /*  Member_H__  */

