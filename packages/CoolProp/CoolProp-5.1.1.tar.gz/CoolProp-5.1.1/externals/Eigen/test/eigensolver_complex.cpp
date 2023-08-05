// This file is part of Eigen, a lightweight C++ template library
// for linear algebra.
//
// Copyright (C) 2008-2009 Gael Guennebaud <gael.guennebaud@inria.fr>
// Copyright (C) 2010 Jitse Niesen <jitse@maths.leeds.ac.uk>
//
// This Source Code Form is subject to the terms of the Mozilla
// Public License v. 2.0. If a copy of the MPL was not distributed
// with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

#include "main.h"
#include <limits>
#include <Eigen/Eigenvalues>
#include <Eigen/LU>

/* Check that two column vectors are approximately equal upto permutations,
   by checking that the k-th power sums are equal for k = 1, ..., vec1.rows() */
template<typename VectorType>
void verify_is_approx_upto_permutation(const VectorType& vec1, const VectorType& vec2)
{
  typedef typename NumTraits<typename VectorType::Scalar>::Real RealScalar;

  VERIFY(vec1.cols() == 1);
  VERIFY(vec2.cols() == 1);
  VERIFY(vec1.rows() == vec2.rows());
  for (int k = 1; k <= vec1.rows(); ++k)
  {
    VERIFY_IS_APPROX(vec1.array().pow(RealScalar(k)).sum(), vec2.array().pow(RealScalar(k)).sum());
  }
}


template<typename MatrixType> void eigensolver(const MatrixType& m)
{
  typedef typename MatrixType::Index Index;
  /* this test covers the following files:
     ComplexEigenSolver.h, and indirectly ComplexSchur.h
  */
  Index rows = m.rows();
  Index cols = m.cols();

  typedef typename MatrixType::Scalar Scalar;
  typedef typename NumTraits<Scalar>::Real RealScalar;

  MatrixType a = MatrixType::Random(rows,cols);
  MatrixType symmA =  a.adjoint() * a;

  ComplexEigenSolver<MatrixType> ei0(symmA);
  VERIFY_IS_EQUAL(ei0.info(), Success);
  VERIFY_IS_APPROX(symmA * ei0.eigenvectors(), ei0.eigenvectors() * ei0.eigenvalues().asDiagonal());

  ComplexEigenSolver<MatrixType> ei1(a);
  VERIFY_IS_EQUAL(ei1.info(), Success);
  VERIFY_IS_APPROX(a * ei1.eigenvectors(), ei1.eigenvectors() * ei1.eigenvalues().asDiagonal());
  // Note: If MatrixType is real then a.eigenvalues() uses EigenSolver and thus
  // another algorithm so results may differ slightly
  verify_is_approx_upto_permutation(a.eigenvalues(), ei1.eigenvalues());

  ComplexEigenSolver<MatrixType> ei2;
  ei2.setMaxIterations(ComplexSchur<MatrixType>::m_maxIterationsPerRow * rows).compute(a);
  VERIFY_IS_EQUAL(ei2.info(), Success);
  VERIFY_IS_EQUAL(ei2.eigenvectors(), ei1.eigenvectors());
  VERIFY_IS_EQUAL(ei2.eigenvalues(), ei1.eigenvalues());
  if (rows > 2) {
    ei2.setMaxIterations(1).compute(a);
    VERIFY_IS_EQUAL(ei2.info(), NoConvergence);
    VERIFY_IS_EQUAL(ei2.getMaxIterations(), 1);
  }

  ComplexEigenSolver<MatrixType> eiNoEivecs(a, false);
  VERIFY_IS_EQUAL(eiNoEivecs.info(), Success);
  VERIFY_IS_APPROX(ei1.eigenvalues(), eiNoEivecs.eigenvalues());

  // Regression test for issue #66
  MatrixType z = MatrixType::Zero(rows,cols);
  ComplexEigenSolver<MatrixType> eiz(z);
  VERIFY((eiz.eigenvalues().cwiseEqual(0)).all());

  MatrixType id = MatrixType::Identity(rows, cols);
  VERIFY_IS_APPROX(id.operatorNorm(), RealScalar(1));

  if (rows > 1)
  {
    // Test matrix with NaN
    a(0,0) = std::numeric_limits<typename MatrixType::RealScalar>::quiet_NaN();
    ComplexEigenSolver<MatrixType> eiNaN(a);
    VERIFY_IS_EQUAL(eiNaN.info(), NoConvergence);
  }
}

template<typename MatrixType> void eigensolver_verify_assert(const MatrixType& m)
{
  ComplexEigenSolver<MatrixType> eig;
  VERIFY_RAISES_ASSERT(eig.eigenvectors());
  VERIFY_RAISES_ASSERT(eig.eigenvalues());

  MatrixType a = MatrixType::Random(m.rows(),m.cols());
  eig.compute(a, false);
  VERIFY_RAISES_ASSERT(eig.eigenvectors());
}

void test_eigensolver_complex()
{
  int s = 0;
  for(int i = 0; i < g_repeat; i++) {
    CALL_SUBTEST_1( eigensolver(Matrix4cf()) );
    s = internal::random<int>(1,EIGEN_TEST_MAX_SIZE/4);
    CALL_SUBTEST_2( eigensolver(MatrixXcd(s,s)) );
    CALL_SUBTEST_3( eigensolver(Matrix<std::complex<float>, 1, 1>()) );
    CALL_SUBTEST_4( eigensolver(Matrix3f()) );
    TEST_SET_BUT_UNUSED_VARIABLE(s)
  }
  CALL_SUBTEST_1( eigensolver_verify_assert(Matrix4cf()) );
  s = internal::random<int>(1,EIGEN_TEST_MAX_SIZE/4);
  CALL_SUBTEST_2( eigensolver_verify_assert(MatrixXcd(s,s)) );
  CALL_SUBTEST_3( eigensolver_verify_assert(Matrix<std::complex<float>, 1, 1>()) );
  CALL_SUBTEST_4( eigensolver_verify_assert(Matrix3f()) );

  // Test problem size constructors
  CALL_SUBTEST_5(ComplexEigenSolver<MatrixXf> tmp(s));
  
  TEST_SET_BUT_UNUSED_VARIABLE(s)
}
