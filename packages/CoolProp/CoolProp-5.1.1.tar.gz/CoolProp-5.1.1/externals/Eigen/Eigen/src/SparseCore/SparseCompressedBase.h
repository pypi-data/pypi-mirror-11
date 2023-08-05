// This file is part of Eigen, a lightweight C++ template library
// for linear algebra.
//
// Copyright (C) 2015 Gael Guennebaud <gael.guennebaud@inria.fr>
//
// This Source Code Form is subject to the terms of the Mozilla
// Public License v. 2.0. If a copy of the MPL was not distributed
// with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

#ifndef EIGEN_SPARSE_COMPRESSED_BASE_H
#define EIGEN_SPARSE_COMPRESSED_BASE_H

namespace Eigen { 

template<typename Derived> class SparseCompressedBase;
  
namespace internal {

template<typename Derived>
struct traits<SparseCompressedBase<Derived> > : traits<Derived>
{};

} // end namespace internal

template<typename Derived>
class SparseCompressedBase
  : public SparseMatrixBase<Derived>
{
  public:
    typedef SparseMatrixBase<Derived> Base;
    _EIGEN_SPARSE_PUBLIC_INTERFACE(SparseCompressedBase)
    using Base::operator=;
    using Base::IsRowMajor;
    
    class InnerIterator;
    class ReverseInnerIterator;
    
  protected:
    typedef typename Base::IndexVector IndexVector;
    Eigen::Map<IndexVector> innerNonZeros() { return Eigen::Map<IndexVector>(innerNonZeroPtr(), isCompressed()?0:derived().outerSize()); }
    const  Eigen::Map<const IndexVector> innerNonZeros() const { return Eigen::Map<const IndexVector>(innerNonZeroPtr(), isCompressed()?0:derived().outerSize()); }
        
  public:
    
    /** \returns the number of non zero coefficients */
    inline Index nonZeros() const
    {
      if(isCompressed())
        return outerIndexPtr()[derived().outerSize()]-outerIndexPtr()[0];
      else if(derived().outerSize()==0)
        return 0;
      else
        return innerNonZeros().sum();
      
    }
    
    /** \returns a const pointer to the array of values.
      * This function is aimed at interoperability with other libraries.
      * \sa innerIndexPtr(), outerIndexPtr() */
    inline const Scalar* valuePtr() const { return derived().valuePtr(); }
    /** \returns a non-const pointer to the array of values.
      * This function is aimed at interoperability with other libraries.
      * \sa innerIndexPtr(), outerIndexPtr() */
    inline Scalar* valuePtr() { return derived().valuePtr(); }

    /** \returns a const pointer to the array of inner indices.
      * This function is aimed at interoperability with other libraries.
      * \sa valuePtr(), outerIndexPtr() */
    inline const StorageIndex* innerIndexPtr() const { return derived().innerIndexPtr(); }
    /** \returns a non-const pointer to the array of inner indices.
      * This function is aimed at interoperability with other libraries.
      * \sa valuePtr(), outerIndexPtr() */
    inline StorageIndex* innerIndexPtr() { return derived().innerIndexPtr(); }

    /** \returns a const pointer to the array of the starting positions of the inner vectors.
      * This function is aimed at interoperability with other libraries.
      * \sa valuePtr(), innerIndexPtr() */
    inline const StorageIndex* outerIndexPtr() const { return derived().outerIndexPtr(); }
    /** \returns a non-const pointer to the array of the starting positions of the inner vectors.
      * This function is aimed at interoperability with other libraries.
      * \sa valuePtr(), innerIndexPtr() */
    inline StorageIndex* outerIndexPtr() { return derived().outerIndexPtr(); }

    /** \returns a const pointer to the array of the number of non zeros of the inner vectors.
      * This function is aimed at interoperability with other libraries.
      * \warning it returns the null pointer 0 in compressed mode */
    inline const StorageIndex* innerNonZeroPtr() const { return derived().innerNonZeroPtr(); }
    /** \returns a non-const pointer to the array of the number of non zeros of the inner vectors.
      * This function is aimed at interoperability with other libraries.
      * \warning it returns the null pointer 0 in compressed mode */
    inline StorageIndex* innerNonZeroPtr() { return derived().innerNonZeroPtr(); }
    
    /** \returns whether \c *this is in compressed form. */
    inline bool isCompressed() const { return innerNonZeroPtr()==0; }
  
};

template<typename Derived>
class SparseCompressedBase<Derived>::InnerIterator
{
  public:
    InnerIterator(const SparseCompressedBase& mat, Index outer)
      : m_values(mat.valuePtr()), m_indices(mat.innerIndexPtr()), m_outer(outer), m_id(mat.outerIndexPtr()[outer])
    {
      if(mat.isCompressed())
        m_end = mat.outerIndexPtr()[outer+1];
      else
        m_end = m_id + mat.innerNonZeroPtr()[outer];
    }

