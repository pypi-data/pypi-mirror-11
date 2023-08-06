! """
! DES: module collecting f90 subroutines for fitting purposes
! """ 
!=============================================================================
SUBROUTINE fit(x,y,a,b,n)
! """
! DES: Least Square fitting on x and y
! INP: 
!      x,y  : the input array
!      n    : the size of the input array
! OUT: a,b  : the result of the fit
!
! """
!INOUT
  integer                       :: n
  real,   dimension(n)          :: x,y
  real                          :: a,b
  !f2py intent(hide),depend(x)  :: n=shape(x)
  !f2py intent(in)              :: x,y
  !f2py intent(out)             :: a,b
!-----------------------------------
  real                          :: meanX,meanY,sumXX,sumXY
!-----------------------------------

! From Mathworld least square fitting
! http://mathworld.wolfram.com/LeastSquaresFitting.html

meanX = SUM(x(:))/n
meanY = SUM(y(:))/n

sumXX = DOT_PRODUCT(x,x)-n*meanX**2
sumXY = DOT_PRODUCT(x,y)-n*meanX*meanY

b = sumXY/sumXX
a = meanY-b*meanX

END SUBROUTINE fit

!=============================================================================
SUBROUTINE fit_slope(x,y,b,n)
! """
! DES: Least Square fitting on x and y, compute and return only the slope
! INP: 
!      x,y : the input array
!      n   : the size of the input array
! OUT: a   : the slope of the fit
!
! """
!INOUT
  integer                       :: n
  real,   dimension(n)          :: x,y
  real                          :: b
  !f2py intent(hide),depend(x)  :: n=shape(x)
  !f2py intent(in)              :: x,y
  !f2py intent(out)             :: b
!-----------------------------------
  real                          :: meanX,meanY,sumXX,sumXY
!-----------------------------------

! From Mathworld least square fitting
! http://mathworld.wolfram.com/LeastSquaresFitting.html

meanX = SUM(x(:))/n
meanY = SUM(y(:))/n

sumXX = DOT_PRODUCT(x,x)-n*meanX**2
sumXY = DOT_PRODUCT(x,y)-n*meanX*meanY

b = sumXY/sumXX

END SUBROUTINE fit_slope

!=============================================================================
SUBROUTINE polyfit(x,y,k,n,coeff)
! """
! DES: Least Square polynomial fitting on x and y
! INP: 
!      x,y   : the input array
!      k     : the order of the polynomial
!      n     : the size of the input array
! OUT: coeff : the coefficient of the polynome
!
! """
!INOUT
  integer                         :: n, k
  real,   dimension(n)            :: x,y
  real,   dimension(k+1)          :: coeff
  !f2py intent(hide),depend(x)    :: n=shape(x)
  !f2py intent(in)                :: x,y,k
  !f2py intent(out)               :: coeff
!-----------------------------------
integer                                       :: I, INFO
double precision, allocatable, dimension(:,:) :: Mat, tMat, InvMat
double precision, allocatable, dimension(:)   :: IPIV, WORK

! From Least Squares Fitting--Polynomial
! http://mathworld.wolfram.com/LeastSquaresFittingPolynomial.html
! need LAPACK to do a matrice inversion

! Tricky memory management to get it running on big arrays...
! use double precision lapack to help the computation
! at most : 2*n*(k+1)+(k+1)**2+4*(k+1)

! Initiate the first matrix X
ALLOCATE(Mat(n,k+1))
DO I=1,k+1
   Mat(:,I) = x(:)**(I-1)
ENDDO

! Save its transposed form
ALLOCATE(tMat(k+1,n))
tMat = TRANSPOSE(Mat)

! The method is based on the inversion of tX.X ...
ALLOCATE(InvMat(k+1,k+1))
InvMat = MATMUL(tMat,Mat)

! ... so inverse it with the help of LAPACK 

! First computes an LU factorization of a general matrix, 
! using partial pivoting with row interchanges.
ALLOCATE(IPIV(k+1))
CALL DGETRF(k+1,k+1,InvMat,k+1,IPIV,INFO)
IF (INFO.ne.0) THEN
   DEALLOCATE(Mat,tMat,InvMat,IPIV)
   PRINT *, "LU factorization failed"
   RETURN
ENDIF

! Then computes the inverse of a general matrix, using the LU
! factorization computed by SGETRF.
ALLOCATE(WORK(3*(k+1)))
CALL DGETRI( k+1, InvMat, k+1, IPIV, WORK, 3*(k+1), INFO )
DEALLOCATE(IPIV,WORK,Mat)

IF (INFO.ne.0) THEN
   DEALLOCATE(tMat,InvMat)
   PRINT *, "Inversing matrix failed"
   RETURN
ENDIF

! Finish the matrix computation need an additionnal Matrix otherwise
! crash - ifc on control, need to be investigated
ALLOCATE(Mat(k+1,n))
Mat = MATMUL(InvMat,tMat)
DEALLOCATE(tMat)

! Finally get the coefficient 
coeff = MATMUL(Mat,y)
DEALLOCATE(InvMat,Mat)

END SUBROUTINE polyfit