    inline InnerIterator& operator++() { m_id++; return *this; }

    inline const Scalar& value() const { return m_values[m_id]; }
    inline Scalar& valueRef() { return const_cast<Scalar&>(m_values[m_id]); }

    inline StorageIndex index() const { return m_indices[m_id]; }
    inline Index outer() const { return m_outer; }
    inline Index row() const { return IsRowMajor ? m_outer : index(); }
    inline Index col() const { return IsRowMajor ? index() : m_outer; }

    inline operator bool() const { return (m_id < m_end); }

  protected:
    const Scalar* m_values;
    const StorageIndex* m_indices;
    const Index m_outer;
    Index m_id;
    Index m_end;
  private:
    // If you get here, then you're not using the right InnerIterator type, e.g.:
    //   SparseMatrix<double,RowMajor> A;
    //   SparseMatrix<double>::InnerIterator it(A,0);
    template<typename T> InnerIterator(const SparseMatrixBase<T>&, Index outer);
};

template<typename Derived>
class SparseCompressedBase<Derived>::ReverseInnerIterator
{
  public:
    ReverseInnerIterator(const SparseCompressedBase& mat, Index outer)
      : m_values(mat.valuePtr()), m_indices(mat.innerIndexPtr()), m_outer(outer), m_start(mat.outerIndexPtr()[outer])
    {
      if(mat.isCompressed())
        m_id = mat.outerIndexPtr()[outer+1];
      else
        m_id = m_start + mat.innerNonZeroPtr()[outer];
    }

    inline ReverseInnerIterator& operator--() { --m_id; return *this; }

    inline const Scalar& value() const { return m_values[m_id-1]; }
    inline Scalar& valueRef() { return const_cast<Scalar&>(m_values[m_id-1]); }

    inline StorageIndex index() const { return m_indices[m_id-1]; }
    inline Index outer() const { return m_outer; }
    inline Index row() const { return IsRowMajor ? m_outer : index(); }
    inline Index col() const { return IsRowMajor ? index() : m_outer; }

    inline operator bool() const { return (m_id > m_start); }

  protected:
    const Scalar* m_values;
    const StorageIndex* m_indices;
    const Index m_outer;
    Index m_id;
    const Index m_start;
};

namespace internal {

template<typename Derived>
struct evaluator<SparseCompressedBase<Derived> >
  : evaluator_base<Derived>
{
  typedef typename Derived::Scalar Scalar;
  typedef typename Derived::InnerIterator InnerIterator;
  typedef typename Derived::ReverseInnerIterator ReverseInnerIterator;
  
  enum {
    CoeffReadCost = NumTraits<Scalar>::ReadCost,
    Flags = Derived::Flags
  };
  
  evaluator() : m_matrix(0) {}
  explicit evaluator(const Derived &mat) : m_matrix(&mat) {}
  
  inline Index nonZerosEstimate() const {
    return m_matrix->nonZeros();
  }
  
  operator Derived&() { return m_matrix->const_cast_derived(); }
  operator const Derived&() const { return *m_matrix; }
  
  typedef typename DenseCoeffsBase<Derived,ReadOnlyAccessors>::CoeffReturnType CoeffReturnType;
  Scalar coeff(Index row, Index col) const
  { return m_matrix->coeff(row,col); }
  
  Scalar& coeffRef(Index row, Index col)
  {
    eigen_internal_assert(row>=0 && row<m_matrix->rows() && col>=0 && col<m_matrix->cols());
      
    const Index outer = Derived::IsRowMajor ? row : col;
    const Index inner = Derived::IsRowMajor ? col : row;

    Index start = m_matrix->outerIndexPtr()[outer];
    Index end = m_matrix->isCompressed() ? m_matrix->outerIndexPtr()[outer+1] : m_matrix->outerIndexPtr()[outer] + m_matrix->innerNonZeroPtr()[outer];
    eigen_assert(end>start && "you are using a non finalized sparse matrix or written coefficient does not exist");
    const Index p =   std::lower_bound(m_matrix->innerIndexPtr()+start, m_matrix->innerIndexPtr()+end,inner)
                    - m_matrix->innerIndexPtr();
    eigen_assert((p<end) && (m_matrix->innerIndexPtr()[p]==inner) && "written coefficient does not exist");
    return m_matrix->const_cast_derived().valuePtr()[p];
  }

  const Derived *m_matrix;
};

}

} // end namespace Eigen

#endif // EIGEN_SPARSE_COMPRESSED_BASE_H
